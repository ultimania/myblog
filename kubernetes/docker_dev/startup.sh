#/bin/sh
# python /opt/${PROJECT_NAME}/manage.py shell_plus --notebook
git clone ${APP_REPOS} /opt/${PROJECT_NAME}
cat ~/${PROJECT_NAME}/${PROJECT_NAME}/my_setting.py >> ~/opt/${PROJECT_NAME}/${PROJECT_NAME}/settings.py
python /opt/${PROJECT_NAME}/manage.py makemigrations
python /opt/${PROJECT_NAME}/manage.py migrate
python /opt/${PROJECT_NAME}/manage.py runserver 0.0.0.0:8080
