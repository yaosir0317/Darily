from flask import Blueprint
from flask import jsonify

import settings
from settings import RESULT

app_content = Blueprint("app_content", __name__)


@app_content.route("/content", methods=["POST"])
def get_content():
    content = list(settings.Mongo_DB.TeddyBears.find({}))

    for index, item in enumerate(content):
        content[index]["_id"] = str(item.get("_id"))

    RESULT["error_not"] = 0
    RESULT["msg"] = "查询的内容"
    RESULT["data"] = content

    return jsonify(RESULT)
