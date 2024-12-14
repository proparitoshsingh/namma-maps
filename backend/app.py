from flask import Flask, request, jsonify
import osmnx as ox
import networkx as nx
from flask_cors import CORS

app = Flask(__name__)

CORS(app)

print("Loading map...")
G = ox.graph_from_place("Bengaluru, India", network_type="drive")
G = ox.project_graph(G)
print("Map loaded and ready to go!")


@app.route('/shortest-path', methods=['POST'])
def shortest_path():
    try:
        data = request.json

        if 'origin' not in data or 'destination' not in data:
            return jsonify({"error": "Both origin and destination are required."}), 400

        origin_lat = data['origin']['lat']
        origin_lng = data['origin']['lng']
        destination_lat = data['destination']['lat']
        destination_lng = data['destination']['lng']

        if not (-90 <= origin_lat <= 90 and -180 <= origin_lng <= 180):
            return jsonify({"error": "Invalid origin coordinates."}), 400
        if not (-90 <= destination_lat <= 90 and -180 <= destination_lng <= 180):
            return jsonify({"error": "Invalid destination coordinates."}), 400

        origin_node = ox.distance.nearest_nodes(G, origin_lng, origin_lat)
        destination_node = ox.distance.nearest_nodes(G, destination_lng, destination_lat)

        shortestPath = nx.shortest_path(G, origin_node, destination_node, weight='length')
        coordinates = [(G.nodes[node]['y'], G.nodes[node]['x']) for node in shortestPath]

        return jsonify({"path": coordinates})

    except Exception as e:
        return jsonify({"error": str(e)}), 500
if __name__ == "__main__":
    app.run(debug=True)