from src.core.settings import *
from src.core.states import *
from src.core.event_bus import EventBus

class Game:
    def __init__(self):
        pygame.init()

        self.screen = pygame.display.set_mode((WINDOW_WIDTH, WINDOW_HEIGHT))
        self.native_surface = pygame.Surface((NATIVE_WIDTH, NATIVE_HEIGHT))
        pygame.display.set_caption('Berg & Woolly')
        self.clock = pygame.time.Clock()
        self.running = True

        self.event_bus = EventBus()
        self.current_day = 1 # Progression tracking

        # Pass game reference to states
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

    def draw(self):
        # States receive both the low-res surface and high-res screen for hybrid rendering
        self.current_state.draw(self.native_surface, self.screen)
        pygame.display.flip()

    def run(self):
        while self.running:
            dt = self.clock.tick(FPS) / 1000
            self.events()
            self.update(dt)
            self.draw()

        pygame.quit()

if __name__ == '__main__':
    game = Game()
    game.run()
