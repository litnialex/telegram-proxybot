FROM python:3.10-alpine
COPY ./ /app/
RUN pip3 install -r /app/proxybot/requirements.txt
CMD /app/flasksrv.py
EXPOSE 8080
EXPOSE 8443
