# Use python as base image
FROM python:3.14.6-slim

#create working directory
WORKDIR /app

# copy current directory contents into container
COPY . /app

# Install dependencies
RUN pip install -r requirements.txt

# Make port 5000 available outside
EXPOSE 5000

# run the flask app
CMD ["python", "app.py", "--host=0.0.0.0", "--port=5000"]