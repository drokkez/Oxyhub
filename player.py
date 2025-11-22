import math
import pygame

class Player:
    def __init__(self, x, y, angle):
        self.x = x
        self.y = y
        self.angle = angle  # Угол направления взгляда
        self.speed = 0.05  # Скорость движения
        self.turn_speed = 0.04  # Скорость поворота
    
    def move(self, keys, game_map):
        # Поворот
        if keys[pygame.K_LEFT]:
            self.angle -= self.turn_speed
        if keys[pygame.K_RIGHT]:
            self.angle += self.turn_speed
        
        # Создаем временные переменные для проверки столкновений
        new_x, new_y = self.x, self.y
        
        # Перемещение вперед/назад
        if keys[pygame.K_UP]:
            new_x += math.cos(self.angle) * self.speed
            new_y += math.sin(self.angle) * self.speed
        if keys[pygame.K_DOWN]:
            new_x -= math.cos(self.angle) * self.speed
            new_y -= math.sin(self.angle) * self.speed
        
        # Боковое движение (стрейфинг)
        if keys[pygame.K_a]:
            new_x += math.cos(self.angle - math.pi/2) * self.speed
            new_y += math.sin(self.angle - math.pi/2) * self.speed
        if keys[pygame.K_d]:
            new_x += math.cos(self.angle + math.pi/2) * self.speed
            new_y += math.sin(self.angle + math.pi/2) * self.speed
        
        # Проверка на столкновение со стенами
        if not self.check_collision(new_x, self.y, game_map):
            self.x = new_x
        if not self.check_collision(self.x, new_y, game_map):
            self.y = new_y
    
    def check_collision(self, x, y, game_map):
        # Проверяем, находится ли позиция внутри стены
        map_x, map_y = int(x), int(y)
        
        # Проверяем границы карты
        if map_x < 0 or map_x >= len(game_map.layout[0]) or map_y < 0 or map_y >= len(game_map.layout):
            return True
        
        # Проверяем, является ли клетка стеной
        if game_map.layout[map_y][map_x] == 1:
            return True
        
        return False