FROM python:3.13.5-bookworm
COPY . .
RUN  pip install -r requirements.txt
CMD ["python", "-m", "backend.app.src.app.app"]
