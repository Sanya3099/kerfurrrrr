import pygame
import random
import datetime
pygame.init()

def setupDisplay():
    global font, fontEyes, screen_height, screen_width, screen
    font = pygame.font.Font(pygame.font.get_default_font(), 36)
    fontEyes = pygame.font.Font(pygame.font.get_default_font(), 140)

    screen_width = 800
    screen_height = 600
    screen = pygame.display.set_mode((screen_width, screen_height))
    pygame.display.set_caption("kerfur")

def loadImageSound():
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
    images.append(pygame.image.load("instructions.png"))

    sounds = []
    sounds.append(pygame.mixer.Sound('kerfur2meow-01.ogg'))
    sounds.append(pygame.mixer.Sound('kerfur2meow-02.ogg'))
    sounds.append(pygame.mixer.Sound('kerfur2meow-03.ogg'))
    sounds.append(pygame.mixer.Sound('VotV-audio-effects-roomwell_on.ogg'))
    sounds.append(pygame.mixer.Sound('kerfurEXE.ogg'))
    return images, sounds

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
   # print("current image number", image_num)
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
    current_time = datetime.datetime.now().strftime("%H:%M")
    drawTextOnly(current_time + " Alarm Time is " + alarm_time.strftime("%H:%M"))

def drawEyeText(text1, text2):
    text_surface = fontEyes.render(text1, True, (255,255,255))
    screen.blit(text_surface, text_surface.get_rect(center=(150,310)))
    text_surface = fontEyes.render(text2, True, (255,255,255))
    screen.blit(text_surface, text_surface.get_rect(center=(650,310)))


def drawEyeTextOnly():
    drawEyeText(f'{alarm_hour:02}',f'{alarm_minute:02}')

def setAlarm(new_hour, new_minute):
    """
    takes in new hour and minute and sets the variables alarm_time, alarm_hour and alarm_minute.
    """
    global alarm_time, alarm_hour, alarm_minute
    alarm_hour = new_hour
    alarm_minute = new_minute

    now = datetime.datetime.now()
    alarm_time = datetime.datetime.now().replace(hour=new_hour, minute=new_minute, second=0, microsecond=0)
    if alarm_time < now:
        alarm_time += datetime.timedelta(days=1)
    print(f"Alarm set for: {alarm_time.strftime('%H:%M:%S')}")

def drawTimeSelection(hour, minute):
    text_surface = fontEyes.render(hour, True, (255,255,255))
    screen.blit(text_surface, text_surface.get_rect(center=(150,310)))
    text_surface = fontEyes.render(minute, True, (255,255,255))
    screen.blit(text_surface, text_surface.get_rect(center=(650,310)))

def run():
    mood = "instructions"
    running = True
    pet = 0

    #setAlarm(1,0)
    #mood = "showAlarm"
    alarm_hour = 1
    alarm_minute = 23
    selected = "hour"

    setAlarm(8,30)
    last_pet_time = datetime.datetime.now()
    last_mouse_button_down_time = None

    while running:
        mouse_touch_y = mouse_touch_x = None
        now = datetime.datetime.now()
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            if event.type == pygame.MOUSEBUTTONDOWN:
                if event.button == 1:
                    last_mouse_button_down_time = now
                    if  mood != "showAlarm":
                        mood = "happy"
                        pet += 1
                        last_pet_time = now
                    else:
                        mouse_touch_x, mouse_touch_y = event.pos
            if event.type == pygame.MOUSEBUTTONUP:
                if event.button == 1:
                    last_mouse_button_down_time = None

        if last_mouse_button_down_time is not None:
            if (now - last_mouse_button_down_time).total_seconds() > 3:
                mood = "showAlarm"

        time_since_last_pet = (now - last_pet_time).total_seconds()
        
        if mood == "instructions":
            drawImage(9)
            if pet >= 1:
                mood = "normal"
        elif mood == "normal":
            drawImage(0)
            random_number = random.randint(0,100)
            if random_number == 0:
                mood = "happy"
            elif random_number < 20:
                mood = "blinking"
            random_number = random.randint(100,500)
            pygame.time.wait(random_number)
            if time_since_last_pet > 60:
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
            drawImage(7)
            playSound(3)
            pygame.time.wait(100)
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
            # See if the user is touching the eyes or nose
            if mouse_touch_x != None:
                print(mouse_touch_x, mouse_touch_y)
                if mouse_touch_y >= 150:
                    if mouse_touch_x <= 316:
                        setAlarm((alarm_hour+1) % 24, alarm_minute)
                    elif mouse_touch_x >= 450:
                        setAlarm(alarm_hour, (alarm_minute+10) % 60 )
                    elif mouse_touch_y >= 340:
                        if mouse_touch_x >320 and mouse_touch_x <490:
                            mood = "wink"

            clearScreen()
            drawImageOnly(0)
            seconds = pygame.time.get_ticks()
            if (seconds // 300) % 2 == 0:
                drawEyeTextOnly()
            pygame.display.flip()
        else:
            raise Exception("Mood not recognized: " + mood)


setupDisplay()
images, sounds = loadImageSound()
run()
# Quit Pygame
pygame.quit()


