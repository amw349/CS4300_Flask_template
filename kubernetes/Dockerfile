#Read from Ubuntu Base Image
FROM python:2.7
RUN mkdir -p /service
# Copy over all the files of interest
ADD requirements.txt /service/requirements.txt
RUN pip install -r /service/requirements.txt
ADD app /service/app
ADD app.py /service/app.py
ADD config.py /service/config.py
ADD manage.py /service/manage.py
WORKDIR /service/
CMD python -u app.py $APP_SETTINGS $DATABASE_URL
