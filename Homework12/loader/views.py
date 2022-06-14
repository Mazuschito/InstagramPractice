from flask import render_template, Blueprint, request, current_app
import logging
from Homework12.classes.data_manager import DataManager
from Homework12.loader.exceptions import OutOfFreeNamesError, PictureFormatNotSupportedError, PictureNotUploadedError
from Homework12.loader.upload_manager import UploadManager

loader_blueprint = Blueprint('loader_blueprint', __name__, template_folder='templates')

logger = logging.getLogger("basic")


@loader_blueprint.route('/post', methods=["GET"])
def page_form():
    return render_template("post_form.html")


@loader_blueprint.route("/post", methods=["POST"])
def page_create_posts():
    path = current_app.config.get("POST_PATH")
    data_manager = DataManager(path)
    upload_manager = UploadManager()

    # Get data
    picture = request.files.get("picture", None)
    content = request.values.get("content", "")

    # Save image with upload manager

    filename_saved = upload_manager.save_with_random_name(picture)

    # Get path for client browser
    web_path = f"/uploads/images/{filename_saved}"

    # Create data to write in file
    post = {"pic": web_path, "content": content}

    # Add data to file
    data_manager.add(post)

    return render_template("post_uploaded.html", pic=web_path, content=content)


@loader_blueprint.errorhandler(OutOfFreeNamesError)
def error_out_of_free_names(e):
    return "No more free names to upload images. Contact the Administrator"


@loader_blueprint.errorhandler(PictureFormatNotSupportedError)
def error_out_of_free_names(e):
    logger.info("Format of the image is not supported")
    return "Format of the image is not supported. Please choose another one"


@loader_blueprint.errorhandler(PictureNotUploadedError)
def error_out_of_free_names(e):
    logger.error("NPicture was not uploaded")
    return "Picture was not uploaded. Contact the Administrator"
