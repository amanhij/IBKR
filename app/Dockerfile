FROM python:3.11
ENV HOME=/app
WORKDIR $HOME
EXPOSE 8000

COPY requirements.txt $HOME
RUN pip install -r requirements.txt --no-cache-dir

COPY . $HOME
RUN python manage.py collectstatic --noinput

ENTRYPOINT ["python3"]
CMD ["manage.py", "runserver", "0.0.0.0:8000", "--noreload"]
