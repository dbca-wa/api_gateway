# syntax = docker/dockerfile:1.2

# Prepare the base environment.
FROM ghcr.io/dbca-wa/docker-apps-dev:ubuntu_2510_base_python AS builder_base_apigw

LABEL maintainer="asi@dbca.wa.gov.au"
LABEL org.opencontainers.image.source="https://github.com/dbca-wa/api_gateway"

# FIELD_ENCRYPTION_KEY dummy value below for Build purposes only
ENV DEBIAN_FRONTEND=noninteractive \
    TZ=Australia/Perth \
    PRODUCTION_EMAIL=True  \
    SECRET_KEY="ThisisNotRealKey" \
    FIELD_ENCRYPTION_KEY="Mv12YKHFm4WgTXMqvnoUUMZPpxx1ZnlFkfGzwactcdM="


RUN apt-get clean && \
    apt-get update && \
    apt-get upgrade -y && \
    apt-get install --no-install-recommends -y \
    python3-pil \
    python3-venv \
    ssh


FROM builder_base_apigw AS configure_apigw

COPY startup.sh /

RUN chmod 755 /startup.sh && \
    chmod +s /startup.sh && \
    groupadd -g 5000 oim && \
    useradd -g 5000 -u 5000 oim -s /bin/bash -d /app && \
    usermod -a -G sudo oim && \
    echo "oim  ALL=(ALL)  NOPASSWD: /startup.sh" > /etc/sudoers.d/oim && \
    mkdir /app && \
    chown -R oim:oim /app && \
    mkdir /app/apigw/ && \
    mkdir /app/apigw/cache/ && \
    chmod 777 /app/apigw/cache/ && \
    ln -snf /usr/share/zoneinfo/$TZ /etc/localtime && echo $TZ > /etc/timezone && \
    rm -rf /tmp/*

FROM configure_apigw AS python_dependencies_apigw

WORKDIR /app
USER oim
ENV VIRTUAL_ENV_PATH=/app/venv
ENV PATH=$VIRTUAL_ENV_PATH/bin:$PATH

COPY --chown=oim:oim requirements.txt gunicorn.ini.py manage.py python-cron ./
COPY --chown=oim:oim .git ./.git
COPY --chown=oim:oim apigw ./apigw

RUN python3.12 -m venv $VIRTUAL_ENV_PATH
RUN $VIRTUAL_ENV_PATH/bin/pip3 install --upgrade pip && \
    $VIRTUAL_ENV_PATH/bin/pip3 install --no-cache-dir -r requirements.txt && \
    rm -rf /var/lib/{apt,dpkg,cache,log}/ /tmp/* /var/tmp/*

RUN $VIRTUAL_ENV_PATH/bin/python3 manage.py collectstatic --clear --noinput

FROM python_dependencies_apigw AS launch_apigw

EXPOSE 8080
HEALTHCHECK --interval=1m --timeout=5s --start-period=10s --retries=3 CMD ["wget", "-q", "-O", "-", "http://localhost:8080/"]
CMD ["/startup.sh"]

