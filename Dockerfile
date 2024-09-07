# Step 1: Use the official Python image as the base image
FROM python:3.9-slim

# Step 2: Set environment variables
ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1

# Step 3: Set the working directory in the container
WORKDIR /todoapp

# Step 4: Copy the requirements.txt file to the container
COPY requirements.txt .

# Step 5: Install the Python dependencies
RUN pip install --no-cache-dir -r requirements.txt

# Step 6: Copy the application code to the container
COPY . /todoapp

# Step 7: Expose the port FastAPI will run on
EXPOSE 8000

# Step 8: Run the FastAPI app with uvicorn
CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8000"]