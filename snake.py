import pygame
from random import randint

SCREEN_SIZE = SCREEN_WIDTH, SCREEN_HEIGHT = 640, 640
grid_size = grid_width, grid_height = 16, 16
tick_speed = 200
cell_size = cell_width, cell_height = SCREEN_WIDTH / grid_width, SCREEN_HEIGHT / grid_height
starting_length = 5


def main():
    # Initialization
    pygame.init()
    DISPLAY = pygame.display.set_mode(SCREEN_SIZE)
    pygame.display.set_caption("Snake")
    clock = pygame.time.Clock()

    snake = Snake((grid_width/2, grid_height/2), DISPLAY, direction="E")

    def spawn_apple():
        space_occupied = True
        while space_occupied:
            position = (randint(0, grid_width - 1), randint(0, grid_height - 1))
            space_occupied = False

            body = snake
            while body.tail is not None:
                if body.position == position:
                    space_occupied = True
                body = body.tail

        return Apple(DISPLAY, position)

    apple = spawn_apple()

    for i in range(starting_length - 1):
        snake.grow()

    # Runtime
    running = True
    last_tick = 0

    while running and snake.alive:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False

            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_LEFT and snake.last_direction != "E":
                    snake.direction = "W"
                if event.key == pygame.K_RIGHT and snake.last_direction != "W":
                    snake.direction = "E"
                if event.key == pygame.K_UP and snake.last_direction != "S":
                    snake.direction = "N"
                if event.key == pygame.K_DOWN and snake.last_direction != "N":
                    snake.direction = "S"

        # Ticking
        last_tick += clock.tick()
        if last_tick >= tick_speed:
            last_tick += -tick_speed
            snake.tick()

            if snake.position == apple.position:
                apple = spawn_apple()
                snake.grow()

        # Display update
        DISPLAY.fill((255, 255, 255))
        snake.draw()
        apple.draw()

        pygame.display.update()


class Apple:
    def __init__(self, display, position, color = (255, 0, 0)):
        self.display = display
        self.color = color
        self.position = self.x, self.y = position

    def draw(self):
        rect = pygame.Rect(self.x * cell_width, self.y * cell_height, cell_width, cell_height)
        pygame.draw.ellipse(self.display, self.color, rect)


class Snake:
    def __init__(self, position, display, direction=None, color=(0, 0, 0)):
        self.position = self.x, self.y = position
        self.last_position = position
        self.direction = self.last_direction = direction
        self.tail = None
        self.color = color
        self.display = display
        self.alive = True

    def get_tail(self):
        body = self
        while True:
            if body.tail is None:
                return body
            body = body.tail

    def grow(self):
        tail = self.get_tail()

        tail.tail = Snake(tail.position, self.display)

    def set_position(self, position):
        self.last_position = self.position
        self.position = self.x, self.y = position

    def move_to(self, position):
        self.set_position(position)

        if self.tail is not None:
            self.tail.move_to(self.last_position)

    def draw(self):
        rect = pygame.Rect(self.x * cell_width, self.y * cell_height, cell_width, cell_height)
        pygame.draw.rect(self.display, self.color, rect)

        if self.tail is not None:
            self.tail.draw()

    def tick(self):
        self.last_direction = self.direction

        # Movement
        x_change = 0
        y_change = 0

        if self.direction == "E":
            x_change += 1
        elif self.direction == "W":
            x_change += -1
        elif self.direction == "N":
            y_change += -1
        elif self.direction == "S":
            y_change += 1

        self.move_to((self.x + x_change, self.y + y_change))

        # Collision detection
        body = self
        while body.tail is not None:
            body = body.tail
            if body.position == self.position:
                self.alive = False

        # Boundary detection
        if self.x < 0 or self.x >= grid_width:
            self.alive = False
        if self.y < 0 or self.y >= grid_height:
            self.alive = False 


if __name__ == "__main__":
    main()
