class CellState:
    EMPTY = "empty"
    CROSS = "cross"
    CIRCLE = "circle"


class GameCell:
    def __init__(self, depth: int = 0):
        self.depth = depth
        if depth > 0:
            self.child_cells: list[list[GameCell]] = [
                [
                    GameCell(max(depth - 1, 0)) for _ in range(3)
                ] for _ in range(3)
            ]
        else:
            self.child_cells: list[list[GameCell]] = []
        self.state = "empty"

    def is_leaf(self):
        return len(self.child_cells) == 0

    def __str__(self):
        return f"GameCell({self.state}, {self.depth})"

    def __repr__(self) -> str:
        return f"GameCell({self.state}, {self.depth})"

    def set_state(self, state):
        assert state in ["empty", "cross", "circle"], "invalid state"
        if len(self.child_cells) > 0:
            raise Exception("Cannot set state on non-leaf cell")
        self.state = state

    def get_cell(self, x, y):
        if self.is_leaf():
            raise Exception("Cannot get cell from leaf cell")
        assert 0 <= x < 3, "x out of bounds"
        assert 0 <= y < 3, "y out of bounds"
        return self.child_cells[x][y]

    def get_winner(self):
        if self.is_leaf():
            return self.state
        # Find if 3 are aligned
        for i in range(3):
            if self.child_cells[i][0].get_winner() == self.child_cells[i][1].get_winner() == self.child_cells[i][2].get_winner():
                s = self.child_cells[i][0].get_winner()
                if s != "empty":
                    return s
            if self.child_cells[0][i].get_winner() == self.child_cells[1][i].get_winner() == self.child_cells[2][i].get_winner():
                s = self.child_cells[0][i].get_winner()
                if s != "empty":
                    return s
        if self.child_cells[0][0].get_winner() == self.child_cells[1][1].get_winner() == self.child_cells[2][2].get_winner():
            s = self.child_cells[0][0].get_winner()
            if s != "empty":
                return s
        if self.child_cells[0][2].get_winner() == self.child_cells[1][1].get_winner() == self.child_cells[2][0].get_winner():
            s = self.child_cells[0][2].get_winner()
            if s != "empty":
                return s
        return "empty"


class CellsHandler:
    def __init__(self, depth: int = 2):
        self.root = GameCell(depth)

    def console_print(self):
        def print_cell(cell: GameCell, indent):
            print(indent + str(cell))
            for row in cell.child_cells:
                for child in row:
                    print_cell(child, indent + "  ")
        print_cell(self.root, "")
