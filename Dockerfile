FROM python:3.7
RUN apt-get update \
    && apt-get install -y --no-install-recommends \
        postgresql-client \
    && rm -rf /var/lib/apt/lists/*

WORKDIR /app

ADD . /app

COPY ./requirements.txt /app/requirements.txt

RUN pip install -r requirements.txt

COPY . /app

#EXPOSE 8000
#CMD ["python", "manage.py", "runserver", "0.0.0.0:8000"]
