# naoqi3.py (Python 3)
from naoqi_client import ALProxyWrapper, ALBrokerWrapper


class ALProxy:
    def __init__(self, module_name, ip=None, port=None):
        self._proxy = ALProxyWrapper(module_name, ip, port)

    def __getattr__(self, method_name):
        return getattr(self._proxy, method_name)


class ALBroker:
    def __init__(self, name, ip, port, parent_ip, parent_port):
        self._broker = ALBrokerWrapper(name, ip, port, parent_ip, parent_port)
        self.init_result = self._broker.init_broker()

    def __getattr__(self, method_name):
        return getattr(self._broker, method_name)
