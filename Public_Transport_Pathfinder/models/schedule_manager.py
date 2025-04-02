import json
from typing import Dict, List

class ScheduleManager:
    def __init__(self):
        self.schedules = {}
    
    def load_from_json(self, filepath: str):
        """Load schedule data from JSON file"""
        with open(filepath, 'r') as f:
            self.schedules = json.load(f)
    
    def get_next_departure(self, line: str, station: str, current_time: str) -> str:
        """Get the next departure time for a station on a line"""
        departures = self.schedules.get(line, {}).get(station, [])
        for dep in departures:
            if dep >= current_time:
                return dep
        return None
    
    def get_all_lines_for_station(self, station: str) -> List[str]:
        """Get all lines that serve a particular station"""
        lines = []
        for line, stations in self.schedules.items():
            if station in stations:
                lines.append(line)
        return lines