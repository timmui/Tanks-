# I - Import and Initialize
import pygame, random, TanksSprites

pygame.init()
pygame.mixer.init()


def levelInit(levelNum):
    ''' This function converts an ASCII drawing of the level into coorinates and
    instaniates the created sprites.
    
    Returns sprites and list of walls
    '''

    levelName = str(levelNum) + '.level'
    level = open(("./Resources/Levels/" + levelName), 'r')
    breakableCoor = []
    unbreakableCoor = []

    row = -1
    col = -1

    # Reads each line for letters to build level
    for line in level:
        row += 1
        for block in line:
            col += 1
            if block == 'X':
                unbreakableCoor.append(((col * 32) + 16, (row * 32 + 64) + 16))
            elif block == 'Y':
                breakableCoor.append(((col * 32) + 16, (row * 32 + 64) + 16))
            elif block == 'P':
                playerCoor = ((col * 32) + 16, (row * 32 + 64) + 16)
            elif block == 'E':
                enemyCoor = ((col * 32) + 16, (row * 32 + 64) + 16)
        col = -1

        #Creating Walls
    breakable = []
    unbreakable = []
    for yBricks in breakableCoor:
        breakable.append(TanksSprites.Wall(yBricks, 1))

    for xBricks in unbreakableCoor:
        unbreakable.append(TanksSprites.Wall(xBricks, 0))

    #Grouping walls
    breakableGroup = pygame.sprite.Group(breakable)
    unbreakableGroup = pygame.sprite.Group(unbreakable)

    wallGroup = pygame.sprite.Group(breakableGroup, unbreakableGroup)

    #Creating player and enemy
    walls = [] + breakable + unbreakable

    player = TanksSprites.Player(playerCoor)
    enemy = TanksSprites.Enemy(enemyCoor)

    #Returning sprite groups
    return walls, breakableGroup, unbreakableGroup, player, enemy


def main():
    '''This function defines the 'mainline logic' for our game.'''

    # D - Display configuration
    screen = pygame.display.set_mode((640, 480))
    pygame.display.set_caption("Tanks!")
    pygame.display.set_icon(pygame.image.load('./Resources/icon.png'))

    scorekeeper = TanksSprites.Scorekeeper((462, 32))

    keepGoing = True
    levelNum = 0
    maxLevel = 6

    # Playing Background Music (Usually in Entities, but music should play throughout the game)
    pygame.mixer.music.load('./Resources/Sounds/music.ogg')
    pygame.mixer.music.set_volume(0.3)
    pygame.mixer.music.play(-1)

    while keepGoing:
        # Starts at main menu
        selected = mainMenu(screen)

        #Goes to gameplay
        if selected == 'Play':
            scorekeeper.reset()

            while selected != 'Quit':
                #Initializing variables
                levelNum += 1
                levelFinished = False

                #Goes to upgrade menu
                selected = upgradeMenu(screen, scorekeeper)

                #Checks for quit
                if selected == 'Quit':
                    break

                #Loops and resets level if player died but has lives
                while not (levelFinished):
                    levelFinished, selected = level(levelNum, screen, scorekeeper)

                #Check for beat game
                if levelNum == maxLevel:
                    selected = endScreen(screen, True)
                    break

                #Check for no lives
                if selected == 'Dead':
                    selected = endScreen(screen, False)
                    break

                #Checks for selected options
                if selected:
                    break

            levelNum = 0

        # Goes to Help screen        
        if selected == 'Help':
            selected = helpScreen(screen)

        # Quits the game
        if selected == 'Quit':
            keepGoing = False

    # Close the game window
    pygame.quit()


def mainMenu(screen):
    '''
    This is the main menu containing buttons to go to the gameplay, help screen,
    and quitting.
    
    Returns the selected option
    '''
    # E - Entities
    background = pygame.image.load('./Resources/Main Menu.png')
    background = background.convert()
    screen.blit(background, (0, 0))

    # Creating Crosshair
    crosshair = TanksSprites.Crosshair()

    #Sound effect loading
    shot = pygame.mixer.Sound("./Resources/Sounds/shot.ogg")
    shot.set_volume(0.3)

    #Creating buttons
    playButton = TanksSprites.Button((528, 230), 'Play')
    helpButton = TanksSprites.Button((552, 300), 'Help')
    quitButton = TanksSprites.Button((552, 370), 'Quit')

    buttonGroup = pygame.sprite.Group(playButton, helpButton, quitButton)
    allSprites = pygame.sprite.OrderedUpdates(buttonGroup, crosshair)
    # A - Action (broken into ALTER steps)

    # A - Assign values to key variables
    clock = pygame.time.Clock()
    keepGoing = True
    selected = ''


    # L - Loop
    while keepGoing:
        # T - Timer to set frame rate
        clock.tick(30)

        # E - Event handling
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                selected = 'Quit'
                keepGoing = False

            #Checking for button clicks
            elif event.type == pygame.MOUSEBUTTONDOWN:
                #Sound effect
                shot.play()

                if playButton.rect.colliderect(crosshair.rect):
                    selected = 'Play'
                    keepGoing = False
                if helpButton.rect.colliderect(crosshair.rect):
                    selected = 'Help'
                    keepGoing = False
                if quitButton.rect.colliderect(crosshair.rect):
                    selected = 'Quit'
                    keepGoing = False

            # Crosshair movement
            elif event.type == pygame.MOUSEMOTION:
                crosshair.set_position(pygame.mouse.get_pos())

            elif event.type == pygame.KEYDOWN:
                #Exits to Menu
                if event.key == pygame.K_ESCAPE:
                    selected = 'Quit'
                    keepGoing = False

                    # R - Refresh display
        pygame.mouse.set_visible(0)

        allSprites.clear(screen, background)
        allSprites.update()
        allSprites.draw(screen)

        pygame.display.flip()

    #Returns selected option
    return selected


def upgradeMenu(screen, scorekeeper):
    '''
    The upgrade menu with buttons for more mines and lives. Scorekeeper is also
    shown at the bottom for the player's reference.
    
    Returns selected option
    '''
    # E - Entities
    background = pygame.image.load('./Resources/Upgrade Menu.png')
    background = background.convert()
    screen.blit(background, (0, 0))

    # Creating Crosshair
    crosshair = TanksSprites.Crosshair()

    #Sound effects loading
    shot = pygame.mixer.Sound("./Resources/Sounds/shot.ogg")
    shot.set_volume(0.3)

    #Creating Buttons
    playButton = TanksSprites.Button((528, 300), 'Play')
    mineButton = TanksSprites.Button((133, 150), 'Mine')
    lifeButton = TanksSprites.Button((133, 250), 'Life')
    scoreboard = TanksSprites.Scoreboard((320, 416), scorekeeper)

    scorekeeper.set_pos((462, 416))

    buttonGroup = pygame.sprite.Group(playButton, mineButton, lifeButton)

    allSprites = pygame.sprite.OrderedUpdates(buttonGroup, crosshair, scoreboard, \
                                              scorekeeper)
    # A - Action (broken into ALTER steps)

    # A - Assign values to key variables
    clock = pygame.time.Clock()
    keepGoing = True
    selected = ''


    # L - Loop
    while keepGoing:
        # T - Timer to set frame rate
        clock.tick(30)

        # E - Event handling
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                selected = 'Quit'
                keepGoing = False

            #Checking for button clicks
            elif event.type == pygame.MOUSEBUTTONDOWN:
                #Sound effect
                shot.play()

                if playButton.rect.colliderect(crosshair.rect):
                    selected = 'Play'
                    keepGoing = False
                if lifeButton.rect.colliderect(crosshair.rect):
                    if (scorekeeper.get_cash()) >= 200 and \
                                    scorekeeper.get_lives() < 3:
                        scorekeeper.set_cash(-200)
                        scorekeeper.set_lives(1)
                if mineButton.rect.colliderect(crosshair.rect):
                    if (scorekeeper.get_cash()) >= 50:
                        scorekeeper.set_cash(-50)
                        scorekeeper.set_mines(1)

            # Crosshair movement
            elif event.type == pygame.MOUSEMOTION:
                crosshair.set_position(pygame.mouse.get_pos())

            elif event.type == pygame.KEYDOWN:
                #Exits to Menu
                if event.key == pygame.K_ESCAPE:
                    selected = 'Menu'
                    keepGoing = False

        # R - Refresh display
        pygame.mouse.set_visible(0)

        allSprites.clear(screen, background)
        allSprites.update()
        allSprites.draw(screen)

        pygame.display.flip()

    # Returns the selected next option
    return selected


def helpScreen(screen):
    '''
    The help screen with the objective and controls described in the game. 
    
    Returns the selected option
    '''
    # E - Entities
    background = pygame.image.load('./Resources/Help Screen.png')
    background = background.convert()
    screen.blit(background, (0, 0))

    # Creating Crosshair
    crosshair = TanksSprites.Crosshair()

    #Sound effects loading
    shot = pygame.mixer.Sound("./Resources/Sounds/shot.ogg")
    shot.set_volume(0.3)

    #Creating button
    menuButton = TanksSprites.Button((528, 400), 'Menu')

    allSprites = pygame.sprite.OrderedUpdates(menuButton, crosshair)
    # A - Action (broken into ALTER steps)

    # A - Assign values to key variables
    clock = pygame.time.Clock()
    selected = ''
    keepGoing = True


    # L - Loop
    while keepGoing:
        # T - Timer to set frame rate
        clock.tick(30)

        # E - Event handling
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                selected = 'Quit'
                keepGoing = False

            #Checking for button clicks
            elif event.type == pygame.MOUSEBUTTONDOWN:
                #Sound effect
                shot.play()

                if menuButton.rect.colliderect(crosshair.rect):
                    selected = ''
                    keepGoing = False

            # Crosshair movement
            elif event.type == pygame.MOUSEMOTION:
                crosshair.set_position(pygame.mouse.get_pos())

            elif event.type == pygame.KEYDOWN:
                #Exits to Menu
                if event.key == pygame.K_ESCAPE:
                    selected = 'Menu'
                    keepGoing = False

        # R - Refresh display
        pygame.mouse.set_visible(0)

        allSprites.clear(screen, background)
        allSprites.update()
        allSprites.draw(screen)

        pygame.display.flip()

    # Returns the selected next option
    return selected


def endScreen(screen, win):
    '''
    The end screen called when either the player is out of lives or beats the 
    last level.
    
    Returns the selected option
    '''
    # E - Entities
    if win:
        background = pygame.image.load('./Resources/win.png')
    else:
        background = pygame.image.load('./Resources/lose.png')

    background = background.convert()
    screen.blit(background, (0, 0))

    # Creating Crosshair
    crosshair = TanksSprites.Crosshair()

    #Sound effects loading
    shot = pygame.mixer.Sound("./Resources/Sounds/shot.ogg")
    shot.set_volume(0.3)

    #Creating button
    menuButton = TanksSprites.Button((528, 430), 'Menu')

    allSprites = pygame.sprite.OrderedUpdates(menuButton, crosshair)
    # A - Action (broken into ALTER steps)

    # A - Assign values to key variables
    clock = pygame.time.Clock()
    selected = ''
    keepGoing = True


    # L - Loop
    while keepGoing:
        # T - Timer to set frame rate
        clock.tick(30)

        # E - Event handling
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                selected = 'Quit'
                keepGoing = False

            #Checking for button clicks
            elif event.type == pygame.MOUSEBUTTONDOWN:
                #Sound effect
                shot.play()

                if menuButton.rect.colliderect(crosshair.rect):
                    selected = ''
                    keepGoing = False

            # Crosshair movement
            elif event.type == pygame.MOUSEMOTION:
                crosshair.set_position(pygame.mouse.get_pos())

            elif event.type == pygame.KEYDOWN:
                #Exits to Menu
                if event.key == pygame.K_ESCAPE:
                    selected = 'Menu'
                    keepGoing = False

        # R - Refresh display
        pygame.mouse.set_visible(0)

        allSprites.clear(screen, background)
        allSprites.update()
        allSprites.draw(screen)

        pygame.display.flip()

    # Returns the selected next option
    return selected


def level(levelNum, screen, scorekeeper):
    '''
    This function contains the main gameplay. Level number, the screen, 
    and the scorekeeper are parameters for this funciton.
    
    Returns the selected next option and if the the level is finished
    '''
    # E - Entities
    background = pygame.Surface(screen.get_size())
    background = background.convert()
    background.fill((220, 215, 176))
    screen.blit(background, (0, 0))

    # Preloading bullet image
    bulletImage = pygame.image.load('./Resources/bullet.png')

    #Loading Sound
    shot = pygame.mixer.Sound("./Resources/Sounds/shot.ogg")
    shot.set_volume(0.3)

    explode = pygame.mixer.Sound("./Resources/Sounds/explode.ogg")
    explode.set_volume(0.3)

    scorekeeper.set_pos((462, 32))

    #Creating Crosshair
    crosshair = TanksSprites.Crosshair()

    #Creating Level
    walls, breakableGroup, unbreakableGroup, player, enemy = levelInit(levelNum)

    #Creating Sprite Groups
    scoreboard = TanksSprites.Scoreboard((320, 32), scorekeeper)
    playerGroup = pygame.sprite.Group(player)
    enemyGroup = pygame.sprite.Group(enemy)
    wallGroup = pygame.sprite.Group(breakableGroup, unbreakableGroup)
    bulletGroup = pygame.sprite.Group()

    #Creating Mines off screen
    mineGroup = pygame.sprite.Group()

    for num in range(scorekeeper.get_mines()):
        mineGroup.add(TanksSprites.Mine(1))

    #Putting groups in an ordered update group
    allSprites = pygame.sprite.OrderedUpdates(scoreboard, scorekeeper, wallGroup, \
                                              mineGroup, bulletGroup, \
                                              playerGroup, enemyGroup, crosshair)
    # A - Action (broken into ALTER steps)

    # A - Assign values to key variables
    clock = pygame.time.Clock()
    keepGoing = True
    levelFinished = False
    selected = ''
    currentDir = 'right'

    # L - Loop
    while keepGoing:
        # T - Timer to set frame rate
        clock.tick(30)
        walls = wallGroup.sprites()
        # E - Event handling
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                selected = 'Quit'
                levelFinished = True
                keepGoing = False

            # Player shooting    
            elif event.type == pygame.MOUSEBUTTONDOWN and playerGroup.sprites():

                bulletGroup.add(TanksSprites.Bullet(player.get_pos(), \
                                                    pygame.mouse.get_pos(), 1, \
                                                    bulletImage))
                #Sound effect
                shot.play()

            # Crosshair movement    
            elif event.type == pygame.MOUSEMOTION:
                crosshair.set_position(pygame.mouse.get_pos())

            # Key event handling
            elif event.type == pygame.KEYDOWN:
                #Exits to menu
                if event.key == pygame.K_ESCAPE:
                    selected = 'Menu'
                    levelFinished = True
                    keepGoing = False
                #Drops Mines    
                if event.key == pygame.K_SPACE:
                    if scorekeeper.get_mines():
                        (mineGroup.sprites()[scorekeeper.get_mines() - 1]) \
                            .start(player.get_pos())
                        scorekeeper.set_mines(-1)
        #Enemy Shooting                
        if enemyGroup.sprites() and (((pygame.time.get_ticks()) % 30) == 0):
            bulletGroup.add(TanksSprites.Bullet(enemy.get_pos(), \
                                                player.get_pos(), 0, \
                                                bulletImage))
            #Sound effects
            shot.play()

            #Adding bullets to allSprites
        allSprites.add(bulletGroup)

        # Player Tank Movement            
        keys = pygame.key.get_pressed()

        #Enemy Goes opposite direction of the player
        if keys[pygame.K_a]:
            player.move('left', walls)
            hitWall = enemy.move('right', walls)
            currentDir = 'right'

        elif keys[pygame.K_d]:
            player.move('right', walls)
            hitWall = enemy.move('left', walls)
            currentDir = 'left'

        elif keys[pygame.K_w]:
            player.move('up', walls)
            hitWall = enemy.move('down', walls)
            currentDir = 'down'
        elif keys[pygame.K_s]:
            player.move('down', walls)
            hitWall = enemy.move('up', walls)
            currentDir = 'up'

        else:
            #Continuing movement even if no movement from player
            hitWall = enemy.move(currentDir, walls)

        #Reversing direction if collision with wall    
        if hitWall:
            if currentDir == 'left':
                currentDir = 'right'
            elif currentDir == 'right':
                currentDir = 'left'
            elif currentDir == 'up':
                currentDir = 'down'
            elif currentDir == 'down':
                currentDir = 'up'


        #Collision Handling----------------------------------------------

        #Checking for collisons with bullets            
        for bullet in bulletGroup.sprites():
            shooting, play = bullet.get_shot()

            if not (bullet.get_colliding()):
                #Walls
                if pygame.sprite.spritecollide(bullet, wallGroup, False):
                    bullet.explosion()
                    bullet.set_colliding(True)

                    #Sound effect
                    explode.play()

                #Mines        
                for mine in mineGroup.sprites():
                    if bullet.rect.colliderect(mine.rect) and not (mine.get_colliding()):
                        mine.explosion()
                        bullet.explosion()

                        #Mine collision not set to get collisions with other sprites
                        bullet.set_colliding(True)

                        #Sound effect
                        explode.play()

                #Player        
                if shooting and not (play) and not (player.get_colliding()):
                    if pygame.sprite.spritecollide(player, bulletGroup, False):
                        bullet.explosion()
                        player.explosion()

                        #Reducing player lives
                        scorekeeper.set_lives(-1)

                        player.set_colliding(True)
                        bullet.set_colliding(True)

                        #Sound effect
                        explode.play()

                #Enemy
                if shooting and play and not (enemy.get_colliding()):
                    for enemy in enemyGroup.sprites():
                        if bullet.rect.colliderect(enemy.rect):
                            bullet.explosion()
                            enemy.explosion()

                            #Updating Scorekeeper
                            scorekeeper.set_points(120)
                            scorekeeper.set_cash(120)

                            enemy.set_colliding(True)
                            bullet.set_colliding(True)

                            #Sound effect
                            explode.play()

        #Checking for collisions with mines
        for mine in mineGroup.sprites():
            #Checking the mine has exploded before it collides
            if mine.get_exploding() and not (mine.get_colliding()):
                #Breakable Walls
                if pygame.sprite.spritecollide(mine, breakableGroup, True):
                    #Updating the Scorekeeper
                    scorekeeper.set_points(50)
                    mine.set_colliding(True)

                    #Sound effect
                    explode.play()

                #Enemy    
                for enemy in enemyGroup.sprites():
                    if mine.rect.colliderect(enemy.rect) and not ( \
                            enemy.get_colliding()):
                        enemy.explosion()

                        #Updating the scorekeeper
                        scorekeeper.set_points(100)
                        scorekeeper.set_cash(120)

                        enemy.set_colliding(True)
                        mine.set_colliding(True)

                        #Sound effect
                        explode.play()
                #Player        
                for play in playerGroup.sprites():
                    if mine.rect.colliderect(play.rect) and not ( \
                            enemy.get_colliding()):
                        player.explosion()

                        #Updating the Scorekeeper
                        scorekeeper.set_lives(-1)

                        player.set_colliding(True)
                        mine.set_colliding(True)

                        #Sound effect
                        explode.play()

        # R - Refresh display
        pygame.mouse.set_visible(0)

        allSprites.clear(screen, background)
        allSprites.update()
        allSprites.draw(screen)

        pygame.display.flip()

        #Checking if there are enemies left
        if not (enemyGroup.sprites()):
            levelFinished = True
            keepGoing = False

        #Checking if player is alive    
        elif not (playerGroup.sprites()):
            levelFinished = False
            keepGoing = False

        #Checking if the player is out of lives
        if scorekeeper.get_lives() <= 0:
            selected = 'Dead'
            levelFinished = True
            keepGoing = False

    # Returns if the level is finished and the selected next option    
    return levelFinished, selected

# Call the main function
main()