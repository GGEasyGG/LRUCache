FROM python:3.10

RUN pip install pipenv

RUN mkdir /root/LRUcache

WORKDIR /root/LRUcache

COPY Pipfile Pipfile.lock LRUcache.py Fibonachi.py ./

RUN pipenv install --system --deploy

ENTRYPOINT ["python", "Fibonachi.py"]
