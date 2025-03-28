# naoqi3.py (Python 3)
from naoqi_client import ALProxyWrapper

class ALProxy:
    def __init__(self, module_name, ip, port):
        self._proxy = ALProxyWrapper(module_name, ip, port)

    def __getattr__(self, method_name):
        return getattr(self._proxy, method_name)
