from typing import Dict, List, Optional

class TimeCalculator:
    def __init__(self, schedule_manager):
        self.schedule_manager = schedule_manager
    
    def calculate_wait_time(self, line: str, station: str, current_time: str) -> int:
        """Calculate waiting time in minutes for next departure"""
        next_departure = self.schedule_manager.get_next_departure(line, station, current_time)
        if not next_departure:
            return float('inf')
        
        # Convert "HH:MM" to minutes since midnight
        current_min = self._time_to_minutes(current_time)
        dep_min = self._time_to_minutes(next_departure)
        
        return dep_min - current_min if dep_min >= current_min else (1440 - current_min) + dep_min
    
    def _time_to_minutes(self, time_str: str) -> int:
        """Convert HH:MM string to minutes since midnight"""
        hh, mm = map(int, time_str.split(':'))
        return hh * 60 + mm
    
    def calculate_total_time(
        self, 
        path: List[str], 
        lines: List[str], 
        start_time: str
    ) -> int:
        """Calculate total journey time including waiting times"""
        if not path or len(path) < 2:
            return 0
            
        total_time = 0
        current_time = self._time_to_minutes(start_time)
        
        for i in range(len(path) - 1):
            station = path[i]
            next_station = path[i+1]
            line = lines[i]
            
            # Get waiting time for this line at this station
            wait_time = self.calculate_wait_time(
                line, 
                station, 
                self._minutes_to_time(current_time)
            )
            if wait_time == float('inf'):
                return float('inf')
            
            total_time += wait_time
            current_time += wait_time
            
            # Get travel time to next station
            travel_time = self._get_travel_time(station, next_station, line)
            total_time += travel_time
            current_time += travel_time
        
        return total_time
    
    def _minutes_to_time(self, minutes: int) -> str:
        """Convert minutes since midnight to HH:MM string"""
        hh = (minutes // 60) % 24
        mm = minutes % 60
        return f"{hh:02d}:{mm:02d}"
    
    def _get_travel_time(self, station_a: str, station_b: str, line: str) -> int:
        """Get travel time between two stations on a line"""
        # This would normally come from the graph data
        # For simplicity, we'll assume 3 minutes between stations
        return 3