from flask import Blueprint, render_template
from app.models.models import Direction

main = Blueprint('main', __name__)

@main.route('/')
def index():
    directions = Direction.query.all()  # Получаем все направления из базы данных
    return render_template('main/index.html', directions=directions)