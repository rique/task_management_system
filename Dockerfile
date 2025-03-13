# Use an official Python runtime as a parent image
FROM python:3.12

# Set the working directory in the container
WORKDIR /app

# Copy the requirements file into the container
COPY requirements.txt /app/

# Install any dependencies
RUN pip install --no-cache-dir -r requirements.txt

# Copy the project files into the container
COPY . /app/

# Run migrations.
RUN python manage.py makemigrations
RUN python manage.py migrate

# Expose the port that the app runs on
EXPOSE 8888

# Run migrations and start the development server
CMD ["python", "manage.py", "runserver", "0.0.0.0:8000"]

