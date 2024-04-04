import hashlib
from utils import generate_token
from constants import USER, PASS
from fastapi.exceptions import HTTPException


class Authenticate:
    def __init__(self, user, pwd):
        self.data = {
            "user": user,
            "pass": pwd
        }

    def call(self):
        self._validate_data()

        self._check_hash_data()

        token = self.token

        return token

    @property
    def token(self):
        return generate_token()

    def _validate_data(self):
        if not self.data["user"] or not self.data["pass"]:
            raise HTTPException(422)

    def _hash_string(self, string: str):
        return hashlib.sha256(string.encode("utf-8")).hexdigest()

    def _check_hash_data(self):
        data_amount = self._hash_string(self.data["user"]) + self._hash_string(self.data["pass"])

        hash_data_amount = USER + PASS

        if not data_amount == hash_data_amount:
            raise HTTPException(406)
