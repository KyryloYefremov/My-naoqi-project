# client/fetch_naoqi_constants.py
import os, sys
from naoqi_client import ALProxyWrapper
from config import *


class ConstantGenerator:
    def __init__(self, output_dir=""):
        self._output_dir = output_dir
        self._const_proxy = ALProxyWrapper("CONSTANTS", IP, PORT)
        
    def generate_all(self):
        # create output directory
        os.makedirs(self._output_dir, exist_ok=True)
        
        # get a list of available modules (should be 2)
        modules = self._const_proxy.list_modules()
        
        # generate every module
        for module_name in modules:
            print(">>>" + module_name)
            self._generate_module(module_name)
            
    def _generate_module(self, module_name):
        constants = self._const_proxy.get_constants(module_name)
        
        with open(f"{self._output_dir}/{module_name}.py", "w") as f:
            # create a particular module and put all specific constants there
            f.write(f"# Auto-generated constants from {module_name}\n\n")
            for name, value in constants.items():
                f.write(f"{name} = {repr(value)}\n")
                
        print(f"Generated {module_name}.py with {len(constants)} constants")


if __name__ == "__main__":
    generator = ConstantGenerator(os.getcwd())
    generator.generate_all()
    print("Constants generation completed!")