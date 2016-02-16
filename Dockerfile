FROM centos:latest

ADD frontend/ /frontend 
ADD requirements.txt .

RUN yum install -y epel-release.noarch
RUN yum install -y python.x86_64 python-pip MySQL-python.x86_64
RUN pip install -r requirements.txt

EXPOSE 5050

CMD /bin/bash -c "export PYTHONPATH=/:$PYTHONPATH && python frontend/web.py"
