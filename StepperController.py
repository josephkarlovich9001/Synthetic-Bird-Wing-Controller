#This code is made for the NodeMCU-S3 an ESP32 dev-board
#It depends on the machine liberary provided by micropython, to run this code use the
#Thonny IDE as a brige to the micrio controller, there are VS code varients

#This segment of code is my own stepper controller library
#import machine
#import time

#This code is for controlling steepers with the L298N Dual H-Bridge Motor controller
class Steppers():

    def __init__(self, motors=[], motorID=[], mode="goto", revolution=200):
        self.motors = motors
        self.motorID = motorID
        self.mode = mode
        self.revolution = revolution

    def addStepper(self, pins=[None, None, None, None], ID="a"):
        breaker = False
        appendPins = []
        
        for i in pins:
            if i == None:
                print("None stepper pin")
                breaker = True
            else:
                try:
                    appendPins.append(int(i))     
                except:
                    print("Invalid stepper pin")
                    breaker = True   
        if breaker:
            print("Motor with ID: " + ID + " is incorrect")
        else:
            motor = StepperCTL(pins=pins)
            self.motors.append(motor)
            self.motorID.append(ID)

#This run is intended to only run one motor, I had to change the gotoRotate fund in stepperCTL to do just one rotation, this way
#if two steppers need be used I can trigger them by ticking them both once but with another funtion that calls two or more
#instead of just one

    def run(self, ID=None, dis=None, dir=None, speed=None):
        if self.mode == "goto":
            if ID==None or dis == None:
                print("No ID or distance")
                print("goto mode on single run requires a dis=123 and ID=motorID")
            else:
                for i in range(len(self.motors)):
                    if self.motorID[i] == ID:
                        move=self.motors[i]
                        distance = dis
                        print(self.motorID[i])
                        while distance != 0:
                            distance = move.gotoRotate(distance, dir, speed)
                            #print(distance)
                            
                            
    def runM(self, ID=[], dis=[], dir=[], speed=[]):
        if self.mode == "goto":
            if len(ID)== 0 or len(dis) == 0:
                print("Error")
                print("goto mode on multible run requires a dis=[1,2,3] and ID=[a,b,c]")
            else:
                stop = False
                distance = dis
                triggerlist = []
                for i in range(len(self.motors)):
                    if self.motorID[i] == ID:
                        triggerlist.append(self.motors[i])
                        print(len(triggerlist))
                        while stop == False:
                            done = 0
                            for i in range(len(distance)):
                                if distance[i] != 0:
                                    move=triggerlist[i]
                                    distance[i] = move.gotoRotate(distance, dir, speed)
                                    print(distance)
                                else:
                                    done += 1
                            if done == len(triggerlist):
                                stop = True
    def veiw(self):
        for i in range(len(self.motorID)):
            pinprint = self.motors[i]
            pins = pinprint.veiw()
            print(f"ID:{self.motorID[i]} - Pins:{pins}")
                            
                            
                            
class StepperCTL():

    def __init__(self, pins=[None, None, None, None], speed=1/100, direction=1, distanceOff=0 ):
        self.PinList = [[1,0,0,0],
                        [0,1,0,0],
                        [0,0,1,0],
                        [0,0,0,1]]
        self.stop = [0,0,0,0]

        self.pins = pins

        self.currentPin = 0
        self.direction = direction
        self.speed = speed
        self.distanceOff = distanceOff

    def veiw(self):
        return self.pins
        

    def ShowGrid(self):
        for i in self.Pins:
            print(i)

    def setGrid(self):
        modifyer=1
        if self.distanceOff > 0:
            modifyer = -1
        if self.direction == 1:
            self.currentPin -= 1*modifyer
            self.distanceOff += 1*modifyer
        elif self.direction == 0:
            self.currentPin += 1*modifyer
            self.distanceOff -= 1*modifyer
    
        self.currentPin = self.currentPin % 4
        return self.PinList[self.currentPin]

    def trigger(self):
        triggers = self.setGrid()
        for i in range(4):
            #Machine mod here, must use micropython interpreter
#            ________________________TEST UNCOMMENT BELOW_______________________________
            #machine.Pin(self.pins[i], triggers[i])
            print(f"Pin:{self.pins[i]} Trigger:{triggers[i]}")
        print(f"Distance: {self.distanceOff}")


    def gotoRotate(self, distance=0, dir=None, speed=None):
        #In this code forward is equal to 1, cw can also be used
        #and the same for backwards which is 0 or ccw
        #you can also just set negitive distance to go reverse what is set
        breaker = False
        if distance != 0:
            self.distanceOff = distance
        else:
            print("Error, No Movement")
            breaker = True
        if dir != None:
            if dir == "cw":
                self.direction = 1
            elif dir == "ccw":
                self.direction = 0
            elif dir == 1 or dir == 0:
                self.direction = dir
            else:
                print("Error, incorrect rotation syntax")
        if speed != None:
            try:
                speed = int(speed)
                self.speed=(1/speed)
            except:
               print("Speed calcualtion error, enter an integer")
        for i in self.pins:
                if i == None:
                    print("4 Pins Required")
                    breaker = True
        if not breaker:
            #while self.distanceOff != 0:
            #for i in range(10):
            self.trigger()
            return(self.distanceOff)
                
            




Test = Steppers()
Test.addStepper(pins=[1,2,3,4], ID="a")
Test.addStepper(pins=[5,6,7,8], ID="b")
Test.addStepper(pins=[5,6,7,8], ID="b")
Test.run(ID="b", dis=4)
#Test.veiw()
#Test.runM(ID=["a","b"], dis=[4,-4])