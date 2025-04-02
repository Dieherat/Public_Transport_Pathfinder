import heapq
from typing import Dict, List, Tuple
from math import sqrt

class AStarOptimized:
    def __init__(self, coordinates: Dict[str, Tuple[float, float]]):
        """Initialize with station coordinates for heuristic"""
        self.coordinates = coordinates
    
    def heuristic(self, a: str, b: str) -> float:
        """Euclidean distance heuristic between two stations"""
        x1, y1 = self.coordinates.get(a, (0, 0))
        x2, y2 = self.coordinates.get(b, (0, 0))
        return sqrt((x1 - x2)**2 + (y1 - y2)**2)
    
    def find_path(self, graph, start: str, end: str, transfer_penalty: int = 2):
        """A* search with transfer awareness"""
        heap = [(0, 0, start, None, [start])]  # (f_score, g_score, station, line, path)
        visited = {}  # {station: (best_g_score, best_line)}
        g_scores = {station: float('inf') for station in graph.graph}
        g_scores[start] = 0
        
        while heap:
            f_score, g_score, station, line, path = heapq.heappop(heap)
            
            if station == end:
                return (g_score, path)
            
            if station in visited:
                continue
            visited[station] = (g_score, line)
            
            for neighbor, time, new_line in graph.get_neighbors(station):
                tentative_g = g_score + time
                
                # Apply transfer penalty if changing lines
                if new_line != line and line is not None:
                    tentative_g += transfer_penalty
                
                if tentative_g < g_scores.get(neighbor, float('inf')):
                    g_scores[neighbor] = tentative_g
                    f_score = tentative_g + self.heuristic(neighbor, end)
                    heapq.heappush(
                        heap,
                        (f_score, tentative_g, neighbor, new_line, path + [neighbor])
                    )
        
        return (float('inf'), [])