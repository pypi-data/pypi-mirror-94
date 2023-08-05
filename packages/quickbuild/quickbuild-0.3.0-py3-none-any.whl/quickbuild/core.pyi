import abc
from abc import ABC, abstractmethod
from collections import namedtuple
from quickbuild.endpoints.builds import Builds as Builds
from quickbuild.endpoints.users import Users as Users
from quickbuild.exceptions import QBError as QBError, QBForbidden as QBForbidden, QBNotFoundError as QBNotFoundError, QBProcessingError as QBProcessingError
from typing import Any, Callable, Optional

Response = namedtuple('Response', ['status', 'body'])
ServerVersion: Any

class QuickBuild(ABC, metaclass=abc.ABCMeta):
    builds: Any = ...
    users: Any = ...
    def __init__(self) -> None: ...
    @abstractmethod
    def close(self) -> None: ...
    @abstractmethod
    def request(self, callback: Callable, method: str, path: str, fcb: Optional[Callable]=..., **kwargs: Any) -> Any: ...
    def get_version(self) -> ServerVersion: ...
