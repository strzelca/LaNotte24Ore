FROM python:3.10-alpine
WORKDIR /app

# FLASK ENVIRONMENT VARIABLES
ENV FLASK_APP=app.py
ENV FLASK_RUN_HOST=0.0.0.0
ENV CONFIG_TYPE=config.ProductionConfig

LABEL org.opencontainers.image.source=https://github.com/owosrl/lanotte24ore
LABEL org.opencontainers.image.description="La Notte 24 Ore"
LABEL org.opencontainers.image.licenses=GPL-3.0-or-later

# INSTALL BUILD DEPS
RUN apk add --no-cache nodejs npm gcc g++ gfortran musl-dev jpeg-dev zlib-dev libffi-dev cairo-dev pango-dev gdk-pixbuf-dev
RUN python -m pip install --upgrade pip

COPY . .

# INSTALL AND BUILD DEPENDENCIES
RUN pip install -r requirements.txt
RUN npm install --save
RUN npm run build:prod

HEALTHCHECK --interval=30s --timeout=30s --start-period=5s --retries=3 CMD [ "python", "-m", "pytest", "-v" ]

EXPOSE 8080
CMD [ "python", "app.py" ]
