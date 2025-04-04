"""
This module is used to track initialised ALProxy instances from naoqi.
"""

from naoqi import ALProxy, ALBroker, ALModule
import types


class ProxyService:

    def __init__(self):
        self.pool = {}
        self.brokers = {}
        self.constant_modules = {
            'vision_definitions': __import__('vision_definitions'),
            'motion': __import__('motion')
        }

    def get_proxy(self, module_name, ip, port):
        key = (module_name, ip, port)
        if key not in self.pool:
            # if no port and no port provided => it is expected that ALBroker is active
            # and ALProxy will connect via it. So we don't need to specify port and ip 
            if port is None:
                self.pool[key] = ALProxy(module_name)
            else:
                
                self.pool[key] = ALProxy(module_name, ip, port)

        return self.pool[key]
    
    def handle_proxy_command(self, module_name, method, ip, port, args):
        proxy = self.get_proxy(module_name=module_name, ip=ip, port=port)
        # Execute the requested method         
        return getattr(proxy, method)(*args)
    
    def handle_broker_command(self, method, ip, port, broker_name, parent_ip, parent_port, args):
        """
        
        """
        # if the command from client was to manually initialise broker
        if method == 'init_broker':
            broker = ALBroker(str(broker_name), str(ip), int(port), str(parent_ip), int(parent_port))
            self.brokers[broker_name] = broker
            return True
        # else perform requested method with provided args
        else:
            broker = self.brokers.get(broker_name)
            # if broker was found, call method(args) on NAOqi instance
            if broker:                
                return getattr(broker, method)(*args) 
            return False

    def get_constants(self, module_name):
        """Return all constants from naoqi modules"""
        module = self.constant_modules.get(module_name)
        if not module:
            raise ValueError("Module " + module_name + " not found")
        
        return {
            name: value
            for name, value in vars(module).items()
            if not name.startswith('__')  # exclude special attributes
            and not isinstance(value, (types.FunctionType, types.BuiltinFunctionType, type, types.ModuleType))  # exclude built-in funcs, types and so on.
        }

    def list_constant_modules(self):
        """Return list of available constans from modules"""
        return list(self.constant_modules.keys())
    