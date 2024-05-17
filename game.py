import pygame
from settings import *

class Game:
    def __init__(self, screen):
        self.screen = screen
        self.font = pygame.font.SysFont('Arial', 30)
        self.board = [[None for _ in range(3)] for _ in range(3)]
        self.current_player = 'X'
        self.game_over = False
        self.board_size = min(WINDOW_WIDTH, WINDOW_HEIGHT) // 2  # Initialize board size here

    def draw_board(self):
        self.screen.fill((105, 135, 250))  # Clear the screen / fill with background color

        # Dimensions for the centered square board
        board_size = min(WINDOW_WIDTH, WINDOW_HEIGHT) // 2  # Smaller and more centered
        top_left_x = (WINDOW_WIDTH - board_size) // 2
        top_left_y = (WINDOW_HEIGHT - board_size) // 2
        cell_size = board_size // 3
        border_thickness = 10  # Thickness of the border

        # Draw the border (black rectangle)
        pygame.draw.rect(self.screen, (0, 0, 0), (top_left_x - border_thickness, top_left_y - border_thickness,
                                                  board_size + 2 * border_thickness, board_size + 2 * border_thickness))

        # Draw the background for the board (light grey rectangle inside the black border)
        background_color = (200, 200, 200)  # Light grey
        pygame.draw.rect(self.screen, background_color, (top_left_x, top_left_y, board_size, board_size))

        # Draw vertical lines
        for i in range(1, 3):
            x = top_left_x + i * cell_size
            pygame.draw.line(self.screen, (0, 0, 0), (x, top_left_y), (x, top_left_y + board_size), 5)

        # Draw horizontal lines
        for i in range(1, 3):
            y = top_left_y + i * cell_size
            pygame.draw.line(self.screen, (0, 0, 0), (top_left_x, y), (top_left_x + board_size, y), 5)

        pygame.display.update()

    def handle_click(self, pos):
        top_left_x = (WINDOW_WIDTH - self.board_size) // 2
        top_left_y = (WINDOW_HEIGHT - self.board_size) // 2
        cell_size = self.board_size // 3

        # Calculate which cell is clicked
        if top_left_x < pos[0] < top_left_x + self.board_size and top_left_y < pos[1] < top_left_y + self.board_size:
            row = (pos[1] - top_left_y) // cell_size
            col = (pos[0] - top_left_x) // cell_size

            if self.board[row][col] is None:  # Only allow to place if the cell is empty
                self.board[row][col] = self.current_player
                self.current_player = 'O' if self.current_player == 'X' else 'X'  # Switch turns
                self.draw_move(row, col)

    def reset_game(self):
        # Code to reset the game to its initial state
        pass

    def draw_move(self, row, col):
        top_left_x = (WINDOW_WIDTH - self.board_size) // 2
        top_left_y = (WINDOW_HEIGHT - self.board_size) // 2
        cell_size = self.board_size // 3
        center_x = top_left_x + col * cell_size + cell_size // 2
        center_y = top_left_y + row * cell_size + cell_size // 2

        if self.board[row][col] == 'X':
            pygame.draw.line(self.screen, (255, 0, 0), (center_x - 20, center_y - 20), (center_x + 20, center_y + 20),
                             5)
            pygame.draw.line(self.screen, (255, 0, 0), (center_x + 20, center_y - 20), (center_x - 20, center_y + 20),
                             5)
        elif self.board[row][col] == 'O':
            pygame.draw.circle(self.screen, (0, 0, 255), (center_x, center_y), 20, 5)

        pygame.display.update()

