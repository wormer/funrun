FROM alpine:3.4
# Use alpine v3.5 for uwsgi-python3 (get rid of this once there is an official Docker tag)
RUN sed -i -e 's/v3\.4/v3.5/' /etc/apk/repositories

WORKDIR /app
CMD docker/entrypoint.sh
EXPOSE 80

RUN apk add --no-cache \
		bash \
		build-base \
		libjpeg-turbo-dev `# for Pillow` \
		nginx \
		postgresql-dev \
		python3 \
		python3-dev \
		sudo \
		supervisor \
		uwsgi \
		uwsgi-python3 \
		zlib-dev `# for Pillow` && \
	pip3 install --no-cache-dir --upgrade pip setuptools && \
	rm -rf /etc/nginx/conf.d && ln -s /app/docker/nginx /etc/nginx/conf.d && \
	ln -snf /app/docker/supervisor.d /etc/supervisor.d && \
	adduser -S app

COPY requirements.txt ./
RUN pip3 install --no-cache-dir --disable-pip-version-check -r requirements.txt

COPY . ./
