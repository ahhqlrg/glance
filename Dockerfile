FROM registry.fit2cloud.com/public/python:v3
MAINTAINER glance Team <ibuler@qq.com>

WORKDIR /opt/glance
RUN useradd glance

COPY ./requirements /tmp/requirements

RUN yum -y install epel-release && cd /tmp/requirements && \
    yum -y install $(cat rpm_requirements.txt)

RUN cd /tmp/requirements &&  pip install -r requirements.txt

COPY . /opt/glance
COPY config_docker.py /opt/glance/config.py
VOLUME /opt/glance/data
VOLUME /opt/glance/logs

ENV LANG=zh_CN.UTF-8
ENV LC_ALL=zh_CN.UTF-8

EXPOSE 8080
ENTRYPOINT ["./entrypoint.sh"]
