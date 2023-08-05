from typing import TypeVar,Any, Tuple,Callable, Coroutine, Dict, List, Optional, Sequence, Type, Union
from types import FunctionType
T = TypeVar("T")
Decorated = TypeVar("Decorated", bound=Callable[..., Any])
ApiFunc = TypeVar("ApiFunc", bound=Callable[..., Any])
Servicer = TypeVar("Servicer", bound=Callable[..., Any])
ServicerImpl = TypeVar("ServicerImpl", bound=Callable[..., Any])
ServicerApi = TypeVar("ServicerApi", bound=Callable[..., Any])
ServicerApiImpl = TypeVar("ServicerApiImpl", bound=Callable[..., Any])
ServicerApiReq = TypeVar("ServicerApiReq", bound=Callable[..., Any])
ServicerApiRes = TypeVar("ServicerApiRes", bound=Callable[..., Any])
