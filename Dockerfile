FROM postgres:13.3
FROM python:3.9

ENV POSTGRES_PASSWORD=postgres
ENV POSTGRES_PASSWORD=httphuggingfapaceTSAGITSArenamapuserpass
ENV POSTGRES_DB=postgres

COPY ./table/init/ docker-entrypoint-initdb.d/

WORKDIR /usr/src/app/horses_test

COPY . .
COPY requirements.txt ./
RUN pip install --no-cache-dir -r requirements.txt

EXPOSE 5432
# CMD ["--port 5432"]
CMD ["/bin/bash", "-c", "python bot.py"]

# use
# сд сюда
# docker buildx build .
# docker images
# первые символы нового image поставить вместо 1234
# docker run -p 8080:5432 1234