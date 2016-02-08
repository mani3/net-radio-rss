#!/usr/bin/env sh

ENV_DIR=flask
if [ ! -d "${ENV_DIR}" ]; then
  ./env.sh ${ENV_DIR}
fi

source ${ENV_DIR}/bin/activate

# Run migration
if [ ! -d "migrations" ]; then
  python manage.py db init
fi
python manage.py db migrate -m "`date '+%Y%m%d%H%M'`"
python manage.py db show
python manage.py db upgrade

gunicorn app:app -c `pwd`/gunicorn_conf.py
deactivate

