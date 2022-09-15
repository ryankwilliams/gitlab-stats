FROM python:3
WORKDIR /usr/src/app
ADD merge_request_stats.py .
ADD requirements.txt .
RUN pip3 install --no-cache -r requirements.txt && rm -rf requirements.txt
ENTRYPOINT [ "python3", "merge_request_stats.py"]
