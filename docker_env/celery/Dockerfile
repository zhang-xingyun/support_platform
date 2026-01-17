FROM art-internal.test.com/library/dvadmin-pro/python38-base-backend:latest
WORKDIR /backend
COPY ./backend/ .
RUN awk 'BEGIN { cmd="cp -i ./conf/env.example.py   ./conf/env.py "; print "n" |cmd; }'
RUN python3 -m pip install -i https://art-internal.test.com/artifactory/api/pypi/pypi/simple -r requirements.txt
CMD ["celery", "-A", "application", "worker", "-B", "--loglevel=info"]

