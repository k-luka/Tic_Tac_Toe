import pygame, sys, time
from game import Game
from settings import *


class TicTacToe:
    def __init__(self):
        pygame.init()
        self.screen = pygame.display.set_mode((WINDOW_WIDTH, WINDOW_HEIGHT))
        pygame.display.set_caption('Tic-Tac-Toe')
        self.clock = pygame.time.Clock()
        self.font = pygame.font.SysFont('Arial', 30)
        self.game = Game(self.screen)

    def draw_menu(self):
        self.screen.fill((105, 135, 250))  # Fill the screen with white color

        # Welcome text
        welcome_text = self.font.render('Tic-Tac-Toe', True, (255, 255, 255))
        welcome_text_rect = welcome_text.get_rect(center=(WINDOW_WIDTH // 2, WINDOW_HEIGHT // 4))

        # Define buttons
        play_pvp_button = pygame.Rect(WINDOW_WIDTH // 4, WINDOW_HEIGHT // 3, WINDOW_WIDTH // 2, 50)
        play_ai_button = pygame.Rect(WINDOW_WIDTH // 4, WINDOW_HEIGHT // 3 + 100, WINDOW_WIDTH // 2, 50)

        # Render text for buttons
        play_pvp_text = self.font.render('Player vs Player', True, (0, 0, 0))
        play_ai_text = self.font.render('Player vs AI', True, (0, 0, 0))

        # Calculate text positioning to center it within the buttons
        pvp_text_x = play_pvp_button.x + (play_pvp_button.width - play_pvp_text.get_width()) // 2
        pvp_text_y = play_pvp_button.y + (play_pvp_button.height - play_pvp_text.get_height()) // 2

        ai_text_x = play_ai_button.x + (play_ai_button.width - play_ai_text.get_width()) // 2
        ai_text_y = play_ai_button.y + (play_ai_button.height - play_ai_text.get_height()) // 2

        # Draw buttons
        pygame.draw.rect(self.screen, (0, 0, 0), play_pvp_button, 2)  # Draw outline for button
        pygame.draw.rect(self.screen, (0, 0, 0), play_ai_button, 2)

        # Blit the centered text onto the screen
        self.screen.blit(play_pvp_text, (pvp_text_x, pvp_text_y))
        self.screen.blit(play_ai_text, (ai_text_x, ai_text_y))
        self.screen.blit(welcome_text, welcome_text_rect.topleft)

        pygame.display.update()  # Update the full display Surface to the screen

        return play_pvp_button, play_ai_button

    def run(self):
        in_menu = True
        play_pvp_button, play_ai_button = self.draw_menu()  # Draw the menu and get button positions

        while True:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()

                if in_menu and event.type == pygame.MOUSEBUTTONDOWN:
                    mouse_pos = event.pos
                    if play_pvp_button.collidepoint(mouse_pos):
                        print('Player vs Player mode selected')
                        in_menu = False
                        self.game.is_ai_game = False
                        self.game.draw_board()  # Draw the game board for PvP
                    elif play_ai_button.collidepoint(mouse_pos):
                        print('Player vs AI mode selected')
                        in_menu = False
                        self.game.is_ai_game = True
                        self.game.draw_board()

                elif not in_menu and event.type == pygame.MOUSEBUTTONDOWN:
                    action = self.game.handle_click(event.pos)  # Modified to handle clicks for placing moves and checking back button
                    if action == 'back':  # If 'back' is returned from handle_click, it means the back button was pressed
                        in_menu = True
                        play_pvp_button, play_ai_button = self.draw_menu()  # Redraw the menu

            pygame.display.update()
            self.clock.tick(FPS)


if __name__ == '__main__':
    game = TicTacToe()
    game.run()





