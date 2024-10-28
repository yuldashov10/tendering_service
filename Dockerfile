FROM python:3.10-slim

WORKDIR /app
COPY requirements.txt .

RUN pip install --no-cache-dir -r requirements.txt
COPY . .

ENV SERVER_ADDRESS=0.0.0.0:8080
ENV POSTGRES_CONN=postgres://username:password@localhost:5432/dbname
ENV POSTGRES_JDBC_URL=jdbc:postgresql://localhost:5432/dbname
ENV POSTGRES_USERNAME=postgres
ENV POSTGRES_PASSWORD=postgres
ENV POSTGRES_HOST=localhost
ENV POSTGRES_PORT=5432
ENV POSTGRES_DATABASE=zadanie_db

EXPOSE 8080

COPY entrypoint.sh /app/entrypoint.sh
RUN chmod +x /app/entrypoint.sh

CMD ["/app/entrypoint.sh"]
