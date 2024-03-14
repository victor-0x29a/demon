from datetime import datetime
from redis_om import NotFoundError

from .. import Host, ApplicationError


class AddHostUseCase:
    def __init__(self, ip_address):
        self.ip_address = ip_address

        self._start()

    def _start(self):
        self._validate_data()

        host = self._find_host(self.data.ip_address)

        if not host:
            self._add_host()
        else:
            self._update_health_check(host)

    def _validate_data(self):
        if not self.ip_address:
            raise ApplicationError('Ip address is necessary.')

    def _find_host(self):
        try:
            finded_host = Host.get(Host.ip_address == self.ip_address)
        except NotFoundError:
            finded_host = None

        return finded_host

    def _add_host(self):
        Host(**{
            "ip_address": self.ip_address,
            "health_check_datetime_string": self.now_datetime_string,
            "is_active": 1
        }).save()

    def _update_health_check(self, host: Host):
        host.update(**{
            "health_check_datetime_string": self.now_datetime_string
        })

    @property
    def now_datetime_string(self):
        return datetime.now().date
