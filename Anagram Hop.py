from tkinter import *
from time import *
from random import *
from enchant import *

root = Tk()
s = Canvas(root, width=1200, height=800, background="lightblue")


## SETUP -------------------------------------------------------------------------------------------------------------------------------------    
def loadImages():
    global logoboard, keypressboard, titleLetters
    global lilypads, frogStill, frogJump, frogDisplay
    global spin

    #Title
    logoboard = PhotoImage(file = "logoboard.gif")
    keypressboard = PhotoImage(file = "keypressboard.gif")
    
    #format: letter = [image, width, unscrambled x-pos, current x-pos, speed]
    A = [PhotoImage(file = "data/A.gif"),113,155,None,None]
    N = [PhotoImage(file = "data/N.gif"),80,239,None,None]
    A1 = [PhotoImage(file = "data/A1.gif"),91,326,None,None]
    G = [PhotoImage(file = "data/G.gif"),96,429,None,None]
    R = [PhotoImage(file = "data/R.gif"),83,516,None,None]
    A2 = [PhotoImage(file = "data/A2.gif"),90,601,None,None]
    M = [PhotoImage(file = "data/M.gif"),101,697,None,None]
    space = [PhotoImage(file = "data/space.gif"),48,765,None,None]
    H = [PhotoImage(file = "data/H.gif"),118,858,None,None]
    O = [PhotoImage(file = "data/O.gif"),97,958,None,None]
    P = [PhotoImage(file = "data/P.gif"),83,1051,None,None]
    titleLetters = [A, N, A1, G, R, A2, M, space, H, O, P]

    #lilypads
    lilypad1 = PhotoImage(file = "data/lilypad.gif")
    lilypad2 = PhotoImage(file = "data/lilypad2.gif")
    lilypad3 = PhotoImage(file = "data/lilypad3.gif")
    lilypad4 = PhotoImage(file = "data/lilypad4.gif")
    lilypad5 = PhotoImage(file = "data/lilypad5.gif")
    lilypad6 = PhotoImage(file = "data/lilypad6.gif")
    lilypad7 = PhotoImage(file = "data/lilypad7.gif")
    lilypad8 = PhotoImage(file = "data/lilypad8.gif")
    lilypad9 = PhotoImage(file = "data/lilypad9.gif")
    lilypad10 = PhotoImage(file = "vlilypad10.gif")
    lilypad11 = PhotoImage(file = "data/lilypad11.gif")
    lilypad12 = PhotoImage(file = "data/lilypad12.gif")
    lilypad13 = PhotoImage(file = "data/lilypad13.gif")
    lilypad14 = PhotoImage(file = "data/lilypad14.gif")
    lilypad15 = PhotoImage(file = "data/lilypad15.gif")

    lilypads = [lilypad1, lilypad2, lilypad3, lilypad4, lilypad5, lilypad6, lilypad7, lilypad8, lilypad9, lilypad10,
                lilypad11, lilypad12, lilypad13, lilypad14, lilypad15]

    #turbines
    t1 = PhotoImage(file = "data/propellor1.gif")
    t2 = PhotoImage(file = "data/propellor2.gif")
    t3 = PhotoImage(file = "data/propellor3.gif")
    t4 = PhotoImage(file = "data/propellor4.gif")
    t5 = PhotoImage(file = "data/propellor5.gif")
    t6 = PhotoImage(file = "data/propellor6.gif")
    t7 = PhotoImage(file = "data/propellor7.gif")
    t8 = PhotoImage(file = "data/propellor8.gif")
    spin = [t1,t2,t3,t4,t5,t6,t7,t8]

    #froggy
    frogDisplay = PhotoImage(file = "data/frogDisplay.gif")
    frogStill = PhotoImage(file = "data/frog.gif")
    frogJump = PhotoImage(file = "data/frogjump.gif")

def setIntroValues():
    #This procedure sets values that should only be set once, at the start of the running of the program
    #Because bubbles and turbines don't get rerandomized/reset at the start of every game
    global f, bubbleXs, bubbleYs, bubbleColour, bubbleSize, bubbles, turbineXs, turbinePos, turbines, dam
    global boardLogo

    f = 0
    
    #creating arrays for bubbles
    bubbleXs = [randint(0,1200) for b in range(100)]
    bubbleYs = [randint(0,800) for b in range(100)]
    bubbleColour = [choice(["#c2e2fc","#c2f2fc","#d1e9fc"]) for b in range(100)]
    bubbleSize = [choice([4,8,12]) for b in range(100)]
    bubbles = [0 for b in range(100)]

    #creating turbine arrays
    dam = 0
    turbineXs = [i*120+60 for i in range(10)]
    turbinePos = [randint(0,7) for i in range(10)]
    turbines = [0 for i in range(10)]
    boardLogo = 0

def setGameValues():
    #this procedure sets values that need to be reset every single game
    global jump, gameRunning, score, startTime, dictionary, words
    global tryText, screenText, scoreDisplay, timeDisplay
    global frog, frogX, frogY, frogXspeed, frogYspeed, frogChoice, goalX, goalY, frogOn

    dictionary = enchant.Dict("en_US")
    words = [x[:-1] for x in open("data/words.txt").readlines()] #opens word list document, converts into list
    startTime = time()
    score = 0
    jump = False
    gameRunning = True

    scrambleWords()
    fillPadArrays()

    #frog
    frog = 0
    frogX = padXs[0]
    frogY = padYs[0]
    frogXspeed = 0
    frogYspeed = speed
    frogChoice = frogStill
    goalX = -10
    goalY = -10

    #typing text
    tryText = ""
    screenText = 0
    scoreDisplay = 0
    timeDisplay = 0

#WORD SCRAMBLING
def scrambleWords():
    global dsorw, lim, mini

    dsorw = [] #list for shuffled words ("dsorw" is the word "words" scrambled)
    for w in words: 
        if len(w) <= lim and len(w) >= mini: #lim and mini are set in intro screens
            letters = [i for i in w]
            shuffle(letters)
            check = "".join(letters)
            while dictionary.check(check): #this means that check is still an English word
                shuffle(letters) #and so check needs to be reshuffled until it isn't an English word anymore
                check = "".join(letters)
            dsorw.append(check)
    shuffle(dsorw) #randomizes order

#CREATING INITIAL LILYPADS
def fillPadArrays():
    global padpos, padXs, padYs, padWords, padList, wordList, padImages, wordIndex

    padpos = [i*200+100 for i in range(0,6)] #grids out horizontal columns the lilypads can be in (to avoid overlapping)
    shuffle(padpos)

    padXs = [600] # the blank lily pad 
    padYs = [500] # the frog is on initially
    padWords = [""]

    padXs.extend(padpos[:4]) #randomly generates 4 other lilypads
    padYs.extend([randint(0,400) for i in range(4)]) 
    padWords.extend(dsorw[:4])

    padImages = [choice(lilypads) for i in range(5)] #randomly selects lilypad designs
    wordIndex = 5

    padList = [0 for i in range(5)]
    wordList = [0 for i in range(5)]


## INPUT-TRIGGERED PROCEDURES (runs only when user interacts) -------------------------------------------------------------------------------    
#HANDLING TEXT INPUT
def keyDownHandler(event):
    global tryText
    if event.keysym.isalpha() and len(event.keysym) == 1:
        tryText = tryText + event.keysym #adds letter to tryText
    elif event.keysym == "BackSpace":
        tryText = tryText[:len(tryText)-1] #removes letter from tryText
    elif event.keysym == "Return": #sends what is in tryText to verification
        if tryText != "":
            checkMatch(tryText)
            tryText = "" #resets tryText to nothing

#INPUT VERIFICATION
def checkMatch(entry): 
    global delete, score
    for word in padWords:
        x = 0
        for l in entry:
            if word.count(l) != entry.count(l):
                x = 1 #if something doesn't match, x is no longer 0
        if len(entry) == len(word) and x == 0 and dictionary.check(entry):
            i = padWords.index(word)
            score = score + 1
            startJump(i) 
            padWords[i] = "" #deletes the word on the pad the frog is jumping to

#SETS FROG SPEEDS TO JUMP TO LILYPAD
def startJump(i):
    global frogXspeed, frogYspeed, jump, frogChoice, goalX, goalY
    goalX = padXs[i]
    goalY = padYs[i]+20*(speed) #where the desired lilypad will be in 20 frames
    frogXspeed = (goalX-frogX)/20 #speed to get there in 20 frames
    frogYspeed = (goalY-frogY)/20 #speed to get there in 20 frames
    frogChoice = frogJump #changes image of frog
    jump = True
    padWords[padWords.index("")] = "." #marks the pad just jumped off of with a period


## CHECKING/MODIFYING PROCEDURES THAT ARE PART OF THE GAME LOOP-------------------------------------------------------------------------------------------------------------------------------------
#CHECK IF PADS NEED TO BE DELETED (new pads are only added when an old one is deleted)
def checkPads():
    for i in range(len(padList)):       
        if padYs[i] > 750 or padWords[i] == ".": # if the lilypad is off screen, or just jumped off of 
            removePad(i)
            dropPad()

#ADDING A NEW PAD
def dropPad():
    global wordIndex
    padXs.append(choice(padpos))
    padYs.append(min(padYs)-randint(80,100)) #creates lilypad just a bit higher than the highest lilypad
    padImages.append(choice(lilypads))
    
    padWords.append(dsorw[wordIndex]) 
    wordIndex = wordIndex + 1 #since the entire word list of the game was generated at the start, this just shifts the reference index along
    if wordIndex == len(dsorw): #if the player is a master and the program runs out of words...
        scrambleWords()
        wordIndex = 0

#REMOVING A LILYPAD (or removing its info, so that it is not drawn next time drawPads() is called)
def removePad(i):
    del padXs[i]
    del padYs[i]
    del padWords[i]
    del padImages[i]

#CHECK IF FROG NEEDS TO STOP JUMPING (only called when the frog is jumping, or jump == True; see runGame())
def checkFrogJump():
    global frogXspeed, frogYspeed, frogChoice, jump
    if goalX-3 < frogX < goalX + 3 and goalY-3 < frogY < goalY+3: #when the frog is at the pad (adjusts for rounding error)
        frogXspeed = 0
        frogYspeed = speed
        frogChoice = frogStill
        jump = False 
    
#CHECK IF GAME IS OVER
def checkGame():
    global gameRunning
    if frogY > 750:
        gameRunning = False


## DRAWING PROCEDURES-------------------------------------------------------------------------------------------------------------------------------------
def drawBubbles():
    for i in range(len(bubbleXs)):
        s.delete(bubbles[i])
        bubbles[i] = s.create_oval(bubbleXs[i]-bubbleSize[i], bubbleYs[i]-bubbleSize[i],bubbleXs[i]+bubbleSize[i],bubbleYs[i]+bubbleSize[i], outline = "", fill = bubbleColour[i])
        if bubbleYs[i] > 800: #recycles bubbles
            bubbleYs[i] = -bubbleSize[i]
        else:
            bubbleYs[i] += 1 #move bubbles down

def drawTurbines(): #called every frame so that turbines stay above lilypads/frog/bubbles
    global dam
    s.delete(dam)
    dam = s.create_rectangle(0,700,1200,800, fill = "gray35", outline = "")
    for i in range(10):
        s.delete(turbines[i])
        turbines[i] = s.create_image(turbineXs[i],700, image = spin[turbinePos[i]]) 
        if f%8 == 0: #turbines only turn every 8th frame
            turbinePos[i] = turbinePos[i] + 1
            if turbinePos[i] == 8:
                turbinePos[i] = 0
            
def drawPads():
    for i in range(len(padList)):
        s.delete(padList[i], wordList[i])
        padList[i] = s.create_image(padXs[i],padYs[i], image = padImages[i])
        wordList[i] = s.create_text(padXs[i],padYs[i], text = padWords[i], font = ("Georgia", 18, "bold"))
        padYs[i] = padYs[i] + speed #move pads down

def drawFrog():
    global frog, frogX, frogY
    s.delete(frog)
    frog = s.create_image(frogX,frogY, image = frogChoice)
    frogX = frogX + frogXspeed #move frog
    frogY = frogY + frogYspeed

def updateText():
    global screenText, scoreDisplay, timeDisplay
    s.delete(screenText, scoreDisplay, timeDisplay)
    timeDisplay = s.create_text(100,50, text = "Time: "+str(round(time()-startTime)), font = ("Georgia",28,"bold"), fill = "white")
    scoreDisplay = s.create_text(1100,50,text = "Score: "+str(score), font = ("Georgia",28,"bold"), fill = "white")
    screenText = s.create_text(600,750,text = tryText, font = ("Georgia",28,"bold"), fill = "white") #displays the stuff in tryText to help player

## MAIN GAME LOOP ------------------------------------------------------------------------------------------------------------------------------------- 
def runGame():
    global f, frogYspeed
    setGameValues()

    countdown()
    while gameRunning:
        f = f+1
        checkPads()  
        if jump: #only checks if the jump needs to stop when the frog is jumping
            checkFrogJump()
        checkGame()
        drawBubbles()
        drawPads()
        drawFrog()
        drawTurbines()
        updateText()
        s.update()
    endGame()

def countdown(): #FULL FREEZE to help players prepare and for drama
    drawPads()
    drawFrog()
    updateText()
    for x in range(5):
        count = s.create_text(600,350, text = str(5-x), font = ("Georgia",80,"bold"), fill = "white")
        s.update()
        sleep(1)
        s.delete(count)

## INTRO SCREENS (get ready for a wild ride) -------------------------------------------------------------------------------------------------------------------------------------  
def introScreen(): #this is one long procedure instead of many small ones, mainly because introScreen() is only called once
    global f, mode, boardLogo

    mode = "intro"
    loadImages()
    setIntroValues()

    #GRADIENT BACKGROUND
    r = 52
    g = 155
    b = 239
    deltaR = (178-52)/800
    deltaG = (215-155)/800
    deltaB = (244-239)/800
    for y in range(800):
        colour = "#"+hex(int(r))[2:]+hex(int(g))[2:]+hex(int(b))[2:] #the function hex(int) returns a string prefixed wihh "0x", which I don't need
        s.create_line(0, y, 1200,y,fill = colour) #none of the 3 colour components is ever small enough to be a 1-digit hex number, so I took out the "add 0 to front" code
        r = r + deltaR
        g = g + deltaG
        b = b + deltaB
        
    startButton = Button(root, text = "START", font = ("Courier",40, "bold"), command = startButtonPressed, anchor = "center", fg= "#0e7a3d")
    startButton.pack()
    startButton.place(x=500, y=500)
    
    #SCRAMBLED TITLE
    screenTitle = [0 for i in range(len(titleLetters))]#blank array to store images later
    shuffle(titleLetters) #draw letters randomly
    
    #for reference: each sub-array in titleLetters is structured thus:
    #titleLetters[i] = [letter image, letter width, letter x-position when unscrambled, letter x-position now, letter speed]
    
    while mode == "intro":#turns false when startButton is pressed
        f = f+1
        place = 100 #since the logo is centered in a 1200px canvas, and is 1000px wide, the leftmost edge is at 100
        drawBubbles()
        drawTurbines()
        s.delete(boardLogo)
        boardLogo = s.create_image(600,280,image = logoboard)
        for i in range(len(titleLetters)):
            s.delete(screenTitle[i])
            titleLetters[i][3]= place+titleLetters[i][1]/2 #find the center of the letter (place + half of letter width)
            screenTitle[i] = s.create_image(titleLetters[i][3], 250, image = titleLetters[i][0])
            place = place+titleLetters[i][1] #the leftmost edge of the next letter (place+ letter width)
        s.update()

    startButton.destroy()

    #Generates speeds for the images to move to unscrambled position
    for i in range(len(titleLetters)):
        speed = (titleLetters[i][2]-titleLetters[i][3])/20 #where it's supposed to be subtracted by where it is, divided by 20 frames
        titleLetters[i][4]= speed

    shuffle(titleLetters)#randomizes unscrambling animation (which letters are drawn above which)

    #unscrambling
    for frame in range(20):
        f = f+1
        drawBubbles()
        drawTurbines()
        s.delete(boardLogo)
        boardLogo = s.create_image(600,280,image = logoboard)
        for i in range(len(titleLetters)):
            s.delete(screenTitle[i])
            titleLetters[i][3] = titleLetters[i][3]+titleLetters[i][4] #changes x-pos of letter (current x-pos + speed)
            screenTitle[i] = s.create_image(titleLetters[i][3], 250, image = titleLetters[i][0])
        s.update()

    #basically, sleep for 3 seconds, except the bubbles/turbines keep moving
    current = time()
    while time()- current < 3:
        f = f+1
        drawBubbles()
        drawTurbines()
        s.delete(boardLogo)
        boardLogo = s.create_image(600,280,image = logoboard)
        for i in range(len(titleLetters)): 
            s.delete(screenTitle[i])
            screenTitle[i] = s.create_image(titleLetters[i][3], 250, image = titleLetters[i][0])
        s.update()

    for i in range(len(titleLetters)):
        s.delete(screenTitle[i])
    s.delete(boardLogo)

    instructions()

def startButtonPressed():
    global mode
    mode = "instructions"

def instructions(): #instructions screen
    global f
    blurbtext = "Hi, I'm Francis the Frog! Ever since the townsfolk built this dam across my river, I've been in danger of being swept into the turbines.\n\nFortunately, there are lilypads passing downstream! However, for me to hop onto one, you must unscramble the word printed on it. Can you help me stay away from the dam?"
    Typetext = "Type your guess"
    Changetext = "Change your guess"
    Submittext = "Submit your guess!"

    ofCourseButton = Button(root,text = "of course!", font = ("Georgia",24, "bold"), command = ofCoursePressed, anchor = "center", bg =  "white", fg= "#0e7a3d")
    ofCourseButton.pack()
    ofCourseButton.place(x = 490, y = 562)
    
    while mode == "instructions": #keeps looping until ofCourseButton is pressed
        f = f+1
        drawBubbles()
        drawTurbines()
        backing = s.create_rectangle(100,100,1100,540, fill = "white", outline = "")
        
        blurb = s.create_text(700,250, text = blurbtext, font = ("Georgia",18), width = 600)
        froggy = s.create_image(240,260, image = frogDisplay)
        
        typeBlock = s.create_image(267,440, image = keypressboard)
        Type = s.create_text(267,440,text = "QWERTY", font = ("Courier",28, "bold"))
        typeDisplay = s.create_text(267,500, text = Typetext, font = ("Georgia",18))
        changeBlock = s.create_image(600, 440, image = keypressboard)
        Change = s.create_text(600,440,text = "Backspace", font = ("Courier",28, "bold"))
        changeDisplay = s.create_text(600,500, text = Changetext, font = ("Georgia",18))
        submitBlock = s.create_image(933, 440, image = keypressboard)
        Submit = s.create_text(933,440,text = "Return", font = ("Courier",28, "bold"))
        submitDisplay = s.create_text(933,500, text = Submittext, font = ("Georgia",18))
        
        s.update()
        s.delete(backing,blurb,froggy,typeBlock,Type,typeDisplay,changeBlock,Change,changeDisplay,submitBlock,Submit,submitDisplay)

    ofCourseButton.destroy()
    difficultyScreen()

def difficultyScreen(): #difficulty screen
    global f
    easyButton = Button(root, text = "EASY", font = ("Courier",40, "bold"), command = easyButtonPressed, anchor = "center",bg =  "white", fg= "#0e7a3d")
    easyButton.pack()
    mediumButton = Button(root, text = "MEDIUM", font = ("Courier",40, "bold"), command = mediumButtonPressed, anchor = "center",bg =  "white", fg= "#0e7a3d")
    mediumButton.pack()
    hardButton = Button(root, text = "HARD", font = ("Courier",40, "bold"), command = hardButtonPressed, anchor = "center",bg =  "white", fg= "#0e7a3d")
    hardButton.pack()
    easyButton.place(x = 210, y = 400)
    mediumButton.place(x = 480, y = 400)
    hardButton.place(x = 810, y = 400)
    difficultytext = "Select a difficulty:"
  
    while mode == "difficulty": #keeps looping until easy/medium/hardButton is pressed
        f = f+1
        drawBubbles()
        drawTurbines()
        backing = s.create_rectangle(100,100,1100,540, fill = "white", outline = "")
        difficulty = s.create_text(600,300,text = difficultytext, font = ("Georgia",28), width = 800)
        s.update()
        s.delete(backing,difficulty)

    easyButton.destroy()
    mediumButton.destroy()
    hardButton.destroy()

    runGame() #Time to start!

def ofCoursePressed():
    global mode
    mode = "difficulty"

#DIFFICULTY CONTROLS
def easyButtonPressed():
    global mode, mini, lim, speed
    mode = "game"
    mini = 3 #minimum length of words
    lim = 4 #maximum length of words
    speed = 0.5  #speed at which lilypads move at

def mediumButtonPressed():
    global mode, mini, lim, speed
    mode = "game"
    mini = 3
    lim = 5
    speed = 0.9

def hardButtonPressed():
    global mode, mini, lim, speed
    mode = "game"
    mini = 4
    lim = 6
    speed = 1.3

## END OF GAME -------------------------------------------------------------------------------------------------------------------------------------  
def endGame():
    global mode, tryText, f
    mode = "gameEnd"
    timeLasted = str(round(time()-startTime, 2))
    
    for i in range(len(padList)):
        s.delete(padList[i], wordList[i])
    s.delete(frog, screenText, scoreDisplay, timeDisplay)
    tryText = ""
    
    playAgain = Button(root,text = "play again?", font = ("Georgia",28, "bold"), command = playAgainPressed, anchor = "center")
    playAgain.pack()
    playAgain.place(x = 475, y = 450)

    word = " words"
    if score == 1:
        word = " word"
    
    while mode == "gameEnd": #keeps looping until playAgain is pressed
        f = f+1
        drawBubbles()
        drawTurbines()
        backing = s.create_rectangle(100,100,1100,540, fill = "white", outline = "")
        t1 = s.create_text(600,200, text = "Game Over!", font = ("Georgia",40, "bold"), fill = "#0e7a3d")
        t2 = s.create_text(600,300, text = "you lasted for " +timeLasted+ " seconds", font = ("Georgia",18))
        t3 = s.create_text(600,350, text = "you solved " + str(score) + word, font = ("Georgia",18))
        s.update()
        s.delete(backing,t1, t2, t3)

    playAgain.destroy()
    difficultyScreen() #lets user change difficulty for the new game if they wish

def playAgainPressed():
    global mode
    mode = "difficulty"
    
root.after(500, introScreen)
s.bind("<Key>", keyDownHandler)
s.pack()
s.focus_set()
root.mainloop()
