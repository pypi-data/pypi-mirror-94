from grpc_tools._protoc_compiler import run_main
from grpc_tools.protoc import main as protoc_main
import os
import sys
import pkg_resources


def list_dir(file_dir, file_type=None, filenames=None):
    L = []
    for root, dirs, files in os.walk(file_dir):
        for file in files:
            if filenames and file_type:
                if file in [i + file_type for i in filenames]:
                    L.append(os.path.join(root, file))
                continue
            if not file_type or os.path.splitext(file)[1] == file_type:
                L.append(os.path.join(root, file))
    return L


def protoBuild(proto_input_dir, output_dir, building_type=['message', 'service']):
    import subprocess
    if sys.executable is None:
        raise unittest.SkipTest(
            "Running on a interpreter that cannot be invoked from the CLI.")
    proto_dir_path = os.path.abspath(proto_input_dir)
    protoc_args = [sys.executable, "-m", "grpc_tools.protoc", "--proto_path", proto_dir_path]
    building_type = [building_type] if isinstance(building_type, str) else building_type
    for type in building_type:
        if type == 'message':
            protoc_args.extend(["--python_out", os.path.abspath(output_dir)])
        if type == 'service':
            protoc_args.extend(["--grpc_python_out", os.path.abspath(output_dir)])
    for proto in list_dir(proto_dir_path, '.proto'):
        protoc_args.append(proto)
        proc = subprocess.Popen(protoc_args)
        proc.wait()
        protoc_args = protoc_args[:-1]
