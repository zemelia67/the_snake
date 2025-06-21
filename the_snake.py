from random import randint

import pygame

# Константы для размеров поля и сетки:
SCREEN_WIDTH, SCREEN_HEIGHT = 640, 480
GRID_SIZE = 20
GRID_WIDTH = SCREEN_WIDTH // GRID_SIZE
GRID_HEIGHT = SCREEN_HEIGHT // GRID_SIZE

# Направления движения:
UP = (0, -1)
DOWN = (0, 1)
LEFT = (-1, 0)
RIGHT = (1, 0)

# Цвета:
BOARD_BACKGROUND_COLOR = (0, 0, 0)
BORDER_COLOR = (93, 216, 228)
APPLE_COLOR = (255, 0, 0)
SNAKE_COLOR = (0, 255, 0)
HEAD_COLOR = (0, 200, 0)

# Скорость движения змейки:
SPEED = 10

# Настройка игрового окна:
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT), 0, 32)
pygame.display.set_caption('Змейка')
clock = pygame.time.Clock()


# Тут опишите все классы игры.
class GameObject:
    """Описание родительского класса"""

    def __init__(self) -> None:
        self.position = (SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2)
        self.body_color = None
        self.head_color = None

    def draw(self):
        """Метод отрисовки, переопределяется в дочерних классах"""
        pass


class Apple(GameObject):
    """Описание класса яблоко"""

    def __init__(self):
        super().__init__()
        self.body_color = APPLE_COLOR
        self.randomize_position()

    def randomize_position(self):
        """Метод устанавливающий случайное положение яблока на игровом поле"""
        self.position = (
            randint(0, GRID_WIDTH - 1) * GRID_SIZE,
            randint(0, GRID_HEIGHT - 1) * GRID_SIZE
        )

    def draw(self):
        """Метод отрисовки яблока"""
        rect = pygame.Rect(self.position, (GRID_SIZE, GRID_SIZE))
        pygame.draw.rect(screen, self.body_color, rect)
        pygame.draw.rect(screen, BORDER_COLOR, rect, 1)


class Snake(GameObject):
    """Описание класса змейки"""

    def __init__(self):
        super().__init__()
        self.body_color = SNAKE_COLOR
        self.head_color = HEAD_COLOR
        self.direction = RIGHT
        self.next_direction = None
        self.reset()

    def update_direction(self):
        """Метод обновления направления после нажатия на кнопку"""
        if self.next_direction:
            self.direction = self.next_direction
            self.next_direction = None

    def move(self):
        """Метод обновления позиции змейки"""
        head_x, head_y = self.get_head_position()
        dir_x, dir_y = self.direction
        new_x = (head_x + dir_x * GRID_SIZE) % SCREEN_WIDTH
        new_y = (head_y + dir_y * GRID_SIZE) % SCREEN_HEIGHT
        new_position = (new_x, new_y)
        if new_position in self.positions[:-1]:
            self.reset()
            return False
        self.positions.insert(0, new_position)
        self.last = self.positions.pop()
        return True

    def draw_segment(self, position, is_head=False):
        """Метод отрисовки одного сегмента змейки"""
        color = self.head_color if is_head else self.body_color
        rect = pygame.Rect(position, (GRID_SIZE, GRID_SIZE))
        pygame.draw.rect(screen, color, rect)
        pygame.draw.rect(screen, BORDER_COLOR, rect, 1)

    def draw(self):
        """Метод отрисовки змейки на экране"""
        # Отрисовка тела
        for position in self.positions[1:]:
            self.draw_segment(position)
        # Отрисовка головы
        if self.positions:
            self.draw_segment(self.positions[0], is_head=True)

    def get_head_position(self):
        """Метод возвращения позиции головы змейки"""
        return self.positions[0] if self.positions else (0, 0)

    def reset(self):
        """Метод сброса змейки в начальное состояние"""
        self.positions = [(SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2)]
        self.direction = RIGHT
        self.last = None


def handle_keys(game_object):
    """Функция обработки действий пользователя"""
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            raise SystemExit
        elif event.type == pygame.KEYDOWN:
            if event.key == pygame.K_UP and game_object.direction != DOWN:
                game_object.next_direction = UP
            elif event.key == pygame.K_DOWN and game_object.direction != UP:
                game_object.next_direction = DOWN
            elif event.key == pygame.K_LEFT and game_object.direction != RIGHT:
                game_object.next_direction = LEFT
            elif event.key == pygame.K_RIGHT and game_object.direction != LEFT:
                game_object.next_direction = RIGHT


def main():
    """Инициализация PyGame"""
    pygame.init()
    apple = Apple()
    snake = Snake()
    score = 0
    font = pygame.font.SysFont('Arial', 25)

    while True:
        clock.tick(SPEED)
        handle_keys(snake)
        snake.update_direction()
        if snake.move():
            if snake.get_head_position() == apple.position:
                snake.positions.append(snake.last)
                apple.randomize_position()
                score += 1
        else:
            score = 0

        screen.fill(BOARD_BACKGROUND_COLOR)
        apple.draw()
        snake.draw()

        score_text = font.render(f'Score: {score}', True, (255, 255, 255))
        screen.blit(score_text, (5, 5))

        pygame.display.update()


if __name__ == '__main__':
    main()
