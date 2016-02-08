#!/usr/bin/env sh

DIR=$(cd $(dirname $0) && pwd)
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


GUNICORN=${DIR}/${ENV_DIR}/bin/gunicorn
ROOT=${DIR}
PID=/var/run/gunicorn/gunicorn_net_radio_rss.pid
APP=app:app

if [ -f $PID ]; then rm $PID; fi

cd $ROOT
exec $GUNICORN -c $ROOT/gunicorn_conf.py --pid=$PID $APP &

deactivate
