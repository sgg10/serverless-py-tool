DOCKER_TEMPLATE="""# Use a build stage to install dependencies
FROM public.ecr.aws/lambda/python:${python_runtime} AS build

# Set the working directory
WORKDIR $${LAMBDA_TASK_ROOT}

# Copy requirements file if it exists, and install packages
COPY requirements.txt ./
RUN if [ -f "requirements.txt" ]; then pip install --no-cache-dir -r requirements.txt; fi

# Start the final stage
FROM public.ecr.aws/lambda/python:${python_runtime}

# Set the working directory
WORKDIR $${LAMBDA_TASK_ROOT}

# Copy installed packages from the build stage
COPY --from=build $${LAMBDA_TASK_ROOT} $${LAMBDA_TASK_ROOT}

# Copy all other necessary files and directories
COPY . .

# Set the CMD to your handler
CMD [ "${lambda_package}.${lambda_handler}" ]
"""

LAMBDA_FUNCTION_TEMPLATE="""import os
import json

import boto3


def ${lambda_handler}(event, context):
    print("Event: ", event)
    print("Context: ", context)

    return event
"""
