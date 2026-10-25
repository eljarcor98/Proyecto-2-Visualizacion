import os
import sys
import importlib.util

_parent_file = os.path.abspath(os.path.join(os.path.dirname(__file__), '..', 'create_storytelling_dashboard.py'))

if os.path.exists(_parent_file):
    _spec = importlib.util.spec_from_file_location("_root_create_storytelling_dashboard", _parent_file)
    _mod = importlib.util.module_from_spec(_spec)
    _spec.loader.exec_module(_mod)
    build_dashboard = _mod.build_dashboard
    traduccion_paises = getattr(_mod, 'traduccion_paises', {})
else:
    def build_dashboard():
        raise FileNotFoundError("create_storytelling_dashboard.py no encontrado en el directorio raíz.")

if __name__ == '__main__':
    build_dashboard()
