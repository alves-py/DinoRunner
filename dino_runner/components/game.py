from cgitb import reset
import pygame

from dino_runner.components.dinosaur import Dinosaur
from dino_runner.utils.constants import BG, ICON, SCREEN_HEIGHT, SCREEN_WIDTH, TITLE, FPS, RESETE, GAME_OVER, DEFAULT_TYPE, DINO_DEAD
from dino_runner.components.obstacles.obstacle_manager import ObstacleManager
from dino_runner.components.power_ups.power_up_manager import PowerUpManager

FONT_STYLE = "freesansbold.ttf"


class Game:
    def __init__(self):
        pygame.init()
        pygame.display.set_caption(TITLE)
        pygame.display.set_icon(ICON)
        self.screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
        self.clock = pygame.time.Clock()
        self.playing = False
        self.running = False
        self.game_speed = 20
        self.x_pos_bg = 0
        self.y_pos_bg = 380
        self.score = 0
        self.score_accumulator = 0
        self.death_count = 0
        self.player = Dinosaur()
        self.obstacle_manager = ObstacleManager()
        self.power_up_manager = PowerUpManager()

    def execute(self):
        self.running = True
        while self.running:
            if not self.playing:
                self.show_menu()

        pygame.display.quit()
        pygame.quit()

    def run(self):
        self.playing = True
        self.score = 0
        self.obstacle_manager.reset_obstacles()
        self.power_up_manager.reset_power_ups()
        while self.playing:
            self.events()
            self.update()
            self.draw()

    def events(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self.playing = False
                self.running = False

    def update(self):
        user_input = pygame.key.get_pressed()
        self.player.update(user_input)
        self.obstacle_manager.update(self)
        self.power_up_manager.update(self.score, self.game_speed, self.player)

    def update_score(self):
        self.score +=1
        if self.score % 100 == 0:
            self.game_speed += 2

        if self.score >= self.score_accumulator:
            self.score_accumulator = self.score

        self.format_text(f"Score: {self.score}", 1000, 50, 30)

    def draw(self):
        self.clock.tick(FPS)
        self.screen.fill((255, 255, 255))
        self.draw_background()
        self.player.draw(self.screen)
        self.obstacle_manager.draw(self.screen)
        self.update_score()
        self.draw_power_up_time()
        self.power_up_manager.draw(self.screen)
        pygame.display.update()
        pygame.display.flip()

    def draw_power_up_time(self):
        if self.player.has_power_up:
            time_to_show = round((self.player.power_up_time - pygame.time.get_ticks()) / 1000, 2)
            if time_to_show >= 0:
                self.format_text(f"{self.player.type.capitalize()} enabled for {time_to_show} seconds.", 500, 40, 18)
            else:
                self.player.has_power_up = False
                self.player.type = DEFAULT_TYPE

    def draw_background(self):
        image_width = BG.get_width()
        self.screen.blit(BG, (self.x_pos_bg, self.y_pos_bg))
        self.screen.blit(BG, (image_width + self.x_pos_bg, self.y_pos_bg))
        if self.x_pos_bg <= -image_width:
            self.screen.blit(BG, (image_width + self.x_pos_bg, self.y_pos_bg))
            self.x_pos_bg = 0
        self.x_pos_bg -= self.game_speed

    def handle_events_on_menu(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self.playing = False
                self.running = False
            elif event.type == pygame.KEYDOWN:
                self.run()
            
    def format_text(self, dados_inseridos, eixo_y, eixo_x, size_font):
        font = pygame.font.Font(FONT_STYLE, int(size_font))
        text = font.render(dados_inseridos, True, (0, 0, 0))
        text_rect = text.get_rect()
        text_rect.center = (eixo_y, eixo_x)
        self.screen.blit(text, text_rect)

    def show_menu(self):
        self.screen.fill((255, 255, 255))
        half_screen_height = SCREEN_HEIGHT // 2
        half_screen_width = SCREEN_WIDTH // 2

        if self.death_count == 0:
            self.screen.blit(ICON, (half_screen_width - 40, half_screen_height - 250))
            self.format_text("Press any key to start", half_screen_width, half_screen_height, 50)
        else:
            self.screen.blit(DINO_DEAD, (half_screen_width - 20, half_screen_height - 100))
            self.screen.blit(RESETE, (half_screen_width - 20, half_screen_height + 20))
            self.screen.blit(GAME_OVER, (half_screen_width - 170, half_screen_height - 240))
            self.format_text(f"Your Score: {self.score}", half_screen_width - 120, half_screen_height - 150, 20)
            self.format_text(f"Best Score: {self.score_accumulator}", half_screen_width + 120, half_screen_height - 150, 20)
            self.format_text(f"You already died {self.death_count} times", half_screen_width -20, half_screen_height + 200, 30)
            self.format_text("You're dead! Press any key to restart", half_screen_width, half_screen_height + 120, 40)
            self.game_speed = 20

        pygame.display.update()
        self.handle_events_on_menu()
