import pygame
from sys import exit
from os.path import join
from settings import *
from game import Game
from score import Score
from preview import Preview
from random import choice
from slider import Slider
import os
from PIL import Image

class Main:
    def __init__(self):
        pygame.init()
        self.block_settings = BLOCK_SETTINGS()

        self.display_surface = pygame.display.set_mode((WINDOW_WIDTH, WINDOW_HEIGHT))
        self.clock = pygame.time.Clock()
        pygame.display.set_caption('Tetris')

        self.state = 'menu'
        self.font = pygame.font.Font(None, 36)

        # Buttons and colors
        self.buttons = {
            'play': pygame.Rect(WINDOW_WIDTH // 2 - 100, WINDOW_HEIGHT // 2 - 100, 200, 50),
            'settings': pygame.Rect(WINDOW_WIDTH // 2 - 100, WINDOW_HEIGHT // 2 - 50, 200, 50),
            'quit': pygame.Rect(WINDOW_WIDTH // 2 - 100, WINDOW_HEIGHT // 2, 200, 50),
            'back': pygame.Rect(20, 20, 100, 50),
            'main_menu_music_toggle': pygame.Rect(WINDOW_WIDTH - 110, 20, 50, 50),  # Music toggle button position
            'in_game_music_toggle': pygame.Rect(WINDOW_WIDTH // 2 + 110, 20, 50, 50)  # Music toggle button position
        }
        self.button_color = (30, 30, 30)
        self.border_color = (200, 200, 200)

        self.game_over_button = pygame.Rect(WINDOW_WIDTH // 2 - 100, WINDOW_HEIGHT // 2 + 100, 250, 50)
        self.save_button = pygame.Rect(WINDOW_WIDTH // 2 - 75, WINDOW_HEIGHT // 2 + 125, 150, 50)

        # Next shapes
        self.next_shapes = []
        self.choose_next_shapes()

        # Components
        self.game = Game(self.get_next_shape, self.update_score, self.block_settings)
        self.score = Score()
        self.preview = Preview(self.block_settings)

        # Sound
        script_path = os.path.abspath(__file__).split(os.sep)[:-1]
        script_path = os.sep.join(script_path)
        self.music = pygame.mixer.Sound(join(script_path, '..', 'sound', 'music.wav'))
        self.music_volume = 0.1
        self.music.set_volume(self.music_volume)
        self.music.play(-1)

        self.block_fall_sound = pygame.mixer.Sound(join(script_path, '..', 'sound', 'landing.wav'))
        self.block_fall_sound_volume = 0.3
        self.block_fall_sound.set_volume(self.block_fall_sound_volume)

        # Volume control slider for music
        self.volume_slider_music = Slider(WINDOW_WIDTH // 2 - 100, WINDOW_HEIGHT // 2 - 50, 200, 20, 0, 1, self.music_volume)

        # Volume control slider for landing sound
        self.volume_slider_landing = Slider(WINDOW_WIDTH // 2 - 100, WINDOW_HEIGHT // 2 + 50, 200, 20, 0, 1, self.block_fall_sound_volume)

        # Music toggle icon
        self.music_icon = pygame.image.load("../graphics/music_icon.png").convert()
        self.music_icon = pygame.transform.scale(self.music_icon, (30, 30))
        self.music_icon_active = True

        self.is_score_saved = False

    def update_score(self, lines, score, level):
        self.score.lines = lines
        self.score.score = score
        self.score.level = level

    def get_next_shape(self):
        next_shape = self.next_shapes.pop(0)
        selected_tetromino = choice(list(self.block_settings.CURRENT_TETROMINOS.keys()))
        self.next_shapes.append(selected_tetromino)
        return next_shape

    def choose_next_shapes(self):
        self.next_shapes = []
        for _ in range(3):
            selected_tetromino = choice(list(self.block_settings.CURRENT_TETROMINOS.keys()))
            self.next_shapes.append(selected_tetromino)

    def resize_image(self, image, new_width, new_height):
        img = Image.frombytes("RGBA", (image.get_width(), image.get_height()), pygame.image.tobytes(image, "RGBA", False))
        img = img.resize((new_width, new_height))
        return pygame.image.frombytes(img.tobytes(), img.size, img.mode)

    def run_menu(self):
        background_image = pygame.image.load("../graphics/background.png").convert()
        background_image = self.resize_image(background_image, WINDOW_WIDTH, WINDOW_HEIGHT)

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                exit()
            elif event.type == pygame.MOUSEBUTTONDOWN:
                if self.buttons['play'].collidepoint(event.pos):
                    self.game.current_level = 1
                    self.state = 'play'
                    self.score.reset_score()
                    self.game.update_score(self.score.lines, self.score.score, self.game.current_level)
                elif self.buttons['settings'].collidepoint(event.pos):
                    self.state = 'settings'
                elif self.buttons['quit'].collidepoint(event.pos):
                    pygame.quit()
                    exit()
                elif self.buttons['main_menu_music_toggle'].collidepoint(event.pos) or self.buttons:
                    self.music_icon_active = not self.music_icon_active
                    if self.music_icon_active:
                        self.music.play(-1)
                    else:
                        self.music.stop()

        self.display_surface.blit(background_image, (0, 0))
        self.draw_buttons(["Play", "Settings", "Quit"])
        self.draw_music_button(True)


        pygame.display.update()

    def run_game(self):
        background_surface = pygame.Surface((WINDOW_WIDTH, WINDOW_HEIGHT))
        background_surface.fill(GRAY)

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                exit()
            elif event.type == pygame.MOUSEBUTTONDOWN:
                if self.game.is_game_over:
                    if self.game_over_button.collidepoint(event.pos):
                        self.state = 'menu'
                        self.game.is_game_over = False
                        self.block_settings.reset()
                        self.next_shapes = []
                        self.choose_next_shapes()
                        self.score.reset_score()
                        self.game = Game(self.get_next_shape, self.update_score, self.block_settings)

                        if self.is_score_saved:
                            self.is_score_saved = False

                    elif self.save_button.collidepoint(event.pos):
                        if not self.is_score_saved:
                            cwd = os.getcwd()
                            saved_scores_path = os.path.join(cwd, 'saved_scores')
                            if not os.path.exists(saved_scores_path):
                                os.mkdir(saved_scores_path)

                            folder_length = len(os.listdir(saved_scores_path))
                            save_path = os.path.join(saved_scores_path, f"Score{folder_length + 1}.png")
                            pygame.image.save(self.display_surface, save_path)
                            self.is_score_saved = True

                elif self.buttons['back'].collidepoint(event.pos):
                    self.state = 'menu'
                    self.game.is_game_over = False
                    self.block_settings.reset()
                    self.next_shapes = []
                    self.choose_next_shapes()
                    self.score.reset_score()
                    self.game = Game(self.get_next_shape, self.update_score, self.block_settings)
                elif self.buttons['in_game_music_toggle'].collidepoint(event.pos):
                    self.music_icon_active = not self.music_icon_active
                    if self.music_icon_active:
                        self.music.play(-1)
                    else:
                        self.music.stop()

        if self.game.is_game_over:
            self.display_surface.blit(background_surface, (0, 0))
            self.draw_game_over_screen()
            pygame.display.update()
        else:
            self.display_surface.blit(background_surface, (0, 0))
            self.game.run()
            self.score.run()
            self.preview.run(self.next_shapes)
            self.draw_back_button()
            self.draw_music_button(False)
            pygame.display.update()
            self.clock.tick(60)

    def draw_game_over_screen(self):
        background_image = pygame.image.load("../graphics/game_over.png").convert()
        background_image = self.resize_image(background_image, WINDOW_WIDTH, WINDOW_HEIGHT)
        self.display_surface.blit(background_image, (0, 0))

        score_text = self.font.render(f"Score: {self.score.score}", True, (255, 255, 255))
        score_rect = score_text.get_rect(center=(WINDOW_WIDTH // 2, WINDOW_HEIGHT // 2 + 100))
        self.display_surface.blit(score_text, score_rect)

        save_button_rect = pygame.Rect(WINDOW_WIDTH // 2 - 75, WINDOW_HEIGHT // 2 + 125, 150, 50)
        pygame.draw.rect(self.display_surface, (30, 30, 30), save_button_rect)
        pygame.draw.rect(self.display_surface, (200, 200, 200), save_button_rect, 2)
        save_text = pygame.font.Font(None, 36).render("Save Score", True, (255, 255, 255))
        save_text_rect = save_text.get_rect(center=(WINDOW_WIDTH // 2, WINDOW_HEIGHT // 2 + 150))
        self.display_surface.blit(save_text, save_text_rect)

        game_over_button_rect = pygame.Rect(WINDOW_WIDTH // 2 - 100, WINDOW_HEIGHT // 2 + 200, 200, 50)
        pygame.draw.rect(self.display_surface, (30, 30, 30), game_over_button_rect)
        pygame.draw.rect(self.display_surface, (200, 200, 200), game_over_button_rect, 2)
        game_over_button_text = pygame.font.Font(None, 36).render("Return to Menu", True, (255, 255, 255))
        game_over_button_text_rect = game_over_button_text.get_rect(center=game_over_button_rect.center)
        self.display_surface.blit(game_over_button_text, game_over_button_text_rect)

        self.game_over_button = game_over_button_rect


    def run_settings(self):
        background_image = pygame.image.load("../graphics/background.png").convert()
        background_image = self.resize_image(background_image, WINDOW_WIDTH, WINDOW_HEIGHT)

        previous_music_volume = self.music_volume
        previous_block_fall_sound_volume = self.block_fall_sound_volume

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                exit()
            elif event.type in [pygame.MOUSEBUTTONDOWN, pygame.MOUSEBUTTONUP, pygame.MOUSEMOTION]:
                self.volume_slider_music.handle_event(event)
                self.music_volume = self.volume_slider_music.get_value()

                self.volume_slider_landing.handle_event(event)
                self.block_fall_sound_volume = self.volume_slider_landing.get_value()

                if event.type == pygame.MOUSEBUTTONDOWN and self.buttons['back'].collidepoint(event.pos):
                    self.state = 'menu'

        if previous_music_volume != self.music_volume:
            self.music.set_volume(self.music_volume)

        if previous_block_fall_sound_volume != self.block_fall_sound_volume:
            self.block_fall_sound.set_volume(self.block_fall_sound_volume)

        self.display_surface.blit(background_image, (0, 0))
        self.draw_back_button()
        self.draw_volume_sliders()
        pygame.display.update()

    def draw_buttons(self, texts):
        for button, text in zip(self.buttons.values(), texts):
            pygame.draw.rect(self.display_surface, (0, 0, 0), button)
            pygame.draw.rect(self.display_surface, self.border_color, button, 2)

            text_surface = self.font.render(text, True, (255, 255, 255))
            text_rect = text_surface.get_rect(center=button.center)
            self.display_surface.blit(text_surface, text_rect)

            text_surface = self.font.render(text, True, (150, 0, 255))
            text_rect = text_surface.get_rect(center=button.center)
            self.display_surface.blit(text_surface, text_rect)

    def draw_back_button(self):
        back_button_rect = pygame.Rect(20, 20, 100, 50)
        pygame.draw.rect(self.display_surface, (30, 30, 30), back_button_rect)
        pygame.draw.rect(self.display_surface, (200, 200, 200), back_button_rect, 2)
        back_text = self.font.render("Menu", True, (150, 0, 255))
        back_text_rect = back_text.get_rect(center=back_button_rect.center)
        self.display_surface.blit(back_text, back_text_rect)

    def draw_music_button(self, is_on_main_menu):
        if is_on_main_menu:
            music_toggle_button_rect = self.buttons['main_menu_music_toggle']
        else:
            music_toggle_button_rect = self.buttons['in_game_music_toggle']
        pygame.draw.rect(self.display_surface, (0, 0, 0), music_toggle_button_rect)
        if self.music_icon_active:
            pygame.draw.rect(self.display_surface, (255, 0, 0), music_toggle_button_rect, 3)
        self.display_surface.blit(self.music_icon, (
            music_toggle_button_rect.left + 10, music_toggle_button_rect.top + 10))

    def draw_volume_sliders(self):
        # Music volume text and slider position
        music_volume_text = self.font.render("Music Volume", True, (150, 0, 255))
        music_volume_text_rect = music_volume_text.get_rect(midtop=(WINDOW_WIDTH // 2, 100))
        self.display_surface.blit(music_volume_text, music_volume_text_rect)

        self.volume_slider_music.rect.midtop = (WINDOW_WIDTH // 2, 150)
        self.volume_slider_music.draw(self.display_surface)

    def run(self):
        while True:
            if self.state == 'menu':
                self.run_menu()
            elif self.state == 'play':
                self.run_game()
            elif self.state == 'settings':
                self.run_settings()

            pygame.display.update()
            self.clock.tick(60)

if __name__ == '__main__':
    main = Main()
    main.run()
