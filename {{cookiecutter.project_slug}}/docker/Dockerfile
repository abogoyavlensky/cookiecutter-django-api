FROM python:3.6.4-alpine3.7

ENV PYTHONUNBUFFERED 1 \
  PYTHONHASHSEED=random \
  PIPENV_COLORBLIND=true \
  PIPENV_NOSPIN=true \
  PIP_NO_CACHE_DIR=0 \
  TZ=Europe/Moscow

# Create app user and group
RUN addgroup -S app && adduser -S -G app app

# Requirements have to be pulled and installed here, otherwise caching won't work
COPY ./Pipfile ./Pipfile.lock /

# Install build deps, then run `pip install`, then remove unneeded build deps.
RUN set -ex \
    && apk add --no-cache \
            libpq \
            zlib-dev \
            jpeg-dev \
            make \
            git \
            graphviz \
            ttf-freefont \
    && apk add --no-cache --virtual .build-deps \
            gcc \
            libc-dev \
            musl-dev \
            linux-headers \
            pcre-dev \
            postgresql-dev \
            build-base \
            libffi-dev \
            graphviz-dev \
    && pip install pipenv --upgrade \
    && pipenv install --system --dev --ignore-pipfile \
    && find /usr/local \
        \( -type d -a -name test -o -name tests \) \
        -o \( -type f -a -name '*.pyc' -o -name '*.pyo' \) \
        -exec rm -rf '{}' + \
    && runDeps="$( \
            scanelf --needed --nobanner --recursive /user/local \
                    | awk '{ gsub(/,/, "\nso:", $2); print "so:" $2 }' \
                    | sort -u \
                    | xargs -r apk info --installed \
                    | sort -u \
    )" \
    && apk add --virtual .python-rundeps $runDeps \
    && apk del .build-deps \
    && rm -rf ~/.cache

# Copy shell scripts
COPY ./docker/entrypoint.sh /entrypoint.sh
RUN sed -i 's/\r//' /entrypoint.sh && \
    chmod +x /entrypoint.sh && \
    chown app /entrypoint.sh

COPY ./docker/entrypoint-ci.sh /entrypoint-ci.sh
RUN sed -i 's/\r//' /entrypoint-ci.sh && \
    chmod +x /entrypoint-ci.sh && \
    chown app /entrypoint-ci.sh

COPY ./docker/start-dev.sh /start-dev.sh
RUN sed -i 's/\r//' /start-dev.sh && \
    chmod +x /start-dev.sh && \
    chown app /start-dev.sh

COPY ./docker/start-celeryall.sh /start-celeryall.sh
RUN sed -i 's/\r//' /start-celeryall.sh
RUN chmod +x /start-celeryall.sh && \
    chown app /start-celeryall.sh

COPY ./docker/gunicorn.sh /gunicorn.sh
RUN sed -i 's/\r//' /gunicorn.sh && \
    chmod +x /gunicorn.sh && \
    chown app /gunicorn.sh

WORKDIR /app

ARG DOCKER_ENTRYPOINT="entrypoint.sh"
RUN ln -s /${DOCKER_ENTRYPOINT} /executable
ENTRYPOINT ["/executable"]
