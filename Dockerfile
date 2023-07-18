FROM python:3.10

RUN pip install --upgrade pip
ADD requirments.txt /
RUN pip install -r /requirments.txt
