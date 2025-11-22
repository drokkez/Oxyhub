import pygame
from player import Player
from enemy import Enemy
from map import GameMap
import math

class Game:
    def __init__(self):
        self.width = 800
        self.height = 600
        self.screen = pygame.display.set_mode((self.width, self.height))
        pygame.display.set_caption("Doom Python")
        self.clock = pygame.time.Clock()
        self.running = True
        
        # Цвета
        self.WHITE = (255, 255, 255)
        self.BLACK = (0, 0, 0)
        self.RED = (255, 0, 0)
        self.GREEN = (0, 255, 0)
        self.BLUE = (0, 0, 255)
        self.GRAY = (128, 128, 128)
        
        # Инициализация объектов игры
        self.game_map = GameMap()
        self.player = Player(1.5, 1.5, 0)  # Начальная позиция игрока
        self.enemies = [Enemy(4.5, 4.5), Enemy(3.5, 3.5)]  # Пример врагов
        self.bullets = []
        
        # Параметры отображения
        self.resolution = 120  # Количество лучей
        self.fov = math.pi / 3  # Угол обзора
        self.render_dist = 10  # Дистанция отрисовки
        
    def run(self):
        while self.running:
            self.handle_events()
            self.update()
            self.render()
            self.clock.tick(60)
    
    def handle_events(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self.running = False
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_SPACE:
                    # Создание пули при нажатии пробела
                    self.bullets.append(
                        pygame.Rect(
                            self.player.x * 64, 
                            self.player.y * 64, 
                            4, 4
                        )
                    )
    
    def update(self):
        # Обновление позиции игрока
        keys = pygame.key.get_pressed()
        self.player.move(keys, self.game_map)
        
        # Обновление врагов
        for enemy in self.enemies:
            enemy.update(self.player)
        
        # Обновление пуль
        bullets_to_remove = []
        for i, bullet in enumerate(self.bullets):
            # Простое движение пули (в направлении взгляда игрока)
            dx = math.cos(self.player.angle) * 5
            dy = math.sin(self.player.angle) * 5
            bullet.x += dx
            bullet.y += dy
            
            # Проверка столкновений с врагами
            for j, enemy in enumerate(self.enemies):
                if bullet.colliderect(pygame.Rect(enemy.x * 64, enemy.y * 64, 32, 32)):
                    bullets_to_remove.append(i)
                    if j < len(self.enemies):
                        del self.enemies[j]
                    break
            
            # Удаление пуль за пределами карты
            if (bullet.x < 0 or bullet.x > 640 or 
                bullet.y < 0 or bullet.y > 640):
                bullets_to_remove.append(i)
        
        # Удаляем пули в обратном порядке, чтобы не нарушить индексы
        for i in reversed(bullets_to_remove):
            if i < len(self.bullets):
                del self.bullets[i]
    
    def render(self):
        self.screen.fill(self.BLACK)
        
        # Рендеринг 3D вида
        self.render_3d_view()
        
        # Рендеринг 2D миникарты
        self.render_minimap()
        
        pygame.display.flip()
    
    def render_3d_view(self):
        # Алгоритм raycasting для 3D отображения
        for x in range(self.resolution):
            # Рассчитываем угол луча
            ray_angle = self.player.angle - self.fov/2 + (x/self.resolution) * self.fov
            
            # Расстояние до стены
            dist = 0
            hit_wall = False
            
            # Продолжаем отслеживать луч, пока не найдем стену или не достигнем максимальной дистанции
            while not hit_wall and dist < self.render_dist:
                dist += 0.05
                ray_x = self.player.x + math.cos(ray_angle) * dist
                ray_y = self.player.y + math.sin(ray_angle) * dist
                
                # Проверяем, попадает ли луч в стену
                map_x, map_y = int(ray_x), int(ray_y)
                if map_x < 0 or map_x >= len(self.game_map.layout[0]) or map_y < 0 or map_y >= len(self.game_map.layout):
                    hit_wall = True
                    dist = self.render_dist
                elif self.game_map.layout[map_y][map_x] == 1:
                    hit_wall = True
            
            # Рассчитываем высоту стены на экране
            if hit_wall:
                wall_height = min(self.height, (self.height / dist) * 100)
                wall_rect = pygame.Rect(
                    x * (self.width // self.resolution),
                    (self.height - wall_height) // 2,
                    self.width // self.resolution + 1,
                    wall_height
                )
                
                # Определяем яркость в зависимости от расстояния
                brightness = max(0, 255 - dist * 20)
                color = (brightness // 2, brightness, brightness // 3)  # Цвет стены
                
                pygame.draw.rect(self.screen, color, wall_rect)
    
    def render_minimap(self):
        # Размер миникарты
        map_size = 150
        cell_size = map_size // len(self.game_map.layout)
        offset_x = 10
        offset_y = 10
        
        # Рендерим миникарту
        for y, row in enumerate(self.game_map.layout):
            for x, cell in enumerate(row):
                rect = pygame.Rect(
                    offset_x + x * cell_size,
                    offset_y + y * cell_size,
                    cell_size,
                    cell_size
                )
                
                if cell == 1:  # Стена
                    pygame.draw.rect(self.screen, self.GRAY, rect)
                else:  # Пустое пространство
                    pygame.draw.rect(self.screen, self.BLACK, rect)
                    pygame.draw.rect(self.screen, self.WHITE, rect, 1)
        
        # Рисуем игрока на миникарте
        player_x = offset_x + self.player.x * cell_size
        player_y = offset_y + self.player.y * cell_size
        pygame.draw.circle(self.screen, self.BLUE, (int(player_x), int(player_y)), 4)
        
        # Рисуем направление взгляда игрока
        look_x = player_x + math.cos(self.player.angle) * 10
        look_y = player_y + math.sin(self.player.angle) * 10
        pygame.draw.line(self.screen, self.BLUE, (player_x, player_y), (look_x, look_y), 2)
        
        # Рисуем врагов на миникарте
        for enemy in self.enemies:
            enemy_x = offset_x + enemy.x * cell_size
            enemy_y = offset_y + enemy.y * cell_size
            pygame.draw.circle(self.screen, self.RED, (int(enemy_x), int(enemy_y)), 3)