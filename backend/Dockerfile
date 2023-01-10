FROM python:3.10.8

# Set the working directory to /app
WORKDIR /app
COPY ./ ./

RUN pip install -r requirements.txt

ENV FLASK_RUN_HOST=0.0.0.0
ENV FLASK_APP=run.py

CMD ["flask", "run"]