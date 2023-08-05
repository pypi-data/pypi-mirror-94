import gzip
import hashlib
import hmac
from json import dumps
from time import time

import requests


def crud_operation_name(one_char: str) -> str:
    if one_char == "r":
        return "read"
    if one_char == "u":
        return "update"
    if one_char == "c":
        return "create"
    raise ValueError("Unsupported param")


def make_hash_digest(secret, body):
    hmac_hash = hmac.new(
        secret.encode("utf-8"),
        body if type(body) == bytes else body.encode("utf-8"),
        hashlib.sha256,
    )
    return hmac_hash.hexdigest()


class ClientError(Exception):
    pass


class BatchClient:
    def __init__(
        self,
        app_id: int,
        secret: str,
        endpoint: str,
        requests_session: requests.Session = None,
    ):
        self.app_id = app_id
        self.secret = secret
        self.endpoint = endpoint
        self.session = requests_session or requests.Session()
        self.message = {"app_id": self.app_id, "timestamp": None, "items": []}
        self._init_message()

    def _init_message(self):
        self.message = {"app_id": self.app_id, "timestamp": None, "items": []}

    def create(self, location: str, metas: dict = None):
        self.message["items"].append(["c", None, location, metas])
        return self

    def update(self, ark_name: str, location: str, metas: dict = None):
        self.message["items"].append(["u", ark_name, location, metas])
        return self

    def read(self, ark_name):
        self.message["items"].append(["r", ark_name, None, None])
        return self

    @staticmethod
    def _results_iterator(data):
        for batch_item in data:
            data = {
                "crud_operation": crud_operation_name(batch_item[0]),
                "ark_name": batch_item[1],
                "ark_location": batch_item[2],
                "ark_metas": batch_item[3],
            }
            yield data

    def commit(self):
        self.message["timestamp"] = int(time())
        body = gzip.compress(dumps(self.message).encode("utf-8"))
        response = self.session.post(
            self.endpoint + "batch/",
            data=body,
            headers={
                "content-encoding": "gzip",
                "Content-Type": "application/json",
                "Content-length": str(len(body)),
                "Authorization": make_hash_digest(self.secret, body),
            },
        )
        if response.status_code != 200:
            error = ClientError()
            error.response = response
            raise error
        self._init_message()
        return self._results_iterator(response.json())


class Client:
    def __init__(
        self,
        app_id: int,
        secret: str,
        endpoint: str,
        requests_session: requests.Session = None,
    ):
        self.app_id = app_id
        self.secret = secret
        self.endpoint = endpoint
        self.session = requests_session or requests.Session()

    def read(self, ark_name) -> dict:
        response = self.session.get(self.endpoint, params={"ark": ark_name})
        if response.status_code == 200:
            return response.json()
        error = ClientError()
        error.response = response
        raise error

    def create(self, location: str, metas: dict = None) -> str:
        data = {
            "app_id": self.app_id,
            "timestamp": int(time()),
            "ark_location": location,
            "ark_metas": metas,
        }
        body = dumps(data)
        response = self.session.post(
            self.endpoint,
            data=body,
            headers={"Authorization": make_hash_digest(self.secret, body)},
        )
        if response.status_code == 200:
            if response.text:
                return response.text
        error = ClientError()
        error.response = response
        raise error

    def update(self, ark_name: str, location: str, metas: dict = None) -> bool:
        data = {
            "app_id": self.app_id,
            "timestamp": int(time()),
            "ark_name": ark_name,
            "ark_location": location,
            "ark_metas": metas,
        }
        body = dumps(data)
        response = self.session.put(
            self.endpoint,
            data=body,
            headers={"Authorization": make_hash_digest(self.secret, body)},
        )
        if response.status_code == 200:
            return True
        error = ClientError()
        error.response = response
        raise error

    def batch(self) -> BatchClient:
        return BatchClient(self.app_id, self.secret, self.endpoint, self.session)
