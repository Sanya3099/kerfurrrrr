import pygame
import random
import datetime
pygame.init()

class HeadGraphics:
    def __init__(self):
        self.font = pygame.font.Font(pygame.font.get_default_font(), 36)
        self.fontEyes = pygame.font.Font(pygame.font.get_default_font(), 140)

        self.screen_width = 800
        self.screen_height = 600
        self.screen = pygame.display.set_mode((self.screen_width, self.screen_height))
        pygame.display.set_caption("kerfur")
        self._loadImageSound()

    def _loadImageSound(self):
        image_files = [
            "kerfur-face1.webp",
            "kerfur-face2.webp",
            "kerfur-face3.webp",
            "kerfur-face3b.webp",
            "kerfur-face3c.webp",
            "kerfur-sleep_a.webp",
            "kerfur-sleep_b.webp",
            "kerfur-wink-left_b.webp",
            "kerfur-wink-right-b.webp",
            "instructions.png"
        ]
        self.images = []
        for filename in image_files:
            self.images.append(pygame.image.load(filename))

        sound_files = [
            'kerfur2meow-01.ogg',
            'kerfur2meow-02.ogg',
            'kerfur2meow-03.ogg',
            'VotV-audio-effects-roomwell_on.ogg',
            'kerfurEXE.ogg',
        ]

        self.sounds = []
        for soundname in sound_files:
            self.sounds.append(pygame.sound.load(soundname))

    def _playSound(self, sounds_num):
        channel = self.sounds[sounds_num].play()
        while channel.get_busy():
            pygame.time.delay(100)

    def playMeowSound(self):
        self._playSound(random.randint(0,2))

    def clearScreen(self):
        # Clear the screen
        self.screen.fill((0, 0, 0))  # black background

    def _drawImageOnly(self,image_num):
    # print("current image number", image_num)
        # Get the image's rectangle
        image_rect = self.images[image_num].get_rect()
        image_rect.center = (self.screen_width // 2, self.screen_height // 2)
        # Draw the image
        self.screen.blit(images[image_num], image_rect)

    def _drawImage(self, image_num):
        self.clearScreen()
        self._drawImageOnly(image_num)
        # Update the display
        pygame.display.flip()

    def drawTextOnly(self, text):
        text_surface = self.font.render(text, True, (255,255,255))
        self.screen.blit(text_surface, (0,0))

    def drawTimeOnly(self):
        current_time = datetime.datetime.now().strftime("%H:%M")
        self.drawTextOnly(current_time + " Alarm Time is " + alarm_time.strftime("%H:%M"))

    def drawEyeText(self, text1, text2):
        text_surface = self.fontEyes.render(text1, True, (255,255,255))
        self.screen.blit(text_surface, text_surface.get_rect(center=(150,310)))
        text_surface = self.fontEyes.render(text2, True, (255,255,255))
        self.screen.blit(text_surface, text_surface.get_rect(center=(650,310)))


    def drawEyeTextOnly(self):
        self.drawEyeText(f'{alarm_hour:02}',f'{alarm_minute:02}')

    def drawTimeSelection(self, hour, minute):
        text_surface = self.fontEyes.render(hour, True, (255,255,255))
        self.screen.blit(text_surface, text_surface.get_rect(center=(150,310)))
        text_surface = self.fontEyes.render(minute, True, (255,255,255))
        self.screen.blit(text_surface, text_surface.get_rect(center=(650,310)))


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


def run():
    headGraphics = HeadGraphics()
    mood = "instructions"
    running = True
    pet = 0
    alarm_hour = 1
    alarm_minute = 23

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
            headGraphics._drawImage(9)
            if pet >= 1:
                mood = "normal"
        elif mood == "normal":
            headGraphics._drawImage(0)
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
            headGraphics._drawImage(1)
            mood = "normal"
            pygame.time.wait(300)
        elif mood == "happy":
            headGraphics._drawImage(2)
            headGraphics.playMeowSound()
            mood = "normal"
            if pet > 5:
                mood = "wink"
        elif mood == "wink":
            headGraphics._drawImage(7)
            headGraphics._playSound(3)
            pygame.time.wait(100)
            headGraphics._drawImage(8)
            pygame.time.wait(300)
            pet = 0
            mood = "normal"
        elif mood == "sleepy":
            headGraphics.clearScreen()
            headGraphics._drawImageOnly(1)      #  blit, 
            headGraphics.drawTextOnly("I can't wait to meow with you again!") # just blits

            pygame.display.flip()
            pygame.time.wait(1000)
            headGraphics._drawImage(5)
            pygame.time.wait(1000)
            mood = "sleeping"
        elif mood == "sleeping":
            if now > alarm_time:
                mood = "alarmed"
            elif pet >= 1:
                mood = "normal"
            else:
                headGraphics.clearScreen()
                headGraphics._drawImageOnly(6)      #  blit, 
                headGraphics.drawTimeOnly() # just blits
                pygame.display.flip()
                pygame.time.wait(300)
        elif mood == "alarmed":
            alarm_time += datetime.timedelta(days = 1 )
            headGraphics.clearScreen()
            headGraphics._drawImageOnly(2)   #  blit, 
            headGraphics.drawTimeOnly() # just blits
            pygame.display.flip()
            headGraphics._playSound(4)

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

            headGraphics.clearScreen()
            headGraphics.drawImageOnly(0)
            seconds = pygame.time.get_ticks()
            if (seconds // 300) % 2 == 0:
                headGraphics.drawEyeTextOnly()
            pygame.display.flip()
        else:
            raise Exception("Mood not recognized: " + mood)


run()
# Quit Pygame
pygame.quit()
