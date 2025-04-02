from collections import defaultdict
import json
from typing import Dict, List, Tuple, Optional, Set
from dataclasses import dataclass

@dataclass
class Connection:
    neighbor: str
    time: int
    line: str

class TransportGraph:
    def __init__(self, transfer_penalty: int = 2):
        """
        Initialize transport graph with:
        - graph: adjacency list of stations
        - stations: set of all stations
        - lines: mapping of lines to their stations
        - transfer_penalty: time cost when changing lines
        """
        self.graph: Dict[str, List[Connection]] = defaultdict(list)
        self.stations: Set[str] = set()
        self.lines: Dict[str, Set[str]] = defaultdict(set)
        self.transfer_penalty = transfer_penalty

    def load_from_json(self, filepath: str) -> None:
        """Load and validate station network from JSON file"""
        try:
            with open(filepath, 'r') as f:
                data = json.load(f)
                for station, connections in data.items():
                    if not isinstance(connections, list):
                        raise ValueError(f"Invalid connections format for station {station}")
                    
                    for conn in connections:
                        self._validate_connection(conn)
                        self.add_connection(
                            station,
                            conn["neighbor"],
                            conn["time"],
                            conn["line"]
                        )
        except (FileNotFoundError, json.JSONDecodeError) as e:
            raise ValueError(f"Failed to load graph data: {str(e)}")

    def _validate_connection(self, conn: Dict) -> None:
        """Validate connection dictionary structure"""
        required = {"neighbor", "time", "line"}
        if not all(key in conn for key in required):
            raise ValueError(f"Connection missing required fields: {required}")
        if not isinstance(conn["time"], (int, float)) or conn["time"] <= 0:
            raise ValueError("Travel time must be a positive number")

    def add_connection(self, station_a: str, station_b: str, time: int, line: str) -> None:
        """Add bidirectional connection with validation"""
        if time <= 0:
            raise ValueError("Travel time must be positive")
        
        connection = Connection(neighbor=station_b, time=time, line=line)
        self.graph[station_a].append(connection)
        
        # Add reverse connection
        reverse_connection = Connection(neighbor=station_a, time=time, line=line)
        self.graph[station_b].append(reverse_connection)
        
        # Update metadata
        self.stations.update([station_a, station_b])
        self.lines[line].update([station_a, station_b])

    def get_neighbors(self, station: str) -> List[Connection]:
        """Get all connected stations with travel info"""
        return self.graph.get(station, [])

    def get_transfer_penalty(self) -> int:
        """Get current transfer penalty"""
        return self.transfer_penalty

    def set_transfer_penalty(self, penalty: int) -> None:
        """Set transfer penalty with validation"""
        if penalty < 0:
            raise ValueError("Transfer penalty cannot be negative")
        self.transfer_penalty = penalty

    def get_stations_on_line(self, line: str) -> Set[str]:
        """Get all stations on a specific line"""
        return self.lines.get(line, set())

    def validate_station(self, station: str) -> None:
        """Check if station exists in the network"""
        if station not in self.stations:
            raise ValueError(f"Station {station} not found in network")