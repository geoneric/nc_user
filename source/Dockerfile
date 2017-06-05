FROM posbank.geoneric.eu:5000/nca/nc_base:latest

MAINTAINER Kor de Jong <k.dejong1@uu.nl>

COPY cmd.sh server.py server_flask.py uwsgi.ini /
COPY nc_user /nc_user
COPY test /test

CMD ["/cmd.sh"]
