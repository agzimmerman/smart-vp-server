# FROM leguark/gempy
FROM python:3.8

# WORKDIR /home/$NB_USER/work

#RUN apt-get update && \
#    apt-get install -y \
#        git \
#        openssh-server \
#        libmysqlclient-dev && \
#    pip install --upgrade pip


# add credentials on build
# ARG ssh_prv_key

# Authorize SSH Host
#RUN mkdir -p /root/.ssh && \
#    chmod 0700 /root/.ssh && \
#    ssh-keyscan github.com > /root/.ssh/known_hosts

# Add the keys and set permissions
#RUN echo "$ssh_prv_key" > /root/.ssh/id_rsa && \
#    chmod 600 /root/.ssh/id_rsa && \
#    echo '00000001' >/dev/null && git clone git@github.com:farmin-developers/gempy_server.git && \
#    rm -rf /root/.ssh/
RUN apt-get update && apt-get install -yq --no-install-recommends wget && \
    apt-get install -y libgl1-mesa-glx libsm6 && \
    wget --quiet https://github.com/krallin/tini/releases/download/v0.9.0/tini && \
    echo "faafbfb5b079303691a939a747d7f60591f2143164093727e870b289a44d9872 *tini" | sha256sum -c - && \
    mv tini /usr/local/bin/tini && \
    chmod +x /usr/local/bin/tini

ENV NB_USER gempy

COPY . /home/$NB_USER/work/gempy_server
WORKDIR /home/$NB_USER/work/gempy_server

RUN sudo apt-get -y update && \
    sudo apt-get -y install xvfb & \
    export DISPLAY=:99.0 && \
    export PYVISTA_OFF_SCREEN=true && \
    export PYVISTA_USE_PANEL=true && \
    Xvfb :99 -screen 0 1024x768x24 > /dev/null 2>&1 & \
    sleep 3

RUN pip install -r requirements.txt


# Set the locale
#RUN sed -i -e 's/# en_US.UTF-8 UTF-8/en_US.UTF-8 UTF-8/' /etc/locale.gen && \
#    locale-gen
ENV LANG en_US.UTF-8
ENV LANGUAGE en_US:en
ENV LC_ALL en_US.UTF-8

ENV FLASK_APP /home/$NB_USER/work/gempy_server/app/wsgi.py

WORKDIR /home/$NB_USER/work/gempy_server/app

EXPOSE 5000

RUN mkdir -m 777 -p /root/.theano && cd /home/gempy/work/gempy_server && pip install . && pytest
ENTRYPOINT ["tini", "--", "python", "wsgi.py"]
#ENTRYPOINT ["tini", "--", "flask", "run",  "-h", "0.0.0.0", "-p", "5000", "--with-threads", "--debugger"]