FROM python:3.9-slim

# Install dependencies
RUN pip install canvasapi>=3.0.0

# Copy our sync script
COPY canvas-update.py /canvas-update.py

# Set the entrypoint
ENTRYPOINT ["python", "/canvas-update.py"] 