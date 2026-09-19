from src.core.settings import *
from src.core.states import *

class Game:
    def __init__(self):
        pygame.init()

        self.screen = pygame.display.set_mode((WINDOW_WIDTH, WINDOW_HEIGHT))
        pygame.display.set_caption('rime and pebble')
        self.clock = pygame.time.Clock()
        self.running = True

        self.states = {
            StateID.MENU: MenuState(self),
            StateID.PLAYING: PlayingState(self),
            StateID.PAUSE: PauseState(self),
            StateID.DAY_COMPLETE: DayCompleteState(self),
            StateID.SETTINGS: SettingsState(self)
        }

        self.current_state = self.states[StateID.MENU]

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
            if event.type == pygame.KEYDOWN: 
                if event.key == pygame.K_q:
                    self.running = False

            self.current_state.events(event)

    def update(self, dt):
        self.current_state.update(dt)

    def draw(self, screen):
        self.current_state.draw(screen)
        pygame.display.flip()

    def run(self):
        while self.running:
            dt = self.clock.tick(FPS) / 1000
            self.events()
            self.update(dt)
            self.draw(self.screen)

        pygame.quit()

if __name__ == '__main__':
    game = Game()
    game.run()
