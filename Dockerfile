FROM python:3.9.5-slim-buster

RUN mkdir -p /app
WORKDIR /app

# Cache dependencies
COPY ./requirements.txt ./
RUN pip install -r requirements.txt

# Copy the rest
COPY . ./

ENTRYPOINT ["sh", "docker-entrypoint.sh"]
