FROM python:3


#RUN pip install --no-cache-dir -r requirements.txt
#RUN apt-get update  

#RUN apt-get upgrade \
#	&& apt-get install  python3-dev \
#RUN	 apt-get  python3-pip


# We copy just the requirements.txt first to leverage Docker cache
COPY ./requirements.txt /app/requirements.txt

WORKDIR /app

#RUN pip install -r requirements.txt

RUN pip install --no-cache-dir -r requirements.txt
#RUN apt-get update  

COPY . /app

ENTRYPOINT ["python"]

CMD ["app.py"]
