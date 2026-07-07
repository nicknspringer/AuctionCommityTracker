# Use python as base image
FROM python:3.14.6-slim

# copy current directory contents into container
copy . .

# Install dependencies
run pip instasll -r requirements.txt

# Make port 5000 available outside
EXPOSE 5000

# run the flask app
CMD ["python", "app.py"]