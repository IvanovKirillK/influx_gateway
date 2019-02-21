FROM python:3.6

ENV PYTHONPATH=$PYTHONPATH:$(pwd)

COPY . .

RUN pip install -r requirements.txt
RUN pip install -r test-requirements.txt

CMD ls -la
CMD pytest
