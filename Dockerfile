FROM python:3.12-bookworm

WORKDIR /app

RUN apt-get update --yes
RUN apt-get install --yes --no-install-recommends
RUN apt-get install nodejs -y
RUN apt install npm -y --fix-missing

COPY requirements.txt .
RUN pip install -r requirements.txt

COPY . .

RUN python manage.py init_data
RUN python manage.py tailwind install
RUN python manage.py tailwind build
RUN python manage.py collectstatic --noinput --clear
RUN python manage.py migrate

CMD gunicorn poketrader.wsgi:application --bind 0.0.0.0:8000
