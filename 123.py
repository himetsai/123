import pygame as pg
from pygame.locals import *
import random , os

CREDIT = "2xDx25x2E3"
CURRENTPATH = os.path.dirname(__file__)

class enemy (pg.sprite.Sprite):
    def __init__(self, pos_y):
        super(enemy, self).__init__()
        self.images = []
        self.images.append(pg.transform.scale(pg.image.load("123/1.png"),(int(170*screenRatio), int(170*screenRatio))))
        self.images.append(pg.transform.scale(pg.image.load("123/2.png"),(int(170*screenRatio), int(170*screenRatio))))
        self.image = self.images[0]
        self.image.set_colorkey((255, 255, 255), RLEACCEL)
        self.num = random.randint(1, 3)
        self.pos_x = [0, int(170*screenRatio), int(340*screenRatio)]
        self.rect = self.image.get_rect(topleft=(self.pos_x[self.num - 1], pos_y))
        self.jumpCount = 6
        self.neg = 1
        self.jumpFinish = True

    def check(self, key):
        if self.rect.top == int(680*screenRatio):
            if key == self.num:
                global generate, moveCount
                generate = True
                moveCount += 2
                if self.num == 1:
                    hand1.isSlap = True
                elif self.num == 2:
                    hand2.isSlap = True
                elif self.num == 3:
                    hand3.isSlap = True
                self.kill()
                pg.event.post(scored)
                return True
            elif key in [1, 2, 3] and key != self.num:
                pg.event.post(miss)
        return False

    def update(self):
        self.rect.move_ip(0, int(85*screenRatio))

    def jump(self):
        if self.rect.bottom > int(680*screenRatio):
            if self.jumpCount >= -6:
                self.rect.bottom =int((850 - 1.8 * (36 - (self.jumpCount ** 2))) * screenRatio)
                self.jumpCount -= 1
                pg.event.post(miss)
                self.jumpFinish = False
            else:
                self.jumpCount = 6
                self.jumpFinish = True
            return True
        return False

class hand(pg.sprite.Sprite):
    def __init__(self, pos_x):
        super(hand, self).__init__()
        self.images = []
        self.images.append(pg.transform.scale(pg.image.load("hand/1.png"),(int(91*screenRatio), int(132*screenRatio))))
        self.images.append(pg.transform.scale(pg.image.load("hand/2.png"),(int(126*screenRatio), int(154*screenRatio))))
        self.images.append(pg.transform.scale(pg.image.load("hand/3.png"),(int(139*screenRatio), int(144*screenRatio))))
        self.index = 2
        self.image = self.images[self.index]
        self.image.set_colorkey((255, 255, 255), RLEACCEL)
        self.rect = self.image.get_rect(bottomright=(pos_x, int(1020*screenRatio)))
        self.isSlap = False
        self.count = 0
        self.slapHz = 3

    def update(self):
        self.index += 1
        if self.index >= len(self.images):
            self.index = 0
        self.image = self.images[self.index]

class timer (pg.sprite.Sprite):
    def __init__(self):
        super(timer, self).__init__()
        self.surf = pg.Surface((int(40*screenRatio), int(30*screenRatio)))
        self.rect = self.surf.get_rect(topleft=(0, 0))
        self.font = pg.font.SysFont(fontPath,int(30*screenRatio),True)
        self.timeCount = 20
        self.text = self.font.render("TIME:" + str(self.timeCount), True, (0,0,0))

    def update(self):
        self.timeCount -= 1
        if self.timeCount <= 0:
            self.timeCount = 0
        self.text = self.font.render("TIME:"+str(self.timeCount), True, (0, 0, 0))

class scoreboard (pg.sprite.Sprite):
    def __init__(self):
        super(scoreboard, self).__init__()
        self.surf = pg.Surface((int(40*screenRatio), int(30*screenRatio)))
        self.rect = self.surf.get_rect(topleft=(0, int(30*screenRatio)))
        self.font = pg.font.SysFont(fontPath,int(30*screenRatio),True)
        self.score = 0
        self.text = self.font.render("SCORE:"+str(self.score), True, (0,0,0))

    def update(self):
        self.text = self.font.render("SCORE:"+str(self.score), True, (0, 0, 0))

class endScore(pg.sprite.Sprite):
    def __init__(self,score=0):
        super(endScore, self).__init__()
        self.surf = pg.Surface((int(100*screenRatio), int(100*screenRatio)))
        self.score = score
        self.font = pg.font.SysFont(fontPath, int(73*screenRatio), True)
        self.rect = self.surf.get_rect(center=(int(335*screenRatio), int(295*screenRatio)))
        self.count = 0
        self.images = []
        self.images.append(pg.transform.scale(pg.image.load("bg/endbg1.png"),(int(510*screenRatio), int(1020*screenRatio))))
        self.images.append(pg.transform.scale(pg.image.load("bg/endbg2.png"),(int(510*screenRatio), int(1020*screenRatio))))
        self.image = self.images[self.count]
        self.image.set_colorkey((255, 255, 255), RLEACCEL)
        self.text = self.font.render(str(self.score), True, (0, 0, 0))

    def update(self,score):
        self.count += 1
        self.count %= 2
        if self.count == 0:
            self.text = self.font.render(str(score), True, (0, 0, 0))
        else:
            self.text = self.font.render("", False, (0,0,0))
        self.image = self.images[self.count]

class explosion (pg.sprite.Sprite):
    def __init__(self):
        super(explosion, self).__init__()
        global showingCredit
        self.surf = pg.Surface((int(450*screenRatio), int(641*screenRatio)))
        self.images = []
        self.index = 0
        self.path = os.path.join(CURRENTPATH, "explosion")
        for i in range(1,18):
            self.images.append(pg.transform.scale(pg.image.load(os.path.join(self.path, "%d.png"%i)),(int(400 * screenRatio), int(570 * screenRatio))))
        self.image = self.images[self.index]
        self.image.set_colorkey((255, 255, 255), RLEACCEL)
        self.rect = self.image.get_rect(topleft=(int(55*screenRatio), int(100*screenRatio)))

    def update(self):
        self.index += 1
        if self.index >= len(self.images):
            self.index = 0
        self.image = self.images[self.index]

class ricardo (pg.sprite.Sprite):
    def __init__(self):
        super(ricardo, self).__init__()
        self.surf = pg.Surface((int(450*screenRatio), int(641*screenRatio)))
        self.images = []
        self.index = 0
        for i in range(1,19):
            self.images.append(pg.transform.scale2x(pg.image.load("ricardo/%d.png" % i)))
        self.image = pg.transform.scale(self.images[self.index], (int(self.images[self.index].get_width()*screenRatio),int(self.images[self.index].get_height()*screenRatio)))
        self.image.set_colorkey((255, 255, 255), RLEACCEL)
        self.rect = self.image.get_rect(center=(int(255*screenRatio), int(510*screenRatio)))

    def update(self):
        self.index += 1
        if self.index >= len(self.images):
            pg.event.post(start)
            self.index = 0
        if self.index % 6 == 0:
            pg.event.post(countdown)
        self.image = pg.transform.scale2x(self.images[self.index])
        self.image = pg.transform.scale(self.images[self.index], (
        int(self.images[self.index].get_width() * screenRatio),
        int(self.images[self.index].get_height() * screenRatio)))

class mountainDew (pg.sprite.Sprite):
    def __init__(self):
        super(mountainDew, self).__init__()
        self.images = []
        self.index = 0
        for i in range(1,9):
            self.images.append(pg.image.load("mountaindew/%d.png"%i))
        self.image = pg.transform.scale(self.images[self.index],(int(150*screenRatio), int(150*screenRatio)))
        self.moveSpeed = random.randint(int(30*screenRatio), int(70*screenRatio))
        self.image.set_colorkey((255, 255, 255), RLEACCEL)
        self.rect = self.image.get_rect(center=(random.randint(int(100*screenRatio), int(410*screenRatio)), random.randint(int(100*screenRatio), int(920*screenRatio))))
        self.x_dir = random.choice([1,-1])
        self.y_dir = random.choice([1,-1])

    def update(self):
        self.moveSpeed = random.randint(int(30*screenRatio), int(70*screenRatio))
        self.index += 1
        if self.index >= len(self.images):
            self.index = 0
        self.image = pg.transform.scale(self.images[self.index],(int(150*screenRatio), int(150*screenRatio)))
        self.rect.move_ip(self.x_dir*self.moveSpeed,self.y_dir*self.moveSpeed)
        if self.rect.top <= int(-40*screenRatio):
            self.rect.top = int(-40*screenRatio)
            self.y_dir *= -1
        elif self.rect.bottom >= int(1060*screenRatio):
            self.rect.bottom = int(1060*screenRatio)
            self.y_dir *= -1
        elif self.rect.left <= int(-40*screenRatio):
            self.rect.left = int(-40*screenRatio)
            self.x_dir *= -1
        elif self.rect.right >= int(550*screenRatio):
            self.rect.right = int(550*screenRatio)
            self.x_dir *= -1

class frog (pg.sprite.Sprite):
    def __init__(self, x, isFlip = False):
        super(frog, self).__init__()
        self.surf = pg.Surface((int(201*screenRatio), int(183*screenRatio)))
        self.images = []
        self.index = 0
        self.isFlip = False
        self.isFlip = isFlip
        for i in range(1,11):
            self.images.append(pg.transform.scale(pg.image.load("mlg frog/frogpics/%d.png"%i),(int(210 * screenRatio), int(183 * screenRatio))))
        self.image = pg.transform.flip(self.images[self.index], self.isFlip, False)
        self.image.set_colorkey((255, 255, 255), RLEACCEL)
        self.rect = self.image.get_rect(topleft=(x, int(450*screenRatio)))

    def update(self):
        self.index += 1
        if self.index >= len(self.images):
            self.index = 0
        self.image = pg.transform.flip(self.images[self.index], self.isFlip, False)

class pressSpace (pg.sprite.Sprite):
    def __init__(self):
        super(pressSpace, self).__init__()
        self.surf = pg.Surface((int(450*screenRatio), int(50*screenRatio)))
        self.rect = self.surf.get_rect(topleft=(int(42*screenRatio), int(800*screenRatio)))
        self.font = pg.font.SysFont(fontPath,int(42*screenRatio),True)
        self.count = 0
        self.text = self.font.render("PRESS SPACE TO START", True, (0,0,0))

    def update(self):
        self.count += 11
        self.count %= 2
        if self.count == 0:
            self.text = self.font.render("PRESS SPACE TO START", True, (0,0,0))
        else:
            self.text = self.font.render("", False, (0,0,0))

pg.init()


fontPath = "arial"

width, height = 510, 1020
SCREENSIZE = pg.display.Info()
screenRatio = SCREENSIZE.current_h * 0.9 / height
screen = pg.display.set_mode((int(width*screenRatio), int(height*screenRatio)))
pg.display.set_caption(("打淑麗"))
MISS = pg.USEREVENT + 1
TIME = pg.USEREVENT + 2
SCORE = pg.USEREVENT + 3
START = pg.USEREVENT + 4
COUNTDOWN = pg.USEREVENT + 5
TBCEREND = pg.USEREVENT + 7
SHOWCREDIT = pg.USEREVENT + 8
miss = pg.event.Event(MISS)
playTBC = pg.event.Event(TIME)
scored = pg.event.Event(SCORE)
start = pg.event.Event(START)
countdown = pg.event.Event(COUNTDOWN)
showcredit = pg.event.Event(SHOWCREDIT)

explosion = explosion()
print(explosion.path)
frog1 = frog(0)
frog2 = frog(int(309*screenRatio),True)
mountainDew = mountainDew()
pressSpace = pressSpace()
timer = timer()
scoreboard = scoreboard()
hand1 = hand(int(155*screenRatio))
hand2 = hand(int(325*screenRatio))
hand3 = hand(int(495*screenRatio))
endScore = endScore()
ricardo = ricardo()

startbg = pg.Surface(screen.get_size())
startbg.fill((255,255,255))
startbgHead = pg.transform.scale(pg.image.load("bg/startbg.png"),(int(291*screenRatio), int(494*screenRatio)))
bg = pg.Surface(screen.get_size())
bg = pg.transform.scale(pg.image.load("bg/bg.jpg"),(int(510*screenRatio), int(1020*screenRatio)))
bg = bg.convert()
startbg = startbg.convert()
gameStart = False

boards = pg.sprite.Group()
enemies = pg.sprite.Group()
hands = pg.sprite.Group()
frogs = pg.sprite.Group()
all_sprites = pg.sprite.Group()
boards.add(timer,scoreboard)

hands.add(hand1, hand2, hand3)
frogs.add(frog1,frog2)
all_sprites.add(hand1, hand2, hand3)

pg.mixer.music.set_endevent(TBCEREND)

highscore = open("HighScore.txt", mode="r+")
HighScore = highscore.read()

running = True
while running:
    pg.mixer.music.load("music/begin.mp3")
    newHighScore = False
    pg.event.clear(TBCEREND)
    all_sprites.remove(enemies)
    enemies.empty()
    init_enemy1 = enemy(int(0*screenRatio))
    init_enemy2 = enemy(int(170*screenRatio))
    init_enemy3 = enemy(int(340*screenRatio))
    init_enemy4 = enemy(int(510*screenRatio))
    init_enemy5 = enemy(int(680*screenRatio))
    enemies.add(init_enemy1, init_enemy2, init_enemy3, init_enemy4, init_enemy5)
    all_sprites.add(enemies)
    countdownNums = [3, 2, 1]
    countdownIndex = 0
    creditShow = (255, 255, 255)
    showingCredit = False
    countdownFont = pg.font.SysFont(fontPath, int(170*screenRatio), True)
    creditFont = pg.font.SysFont(fontPath, int(30*screenRatio), True)
    countdownSurface = countdownFont.render(str(countdownNums[countdownIndex]), True, (random.randint(0,255), random.randint(0,255), random.randint(0,255)))
    creditSurface = creditFont.render(CREDIT, True, creditShow)
    gameIsStarted = False
    unlocked = [True, True, True]
    slap = False
    slapIndex = 0
    timeEnd = False
    clock = pg.time.Clock()
    moveCount = 0
    timer.timeCount = 20
    scoreboard.score = 0
    scoreboard.update()
    gameStart = False
    for hand in hands:
        hand.index = 2
    pg.mixer.music.play()

    while not gameIsStarted:
        clock.tick(20)
        for event in pg.event.get():
            if event.type == QUIT:
                highscore.close()
                pg.quit()
                os._exit(0)
            if event.type == KEYDOWN:
                if event.key == K_SPACE:
                    gameIsStarted = True
                    pg.time.set_timer(TIME, 1000)
                    break
                if event.key == K_c:
                    showingCredit = True
        pressSpace.update()
        explosion.update()
        if showingCredit:
            creditSurface = creditFont.render(CREDIT, True, (random.randint(0,255), random.randint(0,255), random.randint(0,255)))
        screen.blit(startbg, (0,0))
        screen.blit(explosion.image,explosion.rect)
        screen.blit(pressSpace.text,pressSpace.rect)
        screen.blit(startbgHead,(int(110*screenRatio),int(110*screenRatio)))
        screen.blit(creditSurface,creditSurface.get_rect(bottomright=(int(500*screenRatio), int(1010*screenRatio))))
        pg.display.flip()

    pg.mixer.music.load("music/TBCER.mp3")

    while not gameStart:
        clock.tick(6)
        for event in pg.event.get():
            if event.type == QUIT:
                highscore.close()
                pg.quit()
                os._exit(0)
            if event.type == START:
                gameStart = True
            if event.type == COUNTDOWN:
                countdownIndex += 1
                if countdownIndex > 2:
                    countdownSurface = countdownFont.render("", True, (random.randint(0,255), random.randint(0,255), random.randint(0,255)))
                    countdownIndex = 0
                else:
                    countdownSurface = countdownFont.render(str(countdownNums[countdownIndex]), True, (random.randint(0,255), random.randint(0,255), random.randint(0,255)))
        ricardo.update()
        screen.blit(bg, (0, 0))
        for entity in hands:
            screen.blit(entity.images[2], entity.rect)
        screen.blit(ricardo.image, ricardo.rect)
        screen.blit(countdownSurface, (int(215*screenRatio),int(170*screenRatio)))
        pg.display.flip()

    while gameIsStarted:
        clock.tick(30)
        num = 0
        generate = False
        for event in pg.event.get():
            if event.type == QUIT:
                highscore.close()
                pg.quit()
                os._exit(0)
            if event.type == KEYUP:
                if event.key == K_1 or event.key == K_KP1:
                    unlocked[0] = True
                elif event.key == K_2 or event.key == K_KP2:
                    unlocked[1] = True
                elif event.key == K_3 or event.key == K_KP3:
                    unlocked[2] = True
            if event.type == MISS:
                for entity in enemies:
                    if entity.jump():
                        entity.image = entity.images[1]
                        if not entity.jumpFinish:
                            unlocked = [False, False, False]
                        else:
                            unlocked = [True, True, True]
                            entity.image = entity.images[0]
            if event.type == TIME:
                if timer.timeCount > 0:
                    timer.update()
                else:
                    gameIsStarted = False
                    timeEnd = True
                if timer.timeCount == 3:
                    pg.event.clear(TBCEREND)
                    pg.mixer.music.play()
            if event.type == SCORE:
                scoreboard.score += 1
                scoreboard.update()

        screen.blit(bg, (0, 0))
        pressed_keys = pg.key.get_pressed()
        if (pressed_keys[K_1] or pressed_keys[K_KP1]) and unlocked[0]:
            num = 1
            unlocked[0] = False
        elif (pressed_keys[K_2] or pressed_keys[K_KP2]) and unlocked[1]:
            num = 2
            unlocked[1] = False
        elif (pressed_keys[K_3] or pressed_keys[K_KP3]) and unlocked[2]:
            num = 3
            unlocked[2] = False
        for entity in enemies:
            if entity.check(num):
                break
        if generate:
            new_enemy = enemy(int(-170*screenRatio))
            enemies.add(new_enemy)
            all_sprites.add(new_enemy)
        if hand1.isSlap:
            if hand1.count % hand1.slapHz == 0:
                hand1.update()
            hand1.count += 1
            if hand1.count >= len(hand1.images) * hand1.slapHz:
                hand1.isSlap = False
                hand1.count = 0
                hand1.index = 2
        if hand2.isSlap:
            if hand2.count % hand2.slapHz == 0:
                hand2.update()
            hand2.count += 1
            if hand2.count >= len(hand2.images) * hand2.slapHz:
                hand2.isSlap = False
                hand2.count = 0
                hand2.index = 2
        if hand3.isSlap:
            if hand3.count % hand3.slapHz == 0:
                hand3.update()
            hand3.count += 1
            if hand3.count >= len(hand3.images) * hand3.slapHz:
                hand3.isSlap = False
                hand3.count = 0
                hand3.index = 2
        if moveCount > 0:
            moveCount -= 1
            enemies.update()

        for entity in all_sprites:
            screen.blit(entity.image, entity.rect)
        for board in boards:
            screen.blit(board.text, board.rect)
        pg.display.flip()

    pg.event.clear(TBCEREND)
    while timeEnd:
        clock.tick(30)
        for event in pg.event.get():
            if event.type == QUIT:
                highscore.close()
                pg.quit()
                os._exit(0)
            if event.type == KEYDOWN:
                if event.key == K_SPACE:
                    timeEnd = False
            if event.type == TBCEREND:
                timeEnd = False
        screen.blit(startbg, (0, 0))
        if scoreboard.score > int(HighScore):
            newHighScore = True
            HighScore = str(scoreboard.score)
            highscore.seek(0)
            highscore.truncate()
            highscore.write(HighScore)
            highscore.seek(0)

        highscoreFont = pg.font.SysFont(fontPath, int(42*screenRatio), True)
        if newHighScore:
            highscoreSurface = highscoreFont.render("NEW HIGHSCORE %s !!!" % HighScore, True, (
                random.randint(0, 255), random.randint(0, 255), random.randint(0, 255)))
            screen.blit(highscoreSurface,(int(43*screenRatio),int(700*screenRatio)))
        else:
            highscoreSurface = highscoreFont.render("HIGHSCORE: %s" % HighScore, True, (0,0,0))
            screen.blit(highscoreSurface,(int(105*screenRatio),int(700*screenRatio)))
        frogs.update()
        mountainDew.update()
        endScore.update(scoreboard.score)
        screen.blit(endScore.image,(0,0))
        if scoreboard.score/100 > 0:
            endScore.rect.left -= int(81*screenRatio)
            screen.blit(endScore.text, endScore.rect)
            endScore.rect.left += int(81*screenRatio)
        elif scoreboard.score == 0:
            endScore.rect.left -= int(55*screenRatio)
            screen.blit(endScore.text, endScore.rect)
            endScore.rect.left += int(55*screenRatio)
        else:
            screen.blit(endScore.text, endScore.rect)
        for frog in frogs:
            screen.blit(frog.image,frog.rect)
        screen.blit(mountainDew.image, mountainDew.rect)
        pg.display.flip()
highscore.close()
pg.quit()
os._exit(0)