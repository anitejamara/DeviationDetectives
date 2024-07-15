# Use an official Python runtime as a parent image
FROM python:3.12.4-slim

# Set the working directory in the container
WORKDIR /app

# Copy the current directory contents into the container at /app
COPY . .

# Install any needed packages specified in requirements.txt
RUN pip install --no-cache-dir -r requirements.txt

# Expose port 8000 to the outside world
EXPOSE 8000

# Run app.py when the container launches
CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8000"]


# FROM ubuntu

# RUN apt-get update && apt-get install -y --no-install-recommends \
#     python3.12 \
#     python3-pip \
#     && \
# apt-get clean && \
# rm -rf /var/lib/apt/lists/*

# RUN pip install fastapi  --break-system-packages
# RUN pip install uvicorn --break-system-packages
# RUN pip install pydantic --break-system-packages
# RUN pip install transformers --break-system-packages
# RUN pip install torch --break-system-packages
# RUN pip install PyMuPDF --break-system-packages
# RUN pip install levenshtein --break-system-packages
# RUN pip install scikit-learn --break-system-packages
# RUN pip install sentence-transformers --break-system-packages
# RUN pip install scipy --break-system-packages
# RUN pip install python-Levenshtein --break-system-packages
# RUN pip install fastapi-cors --break-system-packages
# RUN pip install python-multipart --break-system-packages
# RUN pip install PyPDF2 --break-system-packages

# COPY . .



# # # Set working directory
# # WORKDIR /app

# # Expose the port your application listens on
# EXPOSE 8000  

# # CMD ["cd",".."]

# # Start your application using uvicorn with hot reloading and debug logging
# CMD ["uvicorn", "app.main:app", "--reload", "--log-level", "debug"]
