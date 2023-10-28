FROM python:3.11-alpine-3.17
WORKDIR /app
COPY . .
RUN python3 -m venv venv
RUN source venv/bin/activate
RUN pip install -r requirements.txt
CMD ["streamlit", "run", "webapp.py"]
