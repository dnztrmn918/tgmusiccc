FROM nikolaik/python-nodejs:python3.10-nodejs20

# 1. Sistemin Node.js'i görmesi için yolu (PATH) zorluyoruz
ENV PATH="/usr/bin:/usr/local/bin:${PATH}"

# 2. Senin orijinal ffmpeg kurulumun - dokunmadık
RUN curl -L https://johnvansickle.com/ffmpeg/releases/ffmpeg-release-amd64-static.tar.xz \
    -o ffmpeg.tar.xz && \
    tar -xJf ffmpeg.tar.xz && \
    mv ffmpeg-*-static/ffmpeg /usr/local/bin/ && \
    mv ffmpeg-*-static/ffprobe /usr/local/bin/ && \
    rm -rf ffmpeg*

# 3. Node.js'in kurulu olduğundan ve her yerden erişildiğinden emin oluyoruz
RUN apt-get update && apt-get install -y nodejs

COPY . /app/
WORKDIR /app/

RUN pip3 install --no-cache-dir -r requirements.txt

CMD ["bash", "start"]
