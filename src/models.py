from typing import Literal
from typing import TypeVar

from pydantic import AnyHttpUrl
from pydantic import BaseModel
from pydantic import Field
from pydantic import PositiveInt

HorizontalIntStr = TypeVar(
    "HorizontalIntStr", PositiveInt, Literal["center", "left", "right"]
)
VerticalIntStr = TypeVar("VerticalIntStr", PositiveInt, Literal["top", "bottom"])


class GifRequest(BaseModel):
    text: str = Field(..., description="Text to render on the image")
    gif: AnyHttpUrl = Field(
        None, description="URL of the image. Leave blank if providing 'search'"
    )
    search: str = Field(
        None, description="Search term to find image. Leave blank if providing 'gif'"
    )
    hor_align: HorizontalIntStr = Field(
        "center",
        description="Horizontal alignment, as a word (center) or integer offset",
    )
    ver_align: VerticalIntStr = Field(
        "top",
        description="Vertical alignment, as a word (top, bottom) or integer offset",
    )
    text_height: int = Field(
        20, gt=0, lt=100, description="Text height, as a percentage of the image"
    )
    text_width: int = Field(
        60, gt=0, lt=100, description="Text width, as a percentage of the image"
    )

    class Config:
        schema_extra = {
            "example": {
                # example2:
                # {
                #     "text": "time for work",
                #     "gif": "http://25.media.tumblr.com/tumblr_m810e8Cbd41ql4mgjo1_500.gif",
                # }
                "text": "hey guys",
                "search": "elf wave",
            }
        }
