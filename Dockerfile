FROM python:3.11-slim

RUN pip install --upgrade pip

WORKDIR /app
COPY . /app

RUN apt-get update && apt-get install -y \
    libgl1-mesa-glx \
    libglib2.0-0 \
    ffmpeg \
    && rm -rf /var/lib/apt/lists/*

RUN mkdir photos
RUN pip install -r requirements.txt

CMD ["python", "run_bot.py"]