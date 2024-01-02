FROM python:3.9

WORKDIR /config
COPY ./light-client-exporter.py ./requirements.txt /config/
RUN pip3 install -r requirements.txt
ENV PORT=3000

CMD "python3" "light_client_exporter.py" "$light_client_rpc"
