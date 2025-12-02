from flask import Flask, jsonify, request, render_template
from quotes_manager import QuoteManager
import logging

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

app = Flask(__name__, static_folder="static", template_folder="templates")
qm = QuoteManager("quotes.json")

# UI route
@app.route("/")
def index():
    return render_template("index.html")

# API routes
@app.route("/api/quotes", methods=["GET"])
def list_quotes():
    return jsonify(qm.list_quotes()), 200

@app.route("/api/quote", methods=["GET"])
def random_quote():
    q = qm.get_random()
    if not q:
        return jsonify({"message": "no quotes available"}), 404
    return jsonify(q), 200

@app.route("/api/quotes/<int:qid>", methods=["GET"])
def get_quote(qid):
    q = qm.get_by_id(qid)
    if not q:
        return jsonify({"message": "quote not found"}), 404
    return jsonify(q), 200

@app.route("/api/quotes", methods=["POST"])
def create_quote():
    data = request.get_json(silent=True)
    if data is None:
        return jsonify({"message": "invalid or missing JSON"}), 400

    text = (data.get("text") or "").strip()
    author = (data.get("author") or "").strip()

    if not text:
        return jsonify({"message": "quote text is required"}), 400

    try:
        new = qm.add_quote(text=text, author=author)
        logger.info("Added quote id=%s", new.get("id"))
        return jsonify(new), 201
    except Exception as e:
        logger.exception("Error adding quote")
        return jsonify({"message": "internal server error"}), 500

@app.route("/api/quotes/<int:qid>", methods=["PUT"])
def update_quote(qid):
    data = request.get_json(silent=True)
    if data is None:
        return jsonify({"message": "invalid or missing JSON"}), 400

    text = data.get("text")
    author = data.get("author")

    try:
        updated = qm.update_quote(qid, text=text, author=author)
        if not updated:
            return jsonify({"message": "quote not found"}), 404
        return jsonify(updated), 200
    except Exception:
        logger.exception("Error updating quote id=%s", qid)
        return jsonify({"message": "internal server error"}), 500

@app.route("/api/quotes/<int:qid>", methods=["DELETE"])
def delete_quote(qid):
    try:
        ok = qm.delete_quote(qid)
        if not ok:
            return jsonify({"message": "quote not found"}), 404
        return jsonify({"message": "deleted"}), 200
    except Exception:
        logger.exception("Error deleting quote id=%s", qid)
        return jsonify({"message": "internal server error"}), 500

if __name__ == "__main__":
    app.run(host="127.0.0.1", port=5000, debug=True)
