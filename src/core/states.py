import pygame
from enum import Enum, auto
from pytmx.util_pygame import load_pygame
from os.path import join
from .settings import *
# from .level import Level

class StateID(Enum):
    MENU = auto()
    PLAYING = auto()
    PAUSE = auto()
    DAY_COMPLETE = auto()
    SETTINGS = auto()

class State:
    def __init__(self, game):
        self.game = game

    def events(self, event):
        pass

    def update(self, dt):
        pass

    def draw(self, screen):
        pass

# MENU -> PLAYING or SETTINGS

class MenuState(State):
    def __init__(self, game):
        super().__init__(game)
        self.options = ["PLAY", "SETTINGS", "QUIT"]
        self.selected_index = 0
        self.font_large = pygame.font.SysFont('courier', 64)

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

                elif selected == "SETTINGS":
                    self.game.change_state(StateID.SETTINGS)

                elif selected == "QUIT":
                    self.game.running = False

    def draw(self, screen):
        screen.fill(BLACK)

        for i, option in enumerate(self.options):
            if i == self.selected_index:
                color = YELLOW
                text = f"> {option} <"
            else:
                color = WHITE
                text = option
                
            img = self.font_large.render(text, True, color)
            rect = img.get_frect(center=(WINDOW_WIDTH / 2, WINDOW_HEIGHT / 2 - 64 + i * 64))
            screen.blit(img, rect)

# PLAYING -> PAUSE (ESCAPE) or DAY_COMPLETE

class PlayingState(State):
    def __init__(self, game):
        super().__init__(game)
        self.current_stage = None
        self.current_level_name = ""
        self.start_time = 0 
        self.last_run_time = 0
        self.pause_start_time = 0

    def load_level(self, level_name):
        self.current_level_name = level_name
        tmx_map = load_pygame(join('data', 'levels', f'{level_name}.tmx'))

        # self.current_stage = Level(tmx_map, self)

        self.start_time = pygame.time.get_ticks()
        self.game.audio.play_music('magiksolo-investigation-puzzle.mp3', fade_ms=1000)
        self.game.change_state(StateID.PLAYING)

    def resume_timer(self):
        pause_duration = pygame.time.get_ticks() - self.pause_start_time
        self.start_time += pause_duration

    def events(self, event):
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_ESCAPE:
                self.pause_start_time = pygame.time.get_ticks()
                self.game.change_state(StateID.PAUSE)

    def update(self, dt):
        if self.current_stage:
            self.current_stage.update(dt)
            
            if hasattr(self.current_stage, 'is_completed') and self.current_stage.is_completed:
                final_time_ms = pygame.time.get_ticks() - self.start_time
                self.last_run_time = final_time_ms

                is_new_record = self.game.save_manager.save_best_time(self.current_level_name, final_time_ms)

                if self.current_level_name in LEVEL_ORDER:
                    current_idx = LEVEL_ORDER.index(self.current_level_name)
                    if current_idx + 1 < len(LEVEL_ORDER):
                        next_level_name = LEVEL_ORDER[current_idx + 1]
                        self.game.save_manager.unlock_level(next_level_name)

                self.game.change_state(StateID.DAY_COMPLETE)

    def draw(self, screen):
        if self.current_stage:
            self.current_stage.draw(screen)

            if self.game.current_state == self:
                current_time_ms = pygame.time.get_ticks() - self.start_time
            else:
                current_time_ms = self.pause_start_time - self.start_time

            seconds = (current_time_ms // 1000) % 60
            minutes = (current_time_ms // 60000) % 60
            millis = (current_time_ms % 1000) // 10
            
            font = pygame.font.SysFont('courier', 32)

            time_text = font.render(f"TIME: {minutes:02d}:{seconds:02d}:{millis:02d}", True, (0, 255, 0))
            screen.blit(time_text, (screen.width - (time_text.width + 64), 64)) #y = screen.height - (time_text.height + 64))

# PAUSE -> PLAYING/SETTINGS/MENU

class PauseState(State):
    def __init__(self, game):
        super().__init__(game)
        self.options = ["RESUME", "RESTART LEVEL", "MENU"]
        self.selected_index = 0
        self.font_huge = pygame.font.SysFont('courier', 64, bold=True)
        self.font_large = pygame.font.SysFont('courier', 48, bold=True)

        self.overlay = pygame.Surface((WINDOW_WIDTH, WINDOW_HEIGHT), pygame.SRCALPHA)
        self.overlay.fill((0, 0, 0, 127))

    def events(self, event):
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_ESCAPE:
                self.game.states[StateID.PLAYING].resume_timer()
                self.game.change_state(StateID.PLAYING)

            elif event.key in (pygame.K_UP, pygame.K_w):
                self.selected_index = (self.selected_index - 1) % len(self.options)

            elif event.key in (pygame.K_DOWN, pygame.K_s):
                self.selected_index = (self.selected_index + 1) % len(self.options)

            elif event.key == pygame.K_RETURN:
                selected = self.options[self.selected_index]
                playing_state = self.game.states[StateID.PLAYING]
                
                if selected == "RESUME":
                    playing_state.resume_timer()
                    self.game.change_state(StateID.PLAYING)

                elif selected == "RESTART LEVEL":
                    playing_state.load_level(playing_state.current_level_name)

                elif selected == "MENU":
                    self.game.change_state(StateID.MENU)

    def draw(self, screen):
        self.game.states[StateID.PLAYING].draw(screen)
        screen.blit(self.overlay, (0, 0))

        title = self.font_huge.render("PAUSED", True, WHITE)
        title_rect = title.get_frect(center=(WINDOW_WIDTH / 2, WINDOW_HEIGHT / 2 - 64))
        screen.blit(title, title_rect)

        for i, option in enumerate(self.options):
            if i == self.selected_index:
                color = YELLOW
                text = f"> {option} <" 
            else:
                color = WHITE
                text = option
                
            img = self.font_large.render(text, True, color)
            rect = img.get_frect(center=(WINDOW_WIDTH / 2, WINDOW_HEIGHT / 2 + i * 64))
            screen.blit(img, rect)

# DAY_COMPLETE -> play next level PLAYING(retry or load next level) or quit to MENU

class DayCompleteState(State):
    def enter(self):
        pygame.mixer.music.fadeout(1000)
        playing_state = self.game.states[StateID.PLAYING]
        current_level = playing_state.current_level_name
        
        self.selected_index = 0
        if current_level in LEVEL_ORDER and LEVEL_ORDER.index(current_level) + 1 < len(LEVEL_ORDER):
            self.options = ["NEXT LEVEL", "RETRY", "MENU"]
        else:
            self.options = ["RETRY", "MENU"]

    def __init__(self, game):
        super().__init__(game)
        self.options = ["NEXT LEVEL", "RETRY", "MENU"]
        self.selected_index = 0
        self.font_huge = pygame.font.SysFont('courier', 64, bold=True)
        self.font_large = pygame.font.SysFont('courier', 48, bold=True)
        self.font_small = pygame.font.SysFont('courier', 32)

    def events(self, event):
        if event.type == pygame.KEYDOWN:
            if event.key in (pygame.K_UP, pygame.K_w):
                self.selected_index = (self.selected_index - 1) % len(self.options)

            elif event.key in (pygame.K_DOWN, pygame.K_s):
                self.selected_index = (self.selected_index + 1) % len(self.options)

            elif event.key == pygame.K_RETURN:
                selected = self.options[self.selected_index]
                playing_state = self.game.states[StateID.PLAYING]
                
                if selected == "NEXT LEVEL":
                    current_level = playing_state.current_level_name
                    if current_level in LEVEL_ORDER:
                        idx = LEVEL_ORDER.index(current_level)
                        if idx + 1 < len(LEVEL_ORDER):
                            next_level = LEVEL_ORDER[idx + 1]
                            playing_state.load_level(next_level)

                        else:
                            self.game.change_state(StateID.MENU) 
                            
                elif selected == "RETRY":
                    playing_state.load_level(playing_state.current_level_name)
                    
                elif selected == "MENU":
                    self.game.change_state(StateID.MENU)

    def draw(self, screen):
        screen.fill(YELLOW)
        title = self.font_huge.render("LEVEL COMPLETE", True, BLACK)
        title_rect = title.get_frect(center=(WINDOW_WIDTH / 2, WINDOW_HEIGHT / 2 - 128))
        screen.blit(title, title_rect)

        playing_state = self.game.states[StateID.PLAYING]
        run_time = playing_state.last_run_time
        seconds = (run_time // 1000) % 60
        minutes = (run_time // 60000) % 60
        millis = (run_time % 1000) // 10

        time_text = self.font_small.render(f"YOUR TIME: {minutes:02d}:{seconds:02d}:{millis:02d}", True, RED)
        time_rect = time_text.get_frect(center=(WINDOW_WIDTH / 2, WINDOW_HEIGHT / 2 - 64))
        screen.blit(time_text, time_rect)

        # TOTAL BEST TIME
        total_time = sum(self.game.save_manager.data.get("best_times", {}).values())
        t_seconds = (total_time // 1000) % 60
        t_minutes = (total_time // 60000) % 60
        t_millis = (total_time % 1000) // 10
        
        total_text = self.font_small.render(f"TOTAL TIME: {t_minutes:02d}:{t_seconds:02d}:{t_millis:02d}", True, BLACK)
        total_rect = total_text.get_frect(center=(WINDOW_WIDTH / 2, WINDOW_HEIGHT / 2 - 32))
        screen.blit(total_text, total_rect)

        for i, option in enumerate(self.options):
            if i == self.selected_index:
                color = BLACK
                text = f"> {option} <" 
            else:
                color = RED
                text = option
                
            img = self.font_large.render(text, True, color)
            rect = img.get_frect(center=(WINDOW_WIDTH / 2, WINDOW_HEIGHT / 2 + 48 + i * 64))
            screen.blit(img, rect)

# SETTINGS -> go back to MENU/PAUSE

class SettingsState(State):
    def __init__(self, game):
        super().__init__(game)
        self.options = ["FULLSCREEN", "MINIMALIST", "MUSIC VOL", "SFX VOL", "BACK"]
        self.selected_index = 0
        self.font_large = pygame.font.SysFont('courier', 48, bold=True)
        self.font_huge = pygame.font.SysFont('courier', 64, bold=True)

    def _handle_volume_change(self, selected, step):
        if selected == "MUSIC VOL":
            vol = self.game.save_manager.data["settings"].get("music_volume", 100)
            new_vol = max(0, min(100, vol + step))
            self.game.save_manager.data["settings"]["music_volume"] = new_vol
            self.game.save_manager.save()
            self.game.audio.update_music_volume()

        elif selected == "SFX VOL":
            vol = self.game.save_manager.data["settings"].get("sfx_volume", 100)
            new_vol = max(0, min(100, vol + step))
            self.game.save_manager.data["settings"]["sfx_volume"] = new_vol
            self.game.save_manager.save()
            self.game.audio.play_sfx('jump')

    def _handle_toggle(self, selected):
        if selected == "FULLSCREEN":
            current_val = self.game.save_manager.data["settings"]["fullscreen"]
            self.game.save_manager.data["settings"]["fullscreen"] = not current_val
            self.game.save_manager.save()
            pygame.display.toggle_fullscreen()

        elif selected == "MINIMALIST":
            current_val = self.game.save_manager.data["settings"].get("minimalist", False)
            self.game.save_manager.data["settings"]["minimalist"] = not current_val
            self.game.save_manager.save()

        elif selected == "BACK":
            self.game.change_state(StateID.MENU)

    def events(self, event):
        if event.type == pygame.KEYDOWN:
            if event.key in (pygame.K_UP, pygame.K_w):
                self.selected_index = (self.selected_index - 1) % len(self.options)

            elif event.key in (pygame.K_DOWN, pygame.K_s):
                self.selected_index = (self.selected_index + 1) % len(self.options)

            elif event.key in (pygame.K_LEFT, pygame.K_RIGHT, pygame.K_a, pygame.K_d):
                selected = self.options[self.selected_index]
                step = -10 if event.key in (pygame.K_LEFT, pygame.K_a) else 10
                self._handle_volume_change(selected, step)

            elif event.key == pygame.K_RETURN:
                selected = self.options[self.selected_index]
                self._handle_toggle(selected)

    def _get_option_text(self, option):
        if option == "FULLSCREEN":
            is_on = self.game.save_manager.data["settings"]["fullscreen"]
            return f"FULLSCREEN [{'ON' if is_on else 'OFF'}]"

        elif option == "MINIMALIST":
            is_on = self.game.save_manager.data["settings"].get("minimalist", False)
            return f"MINIMALIST [{'ON' if is_on else 'OFF'}]"

        elif option == "MUSIC VOL":
            vol = self.game.save_manager.data["settings"].get("music_volume", 100)
            return f"MUSIC VOL < {vol}% >"

        elif option == "SFX VOL":
            vol = self.game.save_manager.data["settings"].get("sfx_volume", 100)
            return f"SFX VOL   < {vol}% >"

        return option

    def draw(self, screen):
        screen.fill(BLACK)

        title = self.font_huge.render("SETTINGS", True, WHITE)
        title_rect = title.get_frect(center=(WINDOW_WIDTH / 2, WINDOW_HEIGHT / 2 - 160))
        screen.blit(title, title_rect)

        for i, option in enumerate(self.options):
            display_text = self._get_option_text(option)
            color = YELLOW if i == self.selected_index else WHITE
            text = f"> {display_text} <" if i == self.selected_index else display_text
            img = self.font_large.render(text, True, color)
            rect = img.get_frect(center=(WINDOW_WIDTH / 2, WINDOW_HEIGHT / 2 - 24 + i * 64))
            screen.blit(img, rect)
