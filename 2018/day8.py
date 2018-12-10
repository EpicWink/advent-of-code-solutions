import logging as lg

lg.basicConfig(
    level=lg.DEBUG,
    format="%(asctime)s [%(levelname)s] %(name)s: %(message)s",
    datefmt="%H:%M:%S")
_logger = lg.getLogger(__name__)


class Node:
    def __init__(self, children, metadata):
        self.children = children
        self.metadata = metadata

    def sum_metadata(self):
        return sum(self.metadata) + sum([c.sum_metadata() for c in self.children])

    def get_value(self):
        _logger.debug("Node ({} children) metadata: {}".format(len(self.children), self.metadata))
        if self.children:
            cs = self.children
            return sum([cs[idx - 1].get_value() for idx in self.metadata if 0 <= idx - 1 < len(cs)])
        else:
            return sum(self.metadata)


class Parser:
    _node_class = Node

    def __init__(self, data):
        self.data = data
        self.root = None

    @classmethod
    def from_data_str(cls, data_str):
        return cls(list(map(int, data_str.strip().split(" "))))

    def _build_node(self, j):
        n_children = self.data[j]
        n_metadata = self.data[j + 1]
        # _logger.debug("Node at {}: {} children, {} metadata".format(j, n_children, n_metadata))
        children = []
        k = 2
        for _ in range(n_children):
            child, size = self._build_node(j + k)
            children.append(child)
            k += size
        metadata = self.data[j + k:j + k + n_metadata]
        node = self._node_class(children, metadata)
        return node, k + n_metadata

    def parse(self):
        node, size = self._build_node(0)
        assert size == len(self.data)
        self.root = node


with open("input_day8.txt", "r") as f:
    data_str = f.read()
parser = Parser.from_data_str(data_str)
parser.parse()
print("Answer pt1:", parser.root.sum_metadata())

print("Answer pt2:", parser.root.get_value())
