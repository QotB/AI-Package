from pyknow import *

def check(lst, age):
    # print(lst)
    child = (age <= 5)
    low = 0
    high = 0
    for ans in lst:
        if ans == 'shakiness' or ans == 'hunger' or ans == 'sweating' or ans == 'headache' or ans == 'pale':
            low += 1
        if ans == 'thirst' or ans == 'blurred vision' or ans == 'headache' or ans == 'dry mouth' or ans == 'smelling breath' or ans == 'shortness of breath':
            high += 1
    if (child and low > 2):
        return "low sugar"
    elif child and high > 2:
        return "high sugar"
    return "no"

def getAns():
    s = input("Do any one of your parents diabetic(yes/no)? ")
    if (s == 'yes'):
        return True
    else:
        return False

def getAns2(s):
    s = input("Do you have " + s + " (yes/no)? ")
    if (s == 'yes'):
        return True
    else:
        return False

class Medical(KnowledgeEngine):
    @DefFacts()
    def _initial_action(self):
        yield Fact(action='check')

    @Rule(Fact(action='check'),
          NOT(Fact(agee=W())))
    def ask_age(self):
        self.declare(Fact(agee=int(input("How old are you? "))))

    @Rule(Fact(action='check'),  # take symptoms
          Fact(agee=MATCH.agee))
    def ask_symb(self, agee):
        low = 0
        heigh = 0
        if (agee<=5):
            print(
                "our system will check with you about the state of your sugar so please answer the following question carfelly ")
            if (getAns2("shakiness")):
                low += 1
            if (getAns2("hunger")):
                low += 1
            if (getAns2("sweating")):
                low += 1
            if (getAns2("headache")):
                low += 1
                heigh += 1
            if (getAns2("pale")):
                low += 1
            if (getAns2("thirst")):
                heigh += 1
            if (getAns2("blurred vision")):
                heigh += 1
            if (getAns2("dry mouth")):
                heigh += 1
            if (getAns2("smelling breath")):
                heigh += 1
            if (getAns2("shortness of breath)")):
                heigh += 1

        if (low > 2):
            self.declare(Fact(sugar="low sugar"))
        elif (heigh > 2):
            self.declare(Fact(sugar="high sugar"))
        else:
            self.declare(Fact(sugar="no"))

    @Rule(Fact(action='check'), Fact(diabeticParents=MATCH.diabeticParents), Fact(sugar=MATCH.sugar))
    def diab(self, diabeticParents, sugar):
        if (diabeticParents == True and sugar == 'low sugar'):
            print("You could be diabetic")

    @Rule(Fact(action='check'), NOT(Fact(diabeticParents=W())), Fact(sugar=MATCH.sugar))
    def ask_parentsdiab(self, sugar):
        if (sugar == 'low sugar'):
            self.declare(Fact(diabeticParents=getAns()))
        else:
            self.declare(Fact(diabeticParents=False))

    @Rule(Fact(action='check'),
          NOT(Fact(runnyNose=W())), NOT(Fact(cough=W())))
    def runny(self):
        self.declare(Fact(runnyNose=getAns2("runny nose")))
        self.declare(Fact(cough=getAns2("cough")))

    @Rule(Fact(action='check'), Fact(runnyNose=MATCH.runnyNose), Fact(cough=MATCH.cough), Fact(agee=MATCH.agee))
    def cold(self, runnyNose, cough, agee):
        if (runnyNose == True and cough == True):
            print("you have cold")
            self.declare(Fact(cold=True))
        else:
            self.declare(Fact(cold=False))

    @Rule(Fact(action='check'), Fact(cold=MATCH.cold), Fact(agee=MATCH.agee))
    def measles(self, cold, agee):
        yes = True
        if agee <= 5 and cold:
            yes &= getAns2("brownish-pink rash")
            yes &= getAns2("high and fast temperature")
            yes &= getAns2("bloodshot eyes")
            yes &= getAns2("white spots inside cheek")
        else:
            yes = False
        if yes:
            print("you have measles")

    @Rule(Fact(action='check'), Fact(agee=MATCH.agee))
    def mumps(self, agee):
        yes = True
        if agee <= 5:
            yes &= getAns2("moderate temperature")
            yes &= getAns2("saliva is not normal")
            yes &= getAns2("swollen lymph nodes in neck")
            yes &= getAns2("mouth dry")
        else:
            yes = False
        if yes:
            print("you have mumps")

    @Rule(Fact(action='check'), Fact(cold=MATCH.cold), Fact(agee=MATCH.agee))
    def mumps(self, cold, agee):
        yes = True
        if cold:
            yes &= getAns2("conjunctives")
            yes &= getAns2("strong body aches")
            yes &= getAns2("weakness")
            yes &= getAns2("vomiting")
            yes &= getAns2("sore throat")
            yes &= getAns2("sneezing")
        else:
            yes = False
        if yes:
            if (agee <= 5):
                print("you have child-flu")
            else:
                print("you have adult-flu")

####################################################################

class Plant(KnowledgeEngine):
    @DefFacts()
    def _initial_action(self):
        yield Fact(action="diagnose")

    @Rule(Fact(action='diagnose'),
          NOT(Fact(temp=W())))
    def ask_temp(self):
        self.declare(Fact(temp=input("What is the plant temperature? ")))

    @Rule(Fact(action='diagnose'),
          NOT(Fact(humidity=W())))
    def ask_humidity(self):
        self.declare(Fact(humidity=input("What is the plant humidity? ")))

    @Rule(Fact(action='diagnose'),
          NOT(Fact(tuberColor=W())))
    def ask_tuberColor(self):
        self.declare(Fact(tuberColor=input("What is the plant tuber color? ")))

    @Rule(Fact(action='diagnose'),
          NOT(Fact(tuberHas=W())))
    def ask_tuberHas(self):
        self.declare(Fact(tuberHas=input("What does the plant tuber has? ")))

    @Rule(Fact(action='diagnose'),
          NOT(Fact(tuber=W())))
    def ask_tuber(self):
        self.declare(Fact(tuber=input("What is tuber? ")))

    @Rule(Fact(action="diagnose"),
          Fact(temp=MATCH.temp),
          Fact(humidity=MATCH.humidity),
          Fact(tuberColor=MATCH.tuberColor),
          Fact(tuberHas=MATCH.tuberHas),
          Fact(tuber=MATCH.tuber))

    def diagnose(self, temp, humidity, tuberColor, tuberHas, tuber):
        if temp == "high" and humidity == "normal" and tuberColor == "reddish-brown" and tuberHas == "spots":
            print("The plant has black heart")
            self.reset()
            self.run()
        elif temp == "low" and humidity == "high" and tuber == "normal" and tuberHas == "spots":
            print("The plant has late blight")
            self.reset()
            self.run()
        elif temp == "high" and humidity == "normal" and tuber == "dry" and  tuberHas == "circles":
            print("The plant has dry rot")
            self.reset()
            self.run()
        elif temp == "normal" and humidity == "normal" and tuberColor == "brown" and tuberHas == "wrinkles":
            print("The plant has early blight")
            self.reset()
            self.run()
        else:
            print("Please check again")
            self.reset()
            self.run()

while True:
    if input("which class you want to test? ") == 'medical':
        engine = Medical()
        engine.reset()  # Prepare the engine for the execution.
        engine.run()
    else:
        engine = Plant()
        engine.reset()  # Prepare the engine for the execution.engine.run()  # Run it!
        engine.run()
    s = input("Do you want to have another test?(yes/no)")
    if s == 'no':
        break
