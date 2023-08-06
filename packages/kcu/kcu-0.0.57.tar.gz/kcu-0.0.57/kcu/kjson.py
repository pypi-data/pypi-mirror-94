# --------------------------------------------------------------- Imports ---------------------------------------------------------------- #

# System
from typing import Union, Optional, Dict, List, Tuple, Hashable, Any
import json, builtins, os

# Pip
from noraise import noraise
from .filelock import FileLock

# ---------------------------------------------------------------------------------------------------------------------------------------- #



# ---------------------------------------------------------- Public properties ----------------------------------------------------------- #

JSONData = Union[
    str, int, float, bool,
    Dict[Hashable, Any],
    List[Any],
    Tuple[Any]
]


# ------------------------------------------------------------ Public methods ------------------------------------------------------------ #

def get_value(
    d: dict,
    key: Hashable,
    default_value: Optional[any] = None
) -> Optional[any]:
    return d[key] if key in d else default_value

def load(
    path: str,
    default_value: Optional[JSONData] = None,
    save_if_not_exists: bool = False
) -> Optional[JSONData]:
    try:
        with open(path, 'r') as file:
            obj = json.load(file)
    except:
        obj = None

    if obj is None:
        if default_value is not None:
            obj = default_value

            if save_if_not_exists:
                save(path, obj)

    return obj

@noraise()
def load_sync(
    path: str,
    default_value: Optional[JSONData] = None,
    save_if_not_exists: bool = False,
    timeout: Optional[float] = None
) -> Optional[JSONData]:
    with FileLock(path, timeout=timeout):
        return load(path=path, default_value=default_value, save_if_not_exists=save_if_not_exists)

def save(
    path: str,
    obj: Optional[JSONData]
) -> bool:
    with open(path, 'w') as file:
        json.dump(obj, file, indent=4)

    return os.path.exists(path)

@noraise()
def save_sync(
    path: str,
    obj: Optional[JSONData],
    timeout: Optional[float] = None
) -> bool:
    with FileLock(path, timeout=timeout):
        return save(path=path, obj=obj)

def print(obj: JSONData) -> None:
    builtins.print(json.dumps(obj, indent=4))


# ---------------------------------------------------------------------------------------------------------------------------------------- #