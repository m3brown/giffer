FROM python:3

# Install numpy using system package manager
RUN apt-get -y update && apt-get -y install imagemagick

ENV PROJECT_HOME=/app
ENV GIPHY_API_KEY=

RUN mkdir $PROJECT_HOME
WORKDIR $PROJECT_HOME
COPY requirements.txt $PROJECT_HOME
COPY src/ $PROJECT_HOME
COPY .magick/policy.xml /etc/ImageMagick-6/policy.xml

RUN pip install -r requirements.txt

#add soft link so that ffmpeg can executed (like usual) from command line
RUN ln -s /home/myuser/.imageio/ffmpeg/ffmpeg.linux64 /usr/bin/ffmpeg

# Run the image as a non-root user
RUN adduser -system myuser
USER myuser

# install ffmpeg from imageio.
RUN python -c "import imageio; imageio.plugins.ffmpeg.download()"

CMD ["uvicorn", "--host", "0.0.0.0", "--reload", "app:app"]
