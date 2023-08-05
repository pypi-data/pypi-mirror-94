import asyncio
from pathlib import Path
from typing import Optional, Union

from jinja2 import Template
from pydantic import BaseModel
from snap_html import generate_image, HtmlDoc


class FormModel(BaseModel):
    __form__: Template = None

    def generate_image_sync(self, *args, **kwargs) -> bytes:
        return asyncio.get_event_loop().run_until_complete(self.generate_image(*args, **kwargs))

    async def generate_image(self, output_file: Optional[Union[Path, str]] = None) -> bytes:
        html = self.__form__.render(**self.dict())

        return await generate_image(
                target=HtmlDoc(html=html),
                resolution={"width": 1290, "height": 675},
                output_file=output_file
        )
