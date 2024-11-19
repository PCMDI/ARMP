from pathlib import Path

from ARMP.io.input import set_dir
from ARMP.lib.control import init_dataclass
from ARMP.lib.convention import Setting

# ##import ARMP.params.config as config
# ##import json
# ##import os
# print(os.getcwd())


base_dir = Path(__file__).parent.parent
config_file = (base_dir / "params/config.in").resolve()

with open(config_file, "r") as f:
    params_in = f.read()

params_in = "\n".join(
    line for line in params_in.splitlines() if not line.strip().startswith("#")
)

exec(params_in)

excluded_vars = {"f", "config_file_path", "params_in"}


if not Path(globals()["dir_in"]).is_absolute():
    dir_in = set_dir(globals()["dir_in"])

if not Path(globals()["dir_out"]).is_absolute():
    dir_out = set_dir(globals()["dir_out"])

if not Path(globals()["dir_fig"]).is_absolute():
    dir_fig = set_dir(globals()["dir_fig"])


# print("dir_in = ",dir_in)

# dic = {var: getattr(config, var) for var in dir(config) if not var.startswith("__")}
# dic = {var: getattr(params_in, var) for var in dir(params_in) if not var.startswith("__")}
# dic = {var: globals()[var] for var in globals() if not var.startswith("__")}

dic = {
    var: globals()[var]
    for var in globals()
    if not var.startswith("__")  # Exclude special Python variables
    and not callable(globals()[var])  # Exclude functions or callable objects
    # and not isinstance(globals()[var], type(os))
    # and isinstance(globals()[var], (str, int, float, bool, Path))
    # and var not in globals().get("__builtins__", {})
    and var not in excluded_vars and var != "excluded_vars"
}

# print("\ndic= ", dic)
# print(json.dumps(dic, indent=4))

setting = init_dataclass(Setting, dic)
