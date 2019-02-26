FROM python:3.6-slim

#RUN apt-get update
#RUN apt-get upgrade -y

# Install your software
RUN pip install pysqlite3 

# Set working dir
WORKDIR .

# Copy dataset to working dir
COPY unique_tracks.txt .
COPY triplets_sample_20p.txt .

# Copy your code
COPY main.py .

# Set starting command (run your code)
CMD python main.py