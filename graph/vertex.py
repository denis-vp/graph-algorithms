class Vertex:

    """
    Class that represents a vertex in a graph.
    """

    def __init__(self, value):
        self.__value = value

    @property
    def value(self):
        return self.__value

    # ----------------------- #

    def __eq__(self, other):
        return self.value == other.value

    def __ne__(self, other):
        return not self.__eq__(other)

    # ----------------------- #

    def __lt__(self, other):
        return self.value < other.value

    def __le__(self, other):
        return self.value <= other.value

    def __gt__(self, other):
        return self.value > other.value

    def __ge__(self, other):
        return self.value >= other.value

    # ----------------------- #

    def __hash__(self):
        return hash(self.__value)

    def __str__(self):
        return str(self.__value)

    def __repr__(self):
        return str(self.__value)
