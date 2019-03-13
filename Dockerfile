FROM python:3.6-alpine

COPY src/ /application
COPY requirements.pip /application
COPY ./entrypoint.sh /bin/entrypoint.sh
COPY ./app_env /bin/

WORKDIR /application
RUN \
 apk add --no-cache postgresql-libs && \
 apk add --no-cache --virtual .build-deps gcc musl-dev postgresql-dev && \
 python3 -m pip install -r requirements.pip --no-cache-dir && \
 apk --purge del .build-deps


RUN pip install -U pip

EXPOSE 5000
RUN chmod +x /bin/entrypoint.sh

CMD ["entrypoint.sh"]