FROM python:3

MAINTAINER Byron Ruth <b@devel.io>

# Install dependencies
RUN apt-get -qq update && apt-get -qq install unzip libaio1

ADD instantclient-basic-linux.x64-11.2.0.4.0.zip /app/
ADD instantclient-sdk-linux.x64-11.2.0.4.0.zip /app/

RUN unzip -qq /app/instantclient-basic-linux.x64-11.2.0.4.0.zip -d /usr/local/lib
RUN unzip -qq /app/instantclient-sdk-linux.x64-11.2.0.4.0.zip -d /usr/local/lib
RUN ln -s /usr/local/lib/instantclient_11_2/libclntsh.so.11.1 /usr/local/lib/instantclient_11_2/libclntsh.so

ENV ORACLE_HOME /usr/local/lib/instantclient_11_2
ENV LD_LIBRARY_PATH /usr/local/lib/instantclient_11_2

# Contents of requirements.txt each on a separate line for incremental builds
RUN pip install SQLAlchemy==0.9.8
RUN pip install psycopg2==2.5.4
RUN pip install mysqlclient==1.3.9
RUN pip install cx-Oracle==5.2.1

ADD . /src

WORKDIR /src

ENTRYPOINT ["python", "/src/main.py"]
