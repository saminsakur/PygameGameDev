import pygame
import os


class MainWindow:
    def __init__(self):
        self.WIDTH, self.HEIGHT = 900, 500
        self.WINDOW = pygame.display.set_mode((self.WIDTH, self.HEIGHT))

        self.BORDER = pygame.Rect(self.WIDTH//2-5, 0, 10, self.HEIGHT)
        self.VEL = 5
        self.FPS = 60
        
        self.BACKGROUND_IMAGE = pygame.image.load(os.path.join("Assets", "bg.png"))

        self.SPACESHIP_IMAGE_RED = pygame.image.load(os.path.join("Assets", "red_spaceship.png"))
        self.RED_SPACESHIP = pygame.transform.rotate(pygame.transform.scale(self.SPACESHIP_IMAGE_RED, (60, 60)), 90)

        self.SPACESHIP_IMAGE_GREEN = pygame.image.load(os.path.join("Assets", "green_spaceship.png"))
        self.GREEN_SPACESHIP = pygame.transform.rotate(pygame.transform.scale(self.SPACESHIP_IMAGE_GREEN, (60, 60)), 270)



        pygame.display.set_caption("My cool game")
        pygame.init()


    def init_window(self, red, green):
        self.WINDOW.fill((255, 255, 255))   # WHITE
        self.WINDOW.blit(self.BACKGROUND_IMAGE, (0, 0))

        pygame.draw.rect(self.WINDOW, (0, 0, 0), self.BORDER)
        self.WINDOW.blit(self.GREEN_SPACESHIP, (green.x, green.y))
        self.WINDOW.blit(self.RED_SPACESHIP, (red.x, red.y))

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


    def main(self):
        self.red = pygame.Rect(700, 300, 60, 60)
        self.green = pygame.Rect(100, 300, 60, 60)
        # pygame.Rect()

        clock = pygame.time.Clock()
        running = True
        while running:
            clock.tick(self.FPS)
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    running = False
            
            keys_pressed = pygame.key.get_pressed()
            self.handle_red_movement(keys_pressed=keys_pressed)
            self.handle_green_movement(keys_pressed=keys_pressed)
            self.init_window(self.red, self.green)

        pygame.quit()


if __name__ == "__main__":
    GAMEWINDOW = MainWindow()
    GAMEWINDOW.main()