import os
import types
import marshal
import importlib.util

def get_pyc(file_name):
    p = os.path.dirname(os.path.abspath(__file__)).split("/")
    file_path = os.path.join("/", *p[1:4], "src", *p[5:6],*p[5:6], "lib/pyc", file_name)
    pyc = open(file_path, 'rb').read()
    code = marshal.loads(pyc[16:])
    module = types.ModuleType('module_name')
    exec(code, module.__dict__)
    return module

def get_py(file_name):
    p = os.path.dirname(os.path.abspath(__file__)).split("/")
    file_path = os.path.join("/", *p[1:4], "src", *p[5:6], *p[5:6], "lib", file_name)

    spec = importlib.util.spec_from_file_location("module_name", file_path)
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module

basic = get_py("012_deploy_lib.py")
