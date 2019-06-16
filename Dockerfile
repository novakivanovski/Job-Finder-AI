FROM python:3

WORKDIR /usr/local/jobfinder
COPY requirements.txt ./
COPY ./src .
RUN pip install --no-cache-dir -r requirements.txt
RUN python -m nltk.downloader punkt
ENTRYPOINT [ "/bin/bash", "run.sh"]