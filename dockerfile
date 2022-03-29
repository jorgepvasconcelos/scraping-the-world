FROM python:3.8-slim-buster
COPY ./requirements.txt /var/www/requirements.txt
WORKDIR /var/www
RUN pip install -r requirements.txt
COPY . /var/www
WORKDIR /var/www
ENV PYTHONPATH "${PYTHONPATH}:/var/www/scraping_the_world"
CMD [ "python", "scraping_the_world/app.py" ]