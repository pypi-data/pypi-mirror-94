import os
def create(project_name, project_type):
    os.mkdir(project_name)
    path = os.getcwd()
    os.chdir(path+'\\'+project_name)
    with open("main.py", "w") as file:
        if project_type == "pygame":
            file.write("""from pygame import *

class GameSprite(sprite.Sprite):
    def __init__(self, player_image, player_x, player_y, player_speed):
        super().__init__()
        self.image = transform.scale(image.load(player_image),(65,65))
        self.speed = player_speed
        self.rect = self.image.get_rect()
        self.rect.x = player_x
        self.rect.y = player_y
    def reset(self):
        window.blit(self.image, (self.x, self.y))
        
window = display.set_mode((700,500))
display.set_caption("")
#mixer.init()
#mixer.music.play()
#background = transform.scale(image.load("background.jpg"), (700,500))
clock = time.Clock()
FPS = 60

game = True
while game:
    #window.blit(background, (0,0))
    for e in event.get():
        if e.type == QUIT:
            game = False
    display.update()
    clock.tick(FPS)""")
