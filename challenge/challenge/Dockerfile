FROM python:3.7

# Create app directory
WORKDIR /app

# Install app dependencies
COPY requirements.txt /app

RUN pip install -r /app/requirements.txt

# Bundle app source
COPY src /app
COPY data /app

CMD [ "python", "/app/summarize.py", "input.jsonl" ]