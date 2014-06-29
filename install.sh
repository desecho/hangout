./installation_settings.sh

pip install -r requirements.txt
bower install

#install crontab records
crontab -l > crontab
echo "* * * * * $PYTHON_PATH/python $PWD/hangout_project/manage.py find_matches" > crontab
echo "0 0 * * * $PYTHON_PATH/python $PWD/hangout_project/manage.py update_visibility" > crontab
echo "* * * * * $PYTHON_PATH/python $PWD/hangout_project/manage.py disable_sleep_time" > crontab
echo "*/10 * * * * $PYTHON_PATH/python $PWD/hangout_project/manage.py disable_timer_time" > crontab
crontab crontab
rm crontab

cd hangout_project/static/bower/jquery-mobile-datebox/i18n/
./make-all-i18n.py
