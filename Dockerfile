FROM python:3

WORKDIR /usr/local/jobfinder
COPY run.sh ./
COPY requirements.txt ./
COPY ./src .
RUN pip install --no-cache-dir -r requirements.txt
RUN python -m nltk.downloader punkt
CMD [ "sh", "/usr/local/jobfinder/run.sh" ]
echo Current directory: $PWD
