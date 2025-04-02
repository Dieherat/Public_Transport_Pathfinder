import os
import sys
import json
from flask import Flask, render_template, jsonify, request

# Add project root to Python path
project_root = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
sys.path.insert(0, project_root)

# Now import your custom modules
from algorithms.dijkstra_with_transfers import find_shortest_path

app = Flask(__name__, template_folder='templates')

# Load transport data
def load_data():
    data_path = os.path.join(project_root, 'data', 'station_network.json')
    try:
        with open(data_path) as f:
            stations = json.load(f)
        
        # Convert to graph format
        graph = {}
        for station, connections in stations.items():
            graph[station] = [(conn['neighbor'], conn['time'], conn['line']) 
                            for conn in connections]
        return graph
    except FileNotFoundError:
        print(f"Error: Data file not found at {data_path}")
        return {}
    except json.JSONDecodeError:
        print("Error: Invalid JSON format in data file")
        return {}

transport_graph = load_data()

@app.route('/')
def home():
    return render_template('index.html')

@app.route('/api/stations')
def get_stations():
    return jsonify(list(transport_graph.keys()))

@app.route('/api/route')
def get_route():
    start = request.args.get('start')
    end = request.args.get('end')
    
    if not start or not end:
        return jsonify({"error": "Missing start or end station"}), 400
    
    try:
        time, path = find_shortest_path(transport_graph, start, end)
        
        if not path:
            return jsonify({"error": "No route found"}), 404
        
        return jsonify({
            "path": path,
            "time": time
        })
    except Exception as e:
        return jsonify({"error": str(e)}), 500

if __name__ == '__main__':
    app.run(debug=True)