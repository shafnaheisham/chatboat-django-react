FROM python:3.10-alpine3.16

ENV PYTHONUNBUFFERED 1

COPY ./requirements.txt /requirements.txt

ENV PATH="/scripts:${PATH}"

RUN apk add --upgrade --no-cache build-base linux-headers && \
    pip install --upgrade pip && \
    python -m venv /py && \
    pip install -r /requirements.txt

RUN pip install --no-cache-dir -r /requirements.txt
COPY ./backend /backend  
WORKDIR /backend
CMD ["uWSGI","python", "mange.py", "runserver", "0.0.0:8000"] 