
FROM python:3.10
ENV PYTHONUNBUFFERED 1
WORKDIR /test_task
COPY requirements.txt /test_task/
RUN pip install --no-cache-dir -r requirements.txt
COPY . /test_task/
RUN python manage.py migrate
RUN python manage.py collectstatic --noinput
CMD ["python", "manage.py", "runserver", "0.0.0.0:8000"]