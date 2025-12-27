# Use a lightweight base image
FROM python:3.12-slim

WORKDIR /app

# Copy requirements and install
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copy all code
COPY . .

# Set port for Cloud Run
ENV PORT=8080
EXPOSE 8080

# Start Streamlit
CMD ["bash", "-lc", "streamlit run app/streamlit_app.py --server.port $PORT --server.address 0.0.0.0"]

