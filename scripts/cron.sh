source .virtualenvs/ottozen/activate
cd $OTTOZEN_HOME
python ottozen/manage.py cron store_alerts
python ottozen/manage.py cron send_alerts
