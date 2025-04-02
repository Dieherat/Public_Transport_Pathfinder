import pytest
from models.transport_graph import TransportGraph
from algorithms.a_star_optimized import AStarOptimized

@pytest.fixture
def sample_graph_with_coords():
    graph = TransportGraph()
    graph.add_connection("A", "B", 5, "Blue")
    graph.add_connection("B", "C", 4, "Blue")
    graph.add_connection("A", "C", 10, "Red")
    
    coordinates = {
        "A": (0, 0),
        "B": (1, 0),
        "C": (1, 1)
    }
    return graph, coordinates

def test_a_star(sample_graph_with_coords):
    graph, coordinates = sample_graph_with_coords
    astar = AStarOptimized(coordinates)
    time, path = astar.find_path(graph, "A", "C")
    assert path == ["A", "C"]
    assert time == 10