# Use AWS provided base image for Python 3.10 Lambda runtime
FROM public.ecr.aws/lambda/python:3.10

# Copy your app.py into the container at /var/task
COPY app.py ${LAMBDA_TASK_ROOT}/

# Install dependencies
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Set the CMD to your handler function
CMD ["app.lambda_handler"]
