#This code is made for the NodeMCU-S3 an ESP32 dev-board
#It depends on the machine liberary provided by micropython, to run this code use the
#Thonny IDE as a brige to the micrio controller, there are VS code varients

#This segment of code is my own stepper controller library
#import machine
#import time

#This code is for controlling steepers with the L298N Dual H-Bridge Motor controller
class Steppers():

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


    def Rotate(self, distance=0, dir=None, speed=None):
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
            while self.distanceOff != 0:
            #for i in range(10):
                self.trigger()
                
            




Test = Steppers(pins=[1,2,3,4])

Test.Rotate(10)