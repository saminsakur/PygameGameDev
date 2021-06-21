import pygame
import os


class MainWindow:
    def __init__(self):
        # Initializes stuffs
        pygame.init()
        pygame.font.init()
        pygame.display.init()
        pygame.mixer.init()

        self.WIDTH, self.HEIGHT = 900, 500
        self.WINDOW = pygame.display.set_mode((self.WIDTH, self.HEIGHT))

        self.BORDER = pygame.Rect(self.WIDTH//2-5, 0, 10, self.HEIGHT)

        self.VEL = 5
        self.FPS = 60
        self.BULLET_VEL = 7
        self.MAX_BULLETS = 3

        self.HEALTH_FONT = pygame.font.SysFont("comicsans", 40)
        self.WINNER_FONT = pygame.font.SysFont('comicsans', 100)
        self.EXIT_KEY_PRESSED = pygame.font.SysFont("comicsans", 50)

        self.GREEN_HIT = pygame.USEREVENT + 1
        self.RED_HIT = pygame.USEREVENT + 2
        
        self.BACKGROUND_IMAGE = pygame.transform.scale(
            pygame.image.load(
                os.path.join("Assets", "bg.png")), (self.WIDTH, self.HEIGHT))

        self.SPACESHIP_IMAGE_RED = pygame.image.load(os.path.join("Assets", "red_spaceship.png"))
        self.RED_SPACESHIP = pygame.transform.rotate(
            pygame.transform.scale(
                self.SPACESHIP_IMAGE_RED, (60, 60)), 90)

        self.SPACESHIP_IMAGE_GREEN = pygame.image.load(os.path.join("Assets", "green_spaceship.png"))
        self.GREEN_SPACESHIP = pygame.transform.rotate(
            pygame.transform.scale(
                self.SPACESHIP_IMAGE_GREEN, (60, 60)), 270)

        # self.BULLET_SHOOT_SOUND = pygame.mixer.load()
        # self.BULLET_FIRED_SOUND = pygame.music.load()



        pygame.display.set_caption("My cool game")


    def drawWinner(self, text, exit_text):
        winner_text_game_over = self.WINNER_FONT.render(text, 1, (255, 255, 255))
        press_any_key_to_retry = self.EXIT_KEY_PRESSED.render(exit_text, 1, (255, 255, 255))

        self.WINDOW.blit(
            winner_text_game_over, (
                self.WIDTH/2 - winner_text_game_over.get_width()/2, self.HEIGHT/2 - winner_text_game_over.get_height()/2
            )
        )
        self.WINDOW.blit(
            press_any_key_to_retry, (
                self.WIDTH/2 - press_any_key_to_retry.get_width()/2, press_any_key_to_retry.get_height() + winner_text_game_over.get_height() + 300
            )
        )

        for event in pygame.event.get():
            if event.type == pygame.KEYDOWN:
                self.main()

        pygame.display.update()
        pygame.time.delay(5000)


    def init_window(self, red, green, red_bullets, green_bullets, red_health, green_health):
        self.WINDOW.blit(self.BACKGROUND_IMAGE, (0, 0))
        pygame.draw.rect(self.WINDOW, (0, 0, 0), self.BORDER)

        red_health_text = self.HEALTH_FONT.render("Health: " + str(red_health), 1, (255, 255, 255))
        green_health_text = self.HEALTH_FONT.render("Health: " + str(green_health), 1, (255, 255, 255))
        self.WINDOW.blit(red_health_text, (self.WIDTH - red_health_text.get_width() - 10, 10))
        self.WINDOW.blit(green_health_text, (10, 10))

        self.WINDOW.blit(self.GREEN_SPACESHIP, (green.x, green.y))
        self.WINDOW.blit(self.RED_SPACESHIP, (red.x, red.y))

        for bullet in red_bullets:
            pygame.draw.rect(self.WINDOW, (255, 0, 0), bullet)

        for bullet in green_bullets:
            pygame.draw.rect(self.WINDOW, (255, 255, 0), bullet)

        pygame.display.update()


    def handle_green_movement(self, keys_pressed): 
        if keys_pressed[pygame.K_a] and self.green.x - self.VEL > 0:    # Left key
            self.green.x -= self.VEL

        elif keys_pressed[pygame.K_d] and self.green.x + self.VEL + self.green.width < self.BORDER.x:   # right key
            self.green.x += self.VEL

        elif keys_pressed[pygame.K_w] and self.green.y - self.VEL > 0:  # up
            self.green.y -= self.VEL
            
        elif keys_pressed[pygame.K_s] and self.green.y + self.VEL + self.green.height < self.HEIGHT:  # down
            self.green.y += self.VEL


    def handle_red_movement(self, keys_pressed): 
        if keys_pressed[pygame.K_LEFT] and self.red.x - self.VEL > self.BORDER.x + self.BORDER.width:    # Left key
            self.red.x -= self.VEL

        elif keys_pressed[pygame.K_RIGHT] and self.red.x + self.VEL + self.red.width < self.WIDTH:  # right key
                self.red.x += self.VEL

        elif keys_pressed[pygame.K_UP] and self.red.y - self.VEL > 0:  # up
                self.red.y -= self.VEL
            
        elif keys_pressed[pygame.K_DOWN] and self.red.y + self.VEL + self.red.height < self.HEIGHT:  # down
                self.red.y += self.VEL


    def handle_bullets(self, green_bullets, red_bullets):
        for bullet in green_bullets:
            bullet.x += self.BULLET_VEL
            if self.red.colliderect(bullet):
                pygame.event.post(pygame.event.Event(self.RED_HIT))
                green_bullets.remove(bullet)

            elif bullet.x > self.WIDTH:
                green_bullets.remove(bullet)


        for bullet in red_bullets:
            bullet.x -= self.BULLET_VEL
            if self.green.colliderect(bullet):
                pygame.event.post(pygame.event.Event(self.GREEN_HIT))
                red_bullets.remove(bullet)

            elif bullet.x < 0:
                red_bullets.remove(bullet)


    def main(self):
        self.red = pygame.Rect(700, 300, 60, 60)
        self.green = pygame.Rect(100, 300, 60, 60)

        red_bullets = []
        green_bullets = []

        red_health = 10
        green_health = 10

        clock = pygame.time.Clock()
        running = True
        while running:
            clock.tick(self.FPS)
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    running = False

                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_LCTRL and len(green_bullets) < self.MAX_BULLETS:
                        green_bullets.append(
                            pygame.Rect(
                                self.green.x + self.green.width, self.green.y + self.green.height//2 - 2, 10, 5
                                )
                            )

                    if event.key == pygame.K_RCTRL and len(red_bullets) < self.MAX_BULLETS:
                        red_bullets.append(
                            pygame.Rect(
                                self.red.x, self.red.y + self.red.height//2 - 2, 10, 5
                                )
                            )

                if event.type == self.RED_HIT:
                    red_health -= 1

                if event.type == self.GREEN_HIT:
                    green_health -= 1

            winner_text = ""
            if red_health <= 0:
                winner_text = "Player1 Wins!"

            elif green_health <= 0:
                winner_text = "Player2 Wins!"

            if winner_text != "":
                self.drawWinner(winner_text, None)
                self.main()
            
            keys_pressed = pygame.key.get_pressed()
            self.handle_red_movement(keys_pressed=keys_pressed)
            self.handle_green_movement(keys_pressed=keys_pressed)

            self.handle_bullets(green_bullets, red_bullets)
            self.init_window(self.red, self.green, red_bullets, green_bullets, red_health, green_health)

            # pygame.display.flip()
        
        # self.main()
        pygame.quit()


if __name__ == "__main__":
    GAMEWINDOW = MainWindow()
    GAMEWINDOW.main()