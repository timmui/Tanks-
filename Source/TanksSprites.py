import math

import pygame


class Player(pygame.sprite.Sprite):
    '''The tank that will be controlled by the user.'''

    def __init__(self, position):
        ''' The initializer method for the player sprite. This method
        takes the following parameters:
        
        position -Position of sprite  
        '''
        # Call the parent __init__() method
        pygame.sprite.Sprite.__init__(self)

        # Loading the images
        # Right - 0|Left - 1|Up - 2|Down -3
        self.__images = []
        for direction in ['Right', 'Left', 'Up', 'Down']:
            current = []
            for image in range(1, 8):
                name = ('./Resources/Player/%s/' % direction) + str(image) + '.png'
                tempImage = pygame.image.load(name)
                current.append(tempImage)
            self.__images.append(current)

        # Loading Explosion images
        self.__explosions = []
        for num in range(1, 24):
            self.__explosions.append(pygame.image.load(
                './Resources/Explosion/%d.png' % num))

        self.image = self.__images[0][0]
        self.rect = self.image.get_rect()
        self.rect.center = position

        # Instance Variables
        self.__position = position
        self.__speed = 2

        self.__left = 0
        self.__right = 0
        self.__up = 0
        self.__down = 0

        self.__frames = 0
        self.__counter = 0
        self.__exploding = False

        self.__colliding = False

    def move(self, direction, walls):
        '''
        Moves the player sprite towards a certain direction and __speed. Changes
        image of the sprite to reflect how it is moving. 

        It takes a direction and a list of all walls as a parameter.
        '''
        # Checks if the player is exploding
        if self.__exploding == False:

            # Checking if there is collision with wall then moving
            if direction == 'left':
                self.rect.left -= self.__speed

                if self.__left <= 6:
                    self.image = self.__images[1][self.__left]
                    self.__left += 1
                else:
                    self.__left = 0

                for wall in walls:
                    if self.rect.colliderect(wall.rect):
                        # Moving left; Hit the right side of the wall
                        self.rect.left = wall.rect.right

            elif direction == 'right':
                self.rect.left += self.__speed

                if self.__right <= 6:
                    self.image = self.__images[0][self.__right]
                    self.__right += 1
                else:
                    self.__right = 0

                for wall in walls:
                    if self.rect.colliderect(wall.rect):
                        # Moving right; Hit the left side of the wall
                        self.rect.right = wall.rect.left

            elif direction == 'up':
                self.rect.top -= self.__speed

                if self.__up <= 6:
                    self.image = self.__images[2][self.__up]
                    self.__up += 1
                else:
                    self.__up = 0

                for wall in walls:
                    if self.rect.colliderect(wall.rect):
                        # Moving up; Hit the bottom side of the wall
                        self.rect.top = wall.rect.bottom

            elif direction == 'down':
                self.rect.top += self.__speed

                if self.__down <= 6:
                    self.image = self.__images[3][self.__down]
                    self.__down += 1
                else:
                    self.__down = 0

                for wall in walls:
                    if self.rect.colliderect(wall.rect):
                        # Moving down; Hit the top side of the wall
                        self.rect.bottom = wall.rect.top

    def get_pos(self):
        '''
        Returns the current position of the player tank sprite.
        '''
        return self.rect.center

    def update(self):
        '''
        Update method for player. Calls explosion if exploding.
        '''
        if self.__exploding:
            self.explosion()

    def explosion(self):
        '''
        Sets the image of the sprite as an animated explosion
        '''
        self.__exploding = True
        self.__position = self.rect.center

        if self.__counter <= 22:
            self.image = self.__explosions[self.__counter]
            self.rect = self.image.get_rect()
            self.rect.center = self.__position
        else:
            self.kill()

        self.__counter += 1

    def get_colliding(self):
        '''
        Returns if the sprite is colliding or not
        '''
        return self.__colliding

    def set_colliding(self, colliding):
        '''
        Sets if the sprite is colliding or not
        '''
        self.__colliding = colliding


class Bullet(pygame.sprite.Sprite):
    '''The bullet sprite for either the Enemy or the Player tank.'''

    def __init__(self, position, target, player, image):
        ''' The initializer method for the bullet sprite. This method
        takes the following parameters:
        
        position - Position of sprite  
        target - Target destination of bullet
        player - The player that shot the bullet
        image - The image of the bullet
        '''
        # Call the parent __init__() method
        pygame.sprite.Sprite.__init__(self)

        # Loading the image
        self.image = image
        self.rect = self.image.get_rect()
        self.rect.center = position

        # Loading Explosion images
        self.__explosions = []
        for num in range(1, 24):
            self.__explosions.append(pygame.image.load(
                './Resources/Explosion/%d.png' % num))

        # Instance Variables

        self.__target = target
        self.__speed = 0.02
        self.__origin = position

        # Calculating the trajectory of the bullet
        self.__trajectory = [self.__speed * (self.__target[0] - self.rect.centerx
            ), self.__speed * (self.__target[1] -
                               self.rect.centery)]

        self.__frames = 0
        self.__counter = 0
        self.__exploding = False

        self.__time = 0
        self.__shot = False
        self.__player = player

        self.__colliding = False

    def update(self):
        '''
        Refreshes the position of the bullet moving towards the target. Sets 
        explosion if appropriate.
        '''
        self.__time += 1

        if self.__exploding == False:
            if self.__time > 30:
                self.__shot = True

            self.rect.move_ip(self.__trajectory)

            if self.rect.left < 0 or self.rect.right > 640 or self.rect.top < \
                    64 or self.rect.bottom > 480:
                # the missile went off the screen without hitting anything
                self.kill()
        else:
            self.explosion()

    def explosion(self):
        '''
        Sets the image of the sprite as an animated explosion
        '''
        self.__exploding = True
        position = self.rect.center
        if self.__counter <= (22):
            self.image = self.__explosions[self.__counter]
            self.rect = self.image.get_rect()
            self.rect.center = position
        else:
            self.kill()

        self.__counter += 1

    def get_shot(self):
        '''
        Returns the value of __shot and __player
        '''
        return self.__shot, self.__player

    def set_colliding(self, colliding):
        '''
        Sets if the sprite is colliding or not
        '''
        self.__colliding = colliding

    def get_colliding(self):
        '''
        Returns if the sprite is colliding or not
        '''
        return self.__colliding


class Mine(pygame.sprite.Sprite):
    '''The mine sprite for either the Player or Enemy tank.'''

    def __init__(self, player):
        ''' The initializer method for the mine sprite. This method
        takes the following parameters:
        
        player - Identifies if the player or the enemy drops the mine.
        '''
        # Call the parent __init__() method
        pygame.sprite.Sprite.__init__(self)

        # Loading the image
        if player:
            self.image = pygame.image.load('./Resources/Mines/Player.png')
        else:
            self.image = pygame.image.load('./Resources/Mines/Enemy.png')

        self.rect = self.image.get_rect()
        self.rect.center = (700, 700)

        # Loading Explosion images
        self.__explosions = []
        for num in range(1, 24):
            self.__explosions.append(pygame.image.load(
                './Resources/Explosion/%d.png' % num))

        # Instance Variables
        self.__position = (700, 700)
        self.__frames = 0
        self.__time = 5
        self.__counter = 0
        self.__start = 0
        self.__exploding = False
        self.__colliding = False

    def update(self):
        '''
        Calls the explosion() method when __time has elapsed
        '''
        if self.__start:
            self.__frames += 1

            if self.__frames >= (30 * self.__time):
                self.explosion()

        if self.__exploding:
            self.explosion()

    def explosion(self):
        '''
        Changes the image of the mine to animate explosion
        '''
        self.__exploding = True

        if self.__counter <= (22):
            self.image = self.__explosions[self.__counter]
            self.rect = self.image.get_rect()

            self.rect.center = self.__position
        else:
            self.kill()

        self.__counter += 1

    def start(self, position):
        '''
        Initiates the mine at the inputted position. Also starts 'fuse'(__start)
        to explode the bomb after a set period of time.
        '''
        self.__start = 1
        self.rect.center = position
        self.__position = position

    def get_exploding(self):
        '''
        Returns if the mine is exploding or not.
        '''
        return self.__exploding

    def set_colliding(self, colliding):
        '''
        Sets the mine as colliding with another sprite or not with the boolean
        parameter, colliding
        '''
        self.__colliding = colliding

    def get_colliding(self):
        '''
        Returns if the mine is colliding or not.
        '''
        return self.__colliding


class Crosshair(pygame.sprite.Sprite):
    '''The crosshair sprite for the Player.'''

    def __init__(self):
        ''' The initializer method for the crosshair sprite. This method
        takes no parameters.
        '''
        # Call the parent __init__() method
        pygame.sprite.Sprite.__init__(self)

        # Loading the image
        self.image = pygame.image.load('./Resources/crosshairInit.png')

        # self.image = self.image.convert ()
        self.rect = self.image.get_rect()
        self.image = pygame.image.load('./Resources/crosshair.png')

        self.set_position((320, 272))

    def get_position(self):
        '''
        Returns the current position of the crosshair.
        '''
        return self.rect.center

    def set_position(self, position):
        '''
        Updates center of the crosshair as the position of the mouse.
        '''
        self.rect.center = position


class Enemy(pygame.sprite.Sprite):
    '''The enemy tank sprite.'''

    def __init__(self, position):
        ''' The initializer method for the enemy sprite. This method
        takes the following parameters:
        
        position - Position of sprite  
        '''
        # Call the parent __init__() method
        pygame.sprite.Sprite.__init__(self)

        # Loading the images
        # Right - 0|Left - 1|Up - 2|Down -3
        self.__images = []
        for direction in ['Right', 'Left', 'Up', 'Down']:
            current = []
            for image in range(1, 8):
                name = ('./Resources/Enemy/%s/' % direction) + str(image) + '.png'
                tempImage = pygame.image.load(name)
                current.append(tempImage)
            self.__images.append(current)
        # Loading Explosion images
        self.__explosions = []
        for num in range(1, 24):
            self.__explosions.append(pygame.image.load(
                './Resources/Explosion/%d.png' % num))

        self.image = self.__images[1][0]
        self.rect = self.image.get_rect()
        self.rect.center = position

        # Instance Variables
        self.__position = position
        self.__speed = 2

        self.__left = 0
        self.__right = 0
        self.__up = 0
        self.__down = 0

        self.__frames = 0
        self.__counter = 0
        self.__exploding = False

        self.__colliding = False

    def move(self, direction, walls):
        '''
        Moves the player sprite towards a certain direction and __speed. Changes
        image of the sprite to reflect how it is moving.

        Returns if walls were hit.
        '''
        hitWall = False

        # Checks if the player is exploding
        if self.__exploding == False:

            # Checking if there is collision with wall then moving
            if direction == 'left':
                self.rect.left -= self.__speed

                if self.__left <= 6:
                    self.image = self.__images[1][self.__left]
                    self.__left += 1
                else:
                    self.__left = 0

                for wall in walls:
                    if self.rect.colliderect(wall.rect):
                        # Moving left; Hit the right side of the wall
                        self.rect.left = wall.rect.right
                        hitWall = True

            elif direction == 'right':
                self.rect.left += self.__speed

                if self.__right <= 6:
                    self.image = self.__images[0][self.__right]
                    self.__right += 1
                else:
                    self.__right = 0

                for wall in walls:
                    if self.rect.colliderect(wall.rect):
                        # Moving right; Hit the left side of the wall
                        self.rect.right = wall.rect.left
                        hitWall = True

            elif direction == 'up':
                self.rect.top -= self.__speed

                if self.__up <= 6:
                    self.image = self.__images[2][self.__up]
                    self.__up += 1
                else:
                    self.__up = 0

                for wall in walls:
                    if self.rect.colliderect(wall.rect):
                        # Moving up; Hit the bottom side of the wall
                        self.rect.top = wall.rect.bottom
                        hitWall = True

            elif direction == 'down':
                self.rect.top += self.__speed

                if self.__down <= 6:
                    self.image = self.__images[3][self.__down]
                    self.__down += 1
                else:
                    self.__down = 0

                for wall in walls:
                    if self.rect.colliderect(wall.rect):
                        # Moving down; Hit the top side of the wall
                        self.rect.bottom = wall.rect.top
                        hitWall = True

        # Returns if the tank hit any walls
        return hitWall

    def get_pos(self):
        '''
        Returns the current position of the enemy tank sprite.
        '''
        return self.rect.center

    def update(self):
        '''
        Update method for enemy. Calls explosion if exploding.
        '''
        if self.__exploding:
            self.explosion()

    def explosion(self):
        '''
        Sets the image of the sprite as an animated explosion
        '''
        self.__exploding = True
        self.__position = self.rect.center

        if self.__counter <= 22:
            self.image = self.__explosions[self.__counter]
            self.rect = self.image.get_rect()
            self.rect.center = self.__position
        else:
            self.kill()

        self.__counter += 1

    def get_colliding(self):
        '''
        Returns if the sprite is colliding or not
        '''
        return self.__colliding

    def set_colliding(self, colliding):
        '''
        Sets if the sprite is colliding or not
        '''
        self.__colliding = colliding


class Scorekeeper(pygame.sprite.Sprite):
    '''The scorekeeper sprite. Keeps track of cash, points, and lives of the 
    player. Also displays mines, points, and cash as text over the Scoreboard.
    '''

    def __init__(self, position):
        ''' The initializer method for the scorekeeper sprite. This method
        takes the following parameters:
        
        position - Position of sprite 
        '''
        # Call the parent __init__() method
        pygame.sprite.Sprite.__init__(self)

        # Instance Variables
        self.__font = pygame.font.Font("./Resources/Fonts/CaptureIt.ttf", 30)

        self.image = self.__font.render('', 1, (55, 120, 205))
        self.rect = self.image.get_rect()

        self.__position = position
        self.__cash = 0
        self.__points = 0
        self.__lives = 3
        self.__mines = 3

    def update(self):
        '''Updates the sprite with number of mines, points, and cash'''
        message = "%d             %3d           $%3d" % \
                  (self.__mines, self.__points, self.__cash)

        self.image = self.__font.render(message, 1, (55, 120, 205))
        self.rect = self.image.get_rect()
        self.rect.center = self.__position

    def get_cash(self):
        '''Returns the amount of cash'''
        return self.__cash

    def set_cash(self, cash):
        '''Sets the amount of cash'''
        self.__cash += cash

    def set_points(self, points):
        '''Sets the amount of points'''
        self.__points += points

    def get_lives(self):
        '''Returns the amount of lives'''
        return self.__lives

    def set_lives(self, lives):
        '''Sets the amount of lives'''
        if self.__lives:
            self.__lives += lives

    def get_mines(self):
        '''Returns the number of mines'''
        return self.__mines

    def set_mines(self, mines):
        '''Sets the number of mines'''
        self.__mines += mines

    def set_pos(self, position):
        '''Sets the position of the scorekeeper'''
        self.__position = position

    def reset(self):
        '''Resets the instance variables after a player loses all lives'''
        self.__cash = 0
        self.__points = 0
        self.__lives = 3
        self.__mines = 3


class Scoreboard(pygame.sprite.Sprite):
    '''
    The background and lives display for the scorekeeper
    '''

    def __init__(self, position, scorekeeper):
        '''The initializer method for the bullet sprite. This method
            takes the following parameters:

        position - Position of sprite
        scorekeeper - The scorekeeper sprite
        '''
        # Call the parent __init__() method
        pygame.sprite.Sprite.__init__(self)
        # Loading the images
        self.__images = []
        for lives in range(4):
            self.__images.append(pygame.image.load( \
                './Resources/Scoreboard/%d.png' % lives))

        self.__scorekeeper = scorekeeper
        self.__position = position

    def update(self):
        ''' Updates background depending on the number of lives'''
        self.image = self.__images[self.__scorekeeper.get_lives()]
        self.rect = self.image.get_rect()
        self.rect.center = self.__position


class Wall(pygame.sprite.Sprite):
    '''
    The wall sprite. There are two types, one that is indestructible and one 
    that is destructible when a mine is near it.
    '''

    def __init__(self, position, breakable):
        ''' The initializer method for the wall sprite. This method
        initializes the following parameters:
        
        position - The position of the button
        breakable - Which type of wall it is
        '''
        # Call the parent __init__() method
        pygame.sprite.Sprite.__init__(self)

        # Loading the image
        if breakable:
            self.image = pygame.image.load('./Resources/Walls/breakable.png')
        else:
            self.image = pygame.image.load('./Resources/Walls/unbreakable.png')

        self.image = self.image.convert()
        self.rect = self.image.get_rect()

        self.rect.center = position


class Button(pygame.sprite.Sprite):
    '''
    The sprite for all Buttons. Different images are loaded for different 
    buttons.
    '''

    def __init__(self, position, button):
        ''' The initializer method for the button sprite. This method
        initializes the following parameters:
        
        position - the position of the button
        button - the type of button
        '''
        # Call the parent __init__() method
        pygame.sprite.Sprite.__init__(self)

        # Loading the image based on button selected
        self.image = pygame.image.load('./Resources/Buttons/%s.png' % button)
        self.image = self.image.convert()
        self.rect = self.image.get_rect()

        self.rect.center = position