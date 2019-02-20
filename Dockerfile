FROM python:3.6

ENV PYTHONPATH /

COPY . .

RUN pip install -r requirements.txt
RUN pip install -r test-requirements.txt

CMD pytest
