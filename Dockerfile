FROM ubuntu:20.04

# Python 구동 환경 설정을 위한 명령어 설치
RUN apt-get update
RUN apt-get install --no-install-recommends -y python3 python3-venv python3-pip supervisor nginx
# for m2
RUN apt-get install --no-install-recommends -y git
RUN apt-get install --no-install-recommends -y postgresql gcc python3-dev libpq5 libpq-dev libhdf5-dev libxml2-dev libxslt1-dev libldap2-dev libsasl2-dev libffi-dev libjpeg-dev zlib1g-dev
RUN apt-get clean && rm -rf /var/lib/apt/lists/*

RUN mkdir /app
# python source를 복사한다.
COPY . /app
WORKDIR /app

# Python 수행 package 설치
RUN pip install --upgrade --ignore-installed pip setuptools
# RUN pip install ez_setup
RUN pip install -r requirements.txt

EXPOSE 8009

CMD ["python3", "run.py"]
