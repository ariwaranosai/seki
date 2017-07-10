import sys
from .import_hooks import MacroFinder

sys.meta_path.insert(0, MacroFinder())
