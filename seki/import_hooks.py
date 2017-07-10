# encoding=utf-8
from .utils import singleton
import six
import ast
import sys

u"""
import hooks to activate macros
"""

class _MacroLoader(object):
    u"""
    see more detail at: https://www.python.org/dev/peps/pep-0302/
    """
    def __init__(self, module_name, mod):
        self.mod = mod
        sys.modules[module_name] = mod

    def load_module(self, fullname):
        self.mod.__loader__ = self
        return self.mod

@singleton
class MacroFinder(object):
    def _get_source(self, module_name, package_path):
        if six.PY2:
            import imp
            (file, pathname, desc) = imp.find_module(
                module_name.split('.')[-1],
                package_path
            )

            source_code = file.read()
            file.close()
            file_path = file.name
        else:
            from importlib.machinery import PathFinder
            loader = PathFinder.find_module(module_name, package_path)
            source_code = loader.get_source(module_name)
            file_path = loader.path

        return source_code, file_path

    def _construct_module(self, module_name, file_path):
        if six.PY3:
            from types import ModuleType
            mod = ModuleType(module_name)
        else:
            import imp
            mod = imp.new_module(module_name)

        mod.__package__ = module_name.rpartition('.')[0]
        mod.__file__ = file_path
        mod.__loader__ = _MacroLoader(module_name, mod)
        return mod


    def find_module(self, fullname, path = None):

        try:
            source, path = self._get_source(fullname, path)
        except:
            """pass if exception occur"""
            return None


        astree = ast.parse(source)
        code = compile(astree, path, "exec")
        module = self._construct_module(fullname, path)
        exec(code, module.__dict__)
        return module.__loader__

