from flask import Blueprint, jsonify, request

from weather.utils import geocode_city, get_city_statistics


cities_bp = Blueprint("cities", __name__)


@cities_bp.route("/autocomplete", methods=["GET"])
def autocomplete():
    query = request.args.get("term")
    if not query:
        return jsonify([])

    # Используем кэшированную функцию геокодирования
    suggestions = geocode_city(query)
    return jsonify(suggestions)


@cities_bp.route("/city_statistics", methods=["GET"])
def city_statistics():
    stats = get_city_statistics()
    return jsonify(stats)
