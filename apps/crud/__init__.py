from flask import Blueprint, render_template

import apps.crud.models

crud = Blueprint("crud", __name__)

@crud.get("/")
def index():
    return render_template("crud/index.html")