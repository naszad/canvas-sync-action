FROM python:3.9-slim

# Install dependencies
COPY requirements.txt /requirements.txt
RUN pip install -r /requirements.txt

# Copy our sync script
COPY canvas-update.py /canvas-update.py

# Set the entrypoint
ENTRYPOINT ["python", "/canvas-update.py"] 