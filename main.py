from game_handler import CellsHandler, GameCell
import pyglet
from pyglet import shapes
from pyglet.window import key

CELL_SIZE = 250
PADDING = 15
GRID_LINE_WIDTH = 2
CROSS_COLOR = (255, 0, 0)
CIRCLE_COLOR = (0, 255, 0)
GRID_COLOR = (0, 0, 255)


class Window(pyglet.window.Window):
    def __init__(self) -> None:
        super().__init__(CELL_SIZE * 3, CELL_SIZE * 3, "Tic Tac Toe: Endgame")
        self.handler = CellsHandler()
        self.x_list = []
        self.y_list = []
        self.turn = "cross"
        self.last_set = None

    def get_current_cell(self) -> GameCell:
        if len(self.x_list) == 0:
            return self.handler.root
        cell = self.handler.root
        for (x, y) in zip(self.x_list, self.y_list):
            cell = cell.get_cell(x, y)
        return cell

    def draw_symbol(self, symbol: str, x: int, y: int, width: int, height: int):
        if symbol == "cross":
            center = (x + width // 2, y + height // 2)
            line = shapes.Line(x, y, x + width, y + height,
                               width=5, color=CROSS_COLOR)
            line.draw()
            line = shapes.Line(x, y + height, x + width,
                               y, width=5, color=CROSS_COLOR)
            line.draw()
        elif symbol == "circle":
            center = (x + width // 2, y + height // 2)
            circle = shapes.Circle(
                center[0], center[1], width // 2, color=CIRCLE_COLOR)
            circle.draw()

    def draw_cell(self, cell: GameCell, x: int, y: int, width: int, height: int):
        # Draw the cell sate in the window rect (x, y, width, height), with the grid

        # Draw the state
        if not cell.is_leaf():
            # Draw the 3x3 grid, using shapes
            for i in range(1, 3):
                line = shapes.Line(x + i * width // 3, y, x + i *
                                   width // 3, y + height, width=GRID_LINE_WIDTH,
                                   color=GRID_COLOR
                                   )
                line.draw()
                line = shapes.Line(x, y + i * height // 3, x + width,
                                   y + i * height // 3, width=GRID_LINE_WIDTH,
                                   color=GRID_COLOR
                                   )
                line.draw()

            # Draw the cells in further dimension
            for row in range(3):
                for col in range(3):
                    self.draw_cell(
                        # TODO: Fix ça, cause des erreurs si width < 0 (que dans les grandes dimensions, ou si on réduit la fenêtre)
                        cell.child_cells[row][col],
                        x + row * width // 3 + PADDING,
                        y + col * height // 3 + PADDING,
                        width // 3 - PADDING * 2,
                        height // 3 - PADDING * 2
                    )

            if cell.get_winner() != "empty":
                # La cell a un winner
                # Actual cross or circle cell
                # Darken the cell a little
                dark = shapes.Rectangle(
                    x, y, width, height, color=(255, 255, 255, 210)
                )
                dark.draw()
                self.draw_symbol(
                    cell.get_winner(), x, y, width, height
                )

        else:
            # Actual cross or circle cell
            self.draw_symbol(
                cell.state, x, y, width, height
            )

    def on_draw(self):
        # Fond blanc
        pyglet.gl.glClearColor(1, 1, 1, 1)
        self.clear()
        self.draw_cell(
            self.get_current_cell(), PADDING, PADDING,
            CELL_SIZE * 3 - PADDING * 2, CELL_SIZE * 3 - PADDING * 2
        )

        # Red rectangle around playable cell
        if self.last_set is not None and not self.x_list:
            x, y = self.last_set
            x = x * CELL_SIZE + (PADDING - 3)
            y = y * CELL_SIZE + (PADDING - 3)

            line = shapes.Line(x, y, x + CELL_SIZE - (PADDING - 3) * 2, y,
                               width=GRID_LINE_WIDTH, color=(255, 0, 0))
            line.draw()
            line = shapes.Line(x, y, x, y + CELL_SIZE - (PADDING - 3) * 2,
                               width=GRID_LINE_WIDTH, color=(255, 0, 0))
            line.draw()
            line = shapes.Line(x + CELL_SIZE - (PADDING - 3) * 2, y, x + CELL_SIZE - (PADDING - 3) * 2,
                               y + CELL_SIZE - (PADDING - 3) * 2, width=GRID_LINE_WIDTH, color=(255, 0, 0))
            line.draw()
            line = shapes.Line(x, y + CELL_SIZE - (PADDING - 3) * 2, x + CELL_SIZE - (PADDING - 3) * 2,
                               y + CELL_SIZE - (PADDING - 3) * 2, width=GRID_LINE_WIDTH, color=(255, 0, 0))
            line.draw()

    def on_mouse_press(self, x, y, button, modifiers):
        if button != 1:
            return
        x = x // CELL_SIZE
        y = y // CELL_SIZE
        parent = self.get_current_cell()
        cell = parent.get_cell(x, y)

        if cell.is_leaf():
            if cell.state == "empty" and parent.get_winner() == "empty":

                # Check if it is the playable cell
                if self.last_set is not None\
                        and (self.x_list[-1] != self.last_set[0] or self.y_list[-1] != self.last_set[1]):
                    return

                if self.turn == "circle":
                    cell.state = "circle"
                    self.turn = "cross"
                else:
                    cell.state = "cross"
                    self.turn = "circle"
                self.last_set = (x, y)
                if self.handler.root.get_cell(x, y).get_winner() != "empty":
                    self.last_set = None
                self.x_list.clear()
                self.y_list.clear()
        else:
            self.x_list.append(x)
            self.y_list.append(y)

    def on_key_press(self, symbol, modifiers):
        if symbol == key.ESCAPE:
            self.x_list = self.x_list[:-1]
            self.y_list = self.y_list[:-1]
            self.on_draw()
            return
        return super().on_key_press(symbol, modifiers)


window = Window()
pyglet.app.run()
