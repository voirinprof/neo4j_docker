from flask import Flask, jsonify, request
from neo4j import GraphDatabase
import os
import math

app = Flask(__name__)

# Connexion à Neo4j
neo4j_uri = os.environ.get('NEO4J_URI')
neo4j_user = os.environ.get('NEO4J_USER')
neo4j_password = os.environ.get('NEO4J_PASSWORD')
driver = GraphDatabase.driver(neo4j_uri, auth=(neo4j_user, neo4j_password))

# Initialisation des données
def init_data():
    with driver.session() as session:
        # Supprimer les données existantes
        session.run("MATCH (n) DETACH DELETE n")
        # Ajouter des lieux avec coordonnées
        session.run("""
            CREATE (p1:Place {name: 'Central Park', longitude: -73.965355, latitude: 40.782865})
            CREATE (p2:Place {name: 'Times Square', longitude: -73.985130, latitude: 40.758896})
            CREATE (p3:Place {name: 'Statue of Liberty', longitude: -74.044500, latitude: 40.689247})
        """)

# Exécuter l'initialisation une seule fois au démarrage
with driver.session() as session:
    result = session.run("MATCH (n) RETURN count(n) AS count").single()
    if result["count"] == 0:
        init_data()

@app.route('/locations', methods=['GET'])
def get_locations():
    with driver.session() as session:
        result = session.run("MATCH (p:Place) RETURN p.name, p.longitude, p.latitude")
        locations = [
            {"name": record["p.name"], "longitude": record["p.longitude"], "latitude": record["p.latitude"]}
            for record in result
        ]
    return jsonify(locations)

@app.route('/locations/add', methods=['POST'])
def add_location():
    data = request.get_json()
    name = data.get('name')
    lon = float(data.get('longitude'))
    lat = float(data.get('latitude'))
    
    if not all([name, lon, lat]):
        return jsonify({"error": "Missing name, longitude, or latitude"}), 400
    
    with driver.session() as session:
        session.run(
            "CREATE (p:Place {name: $name, longitude: $lon, latitude: $lat})",
            name=name, lon=lon, lat=lat
        )
    return jsonify({"message": f"Added {name}"}), 201

@app.route('/locations/near', methods=['GET'])
def get_nearby_locations():
    try:
        lon = float(request.args.get('lon'))
        lat = float(request.args.get('lat'))
        max_distance = float(request.args.get('distance', 1000))  # mètres
        
        with driver.session() as session:
            result = session.run("""
                MATCH (p:Place)
                WITH p, point({latitude: $lat, longitude: $lon}) AS refPoint
                WITH p, point.distance(point({latitude: p.latitude, longitude: p.longitude}), refPoint) AS distance
                WHERE distance <= $max_distance
                RETURN p.name, p.longitude, p.latitude, distance
                ORDER BY distance
            """, lat=lat, lon=lon, max_distance=max_distance)
            
            locations = [
                {
                    "name": record["p.name"],
                    "longitude": record["p.longitude"],
                    "latitude": record["p.latitude"],
                    "distance": record["distance"]
                }
                for record in result
            ]
        return jsonify(locations)
    except Exception as e:
        return jsonify({"error": str(e)}), 400

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)