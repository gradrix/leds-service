from flask import Flask, send_from_directory
from api.endpoints import register_api

# Built assets have content hashes in their names, so they may be cached for a long time.
ONE_YEAR_SECONDS = 31536000

app = Flask(__name__, static_folder="frontend_build", static_url_path="/content")
app.config["SEND_FILE_MAX_AGE_DEFAULT"] = ONE_YEAR_SECONDS

register_api(app)


@app.route("/")
def index():
    return send_from_directory("frontend_build", "index.html", max_age=0)
