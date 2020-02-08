FROM python:3

# Install numpy using system package manager
RUN apt-get -y update && apt-get -y install imagemagick

ENV PROJECT_HOME=/app
ENV GIPHY_API_KEY=

RUN mkdir $PROJECT_HOME
WORKDIR $PROJECT_HOME
COPY requirements.txt $PROJECT_HOME
COPY src/ $PROJECT_HOME
COPY .fonts $PROJECT_HOME/.fonts
#COPY .magick $PROJECT_HOME/.magick
COPY .magick/policy.xml /etc/ImageMagick-6/policy.xml

RUN pip install -r requirements.txt

# install ffmpeg from imageio.
RUN python -c "import imageio; imageio.plugins.ffmpeg.download()"

#add soft link so that ffmpeg can executed (like usual) from command line
RUN ln -s /root/.imageio/ffmpeg/ffmpeg.linux64 /usr/bin/ffmpeg

# modify ImageMagick policy file so that Textclips work correctly.
#RUN cat /etc/ImageMagick-6/policy.xml | sed 's/none/read,write/g'> /etc/ImageMagick-6/policy.xml 

EXPOSE 8000

CMD ["gunicorn", "-b", "0.0.0.0:8000", "app:app"]
