from typing import Dict, Optional, cast, TypeVar, Type
from dataclasses import dataclass
from pytket.config import PytketConfig, PytketExtConfig

T = TypeVar("T", bound="QSharpConfig")


@dataclass
class QSharpConfig(PytketExtConfig):
    resourceId: Optional[str]
    location: Optional[str]
    storage: Optional[str]

    @classmethod
    def from_pytketconfig(cls: Type[T], config: PytketConfig) -> T:
        if "qsharp" in config.extensions:
            config_dict = cast(Dict[str, str], config.extensions["qsharp"])
            return cls(
                config_dict.get("resourceId"),
                config_dict.get("location"),
                config_dict.get("storage"),
            )
        return cls(None, None, None)
