FROM python:3
WORKDIR /
COPY . .
EXPOSE 8080
CMD ["python", "-u", "servidor.py"]