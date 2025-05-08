# Step 1: Use an official Python runtime as a parent image
FROM python:3.12-slim 

# Step 2: Set the working directory in the container
WORKDIR /app

# Step 3: Copy the requirements.txt file into the container
COPY requirements.txt .

# Step 4: Install the dependencies
RUN pip install --no-cache-dir -r requirements.txt

# Step 5: Copy the rest of the app into the container
COPY . .

# Step 6: Expose the port FastAPI will run on
EXPOSE 8000

# Step 7: Run the FastAPI app using Uvicorn
CMD ["uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "8000", "--reload"]
