FROM oraclelinux:7-slim

RUN  yum install -y git && \
     yum-config-manager --disable ol7_developer_EPEL && \
     yum install -y oracle-epel-release-el7 python36 && \
     rm -rf /var/cache/yum && \
     groupadd --gid 1000 fn && \
     adduser --uid 1000 --gid fn fn

WORKDIR /function
ADD requirements.txt .
RUN python3 -m pip install --upgrade pip && \
    python3 -m pip install -r requirements.txt
COPY func.py /function/
ENV PYTHONPATH="$PYTHONPATH:/function"
ENTRYPOINT ["fdk", "/function/func.py", "handler"]