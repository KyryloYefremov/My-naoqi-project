"""
This module is used to track initialised ALProxy instances from naoqi.
"""

from naoqi import ALProxy


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
        """Vrátí všechny konstanty z daného modulu"""
        module = self.constant_modules.get(module_name)
        if not module:
            raise ValueError(f"Module {module_name} not found")
        
        return {
            k: v for k, v in vars(module).items()
            if k.isupper() and not callable(v)
        }

    def list_constant_modules(self):
        """Vrátí seznam dostupných modulů s konstantami"""
        return list(self.constant_modules.keys())
    