FROM python:3.8-slim-buster
VOLUME /result

RUN apt update && \
    apt install -y git file gpg && \
    pip install git+https://github.com/niess/python-appimage pip-tools pipreqs && \
    mkdir -p /result

ADD . /thefuck
WORKDIR /thefuck/thefuck
RUN pipreqs --savepath=requirements.in &&\
        pip-compile && \
        rm ./requirements.in && \
        sed -i -e '1 i\\/thefuck' requirements.txt && \
        mv ./requirements.txt /thefuck/appimage

WORKDIR /thefuck
RUN python -m python_appimage build app -p 3.8 /thefuck/appimage

CMD cp /thefuck/thefuck-x86_64.AppImage /result
