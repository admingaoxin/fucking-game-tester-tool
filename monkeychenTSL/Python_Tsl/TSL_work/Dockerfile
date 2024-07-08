FROM python:3.10
COPY ./ /app
WORKDIR /app
RUN pip install -r requirements.txt -i https://mirrors.cloud.tencent.com/pypi/simple
RUN sed -i 's#http://deb.debian.org/debian#https://mirrors.cloud.tencent.com/debian#g' /etc/apt/sources.list &&  \
    sed -i 's#http://security.debian.org/debiansecurity#https://mirrors.cloud.tencent.com/debian-security#g' /etc/apt/sources.list
RUN apt update
RUN apt install -y libgconf-2-4 libatk1.0-0 libatk-bridge2.0-0 libgdk-pixbuf2.0-0 libgtk-3-0 libgbm-dev libnss3-dev libxss-dev libasound2 fonts-arphic-ukai fonts-arphic-uming default-jre
RUN dpkg -i allure_2.24.1-1_all.deb
CMD ["python", "main.py"]