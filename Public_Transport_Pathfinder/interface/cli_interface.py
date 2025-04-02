from typing import List
from models.transport_graph import TransportGraph
from models.schedule_manager import ScheduleManager
from algorithms.dijkstra_with_transfers import find_shortest_path
from algorithms.time_calculator import TimeCalculator

class CLIInterface:
    def __init__(self):
        self.graph = TransportGraph()
        self.schedule_manager = ScheduleManager()
        self.time_calculator = TimeCalculator(self.schedule_manager)
    
    def load_data(self, network_file: str, schedule_file: str):
        """Load data from JSON files"""
        self.graph.load_from_json(network_file)
        self.schedule_manager.load_from_json(schedule_file)
    
    def run(self):
        """Run the CLI interface"""
        print("Public Transport Pathfinder")
        print("-------------------------")
        
        start = input("Enter start station: ")
        end = input("Enter end station: ")
        departure_time = input("Enter departure time (HH:MM): ")
        
        # Find path
        time, path = find_shortest_path(self.graph, start, end)
        
        if not path:
            print("No route found!")
            return
        
        # Calculate total time including waiting
        lines = self._get_lines_for_path(path)
        total_time = self.time_calculator.calculate_total_time(path, lines, departure_time)
        
        print(f"\nOptimal Route: {' → '.join(path)}")
        print(f"Total Travel Time: {time} minutes")
        print(f"Total Journey Time (with waiting): {total_time} minutes")
    
    def _get_lines_for_path(self, path: List[str]) -> List[str]:
        """Determine which lines are used for each segment of the path"""
        lines = []
        for i in range(len(path) - 1):
            current = path[i]
            next_stop = path[i+1]
            
            # Find the common line between these stations
            for neighbor, time, line in self.graph.get_neighbors(current):
                if neighbor == next_stop:
                    lines.append(line)
                    break
        return lines