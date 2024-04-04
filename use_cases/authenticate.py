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

    def _check_hash_data(self):
        lawful_obj_hash = hashlib.sha256(str({
            "user": USER,
            "pass": PASS
        }))

        new_auth_obj_hash = hashlib.sha256(str(self.data))

        if not lawful_obj_hash == new_auth_obj_hash:
            raise HTTPException(406)
