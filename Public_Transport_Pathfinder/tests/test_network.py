import pytest
from models.transport_graph import TransportGraph

def test_graph_loading():
    graph = TransportGraph()
    graph.add_connection("A", "B", 5, "Blue")
    assert len(graph.graph["A"]) == 1
    assert len(graph.graph["B"]) == 1
    assert graph.graph["A"][0] == ("B", 5, "Blue")

def test_bidirectional_connection():
    graph = TransportGraph()
    graph.add_connection("A", "B", 5, "Blue")
    assert graph.graph["A"][0][0] == "B"
    assert graph.graph["B"][0][0] == "A"