# a game about picking up apples :)
# (its not so simple)
import time as t

print(
    """
Welcome to this little game about picking apples :)
Let's see whether you'll live to see yet another day^^
All you gotta do is decide between the following four options:

You can 'pick' an apple
You can also type 'skip' if you do not wish to pick an apple
With 'eat' you can, well, eat an apple
You can 'drop' your apples if you want to
And most importantly, you can 'deliver' your apples.

Doesn't sound too difficult does it? :D
Good luck!"""
)


gamerlyover = 0
deaths = 0
options = "(pick/skip/eat/drop/deliver)"
message = f"So watcha wanna do next? {options} - "
timelim = [60, 120, 180]
msrachel = 30

turnslim = 60

deliveries = [
    {"nr": 4, "dis": 4}, {"nr": 3, "dis": 5},
    {"nr": 7, "dis": 3}, {"nr": 2, "dis": 9}
]

carrylim = 10

hungerlim = 5

eatlim = 7

# the bigger the less motivation
motlim = 7

skipslim = 3
delfactor = 5
# factor by which effort of deliveries is divided by. the bigger, the less
# hunger is generated by making a delivery


def gameover():
    global breaker
    if gamerlyover == 0:
        print("""You died, the game is over!
You can try again however
""")
    else:
        print("""
YOU DIED
""")
    breaker = 1


def kill():
    if nrapples > carrylim:
        print("""
You feel a sudden flash of pain in your back. You lie down in a rash motion.
Unfortunately, the back of your skull hits a pointy stone on the ground and
breaks upon impact. You die from a severe intracerebral hemorrhage
""")
        gameover()
    elif eaten > eatlim:
        print("""
You hear a shot in the distance. Next you feel a strong cold pain
in your breast, and then, you don't feel anything anymore...
""")
        gameover()
    elif skips > skipslim:
        print("""
You really don't get a lot done today. In order to forego the inevitable
beating by your master, you decide to kill yourself with your swiss army knife
""")
        gameover()
    elif hunger > hungerlim:
        print("""
Your stomach hurts, you feel weak and faint...""")
        t.sleep(4)
        print("""
            ...forever
""")
        gameover()
    elif nrapples < 0:
        if nextdelivery == 0:
            print("""
Ms Duboise looks you over closely. From her back she draws a short
knife and stabs you in the stomach.
""")
            gameover()
        if nextdelivery == 1:
            print("""
Mrs Brodsmoth calls into the house:" Honey, could you come real quick please.
And bring that thing you like to play with so much recently."

Next you see a bulbous face appearing in the doorframe eyeing you suspiciously.
Upon that he quickly draws a gun from behind his back an shoots you in the face
""")
            gameover()
        if nextdelivery == 2:
            print("""
"YOU IMPERTINENT LITTLE KID!" yells Mr Porcroch as he grabs you by your
sholders and throws you into his dog-cage where it does not take long until
you stop feeling the dogs tearing at your flesh and ripping off your skin...
""")
            gameover()
        if nextdelivery == 3:
            print("""
The expression on the Smith's face seems to indicate he just saw the devil.
As he reaches slowly for his hammer he mumbles:" If you dare treat me like that
I shall treat you no more kindly..."
Never have you seen such a massive hammer move that quickly towards your face,
and never shall you again...
""")
            gameover()
    elif motivation > motlim:
        print("""
Recently, you have found your life to be especially bland and meaningless.
You decide to end your void existence with your swiss army knife.
""")
        gameover()


def win():
    global gamerlyover
    if nextdelivery == 3 and nrapples >= 0:
        gamerlyover = 1


def pick():
    global nrturns, nrapples, hunger, motivation, skips
    t.sleep(1)
    if nrturns % 6 == 3 and nrturns != 3:
        nrturns += 1
        print("""
While trying to pick the apple, something bit you in the hand.
it hurts but you just leave that apple alone and continue
""")
        inputt = input(message)
        do(inputt)
        if breaker != 1:
            print("""
You notice that you begin to sweat strongly for no obvious reason""")
        t.sleep(2)
        if breaker != 1:
            print("""
Also your mouth starts tingling and you start twitching in the face""")
        t.sleep(2)
        if breaker != 1:
            print("""
Nonetheless, you continue
""")
        inputt = input(message)
        do(inputt)
        if breaker != 1:
            print("""
Suddenly you need to vomit and you've now got severe muscle spasms""")
        t.sleep(3)
        if breaker != 1:
            print("""
You feel slowly loosing consciousness...""")
        t.sleep(2)
        print("\
                             ...and never wake again...\
")
        gameover()
    else:
        nrturns += 1
        nrapples += 1
        hunger += 0.4
        motivation += 1
        skips = 0
        kill()


def skip():
    global nrturns, hunger, motivation, skips
    t.sleep(1)
    nrturns += 1
    hunger += 0.2
    motivation -= 1
    skips += 1
    kill()


def eat():
    global nrturns, nrapples, hunger, eaten, motivation, skips
    t.sleep(1)
    if nrapples >= 1:
        nrturns += 1
        nrapples -= 1
        hunger = 0
        eaten += 1
        skips += 0.5
        motivation -= 2
        kill()
    else:
        nrturns += 1
        motivation += 2
        skips += 0.5
        print("""
Having tried to eat an apple without even having one in your
basket at the moment, you think strongly about your stupidity.
""")
        kill()
        if breaker != 1:
            print("""
In spite of feeling deep disappointment for yourself, you decide
not to kill yourself this time.
""")


def drop():
    global nrturns, nrapples, motivation, skips
    if nrapples < 1:
        motivation += 2
        kill()
        if breaker != 1:
            print("""
You just tried to drop 0 (zero) (!) apples (idiot)
In spite of feeling deep disappointment for yourself, you decide
not to kill yourself this time.
""")
    else:
        t.sleep(1)
        nrturns += 1
        nrapples = 0
        motivation += 2
        skips += 1
        kill()


def deliver():
    global nrturns, nrapples, hunger, motivation, skips, nextdelivery
    if nextdelivery > 3:
        print("""
You have no more deliveries to make. Your purpose is fullfilled.
This makes you depressive. You decide to end your life with your
beloved swiss army knife.
""")
        gameover()
    else:
        t.sleep(deliveries[nextdelivery]["dis"])
        skips = 0
        nrturns += 1
        journthere = deliveries[nextdelivery]["dis"] * nrapples / delfactor
        hunger += journthere
        kill()
        if breaker != 1:
            nrapples -= deliveries[nextdelivery]["nr"]
            kill()
            if breaker != 1:
                win()
                t.sleep(deliveries[nextdelivery]["dis"])
                motivation = 0
                journback1 = deliveries[nextdelivery]["dis"]
                journback2 = nrapples / delfactor
                journback = journback1 * journback2
                hunger += journback
                kill()
                nextdelivery += 1


def do(pinput):
    pinput == pinput.lower()
    if pinput == "pick":
        pick()
    elif pinput == "skip":
        skip()
    elif pinput == "deliver":
        deliver()
    elif pinput == "drop":
        drop()
    elif pinput == "eat":
        eat()
    else:
        print("Please repeat that...")


def dodo():
    inputt = input(message)
    do(inputt)
    print(
        f"nrturns {nrturns}   "
        f"nextdelivery {nextdelivery}   "
        f"nrapples {nrapples}   "
        f"hunger {hunger}   "
        f"eaten {eaten}   "
        f"motivation {motivation}   "
        f"skips {skips}   "
    )


while gamerlyover != 1:

    nrturns = 0
    nextdelivery = 0
    nrapples = 0
    hunger = 0
    eaten = 0
    motivation = 0
    skips = 0
    breaker = 0
    t1 = t.time()

    deaths += 1

    inputtt = input(f"""
It's a sunny day, you know what you gotta do so...
You wanna {options}? - """)
    do(inputtt)

    while t.time() - t1 < timelim[0] and breaker != 1:
        dodo()
        cond1 = t.time() - t1 > msrachel - 1
        cond2 = t.time() - t1 < msrachel + 1 and breaker != 1
        if cond1 and cond2:
            print("""
Ms Rachel walks by and greets you most kindly
    """)

    if breaker != 1:
        print("""
The weather is getting worse.
The sky gets covered in clouds and a fresh wind stars blowing
    """)

    while t.time() - t1 < timelim[1] and breaker != 1:
        dodo()

    if breaker != 1:
        print("""
More clouds. A faint rain starts pouring down from the sky
    """)

    while t.time() - t1 < timelim[2] and breaker != 1:
        dodo()

    if t.time() - t1 > timelim[2] and breaker != 1:
        print("""
Suddenly, an excessive downpour begins. While running for shelter,
you get struck by lightning and die""")
        gameover()


print(f"""
Congrats, you have successfully mastered the game.
You died {deaths} times. I encourage you to do better
in real life.

The lesson we learned today:

Life is not always easy. Oftentimes, all we can do
is our part for the greater good. In the end, we are all gonna die anyway.
The rich and the poor, the more powerfull and those without freedom,
The slaves and the slavemasters, the shepherd and the sheep.
We can't take anything with us when we go.
Be kind, be helpfull and treat others the way you yourself would
like to be treated.

""")
