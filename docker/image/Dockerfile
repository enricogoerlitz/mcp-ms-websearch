FROM python:3.12-slim

WORKDIR /app

COPY ./backend/research-chat .

RUN pip install --no-cache-dir -r requirements.txt

EXPOSE 8000

# Run app.py when the container launches
# CMD ["python", "app.py"]
CMD if [ "$DEBUG" = "true" ] ; \
    then \
        python wsgi.py ; \
    else \
        gunicorn -b 0.0.0.0:8000 wsgi:app ; \
    fi
