import pygame
pygame.init()

screen_width = 800
screen_height = 600
screen = pygame.display.set_mode((screen_width, screen_height))
pygame.display.set_caption("kerfur")

images = []
images.append(pygame.image.load("kerfur-face1.webp"))
images.append(pygame.image.load("kerfur-face2.webp"))
images.append(pygame.image.load("kerfur-face3.webp"))
images.append(pygame.image.load("kerfur-face4.webp"))
images.append(pygame.image.load("kerfur-face5.webp"))
images.append(pygame.image.load("kerfur-face6.webp"))

def drawImage(image_num):
    # Get the image's rectangle
    image_rect = images[image_num].get_rect()
    image_rect.center = (screen_width // 2, screen_height // 2)
      # Clear the screen
    screen.fill((0, 0, 0))  # black background
     # Draw the image
    screen.blit(images[image_num], image_rect)
    # Update the display
    pygame.display.flip()

mood = "normal"


# Game loop
running = True
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    if mood == "normal":
        drawImage(0)
        mood = "blinking"
        pygame.time.wait(1000)
    elif mood == "blinking":
        drawImage(1)
        mood = "normal"
        pygame.time.wait(300)

# Quit Pygame
pygame.quit()


