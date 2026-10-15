#%%%import machine
#%%%import time


class Stepper():

    def __init__(self, pins=[]):
        self.pattern = [[1,0,0,0],
                        [0,1,0,0],
                        [0,0,1,0],
                        [0,0,0,1]]
        self.stop = [0,0,0,0]
        self.step = 0
        self.pins = []
        for i in pins:
                    try:
                        print(f"Appended pin {i}")
                        pin = i
                        #%%%pin = machine.Pin(pin, machine.Pin.OUT)
                        self.pins.append(pin)
        
                    except:
                        print("Pin error")
  
    def step(self, distance=0):

        if distance < 0:
            self.step -= 1
            distance += 1
        elif distance > 0:
            self.step += 1
            distance -= 1
        
        self.step = self.step % 4
        trigger = self.pattern[self.step]
        for i in range(len(self.pins)):
            #%%%self.pins[i].value(trigger[i])
            continue
        print(f"stepping - {distance} - {i}")
        return(distance)

    def Stop(self):
            for i in range(len(self.pins)):
                #%%%self.pins[i].value(self.stop[i])
                continue
            print(f"stopping - {self.stop}") 



class Controller():

    def __init__(self):
        self.motors = []
        self.speed = []
        self.Csleep=[]
        self.sleep=[]
        self.distance = []
        self.file = ""
        self.fileIndex=[]
        self.Cindex = []
        self.ID = []
        self.numMotors=0
        self.perMotor = []
        self.running = 0
        self.stepsPerRev = []
        self.sleepIndex=[]

    def AddMotor(self, ID="a", pins=[1,2,3,4], stepsPerRev=200):
        #print(f"Added Motor {ID}")
        self.perMotor.append(self.numMotors)
        self.numMotors+=1

        motor = Stepper(pins=pins)
        self.motors.append(motor)
        self.ID.append(ID)
        self.stepsPerRev.append(stepsPerRev)
        
        self.sleep.append([])
        self.Csleep.append([])
        self.distance.append([])
        self.speed.append([])
        self.fileIndex.append(-1)
        self.Cindex.append(0)
        self.sleepIndex.append([])
       

    def ReadFile(self, file="Bcode.txt"):
        self.file = file
        f = open(self.file, "r")
        for i in f:
            
            line = i.split(",")
            line.remove(line[-1])
            try:
                for l in self.perMotor:
                    
                        if line[0] == self.ID[l]:
                            
                            self.distance[l].append(int(line[1]))
                            self.speed[l].append(int(line[2]))
                            self.fileIndex[l] += 1

            except:
                print(f"Skipped line")

            for i in self.perMotor:
                 self.Cindex[i] = 0
                 
    def Run(self, file = "Bcode.txt", ID=[]):
        
        self.ReadFile(file=file)
        #%%%time.sleep(1)
        self.SetTimer()
        self.Timer()
        while self.running != self.numMotors:
            for i in self.perMotor:
                if self.distance[i][self.Cindex[i]] != 0:
                    print(self.distance[i][self.Cindex[i]])
                    motor = self.motors[i]
                    distance = self.distance[i][self.Cindex[i]]
                    self.distance[i][self.Cindex[i]]=motor.step(self.distance[i][self.Cindex[i]])
                    #%%%time.sleep(self.Csleep[self.sleepIndex])
                    self.sleepIndex[i] += 1
                else:
                    self.Cindex[i] += 1
                    self.Timer()
                    
    def SetTimer(self):
       
        for i in self.perMotor:
            distance=self.distance[i]
            for speed in range(len(self.speed[i])):
                try:
                    self.sleep[i].append(1/self.speed[i][speed])
                except:
                    print(f"End of motor {self.ID[i]}")
        

    def Timer(self):
        #print(self.ID)
        print(self.sleep)
        #print(self.distance)

        for i in self.perMotor:
            #print("New Motor")
            if self.Cindex[i] == 0:
                self.Csleep[i] = []
                self.sleepIndex[i] = 0
                for speed in range(self.fileIndex[i]):
                    for distance in range(self.distance[i][speed]):
                        times = []   
                        for add in self.perMotor:
                            try:
                                times.append(self.sleep[add][speed])
                            except:
                                continue
                        #print(f"Speeds:{times} Distance until {distance}")
                        for time in times:
                            #print(self.sleep[i][speed])
                            self.Csleep[i].append(time-times[i%self.numMotors])    
                            
            else:
                continue
            print(self.Csleep)
        

    
test = Controller()
test.AddMotor(ID="1", pins=[1,2,3,4])
test.AddMotor(ID="2", pins=[5,6,7,8])
test.AddMotor(ID="3", pins=[9,10,11,12])

test.Run("Bcode.txt")