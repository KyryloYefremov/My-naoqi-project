"""
This module is used to track initialised ALProxy instances from naoqi.
"""

from naoqi import ALProxy
import types


class ProxyService:

    def __init__(self):
        self.pool = {}
        self.constant_modules = {
            'vision_definitions': __import__('vision_definitions'),
            'motion': __import__('motion')
        }

    def get_proxy(self, module_name, ip, port):
        key = (module_name, ip, port)
        if key not in self.pool:
            self.pool[key] = ALProxy(module_name, ip, port)

        return self.pool[key]
    
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
    