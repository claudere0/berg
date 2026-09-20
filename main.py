import pygame
import sys
from src.core.settings import *
from src.core.states import *
from src.core.event_bus import EventBus
from src.systems.input_manager import InputManager

class Game:
    def __init__(self):
        pygame.init()

        # Hybrid Render surfaces
        self.screen = pygame.display.set_mode((WINDOW_WIDTH, WINDOW_HEIGHT))
        self.native_surface = pygame.Surface((NATIVE_WIDTH, NATIVE_HEIGHT))
        pygame.display.set_caption('Berg: Arena Survival')
        
        self.clock = pygame.time.Clock()
        self.running = True

        # Core Systems
        self.event_bus = EventBus()
        self.input_manager = InputManager()

        # State Machine
        self.states = {
            StateID.MENU: MenuState(self),
            StateID.PLAYING: PlayingState(self),
            StateID.PAUSE: PauseState(self)
            # Мы добавим GAME_OVER и VICTORY позже
        }

        self.current_state = self.states[StateID.MENU]
        self.current_state.enter()

    def change_state(self, state_id: StateID):
        if hasattr(self.current_state, 'exit'):
            self.current_state.exit()
        self.current_state = self.states[state_id]
        if hasattr(self.current_state, 'enter'):
            self.current_state.enter()

    def events(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self.running = False
                
            # Передаем событие текущему состоянию
            self.current_state.events(event)

    def update(self, dt):
        self.current_state.update(dt)

    def draw(self):
        # Очищаем экраны перед отрисовкой
        self.native_surface.fill(BLACK)
        
        # States receive both surfaces for hybrid rendering
        self.current_state.draw(self.native_surface, self.screen)
        
        pygame.display.flip()

    def run(self):
        while self.running:
            dt = self.clock.tick(FPS) / 1000.0
            self.events()
            self.update(dt)
            self.draw()

        pygame.quit()
        sys.exit()

if __name__ == '__main__':
    game = Game()
    game.run()
