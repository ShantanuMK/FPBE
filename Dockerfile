FROM python:3.10
WORKDIR /code
COPY ./app /code/app

ENV PYTHONPATH "${PYTHONPATH}:/code/app"
RUN pip install --no-cache-dir --upgrade -r /code/app/requirements.txt
EXPOSE 8080
CMD ["python3", "app/main.py"]
