from datetime import datetime

from fastapi.exceptions import ValidationException, HTTPException
from pymongo.collection import Collection
from models import Host
from utils import now_to_str


class UpdateHealthCheck:
    def __init__(self, host_collection: Collection, ip_address: str):
        self.ip_address = ip_address
        self.host_collection = host_collection

    def call(self):
        self._validate_data()

        host = self._find_host()

        if host is None:
            self._add_host()
        else:
            self._update_health_check()

    def _validate_data(self):
        if not self.ip_address:
            raise ValidationException(errors=["The ip address is necessary."])

    def _find_host(self):
        try:
            finded_host = self.host_collection.find_one(
                {"ip_address": self.ip_address})
        except Exception:
            raise HTTPException(status_code=500)

        return finded_host

    def _add_host(self):
        host_instance = Host(_id=self.ip_address)
        self.host_collection.insert_one(host_instance.model_dump())

    def _update_health_check(self):
        self.host_collection.update_one({"ip_address": self.ip_address}, {
            "health_check_datetime": now_to_str(datetime.now())
        })
