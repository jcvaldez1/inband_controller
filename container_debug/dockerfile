FROM frolvlad/alpine-python3
WORKDIR /code
RUN pip install flask
RUN pip install requests
RUN pip install websockets
COPY . .
CMD ["python", "./app_test.py"]
