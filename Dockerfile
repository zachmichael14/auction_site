# Use the official Python image as the base image
FROM python:3.11

# Set the working directory in the container
WORKDIR /ibuy

# Copy the application files into the working directory
COPY . /ibuy

# Install the application dependencies
RUN pip install pipenv
RUN pipenv install --system --deploy

# Define the entry point for the container
CMD ["python", "manage.py", "runserver", "0.0.0.0:8000"]