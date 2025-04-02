import pytest
from models.transport_graph import TransportGraph
from algorithms.dijkstra_with_transfers import find_shortest_path

@pytest.fixture
def sample_graph():
    graph = TransportGraph()
    graph.add_connection("A", "B", 5, "Blue")
    graph.add_connection("B", "C", 4, "Blue")
    graph.add_connection("A", "C", 10, "Red")
    return graph

def test_direct_route(sample_graph):
    time, path = find_shortest_path(sample_graph, "A", "C")
    assert path == ["A", "C"]
    assert time == 10

def test_transfer_route(sample_graph):
    sample_graph.add_connection("B", "C", 3, "Green")  # Faster but requires transfer
    time, path = find_shortest_path(sample_graph, "A", "C")
    assert path == ["A", "B", "C"]
    assert time == 5 + 3 + 2  # AB + BC + transfer penalty