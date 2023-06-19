<p align="center"><img src="https://github.com/owosrl/LaNotte24Ore/raw/main/web/static/assets/img/logo/logo_nobg.png"></img></p>

![](https://github.com/strzelca/LaNotte24Ore/actions/workflows/production.yaml/badge.svg) ![](https://img.shields.io/github/license/strzelca/LaNotte24Ore) ![](https://img.shields.io/github/languages/top/strzelca/LaNotte24Ore)

La Notte 24 Ore is a news aggregator powered by NewsAPI for Terranova.


### **Back-end**
* Supabase PostgreSQL
* GraphQL
* Flask
* Openweathermap API
* IPInfo API
* NewsAPI

### **Front-end**
* PostCSS
* Tailwind CSS


### **Docker**
Run with docker-compose:

```bash
docker-compose up -d
```

**Avaliable environment variables**:

* `NEWS_API_KEY` - _NewsAPI key_
* `WEATHER_API_KEY` - _OpenWeatherMap key_
* `IPINFO_API_KEY` - _IPInfo key_
* `SUPABASE_URL` - _Supabase URL_
* `SUPABASE_KEY` - _Supabase key_
* `AUTH_TEST_USER` - _Test user for auth_
* `AUTH_TEST_PASSWORD` - _Test password for auth_

## **Project Team**

- [@einstein1510](https://github.com/einstein1510) | _Project Manager_
- [@strzelca](https://github.com/strzelca) | _Back-end, Front-end and development environment_
- [@lelux666](https://github.com/lelux666)  | _Front-end_
- [@Eciuz](https://github.com/Eciuz) | _Front-end_



_This project is under GNU General Public License v3.0_
