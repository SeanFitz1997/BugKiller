from collections import Callable
from types import ModuleType
from typing import List, Any


def get_object_public_attributes(obj: Any) -> List[Any]:
    return [v for k, v in vars(obj).items() if not k.startswith('_')]


def get_object_public_values(obj: Any) -> List[Any]:
    return [attr for attr in get_object_public_attributes(obj) if not callable(attr)]


def get_object_public_methods(obj: Any) -> List[Callable]:
    return [attr for attr in get_object_public_attributes(obj) if callable(attr)]


def get_local_function_in_module(module: ModuleType) -> List[Callable]:
    functions = get_object_public_methods(module)
    local_functions = [f for f in functions if f.__module__ == module.__name__]
    return local_functions
