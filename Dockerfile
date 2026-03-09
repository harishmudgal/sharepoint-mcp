FROM python:3.11-slim
WORKDIR /app
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt
COPY . .
# Azure Container Apps default to port 8000 or 8080
EXPOSE 8000
# Run the script - FastMCP will now start an SSE server on port 8000
CMD ["python", "server.py"]
