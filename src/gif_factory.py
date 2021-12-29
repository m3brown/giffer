import asyncio
import os
from tempfile import gettempdir
import uuid

import aiofiles
from cache import cache
import httpx
from models import GifRequest
from moviepy.editor import *


class GifFactory(object):
    def __init__(self):
        self.tempdir = gettempdir() + "/"

    async def _write_bytes_to_file(self, data, filename):
        async with aiofiles.open(filename, "wb+") as file:
            await file.write(data)

    async def _download_gif(self, url):
        filename = self.tempdir + str(uuid.uuid4()) + ".gif"

        contents = await cache.get(url)
        if contents is None:
            async with httpx.AsyncClient() as client:
                resp = await client.get(url)
                task1 = asyncio.create_task(cache.set(url, resp.content))
                task2 = asyncio.create_task(
                    self._write_bytes_to_file(resp.content, filename)
                )
                await task1
                await task2
        else:
            await self._write_bytes_to_file(contents, filename)
        # TODO should confirm this is a gif image...
        return filename

    async def create(self, data: GifRequest):
        original_gif_file = await self._download_gif(str(data.gif))
        clip = VideoFileClip(original_gif_file)
        # Generate a text clip. You can customize the font, color, etc.
        txt_size = [
            clip.size[0] * data.text_width / 100,
            clip.size[1] * data.text_height / 100,
        ]
        txt_clip = TextClip(
            data.text,
            color="white",
            size=txt_size,
            method="caption",
            font=".fonts/unicode.impact.ttf",
            stroke_color="black",
            stroke_width=1,
        )

        txt_clip = txt_clip.set_position((data.hor_align, data.ver_align)).set_duration(
            clip.duration
        )

        # Overlay the text clip on the first video clip
        video = CompositeVideoClip([clip, txt_clip])

        os.remove(original_gif_file)

        # Write the result to a file
        filename = self.tempdir + str(uuid.uuid4()) + ".gif"
        video.write_gif(filename)
        return filename
