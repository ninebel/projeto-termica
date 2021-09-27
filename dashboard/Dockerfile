FROM python:3.8-slim-buster

EXPOSE 80

# Keeps Python from generating .pyc files in the container
ENV PYTHONDONTWRITEBYTECODE=1

# Turns off buffering for easier container logging
ENV PYTHONUNBUFFERED=1

# Sets a default directory where the application is going to be installed (root/app)
WORKDIR /api

# Copy files from computer to container
COPY config.py run.py requirements.txt ./
# Copy all the files in app folder to workdir/app/
COPY app app/

# Install pip requirements
RUN python3 -m pip install -r requirements.txt
RUN pip3 install -r requirements.txt

# Run Flask server
CMD ["gunicorn", "-w", "2", "--bind", "0.0.0.0:80", "run:app"]