FROM python:3.10-alpine
WORKDIR /app
ENV FLASK_APP=app.py
ENV FLASK_RUN_HOST=0.0.0.0
ENV FLASK_RUN_PORT=5000
ENV CONFIG_TYPE=config.ProductionConfig
RUN apk add --no-cache nodejs npm gcc musl-dev jpeg-dev zlib-dev libffi-dev cairo-dev pango-dev gdk-pixbuf-dev linux-headers
RUN python -m pip install --upgrade pip
COPY . .
RUN pip install -r requirements.txt
RUN npm run build:prod
EXPOSE 5000
CMD [ "flask", "--app", "app", "run"]
