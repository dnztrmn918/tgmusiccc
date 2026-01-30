FROM nikolaik/python-nodejs:python3.10-nodejs20

# Senin orijinal ffmpeg kurulumun - dokunmadım
RUN curl -L https://johnvansickle.com/ffmpeg/releases/ffmpeg-release-amd64-static.tar.xz \
    -o ffmpeg.tar.xz && \
    tar -xJf ffmpeg.tar.xz && \
    mv ffmpeg-*-static/ffmpeg /usr/local/bin/ && \
    mv ffmpeg-*-static/ffprobe /usr/local/bin/ && \
    rm -rf ffmpeg*

# Node.js'in sistem tarafından tanınması için gerekli ekleme
# (Eksik olan ve botun çökmesine sebep olan kısım buydu)
RUN apt-get update && apt-get install -y nodejs

COPY . /app/
WORKDIR /app/

RUN pip3 install --no-cache-dir -r requirements.txt

CMD ["bash", "start"]
