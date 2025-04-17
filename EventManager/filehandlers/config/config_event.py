from pydantic import BaseModel
import atomics


class ConfigEvent(BaseModel):
    __debugging_mode: bool = False
    __informational_mode: bool = False
    __time_format: atomics.strings.String = "%Y-%m-%d %H:%M:%S"