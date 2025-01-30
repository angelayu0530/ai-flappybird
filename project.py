import pygame
import neat
import random
import time
import os

# stderr to /dev/null
f = open("/dev/null", "w")
os.dup2(f.fileno(), 2)
f.close()


# Window dimensions
WIN_WIDTH = 600
WIN_HEIGHT = 800

# Load images
BIRD_IMGS = [
    pygame.transform.scale2x(pygame.image.load(os.path.join("imgs", "bird1.png"))),
    pygame.transform.scale2x(pygame.image.load(os.path.join("imgs", "bird2.png"))),
    pygame.transform.scale2x(pygame.image.load(os.path.join("imgs", "bird3.png")))
]
PIPE_IMG = pygame.transform.scale2x(pygame.image.load(os.path.join("imgs", "pipe.png")))
BASE_IMG = pygame.transform.scale2x(pygame.image.load(os.path.join("imgs", "base.png")))
BG_IMG = pygame.transform.scale2x(pygame.image.load(os.path.join("imgs", "bg.png")))

# Bird class
class Bird:
    IMGS = BIRD_IMGS
    MAX_ROTATION = 25
    ROT_VEL = 20
    ANIMATION_TIME = 5

    def __init__(self, x, y):
        self.x = x
        self.y = y
        self.tilt = 0  # Angle of the bird
        self.tick_count = 0  # To track when the bird last jumped
        self.vel = 0  # Current velocity
        self.height = self.y  # Starting height of the bird
        self.img_count = 0  # For handling the animation loop
        self.img = self.IMGS[0]  # Set the initial image of the bird

    def jump(self):
        self.vel = -10.5  # Velocity to move upwards
        self.tick_count = 0  # Reset tick count
        self.height = self.y  # Track the height at the start of the jump

    def move(self):
        self.tick_count += 1  # Increment the tick count since the last jump
        # Calculate displacement using velocity and acceleration
        d = self.vel * self.tick_count + 1.5 * self.tick_count**2

        if d >= 16:  # Terminal velocity downward
            d = 16
        if d < 0:  # Moving upwards
            d -= 2

        self.y = self.y + d  # Update the bird's position

        # Adjust tilt based on movement direction
        if d < 0 or self.y < self.height + 50:  # Moving upwards or tracking jumps
            if self.tilt < self.MAX_ROTATION:
                self.tilt = self.MAX_ROTATION
        else:  # Moving downwards
            if self.tilt > -90:
                self.tilt -= self.ROT_VEL

    def draw(self, win):
        self.img_count += 1  # Increment the image counter for animation

        # Cycle through bird images for flapping animation
        if self.img_count < self.ANIMATION_TIME:  # Less than 5 displays the first bird image
            self.img = self.IMGS[0]
        elif self.img_count < self.ANIMATION_TIME * 2:  # Item count less than 10 shows the next one
            self.img = self.IMGS[1]
        elif self.img_count < self.ANIMATION_TIME * 3:  # Less than 15 shows the last image
            self.img = self.IMGS[2]
        elif self.img_count < self.ANIMATION_TIME * 4:  # Less than 20 shows the second image since it is going down
            self.img = self.IMGS[1]
        elif self.img_count < self.ANIMATION_TIME * 4 + 1:  # Less than 21 shows the first image
            self.img = self.IMGS[0]
            self.img_count = 0  # Reset animation counter

        # Adjust image if bird is tilting downward
        if self.tilt <= -80:
            self.img = self.IMGS[1]
            self.img_count = self.ANIMATION_TIME * 2  # Maintain the second image

        # Rotate the bird image based on its tilt
        rotated_image = pygame.transform.rotate(self.img, self.tilt)
        # Adjust the rotated image's position to stay centered
        new_rect = rotated_image.get_rect(center=self.img.get_rect(topleft=(self.x, self.y)).center)
        win.blit(rotated_image, new_rect.topleft)  # Draw the rotated image

    def get_mask(self):
        # Get a mask for pixel-perfect collision detection
        return pygame.mask.from_surface(self.img)
class Pipe:
    Gap = 200
    VEL =5
    def __init__(self,x):
        self.x = x

# Function to draw the game window
def draw_window(win, bird):
    win.blit(BG_IMG, (0, 0))  # Draw the background
    bird.draw(win)  # Draw the bird
    pygame.display.update()  # Update the display


def main():
    bird = Bird(200, 200)  # Create a bird instance
    win = pygame.display.set_mode((WIN_WIDTH, WIN_HEIGHT))  # Create the game window
    run = True  # Game loop control variable

    while run:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:  # Quit the game if the window is closed
                run = False

        draw_window(win,bird)  
main ()
        
        
            

 
    