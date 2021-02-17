FROM python:3.7

# to print all console outputs in real time
ENV PYTHONUNBUFFERD 1

# create work directory and use it for the project
RUN mkdir -p /usr/www/finalProject/pytweet
WORKDIR /usr/www/finalProject/pytweet


# copy requirements.txt from this directory to the work directory
#  install the necessary requirements
COPY requirements.txt /usr/www/finalProject/pytweet
RUN pip install --upgrade pip
RUN pip install -r requirements.txt

#  copy all the files in your project folder into the work directory
COPY . /usr/www/finalProject/pytweet

