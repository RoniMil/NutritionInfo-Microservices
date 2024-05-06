FROM python:3.10.10-alpine
WORKDIR ./app
RUN pip install flask
RUN pip install flask_restful
RUN pip install pymongo
COPY diets.py .
EXPOSE 5002
ENV FLASK_APP=diets.py
ENV FLASK_RUN_HOST=0.0.0.0
ENV FLASK_RUN_PORT=5002
CMD ["flask", "run"]
