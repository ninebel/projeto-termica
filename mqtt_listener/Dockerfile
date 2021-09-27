FROM python:3.8-slim-buster

EXPOSE 5001

# Keeps Python from generating .pyc files in the container
ENV PYTHONDONTWRITEBYTECODE=1

# Turns off buffering for easier container logging
ENV PYTHONUNBUFFERED=1

# Sets a default directory where the application is going to be installed (root/app)
WORKDIR /mqtt_listener

# Copy files from computer to container
COPY config.py main.py requirements.txt ./

# Install pip requirements
RUN python3 -m pip install -r requirements.txt
RUN pip3 install -r requirements.txt

# Run Python script
CMD ["python3", "main.py"]