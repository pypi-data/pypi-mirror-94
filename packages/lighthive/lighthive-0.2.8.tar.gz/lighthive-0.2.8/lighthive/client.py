import logging
import uuid
from itertools import cycle

import backoff
import requests

from .exceptions import RPCNodeException
from .broadcast.transaction_builder import TransactionBuilder
from .helpers.account import Account
from .helpers.rc import ResourceCredit


DEFAULT_NODES = [
    "https://api.hive.blog",
    "https://hived.emre.sh",
    "https://api.deathwing.me",
    "https://rpc.ausbit.dev",
    "https://api.pharesim.me",
    "https://rpc.ecency.com",
    "https://hive-api.arcange.eu",
]


class Client:

    def __init__(self, nodes=None, keys=None, connect_timeout=3,
                 read_timeout=30, loglevel=logging.ERROR, chain=None):
        self.nodes = nodes or DEFAULT_NODES
        self.node_list = cycle(nodes or DEFAULT_NODES)
        self.api_type = "condenser_api"
        self.queue = []
        self.connect_timeout = connect_timeout
        self.read_timeout = read_timeout
        self.keys = keys or []
        self.chain = chain or "HIVE"
        self.current_node = None
        self.logger = None
        self.set_logger(loglevel)
        self.next_node()
        self.transaction_builder = TransactionBuilder(self)

    def __getattr__(self, attr):
        def callable(*args, **kwargs):
            return self.request(attr, *args, **kwargs)

        return callable

    def __call__(self, *args, **kwargs):
        # This is not really thread-safe
        # multi-threaded environments shouldn't share client instances
        self.api_type = args[0]

        return self

    def set_logger(self, loglevel):
        self.logger = logging.getLogger(__name__)
        handler = logging.StreamHandler()
        formatter = logging.Formatter(
            '%(asctime)s %(name)-12s %(levelname)-8s %(message)s')
        handler.setFormatter(formatter)
        self.logger.addHandler(handler)
        self.logger.setLevel(loglevel)

    def next_node(self):
        self.current_node = next(self.node_list)
        self.logger.info("Node set as %s", self.current_node)

    def pick_id_for_request(self):
        return str(uuid.uuid4())

    def get_rpc_request_body(self, args, kwargs):
        method_name = args[0]
        if len(args) == 1:
            # condenser_api expects an empty list
            # while other apis expects an empty dict if no arguments
            # sent by the user.
            params = [] if self.api_type == "condenser_api" else {}
        else:
            params = args[1:] if self.api_type == "condenser_api" else args[1]

        data = {
            "jsonrpc": "2.0",
            "method": f"{self.api_type}.{method_name}",
            "params": params,
            "id": kwargs.get("id") or self.pick_id_for_request(),
        }

        return data

    @backoff.on_exception(backoff.expo,
                          (requests.exceptions.Timeout,
                           requests.exceptions.RequestException),
                          max_tries=5)
    def _send_request(self, url, request_data, timeout):
        self.logger.info("Sending request: %s", request_data)
        r = requests.post(
            url,
            json=request_data,
            timeout=timeout,
        )

        r.raise_for_status()
        self.logger.info("Response: %s", r.text)

        return r.json()

    def request(self, *args, **kwargs):
        batch_data = kwargs.get("batch_data")
        if batch_data:
            # if that's a batch call, don't do any formatting on data.
            # since it's already formatted for the app base.
            request_data = batch_data
        else:
            request_data = self.get_rpc_request_body(args, kwargs)

        if kwargs.get("batch"):
            self.queue.append(request_data)
            return

        try:
            response = self._send_request(
                self.current_node,
                request_data,
                (self.connect_timeout, self.read_timeout),
            )
        except requests.exceptions.RequestException as e:
            self.logger.error(e)
            num_retries = kwargs.get("num_retries", 1)

            if num_retries >= len(self.nodes):
                raise e

            kwargs.update({"num_retries": num_retries + 1})
            self.logger.info("Retrying in another node: %s, %s", args, kwargs)
            self.next_node()

            return self.request(*args, **kwargs)

        self.validate_response(response)

        if isinstance(response, dict):
            return response["result"]
        elif isinstance(response, list):
            return [r["result"] for r in response]

        raise Exception("Unexpected response: %s" % response)

    def validate_response(self, response):
        if 'error' in response:
            # single request error, no batch call.
            raise RPCNodeException(
                response["error"].get("message"),
                code=response["error"].get("code"),
                raw_body=response,
            )
        if isinstance(response, list):
            # batch calls returns multiple responses.
            # what should happen if one of the request is failed, and the other
            # one is success? Currently, it raises an RPCNodeException anyway.
            return [self.validate_response(r) for r in response]

    def process_batch(self):
        try:
            resp = self.request(batch_data=self.queue)
        finally:
            # flush the queue in case if any error happens
            self.queue = []
        return resp

    def broadcast(self, op, dry_run=False):
        return self.transaction_builder.broadcast(
            op, chain=self.chain, dry_run=dry_run)

    def broadcast_sync(self, op, dry_run=False):
        return self.transaction_builder.broadcast(
            op, chain=self.chain, dry_run=dry_run, sync=True)

    def account(self, username):
        return Account(self, username)

    def rc(self):
        return ResourceCredit(self)
