FROM python:3.9


RUN mkdir -p /usr/src/app
WORKDIR /usr/src/app/


EXPOSE 5050
COPY requirements.txt /usr/src/app/


RUN pip3 install -r /usr/src/app/requirements.txt


#Copying Flask App files
COPY app.py /usr/src/app/
COPY utils.py /usr/src/app/

ENV OPENAI_API_KEY=""


CMD ["python","-u","/usr/src/app/app.py"]