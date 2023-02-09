FROM python:3.10-alpine
WORKDIR /app
ENV FLASK_APP=app.py
ENV FLASK_RUN_HOST=0.0.0.0
ENV CONFIG_TYPE=config.ProductionConfig
RUN apk add --no-cache nodejs npm gcc g++ musl-dev jpeg-dev zlib-dev libffi-dev cairo-dev pango-dev gdk-pixbuf-dev linux-headers
RUN python -m pip install --upgrade pip
COPY . .
RUN pip install -r requirements.txt
RUN npm install --save
RUN npm run build:prod
HEALTHCHECK --interval=30s --timeout=30s --start-period=5s --retries=3 CMD [ "python", "-m", "pytest", "-v" ]
EXPOSE 8080
CMD [ "python", "app.py" ]
