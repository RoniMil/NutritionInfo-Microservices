FROM python:3.10.10-alpine
WORKDIR ./app
RUN pip install flask
RUN pip install flask_restful
RUN pip install pymongo
RUN pip install requests
RUN pip install python-dotenv
COPY dishes_meals.py .
EXPOSE 5001
ENV FLASK_APP=dishes_meals.py
ENV FLASK_RUN_HOST=0.0.0.0
ENV FLASK_RUN_PORT=5001
CMD ["flask", "run"]