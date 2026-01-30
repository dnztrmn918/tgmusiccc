FROM nikolaik/python-nodejs:python3.10-nodejs20

RUN apt-get update && apt-get install -y ffmpeg nodejs

WORKDIR /app
COPY . .

# Bağımlılıkları en baştan temiz bir şekilde kuruyoruz
RUN pip3 install --upgrade pip
RUN pip3 install --no-cache-dir -r requirements.txt

CMD ["python3", "-m", "ShrutiMusic"]
