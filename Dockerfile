FROM python:3.10-slim-bullseye
WORKDIR /app

# FLASK ENVIRONMENT VARIABLES
ENV FLASK_APP=app.py
ENV FLASK_RUN_HOST=0.0.0.0
ENV CONFIG_TYPE=config.ProductionConfig

LABEL org.opencontainers.image.source=https://github.com/owosrl/lanotte24ore
LABEL org.opencontainers.image.description="La Notte 24 Ore"
LABEL org.opencontainers.image.licenses=GPL-3.0-or-later

# INSTALL BUILD DEPS
RUN apt-get update && apt-get install -y curl
RUN curl -fsSL https://deb.nodesource.com/setup_current.x | bash -
RUN apt-get install -y nodejs build-essential musl-dev
RUN python -m pip install --upgrade pip

COPY . .

# INSTALL AND BUILD DEPENDENCIES
RUN pip install --no-cache -r requirements.txt
RUN npm install --save
RUN npm run build:prod

HEALTHCHECK --interval=30s --timeout=30s --start-period=5s --retries=3 CMD [ "python", "-m", "pytest", "-v" ]

EXPOSE 8080
CMD [ "python", "app.py" ]
