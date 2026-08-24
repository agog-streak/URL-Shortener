from flask import (
    Blueprint,
    jsonify,
    redirect,
    render_template,
    request
)

from app.services import (
    create_short_url,
    get_url_by_code,
    is_valid_url
)

#Створюємо Blueprint
main = Blueprint(
    "main",
    __name__
)

@main.route("/", methods=["GET"])

#Головна сторінка
def index():
    return render_template("index.html")

@main.route("/shorten", methods=["POST"])

#Створення короткого посилання
def shorten_url():
    data = request.get_json(silent=True)
    if not data:
        return jsonify({
            "error": "Request body must contain JSON"
        }), 400
    
    # Отримуємо URL.
    original_url = data.get("url")

    # Перевіряємо наявність URL.
    if not original_url:
        return jsonify({
            "error": "URL is required"
        }), 400

    # Перевіряємо коректність URL.
    if not is_valid_url(original_url):
        return jsonify({
            "error": "Invalid URL"
        }), 400

    # Створюємо скорочену посилання.
    url = create_short_url(original_url)

    # Отримуємо адрес поточного сервера.

    # Наприклад:
    #
    # http://localhost:5000
    base_url = request.host_url.rstrip("/")

    # Формуємо коротку посилання.
    short_url = f"{base_url}/{url.short_code}"

    # Повертаємо JSON.
    return jsonify({
        "original_url": url.original_url,
        "short_code": url.short_code,
        "short_url": short_url,
        "clicks": url.clicks
    }), 201

@main.route("/<short_code>", methods=["GET"])
# Перехід за коротким посиланням
def redirect_to_original(short_code):
    # Отримуємо URL з бази.
    url = get_url_by_code(short_code)

    # Якщо такого кода немає,
    # повертаємо помилку 404.
    if url is None:
        return jsonify({
            "error": "Short URL not found"
        }), 404

    # Збільшуємо кількість переходів.
    url.clicks += 1

    # Зберігаємо нове значення.
    from app import db

    db.session.commit()

    # Перенаправлюєио користувача
    # на оригінальний URL.
    return redirect(url.original_url)

@main.route("/api/stats/<short_code>", methods=["GET"])
#Повертаємо статистику по короткому посиланню
def statistics(short_code):
    # Шукаємо посилання.
    url = get_url_by_code(short_code)

    # Якщо посилання відсутнє.
    if url is None:
        return jsonify({
            "error": "Short URL not found"
        }), 404

    # Повертаємо статистику.
    return jsonify({
        "id": url.id,
        "original_url": url.original_url,
        "short_code": url.short_code,
        "clicks": url.clicks,
        "created_at": url.created_at.isoformat()
    })