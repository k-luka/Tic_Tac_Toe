import pygame
from settings import *

class Game:
    def __init__(self, screen):
        self.screen = screen
        self.font = pygame.font.SysFont('Arial', 30)
        self.board = [[None for _ in range(3)] for _ in range(3)]
        self.current_player = 'X'
        self.game_over = False
        self.board_size = min(WINDOW_WIDTH, WINDOW_HEIGHT) // 2  # Initialize board size
        self.reset_button = pygame.Rect(WINDOW_WIDTH // 2 + 25, WINDOW_HEIGHT // 2 + 250, 100, 40)
        self.back_button = pygame.Rect(WINDOW_WIDTH // 2 - 125, WINDOW_HEIGHT // 2 + 250, 100, 40)

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

        self.draw_back_button()
        self.draw_reset_button()

        pygame.display.update()

    def draw_reset_button(self):
        # Draw reset button
        pygame.draw.rect(self.screen, (128, 128, 128), self.reset_button)
        text = self.font.render('Reset', True, (255, 255, 255))
        text_rect = text.get_rect(center=self.reset_button.center)
        self.screen.blit(text, text_rect)

    def draw_back_button(self):
        pygame.draw.rect(self.screen, (128, 128, 128), self.back_button)
        text2 = self.font.render('Back', True, (255, 255, 255))
        text_rect2 = text2.get_rect(center=self.back_button.center)
        self.screen.blit(text2, text_rect2)



    def handle_click(self, pos):
        if self.reset_button.collidepoint(pos):
            self.reset_game()
            return
        if self.back_button.collidepoint(pos):
            self.reset_game()
            return 'back'  # Return 'back' to indicate the back button was pressed
        if self.game_over:  # Skip handling clicks if the game is over
            return
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

        winner, winning_cells = self.check_win()
        if winner:
            self.game_over = True
            self.display_winner(winner)
            if winning_cells:
                self.draw_winning_line(winning_cells)
        elif self.check_draw():
            self.game_over = True
            self.display_draw()

    def display_winner(self, winner):
        message = f"Player {winner} won!"
        color = (255, 0, 0) if winner == 'X' else (0, 0, 255)
        self.display_message(message, color)

    def display_draw(self):
        self.display_message("It's a draw", (255, 255, 255))

    def display_message(self, message, color):
        # self.screen.fill((105, 135, 250))  # Clear the screen
        text = self.font.render(message, True, color)
        text_rect = text.get_rect(center=(WINDOW_WIDTH // 2, WINDOW_HEIGHT // 2 - 300))
        self.screen.blit(text, text_rect)
        pygame.display.update()

    def check_win(self):
        # Check rows
        for i in range(3):
            if self.board[i][0] == self.board[i][1] == self.board[i][2] != None:
                return self.board[i][0], [(i, 0), (i, 1), (i, 2)]  # Return winner and winning cells

        # Check columns
        for j in range(3):
            if self.board[0][j] == self.board[1][j] == self.board[2][j] != None:
                return self.board[0][j], [(0, j), (1, j), (2, j)]

        # Check diagonals
        if self.board[0][0] == self.board[1][1] == self.board[2][2] != None:
            return self.board[0][0], [(0, 0), (1, 1), (2, 2)]
        if self.board[0][2] == self.board[1][1] == self.board[2][0] != None:
            return self.board[0][2], [(0, 2), (1, 1), (2, 0)]

        return None, None  # No winner

    def check_draw(self):
        for row in self.board:
            if None in row:
                return False
        return True  # No spaces left and no winner

    def draw_winning_line(self, winning_cells):
        start_cell = winning_cells[0]
        end_cell = winning_cells[2]

        cell_size = self.board_size // 3
        half_cell_size = cell_size // 2

        # Calculate the middle points of the start and end cells
        start_x = (WINDOW_WIDTH // 2 - self.board_size // 2) + (start_cell[1] * cell_size) + half_cell_size
        start_y = (WINDOW_HEIGHT // 2 - self.board_size // 2) + (start_cell[0] * cell_size) + half_cell_size
        end_x = (WINDOW_WIDTH // 2 - self.board_size // 2) + (end_cell[1] * cell_size) + half_cell_size
        end_y = (WINDOW_HEIGHT // 2 - self.board_size // 2) + (end_cell[0] * cell_size) + half_cell_size

        # Extend the line slightly beyond the start and end points
        extension = 40  # Pixels to extend beyond the cell
        if start_x == end_x:  # Vertical line
            start_y -= extension
            end_y += extension
        elif start_y == end_y:  # Horizontal line
            start_x -= extension
            end_x += extension
        else:  # Diagonal line
            if start_cell[0] < end_cell[0]:  # Descending diagonal
                start_x += extension
                start_y -= extension
                end_x -= extension
                end_y += extension
            else:  # Ascending diagonal
                start_x -= extension
                start_y += extension
                end_x += extension
                end_y -= extension

        pygame.draw.line(self.screen, (255, 255, 0), (start_x, start_y), (end_x, end_y), 10)
        pygame.display.update()

    def reset_game(self):
        self.board = [[None for _ in range(3)] for _ in range(3)]
        self.current_player = 'X'
        self.game_over = False
        self.draw_board()

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

