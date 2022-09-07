FROM python:3.10-slim

WORKDIR /app

COPY . .

RUN pip install pipenv && \
    pipenv install --deploy --system && \
    pip uninstall pipenv -y

# Wait for postgres
ADD https://github.com/ufoscout/docker-compose-wait/releases/download/2.9.0/wait /wait
RUN chmod +x /wait

CMD /wait && python src/bot.py