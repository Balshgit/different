import math
from itertools import cycle


class Snake:

    def __init__(self):
        self.x = 0
        self.y = 0
        self.move = self.move_right

    def move_right(self) -> None:
        self.x += 1

    def move_left(self) -> None:
        self.x -= 1

    def move_down(self) -> None:
        self.y += 1

    def move_up(self) -> None:
        self.y -= 1

    def move_direction(self) -> cycle:
        return cycle([self.move_right, self.move_down, self.move_left, self.move_up])

    def move_back(self) -> None:
        match self.move:
            case self.move_right:
                self.x -= 1
            case self.move_left:
                self.x += 1
            case self.move_down:
                self.y -= 1
            case self.move_up:
                self.y += 1

    def get_current_element_or_none(self, board: dict[int, list[str]]) -> str | None:
        try:
            return board.get(self.y)[self.x]
        except IndexError:
            return None
        except TypeError:
            return None


def snake(n: int) -> None:
    board: dict[int, list[str]] = {row: ['0' for column in range(n)] for row in range(n)}

    python = Snake()

    move_direction = python.move_direction()
    next(move_direction)
    python.move_back()  # get on -1 position. And next move wil be on zero position

    for number in range(n ** 2):
        python.move()
        element = python.get_current_element_or_none(board)

        if not element or element != '0':
            python.move_back()
            python.move = next(move_direction)
            python.move()

        board[python.y][python.x] = f'{number + 1}'.rjust(int(math.log10(n**2)) + 1, ' ')

    for line in board.values():
        print(*line)


if __name__ == '__main__':
    snake(7)
