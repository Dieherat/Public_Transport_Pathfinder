import heapq
from typing import Dict, List, Tuple, Optional

def find_shortest_path(
    graph, 
    start: str, 
    end: str, 
    transfer_penalty: int = 2
) -> Tuple[int, List[str]]:
    """
    Find shortest path using Dijkstra's algorithm with transfer penalties.
    
    Returns:
        tuple: (total_time, path)
    """
    # Priority queue: (total_time, current_station, current_line, path)
    heap = [(0, start, None, [start])]
    visited = {}  # {station: (best_time, best_line)}
    
    while heap:
        current_time, station, line, path = heapq.heappop(heap)
        
        if station == end:
            return (current_time, path)
        
        if station in visited:
            continue
        visited[station] = (current_time, line)
        
        for neighbor, time, new_line in graph.get_neighbors(station):
            total_time = current_time + time
            
            # Apply transfer penalty if changing lines
            if new_line != line and line is not None:
                total_time += transfer_penalty
            
            heapq.heappush(
                heap,
                (total_time, neighbor, new_line, path + [neighbor])
            )
    
    return (float('inf'), [])  # No path found