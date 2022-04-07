FROM oraclelinux:7-slim

ENV PATH="/usr/local/bin:${PATH}"
ENV VERIFY_CHECKSUM=false

RUN  yum install -y git && \
     yum-config-manager --disable ol7_developer_EPEL && \
     yum install -y oracle-epel-release-el7 python36 && \
     rm -rf /var/cache/yum && \
     groupadd --gid 1000 fn && \
     adduser --uid 1000 --gid fn fn && \
     curl https://raw.githubusercontent.com/helm/helm/main/scripts/get-helm-3 | bash && \ 
     mv /usr/local/bin/helm /usr/bin/helm



WORKDIR /function
ADD requirements.txt .
RUN python3 -m pip install --upgrade pip && \
    python3 -m pip install -r requirements.txt
COPY func.py /function/
ENV PYTHONPATH="$PYTHONPATH:/function"
ENTRYPOINT ["fdk", "/function/func.py", "handler"]