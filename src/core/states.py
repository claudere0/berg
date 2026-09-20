import pygame
from enum import Enum, auto
from .settings import *

class StateID(Enum):
    MENU = auto()
    PLAYING = auto()
    PAUSE = auto()
    GAME_OVER = auto()
    VICTORY = auto()

class State:
    def __init__(self, game):
        self.game = game

    def enter(self):
        pass

    def exit(self):
        pass

    def events(self, event):
        pass

    def update(self, dt):
        pass

    def draw(self, display_surface, screen_surface):
        pass

class MenuState(State):
    def __init__(self, game):
        super().__init__(game)
        self.options = ["PLAY", "QUIT"]
        self.selected_index = 0
        self.font = pygame.font.SysFont('courier', 32, bold=True)

    def events(self, event):
        if event.type == pygame.KEYDOWN:
            if event.key in (pygame.K_UP, pygame.K_w):
                self.selected_index = (self.selected_index - 1) % len(self.options)
            elif event.key in (pygame.K_DOWN, pygame.K_s):
                self.selected_index = (self.selected_index + 1) % len(self.options)
            elif event.key == pygame.K_RETURN:
                selected = self.options[self.selected_index]
                if selected == "PLAY":
                    self.game.change_state(StateID.PLAYING)
                elif selected == "QUIT":
                    self.game.running = False

    def draw(self, display_surface, screen_surface):
        # Отрисовка UI сразу на screen_surface (high-res)
        screen_surface.fill(BLACK)
        
        title = self.font.render("BERG: ARENA SURVIVAL", True, CYAN)
        title_rect = title.get_rect(center=(WINDOW_WIDTH // 2, WINDOW_HEIGHT // 3))
        screen_surface.blit(title, title_rect)

        for i, option in enumerate(self.options):
            color = YELLOW if i == self.selected_index else WHITE
            text = f"> {option} <" if i == self.selected_index else option
            img = self.font.render(text, True, color)
            rect = img.get_rect(center=(WINDOW_WIDTH // 2, WINDOW_HEIGHT // 2 + i * 50))
            screen_surface.blit(img, rect)

class PlayingState(State):
    def __init__(self, game):
        super().__init__(game)

    def enter(self):
        # Инициализация волны, игрока и т.д.
        pass

    def events(self, event):
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_ESCAPE:
                self.game.change_state(StateID.PAUSE)

    def update(self, dt):
        # Обновление InputManager, Сущностей, Менеджера Волн
        self.game.input_manager.update()

    def draw(self, display_surface, screen_surface):
        # 1. Отрисовка пиксель-арта на display_surface (120x90)
        display_surface.fill(GRAY) # Фон арены
        
        # 2. Масштабирование display_surface и наложение на screen_surface
        scaled_surf = pygame.transform.scale(display_surface, (WINDOW_WIDTH, WINDOW_HEIGHT))
        screen_surface.blit(scaled_surf, (0, 0))
        
        # 3. Отрисовка UI (HP, Mana) на screen_surface
        pass

class PauseState(State):
    def __init__(self, game):
        super().__init__(game)
        self.font = pygame.font.SysFont('courier', 48, bold=True)
        self.overlay = pygame.Surface((WINDOW_WIDTH, WINDOW_HEIGHT), pygame.SRCALPHA)
        self.overlay.fill((0, 0, 0, 150))

    def events(self, event):
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_ESCAPE:
                self.game.change_state(StateID.PLAYING)
            elif event.key == pygame.K_q:
                self.game.change_state(StateID.MENU)

    def draw(self, display_surface, screen_surface):
        # Рисуем игру на фоне
        self.game.states[StateID.PLAYING].draw(display_surface, screen_surface)
        
        # Накладываем затемнение и текст
        screen_surface.blit(self.overlay, (0, 0))
        
        text = self.font.render("PAUSED", True, WHITE)
        rect = text.get_rect(center=(WINDOW_WIDTH // 2, WINDOW_HEIGHT // 2))
        screen_surface.blit(text, rect)
