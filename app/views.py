from flask import Blueprint
import services

bp = Blueprint("views", __name__)

from flask import render_template

@bp.route("/", methods=["GET"])
def index():
    # Obtener los datos del usuario con id 1 usando el servicio show_profile
    user = services.show_profile(1)
    # Renderizar la plantilla index.html con los datos del usuario
    return render_template("index.html", user=user)