"""
This module is used to track initialised ALProxy instances from naoqi.
"""

from naoqi import ALProxy


class ProxyService:

    def __init__(self):
        self.pool = {}

    def get_proxy(self, module_name, ip, port):
        key = (module_name, ip, port)
        if key not in self.pool:
            self.pool[key] = ALProxy(module_name, ip, port)

        return self.pool[key]
    