



# Importing the library
import pygame
import random
import time

import sys
 
# Initializing Pygame

clock = pygame.time.Clock()

def main():
    
    gameObject = gameClass(640,800,60)

    while True: 
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()

        
        
        gameObject.checkKeyPress()
        if gameObject.isLost():
            gameObject.drawLose()
            pygame.display.update()
            clock.tick(10)
            continue

        gameObject.moveAllEnemiesDown()

        gameObject.drawSurface()
        gameObject.drawScore()
        gameObject.drawPlayer()
        gameObject.drawEnemies()

        gameObject.spawnEnemies()
        
        gameObject.checkEnemyCollision()
        gameObject.checkIfAnyDodgedEnemies()                    

        pygame.display.update()
        gameObject.incCounter()
        gameObject.limitFps()
        

def checkCollision(player, enemy):
    if pygame.Rect.colliderect(player, enemy):
        return True

class actor:
    def __init__(self, startingPositionX, startingPositionY, movespeed):
        self.posX=startingPositionX
        self.posY=startingPositionY
        self.movespeed=movespeed
        self.width = 60
        self.height = 60
        self.color = (0,0,0)
        self.image = None
        self.rect = pygame.Rect(self.posX, self.posY, self.width, self.height)

    def getX(self):
        return self.posX
    
    def getY(self):
        return self.posY
    
    def getX2(self):
        return self.posX+self.width
    
    def getY2(self):
        return self.posY+self.height

    def getWidth(self):
        return self.width
    
    def getHeight(self):
        return self.height
    
    def getMoveSpeed(self):
        return self.movespeed

    def setMoveSpeed(self, speed):
        self.movespeed = speed

    def getColor(self):
        return self.color
    
    def setColor(self, colorValue):
        self.color = colorValue
    
    def setX(self, x):
        self.posX=x

    def setY(self, y):
        self.posY=y

    def moveLeft(self):
        self.posX -= self.movespeed

    def moveRight(self):
        self.posX += self.movespeed

    def moveUp(self):
        self.posY -= self.movespeed

    def moveDown(self):
        self.posY += self.movespeed  

    def getRect(self):
        return self.rect
    
    def setRect(self, rect):
        self.rect = rect

    def setImage(self, image):
        self.image = image

class gameClass:
    def __init__(self, windowWidth, windowHeight, fps):
        pygame.init()
        pygame.mixer.init()
        pygame.mixer.music.load("assets/sounds/L80ETC.mp3")
        pygame.mixer.music.set_volume(0.7)
        pygame.mixer.music.play()
        self.windowWidth = windowWidth
        self.windowHeight = windowHeight
        self.fps = fps
        self.font = pygame.font.Font('freesansbold.ttf', 32)
        self.score=0
        self.scoreCounter = self.font.render('Score: ' + str(self.score), True, (255,255,255), (0,0,0))
        self.scoreRect = self.scoreCounter.get_rect()
        self.scoreRect.center = (80,30)
        self.surface = pygame.display.set_mode((windowWidth,windowHeight))
        self.background = pygame.image.load("assets/images/bliss.png").convert()
        self.loseScreen = pygame.image.load("assets/images/wasted.png").convert_alpha()
        self.stoneWall = pygame.image.load("assets/images/stoneWall.png").convert()
        self.bomb = pygame.image.load("assets/images/bomb.png").convert_alpha()
        self.explosions = []
        self.bgColor = (0,0,0)
        self.player = actor(windowWidth/2, windowHeight-120, 7)
        self.player.setColor((255,0,0))
        self.nmOfEnemies=10
        self.enemies = []
        self.gameloopDelaySpawn = 280
        self.gameloopCounter = 0
        self.gameLose = False

    def spawnEnemies(self):
        if len(self.enemies) <= self.nmOfEnemies and self.gameloopCounter >= self.gameloopDelaySpawn:
            newActor = actor(0,-60,random.randint(3,15))
            newActor.setX(random.randint(0, self.windowWidth - newActor.getWidth()))
            newActor.setColor((255,255,0))
            self.enemies.append(newActor)
            self.randomDelay()
            self.gameloopCounter=0

    def drawSurface(self):
        self.surface.blit(self.background, (0,0))
        self.surface.blit(self.stoneWall, (0, self.windowHeight-40))


    def drawActor(self, actor):
        return pygame.draw.rect(self.surface, actor.color, pygame.Rect(actor.getX(), actor.getY(), actor.getWidth(), actor.getHeight()))
    
    def drawScore(self):
        self.scoreCounter = self.font.render('Score: ' + str(self.score), True, (255,255,255), (0,0,0))
        self.surface.blit(self.scoreCounter, self.scoreRect)

    def drawLose(self):
        self.surface.blit(self.loseScreen, ((self.windowWidth/2)-(self.loseScreen.get_width()/2), (self.windowHeight/2)-(self.loseScreen.get_height()/2)))

    def drawExplosions(self):
        for exp in self.explosions:
            explosion = exp.img.copy()
            self.surface.blit(explosion, (exp.getX(), exp.getY()))

    def checkKeyPress(self):
        keys = pygame.key.get_pressed()

        if keys[pygame.K_a] and not self.isLost():
            self.moveActorLeft(self.player)

        if keys[pygame.K_d] and not self.isLost():
            self.moveActorRight(self.player)

        if keys[pygame.K_RETURN]:
            self.resetGame()            
    
    def loseGame(self):
        pygame.mixer.music.stop()
        pygame.mixer.music.load("assets/sounds/gta5wasted.mp3")
        pygame.mixer.music.play()
        self.gameLose = True

    def isLost(self):
        return self.gameLose
    
    def resetGame(self):
        self.score=0
        self.scoreCounter = self.drawScore()
        self.gameloopCounter=0
        self.gameloopDelaySpawn = 280
        self.gameLose=False
        pygame.mixer.music.stop()
        pygame.mixer.music.load("assets/sounds/L80ETC.mp3")
        pygame.mixer.music.play()
        for enemy in self.enemies:
            self.enemies.remove(enemy)
    
    def moveActorLeft(self, actor):
        if actor.getX() > 0:
            actor.moveLeft()

    def moveActorRight(self, actor):
        if actor.getX() < self.windowWidth-actor.getWidth()-5:
            actor.moveRight()

    def moveActorUp(self, actor):
        if actor.getY() > 0:
            actor.moveUp()

    def moveActorDown(self, actor):
        if actor.getY() <= self.windowHeight:
            actor.moveDown()

    def moveAllEnemiesDown(self):
        for enemy in self.enemies:
            enemy.moveDown()

    def drawPlayer(self):
        self.drawActor(self.player)

    def drawEnemies(self):
        for enemy in self.enemies:
            enemy.setRect(pygame.draw.rect(self.surface, enemy.getColor(), pygame.Rect(enemy.getX(), enemy.getY(), enemy.getWidth(), enemy.getHeight())))

    def checkCollision(actor1, actor2):
        if actor1.getX() < actor2.getX2() and actor1.getX2() > actor2.getX() and actor1.getY() < actor2.getY2() and actor1.getY2() > actor2.getY():
            return True

    def checkEnemyCollision(self):
        for enemy in self.enemies:
            if gameClass.checkCollision(self.player, enemy):
                self.loseGame()
            for otherEnemy in self.enemies:
                if otherEnemy != enemy:
                    if gameClass.checkCollision(enemy, otherEnemy):
                        enemySpeed = enemy.getMoveSpeed()
                        otherEnemySpeed = otherEnemy.getMoveSpeed()
                        speedDiff = abs(enemySpeed - otherEnemySpeed)
                        if enemySpeed > otherEnemySpeed and enemy.getY() < otherEnemy.getY():
                            enemy.setMoveSpeed(enemySpeed - speedDiff)
                            otherEnemy.setMoveSpeed(otherEnemySpeed + speedDiff)
                        elif otherEnemySpeed > enemySpeed and enemy.getY() > otherEnemy.getY():
                            otherEnemy.setMoveSpeed(otherEnemySpeed - speedDiff)
                            enemy.setMoveSpeed(enemySpeed + speedDiff)

    def checkIfAnyDodgedEnemies(self):
        for exp in self.explosions:
            exp.decDuration()
            if exp.getDuration() <= 0:
                self.explosions.remove(exp)

        for enemy in self.enemies:
            if enemy.getY() > self.windowHeight-enemy.getHeight()-40:
                self.enemies.remove(enemy)
                self.score+=1
                self.explosions.append(explosion(enemy.getX(), self.windowHeight-140))

        self.drawExplosions()

    def incCounter(self):
        self.gameloopCounter+=1

    def limitFps(self):
        clock.tick(self.fps)

    def randomDelay(self):
        self.gameloopDelaySpawn = random.randint(5,40)

class explosion:
    def __init__(self, x, y) -> None:
        self.x = x
        self.y = y
        self.img = pygame.image.load("assets/images/explosion.png").convert_alpha()
        self.lingerDuration = 5

    def decDuration(self): 
        self.lingerDuration-=1

    def getDuration(self):
        return self.lingerDuration
    
    def getX(self):
        return self.x
    
    def getY(self):
        return self.y
    

main()