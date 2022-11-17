from flask import Flask, render_template
from flask_assets import Environment, Bundle


app = Flask(__name__)
assets = Environment(app)
css = Bundle("src/css/style.css", filters="postcss", output="css/style.css")
assets.register("css", css)
css.build()

@app.route('/')
def index():
    return render_template('index.html')

def main():
    app.run(debug=True)

if __name__ == '__main__':
    main()