FROM python:3.7

# Create app directory
WORKDIR /app



# Bundle app source
COPY src /app
COPY data /app

CMD [ "python", "/app/summarize.py", "input.jsonl" ]