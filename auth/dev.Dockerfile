FROM tiangolo/uvicorn-gunicorn-fastapi:python3.7

RUN pip install --upgrade pip
COPY ./app/requirements.txt .
RUN pip install -r requirements.txt
COPY ./app /app
CMD ["/start-reload.sh"]