# Import everything needed to edit video clips
import os
from tempfile import gettempdir
from urllib.request import urlretrieve
import uuid

from moviepy.editor import *


class GifFactory(object):
    def __init__(self):
        self.tempdir = gettempdir() + "/"

    def _download_gif(self, url):
        filename = self.tempdir + str(uuid.uuid4()) + ".gif"
        urlretrieve(url, filename)
        # TODO should confirm this is a gif image...
        return filename

    def create(
        self,
        text,
        gif,
        hor_align="center",
        ver_align="top",
        text_height=20,
        text_width=60,
    ):

        original_gif_file = self._download_gif(gif)
        clip = VideoFileClip(original_gif_file)
        # Generate a text clip. You can customize the font, color, etc.
        txt_size = [clip.size[0] * text_width / 100, clip.size[1] * text_height / 100]
        txt_clip = TextClip(
            text,
            color="white",
            size=txt_size,
            method="caption",
            font=".fonts/unicode.impact.ttf",
            stroke_color="black",
            stroke_width=1,
        )

        txt_clip = txt_clip.set_position((hor_align, ver_align)).set_duration(
            clip.duration
        )

        # Overlay the text clip on the first video clip
        video = CompositeVideoClip([clip, txt_clip])

        os.remove(original_gif_file)

        # Write the result to a file
        filename = self.tempdir + str(uuid.uuid4()) + ".gif"
        video.write_gif(filename)
        return filename
