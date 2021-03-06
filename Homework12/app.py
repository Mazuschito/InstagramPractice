import logging

from flask import Flask, request, render_template, send_from_directory
from main.views import main_blueprint
from loader.views import loader_blueprint
import loggers

app = Flask(__name__)

app.register_blueprint(main_blueprint)
app.register_blueprint(loader_blueprint)

app.config["POST_PATH"] = "data/posts.json"
app.config["UPLOAD_FOLDER"] = "uploads/images"

loggers.create_logger()

logger = logging.getLogger("basic")


# this allows to view files from uploads folder
@app.route("/uploads/<path:path>")
def static_dir(path):
    return send_from_directory("uploads", path)

logger.info("Application starts")

app.run(debug=True)

