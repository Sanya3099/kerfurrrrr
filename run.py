import pygame
import random
import datetime
pygame.init()

font = pygame.font.Font(pygame.font.get_default_font(), 36)
fontEyes = pygame.font.Font(pygame.font.get_default_font(), 140)

screen_width = 800
screen_height = 600
screen = pygame.display.set_mode((screen_width, screen_height))
pygame.display.set_caption("kerfur")

images = []
images.append(pygame.image.load("kerfur-face1.webp"))
images.append(pygame.image.load("kerfur-face2.webp"))
images.append(pygame.image.load("kerfur-face3.webp"))
images.append(pygame.image.load("kerfur-face3b.webp"))
images.append(pygame.image.load("kerfur-face3c.webp"))
images.append(pygame.image.load("kerfur-sleep_a.webp"))
images.append(pygame.image.load("kerfur-sleep_b.webp"))
images.append(pygame.image.load("kerfur-wink-left_b.webp"))
images.append(pygame.image.load("kerfur-wink-right-b.webp"))
sounds = []
sounds.append(pygame.mixer.Sound('kerfur2meow-01.ogg'))
sounds.append(pygame.mixer.Sound('kerfur2meow-02.ogg'))
sounds.append(pygame.mixer.Sound('kerfur2meow-03.ogg'))
sounds.append(pygame.mixer.Sound('VotV-audio-effects-roomwell_on.ogg'))
sounds.append(pygame.mixer.Sound('kerfurEXE.ogg'))

def playSound(sounds_num):
    channel = sounds[sounds_num].play()
    while channel.get_busy():
        pygame.time.delay(100)

def playMeowSound():
    playSound(random.randint(0,2))

def clearScreen():
    # Clear the screen
    screen.fill((0, 0, 0))  # black background

def drawImageOnly(image_num):
    print("current image number", image_num)
    # Get the image's rectangle
    image_rect = images[image_num].get_rect()
    image_rect.center = (screen_width // 2, screen_height // 2)
    # Draw the image
    screen.blit(images[image_num], image_rect)

def drawImage(image_num):
    clearScreen()
    drawImageOnly(image_num)
    # Update the display
    pygame.display.flip()

def drawTextOnly(text):
    text_surface = font.render(text, True, (255,255,255))
    screen.blit(text_surface, (0,0))

def drawTimeOnly():
    current_time = datetime.datetime.now().strftime("%H:%M:%S")
    drawTextOnly(current_time)

def drawEyeText(text1, text2):
    text_surface = fontEyes.render(text1, True, (255,255,255))
    screen.blit(text_surface, text_surface.get_rect(center=(150,310)))
    text_surface = fontEyes.render(text2, True, (255,255,255))
    screen.blit(text_surface, text_surface.get_rect(center=(650,310)))


def drawEyeTextOnly():
    current_time = datetime.datetime.now()
    hour = current_time.strftime("%H")
    minute = current_time.strftime("%M")
    drawEyeText(hour, minute)


def setAlarm(new_hour, new_minute):
    global alarm_time
    now = datetime.datetime.now()
    alarm_time = datetime.datetime.now().replace(hour=new_hour, minute=new_minute, second=0, microsecond=0)
    if alarm_time < now:
        alarm_time += datetime.timedelta(days=1)
        print(f"Alarm set for: {alarm_time.strftime('%H:%M:%S')}")

def setAlarmFromInput():
    new_hour = int(input("Enter hour for alarm: "))
    new_minute = int(input("Enter minute for alarm: "))
    setAlarm(new_hour,new_minute)

def drawTimeSelection(hour, minute):
    text_surface = fontEyes.render(hour, True, (255,255,255))
    screen.blit(text_surface, text_surface.get_rect(center=(150,310)))
    text_surface = fontEyes.render(minute, True, (255,255,255))
    screen.blit(text_surface, text_surface.get_rect(center=(650,310)))




mood = "normal"
running = True
pet = 0

#setAlarm(1,0)
mood = "showAlarm"
alarm_hour = 1
alarm_minute = 0
selected = "hour"

setAlarmFromInput() # sets alarm_time
last_pet_time = datetime.datetime.now()
last_mouse_button_down_time = None

while running:

   # print("mood:", mood, "pet:", pet)
    now = datetime.datetime.now()
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        if event.type == pygame.MOUSEBUTTONDOWN and mood != "showAlarm":
            if event.button == 1:
               mood = "happy"
               pet += 1
               last_pet_time = now
               last_mouse_button_down_time = now
        if event.type == pygame.MOUSEBUTTONUP:
            if event.button == 1:
                last_mouse_button_down_time = None

    if last_mouse_button_down_time is not None:
        if (now - last_mouse_button_down_time).total_seconds() > 3:
            mood = "showAlarm"

    time_since_last_pet = (now - last_pet_time).total_seconds()

    if mood == "normal":
        drawImage(0)
        random_number = random.randint(0,8)
        if random_number == 0:
            mood = "happy"
        else:
            mood = "blinking"
        random_number = random.randint(100,900)
        pygame.time.wait(random_number)
        if time_since_last_pet > 5:
            mood = "sleepy"
            pet = 0
    elif mood == "blinking":
        drawImage(1)
        mood = "normal"
        pygame.time.wait(300)
    elif mood == "happy":
        drawImage(2)
        playMeowSound()
        mood = "normal"
        if pet > 5:
            mood = "wink"
    elif mood == "wink":
        playSound(3)
        drawImage(7)
        pygame.time.wait(1000)
        drawImage(8)
        pygame.time.wait(300)
        pet = 0
        mood = "normal"
    elif mood == "sleepy":
        clearScreen()
        drawImageOnly(1)      #  blit, 
        drawTextOnly("I can't wait to meow with you again!") # just blits

        pygame.display.flip()
        pygame.time.wait(1000)
        drawImage(5)
        pygame.time.wait(1000)
        mood = "sleeping"
    elif mood == "sleeping":
        if now > alarm_time:
            mood = "alarmed"
        elif pet >= 1:
            mood = "normal"
        else:
            clearScreen()
            drawImageOnly(6)      #  blit, 
            drawTimeOnly() # just blits
            pygame.display.flip()
            pygame.time.wait(300)
    elif mood == "alarmed":
        alarm_time += datetime.timedelta(days = 1 )
        clearScreen()
        drawImageOnly(2)   #  blit, 
        drawTimeOnly() # just blits
        pygame.display.flip()
        playSound(4)

    elif mood == "showAlarm":
        clearScreen()
        drawImageOnly(0)
        seconds = pygame.time.get_ticks()
        if (seconds // 500) % 2 == 0:
            drawEyeTextOnly()
        pygame.display.flip()





    else:
        raise Exception("Mood not recognized: " + mood)



# Quit Pygame
pygame.quit()


