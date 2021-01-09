# FROM leguark/gempy
FROM python:3.8

RUN apt-get update

RUN apt-get install -yq --no-install-recommends wget && \
    apt-get install -y libgl1-mesa-glx libsm6
RUN wget --quiet https://github.com/krallin/tini/releases/download/v0.9.0/tini && \
    echo "faafbfb5b079303691a939a747d7f60591f2143164093727e870b289a44d9872 *tini" | sha256sum -c
RUN mv tini /usr/local/bin/tini && \
    chmod +x /usr/local/bin/tini

ENV NB_USER smartVP

COPY . /home/$NB_USER/SMART_VP_server
WORKDIR /home/$NB_USER/SMART_VP_server

# Set vtk headless display
RUN sudo apt-get -y update && \
    sudo apt-get -y install xvfb & \
    export DISPLAY=:99.0 && \
    export PYVISTA_OFF_SCREEN=true && \
    export PYVISTA_USE_PANEL=true && \
    Xvfb :99 -screen 0 1024x768x24 > /dev/null 2>&1 & \
    sleep 3

RUN pip install -r requirements.txt

# Set the locale

ENV LANG en_US.UTF-8
ENV LANGUAGE en_US:en
ENV LC_ALL en_US.UTF-8

ENV FLASK_APP /home/$NB_USER/SMART_VP_server/app/wsgi.py

WORKDIR /home/$NB_USER/SMART_VP_server/app

EXPOSE 5000
RUN  cd /home/gempy/SMART_VP_server
ENTRYPOINT ["tini", "--", "python", "wsgi.py"]
