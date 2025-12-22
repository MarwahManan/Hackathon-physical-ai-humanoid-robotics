# Use Python 3.11 slim image
FROM python:3.11-slim

# Set working directory
WORKDIR /api

# Copy requirements file
COPY requirements.txt .

# Install dependencies
RUN pip install --no-cache-dir -r requirements.txt

# Copy the rest of the application
COPY . .

# Expose port 8000
EXPOSE 8000

# Run the application
CMD ["python", "rag_chatbot.py", "api", "--host", "0.0.0.0", "--port", "8000"]