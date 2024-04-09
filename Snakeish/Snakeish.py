import pygame
import random

#definerer skærmstørrelse og gitterstørrelse
WIDTH, HEIGHT = 800, 600
GRID_SIZE = 20
SNAKE_SPEED = 10
WHITE = (255, 255, 255)
RED = (255, 0, 0)
GREEN = (0, 255, 0)
BLACK = (0, 0, 0)
PURPLE = (128, 32, 160)
BLUE = (0, 0, 255)

#klassen Snake, som repræsenterer slangen
class Snake:
    def __init__(self, game):
        self.game = game
        #initialiserer slangen med en længde på 1, en position midt på skærmen, en tilfældig retning, en farve og en variabel til at styre retningsskift
        self.length = 3
        self.positions = [((WIDTH / 2), (HEIGHT / 2))]
        self.direction = random.choice([(0, -1), (0, 1), (-1, 0), (1, 0)])
        self.color = GREEN
        self.can_turn = True

    #returnerer hovedets position
    def get_head_position(self):
        return self.positions[0]

    #drejer slangen i den angivne retning, hvis det er tilladt
    def turn(self, point):
        if self.length > 1 and (point[0] * -1, point[1] * -1) == self.direction:
            return
        elif self.can_turn:
            self.direction = point
            self.can_turn = False

    #flytter slangen
    def move(self):
        cur = self.get_head_position()
        x, y = self.direction
        new = (((cur[0] + (x * GRID_SIZE))), (cur[1] + (y * GRID_SIZE)))
        
        #tjek om positionen er ude for vinduet (resetter)
        if new[0] < 0 or new[0] >= WIDTH or new[1] < 0 or new[1] >= HEIGHT:
            self.game.game_over = True
        elif len(self.positions) > 2 and new in self.positions[2:]:
            self.game.game_over = True
        else:
            self.positions.insert(0, new)
            if len(self.positions) > self.length:
                self.positions.pop()
        self.can_turn = True

    def reset(self):
            #resetter scoren i spillet
            self.game.score = 0
            self.length = 3
            self.positions = [((WIDTH / 2), (HEIGHT / 2))]
            self.direction = random.choice([(0, -1), (0, 1), (-1, 0), (1, 0)])
            self.can_turn = True

    #tegner slangen på skærmen
    def draw(self, surface):
        for p in self.positions:
            r = pygame.Rect((p[0], p[1]), (GRID_SIZE, GRID_SIZE))
            pygame.draw.rect(surface, self.color, r)


#klassen Food, som repræsenterer føden
class Food:
    def __init__(self):
        #initialiserer føden med en tilfældig position og en farve
        self.position = (0, 0)
        self.color = RED
        self.timer = 0
        self.effectList = ["Normal", "Normal", "Normal", "AntiSnake", "ExtraScore"]
        self.effect = random.choice(self.effectList)
        self.randomize_position()

    #tilfældigt placerer føden på skærmen
    def randomize_position(self):
        self.effect = random.choice(self.effectList)
        if self.effect == "Normal":
            self.color = RED
        elif self.effect == "AntiSnake":
            self.color = PURPLE
        elif self.effect == "ExtraScore":
            self.color = BLUE
        self.position = (random.randint(0, (WIDTH - GRID_SIZE) // GRID_SIZE) * GRID_SIZE,
                         random.randint(0, (HEIGHT - GRID_SIZE) // GRID_SIZE) * GRID_SIZE)

    #tegner føden på skærmen
    def draw(self, surface):
        r = pygame.Rect((self.position[0], self.position[1]), (GRID_SIZE, GRID_SIZE))
        pygame.draw.rect(surface, self.color, r)

class Game:
    def __init__(self):
        #initialiserer spillet med en slange, føde og en score
        self.snake = Snake(self) 
        self.food1 = Food()
        self.food2 = Food()
        self.food3 = Food()
        self.score = 0
        self.game_over = False

    #tegner spillet på skærmen
    def draw(self, surface):
        surface.fill(BLACK)
        self.snake.move()
        self.check_collision()
        self.snake.draw(surface)
        self.food1.draw(surface)
        self.food2.draw(surface)
        self.food3.draw(surface)
        self.draw_score(surface)
        pygame.display.update()

    # Giver forskellige effekter an på typen af føden
    def foodEffect(self, food):
        if food.effect == "Normal":
            self.snake.length += 1
            self.score += 1
        elif food.effect == "AntiSnake":
            self.snake.length -= 1
            self.snake.positions.pop()
            self.score += 1
            if self.snake.length < 1:
                self.game_over = True
        elif food.effect == "ExtraScore":
            self.snake.length += 1
            self.score += 5
        food.timer = 0
        food.randomize_position()
        
    #tjekker om slangen kolliderer med føden
    def check_collision(self):
        if self.snake.get_head_position() == self.food1.position:
            self.foodEffect(self.food1)
        if self.snake.get_head_position() == self.food2.position:
            self.foodEffect(self.food2)
        if self.snake.get_head_position() == self.food3.position:
            self.foodEffect(self.food3)
            
    def checkFoodTimer(self, food):
        food.timer += 1
        if food.timer > 120:
            food.randomize_position()
            food.timer = 0
            
    #tegner scoren på skærmen
    def draw_score(self, surface):
        font = pygame.font.SysFont(None, 36)
        score_text = font.render(f"Score: {self.score}", True, WHITE)
        surface.blit(score_text, (10, 10))

    #resetter spillet
    def reset_game(self):
        self.snake.reset()
        self.food1.randomize_position()
        self.food2.randomize_position()
        self.food3.randomize_position()
        self.score = 0
        self.game_over = False

        #viser game over-skærmen
    def display_game_over_screen(self, surface):
        surface.fill(BLACK)
        font = pygame.font.SysFont(None, 64)
        game_over_text = font.render("Game Over", True, RED)
        score_text = font.render(f"Final Score: {self.score}", True, WHITE)
        restart_text = font.render("Press SPACE to Restart", True, WHITE)
        exit_text = font.render("or ESC to close game", True, WHITE)
        game_over_rect = game_over_text.get_rect(center=(WIDTH // 2, HEIGHT // 2 - 100))
        score_rect = score_text.get_rect(center=(WIDTH // 2, HEIGHT // 2 - 50)) 
        restart_rect = restart_text.get_rect(center=(WIDTH // 2, HEIGHT // 2 + 50))
        exit_rect = exit_text.get_rect(center=(WIDTH // 2, HEIGHT // 2 + 100))
        surface.blit(game_over_text, game_over_rect)
        surface.blit(score_text, score_rect)
        surface.blit(restart_text, restart_rect)
        surface.blit(exit_text, exit_rect)
        pygame.display.update()

#hovedfunktionen, som kører spillet
def main():
    pygame.init()
    clock = pygame.time.Clock()
    screen = pygame.display.set_mode((WIDTH, HEIGHT))
    pygame.display.set_caption("Snakeish")
    pygame.display.set_icon(pygame.image.load('Snakeish/SnakeLogo.png'))
    game = Game()

    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                quit()
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_SPACE and game.game_over:
                    game.display_game_over_screen(screen)
                    game.reset_game()
                elif event.key == pygame.K_ESCAPE and game.game_over:
                    pygame.quit()
                    quit()
                elif event.key == pygame.K_UP or event.key == pygame.K_w:
                    game.snake.turn((0, -1))
                elif event.key == pygame.K_DOWN or event.key == pygame.K_s:
                    game.snake.turn((0, 1))
                elif event.key == pygame.K_LEFT or event.key == pygame.K_a:
                    game.snake.turn((-1, 0))
                elif event.key == pygame.K_RIGHT or event.key == pygame.K_d:
                    game.snake.turn((1, 0))

        if not game.game_over:
            game.draw(screen)
            game.checkFoodTimer(game.food1)
            game.checkFoodTimer(game.food2)
            game.checkFoodTimer(game.food3)
            clock.tick(SNAKE_SPEED)
        else:
            game.display_game_over_screen(screen)

if __name__ == "__main__":
    main()
