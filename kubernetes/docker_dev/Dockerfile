FROM centos
LABEL maintainer="Ultimania <yng.ultimania.gmail.com>"
WORKDIR /root

# OS Packagesインストール
# COPY ./centos7.repo /etc/yum.repos.d/
ENV PATH="$PATH:/usr/local/python/bin"
ENV PYTHON_VERSION="3.8.2"
ENV DJANGO_VERSION="3.0.5"
ENV DB_NAME="django"
RUN set -x && \
    # dnf -y install mariadb-devel libffi-devel xz xz-devel git zlib-devel bzip2 bzip2-devel openssl-devel gcc make && \
    dnf -y install mariadb-devel libffi-devel xz xz-devel git gcc make && \
    cd /usr/local/src && \
    curl -O https://www.python.org/ftp/python/${PYTHON_VERSION}/Python-${PYTHON_VERSION}.tgz && \
    tar xvzf Python-${PYTHON_VERSION}.tgz && \
    cd Python-${PYTHON_VERSION} && \
    ./configure --prefix=/usr/local/python && \
    make && \
    make install && \
    cd ~ && \
    ln -s /usr/local/python/bin/python3 /usr/local/bin/python && \
    ln -s /usr/local/python/bin/pip3 /usr/local/bin/pip

# pip Packagesインストール
RUN set -x && \
    pip install --upgrade pip && \
    pip install django==${DJANGO_VERSION} && \
    pip install django-filter && \
    pip install mysqlclient && \
    pip install sphinx Pillow && \
    pip install pycrypto && \
    pip install gensim && \
    pip install django-extensions && \
    pip install jupyterlab
    pip install django-widget-tweaks && \
    ## pip install uwsgi && \
    ## pip install django-hamlpy && \
    ## pip install mpl_finance && \
    ## pip install PyMySQL && \
    ## django-admin startproject ${PROJECT_NAME}

# Djangoプロジェクトの作成
COPY ./kubernetes/docker_dev/my_setting.py /root/
COPY ./kubernetes/docker_dev/startup.sh /root/
RUN set -x && \
    useradd admin -G root && \
    chmod 777 /root/startup.sh
ENV DB_HOST="django-dev"

# DBの同期, API Server起動
CMD [ "/bin/sh" , "/root/startup.sh"]