FROM python:3.11-bookworm

WORKDIR /app

RUN apt-get update --yes --quiet
RUN apt-get install --yes --quiet --no-install-recommends
RUN apt-get install nodejs -y
RUN apt install npm -y --fix-missing

COPY requirements.txt .
RUN pip install -r requirements.txt

COPY . .

RUN python manage.py tailwind install
RUN python manage.py tailwind build
RUN python manage.py collectstatic --noinput --clear

RUN chown -R django:django /app
USER django

CMD gunicorn poketrader.wsgi:application --bind 0.0.0.0:8000
