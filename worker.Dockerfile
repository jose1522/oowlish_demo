FROM python:3.9.15-bullseye as requirements-stage
WORKDIR /tmp
ADD requirements /tmp
RUN pip install pip-tools
RUN make base.txt & pip install -r base.txt
FROM python:3.9.15-bullseye
ADD ./worker /worker
COPY --from=requirements-stage /tmp/base.txt requirements.txt
RUN pip install --no-cache-dir --upgrade -r requirements.txt
WORKDIR /worker
EXPOSE 8080/tcp
CMD ["uvicorn", "main:app", "--port", "8080", "--host", "127.0.0.1"]