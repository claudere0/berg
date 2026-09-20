import pygame

class InputManager:
    """
    Отвечает за сбор ввода с клавиатуры/мыши и формирование команд для объектов.
    Разделяет логику чтения ввода от логики реакции на этот ввод.
    """
    def __init__(self):
        self.keys_pressed = {}
        self.keys_just_pressed = {}
        self._previous_keys = {}

    def update(self):
        keys = pygame.key.get_pressed()
        
        # Переводим tuple в dict для удобства, либо используем pygame.key.get_pressed() напрямую.
        # Для простоты:
        self._previous_keys = self.keys_pressed.copy()
        
        self.keys_pressed = {
            'left': keys[pygame.K_LEFT] or keys[pygame.K_a],
            'right': keys[pygame.K_RIGHT] or keys[pygame.K_d],
            'up': keys[pygame.K_UP] or keys[pygame.K_w],
            'down': keys[pygame.K_DOWN] or keys[pygame.K_s],
            'jump': keys[pygame.K_SPACE],
            'dash': keys[pygame.K_LSHIFT] or keys[pygame.K_RSHIFT],
            'shoot': keys[pygame.K_f],
            'block': keys[pygame.K_v]
        }

        # Определяем клавиши, которые были нажаты ИМЕННО В ЭТОМ кадре (just pressed)
        self.keys_just_pressed = {}
        for key, is_pressed in self.keys_pressed.items():
            was_pressed = self._previous_keys.get(key, False)
            self.keys_just_pressed[key] = is_pressed and not was_pressed

    def is_pressed(self, action: str) -> bool:
        return self.keys_pressed.get(action, False)

    def is_just_pressed(self, action: str) -> bool:
        return self.keys_just_pressed.get(action, False)

    def get_input_vector(self):
        """Возвращает вектор направления движения на основе нажатых клавиш (x, y)"""
        x = 0
        y = 0
        if self.is_pressed('left'):
            x -= 1
        if self.is_pressed('right'):
            x += 1
        if self.is_pressed('up'):
            y -= 1
        if self.is_pressed('down'):
            y += 1
            
        return pygame.math.Vector2(x, y)
