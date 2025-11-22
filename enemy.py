import math
import random

class Enemy:
    def __init__(self, x, y):
        self.x = x
        self.y = y
        self.size = 0.5  # Размер врага
        self.speed = 0.02  # Скорость движения врага
        self.health = 100  # Здоровье врага
        self.detection_range = 3  # Диапазон обнаружения игрока
    
    def update(self, player):
        # Рассчитываем расстояние до игрока
        dist_to_player = math.sqrt((self.x - player.x)**2 + (self.y - player.y)**2)
        
        # Если игрок в пределах диапазона обнаружения
        if dist_to_player < self.detection_range:
            # Двигаемся в направлении игрока
            dx = player.x - self.x
            dy = player.y - self.y
            dist = max(0.01, math.sqrt(dx**2 + dy**2))  # Избегаем деления на 0
            
            # Нормализуем вектор направления
            dx /= dist
            dy /= dist
            
            # Обновляем позицию врага
            self.x += dx * self.speed
            self.y += dy * self.speed