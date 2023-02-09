from web import create_app
from datetime import datetime
from waitress import serve
from config import Config

app = create_app("lanotte24ore")

@app.template_filter()
def format_datetime(value):
    return datetime.strptime(value, "%Y-%m-%dT%H:%M:%SZ").strftime("%d %B %Y")

if __name__ == '__main__':
    serve(app, host=Config.HOST, port=Config.PORT)
