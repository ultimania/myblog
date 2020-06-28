#/bin/sh
# python /opt/${PROJECT_NAME}/manage.py shell_plus --notebook
export PROJECT_NAME="myblog"
export APP_REPOS="https://github.com/ultimania/myblog.git"

git clone ${APP_REPOS} /opt/${PROJECT_NAME}
cat /root/my_setting.py >> ~/opt/${PROJECT_NAME}/${PROJECT_NAME}/settings.py
python /opt/${PROJECT_NAME}/manage.py makemigrations
python /opt/${PROJECT_NAME}/manage.py migrate
python /opt/${PROJECT_NAME}/manage.py runserver 0.0.0.0:8080
