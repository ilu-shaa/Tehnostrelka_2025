# search_service/search_app.py

from flask import Flask, request, jsonify
from synonyns import expand_query

app = Flask(__name__)

@app.route('/')
def index():
    return "Search service is running!"

@app.route('/expand', methods=['GET'])
def expand():
    """
    Пример:
      GET /expand?q=любовь
    Вернёт JSON: ["romance","love","relationship","романтика","любовь"]
    """
    query = request.args.get('q', '')
    expanded = expand_query(query)
    return jsonify(expanded)

@app.route('/autocomplete', methods=['GET'])
def autocomplete():
    """
    Заглушка для автодополнения. В реальном проекте 
    здесь можно возвращать популярные запросы,
    жанры, названия.
    """
    query = request.args.get('q', '').lower()
    # Например, просто возвращаем ["film1","film2"] (заглушка)
    if not query:
        return jsonify([])

    # Пример - любые 3 подсказки:
    suggestions = [f"{query}_1", f"{query}_2", f"{query}_3"]
    return jsonify(suggestions)

if __name__ == "__main__":
    app.run(host="127.0.0.1", port=5000, debug=True)