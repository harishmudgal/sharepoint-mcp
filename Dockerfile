FROM python:3.11-slim
WORKDIR /app
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt
COPY . .
# Azure Container Apps default to port 8000 or 8080
EXPOSE 8000
# Use uvicorn to handle the Streamable HTTP traffic correctly
CMD ["uvicorn", "server:app", "--host", "0.0.0.0", "--port", "8000"]
