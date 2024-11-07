# this allows us to use code from
# the open-source pygame library
# throughout this file

import pygame
from constants import *
from player import *
from asteroid import *
from asteroidfield import AsteroidField
from shot import Shot

def main():
    pygame.init()
    clock = pygame.time.Clock()

    screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
    
    updatable = pygame.sprite.Group()
    drawable = pygame.sprite.Group()
    asteroids = pygame.sprite.Group()
    shots = pygame.sprite.Group()
     
    Player.containers = (updatable, drawable)
    player = Player(SCREEN_WIDTH / 2, SCREEN_HEIGHT / 2) 
    
    Asteroid.containers = (asteroids, updatable, drawable)
    AsteroidField.containers = (updatable)
    asteroidfield = AsteroidField()
    
    Shot.containers = (updatable, drawable, shots)

    dt = 0
    
    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                return
        for updatables in updatable:
            updatables.update(dt)
        
        screen.fill('black')
        
        for drawables in drawable:
            drawables.draw(screen)

        for asteroid in asteroids:
            if asteroid.collisioncheck(player):
                print("Game over!")
                return

        for asteroid in asteroids:
            for shot in shots:
                if asteroid.collisioncheck(shot):
                    shot.kill()
                    asteroid.split()
        pygame.display.flip()
        dt = clock.tick(60)/1000


if __name__ == "__main__":
    main()
