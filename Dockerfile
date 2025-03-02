
FROM python:3.11-buster

WORKDIR /home

COPY code/main.py .
COPY code/config.json .
COPY docs/requirements.txt .

RUN pip install -r requirements.txt
RUN pip install grobid-client

RUN git clone https://github.com/kermitt2/grobid_client_python && cd grobid_client_python && python setup.py install
RUN cd ..

CMD ["python", "-u", "main.py"]