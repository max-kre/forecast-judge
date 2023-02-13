import pygame

DURATION = 20

class Explosion(pygame.sprite.Sprite):
    def __init__(self, pos, image, groups) -> None:
        super().__init__(groups)
        self.image = image
        self.rect = self.image.get_rect(center=pos)
        self.startTime = pygame.time.get_ticks()

    def check_timeout(self):
        if pygame.time.get_ticks() > self.startTime + DURATION:
            self.kill()

    def update(self):
        self.check_timeout()
    