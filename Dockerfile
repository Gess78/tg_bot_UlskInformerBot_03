FROM python:3.9-slim
ENV BOT_NAME=$BOT_NAME

WORKDIR /usr/src/app/"${BOT_NAME:-tg_bot}"

COPY requirements.txt /usr/src/app/"${BOT_NAME:-tg_bot}"
RUN pip install -r /usr/src/app/"${BOT_NAME:-tg_bot}"/requirements.txt
RUN apt-get update && apt-get install -y  wkhtmltopdf
RUN #apk add --no-cache wkhtmltopdf
#RUN apt-get update && apt-get install -y wget
#RUN wget https://github.com/wkhtmltopdf/packaging/releases/download/0.12.6-1/wkhtmltox_0.12.6-1.focal_amd64.deb
#RUN apt-get update && apt-get install -y ./wkhtmltox_0.12.6-1.focal_amd64.deb
COPY . /usr/src/app/"${BOT_NAME:-tg_bot}"

CMD python3 -m bot
