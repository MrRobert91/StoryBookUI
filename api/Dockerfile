FROM python:3.11-slim
WORKDIR /app

# Copy requirements first
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# CHANGE: Copy the current directory (.) into /app/api
# This ensures that 'import api.main' works if we run from /app
COPY . ./api/

# CHANGE: Set PYTHONPATH to /app so python can find the 'api' package
ENV PYTHONPATH=/app

# CHANGE: Run command now points to the module inside the api package
CMD ["uvicorn", "api.main:app", "--host", "0.0.0.0", "--port", "8000"]
