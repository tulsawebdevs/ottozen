source .virtualenvs/ottozen/activate
cd $OTTOZEN_HOME
python manage.py cron store_alerts
python manage.py cron send_alerts
