FROM python:3.9


RUN apt-get update && apt-get install -y \
    gcc \
    redis-server \
    && rm -rf /var/lib/apt/lists/*

WORKDIR /app

COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt
RUN pip install flagsmith

COPY . .

RUN chmod +x start.sh

EXPOSE 5000

CMD ["./start.sh"]
