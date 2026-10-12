

class Control():

    def __init__(self, pins=[None, None, None, None], stepsPerRev=200, speed=500, step=0, ID="a"):
        self.time=0
        self.ID=ID
        self.pattern = [[1,0,0,0],
                        [0,1,0,0],
                        [0,0,1,0],
                        [0,0,0,1]]
        self.distance = 0
        self.speed=speed
        self.stepsPerRev=stepsPerRev
        self.step=step
        self.stop = [0,0,0,0]
        self.pins = []
        for i in pins:
            if i == None:
                print("Missing Pins")
                break
            else:
                #%%%pin = machine.Pin(i, machine.Pin.OUT)
                #%%%self.pins.append(pin)
                print(f'appended {i}')

    def Step(self):
            
            if self.distance < 0:
                self.step -= 1
                self.distance += 1
            elif self.distance > 0:
                self.step += 1
                self.distance -= 1

            self.step = self.step % 4
            trigger = self.pattern[self.step]
            for i in range(len(self.pins)):
            #%%%self.pins[i].value(trigger[i])
                continue
            print(f"stepping - {self.distance} - {trigger}")
            return(self.distance)

    def Stop(self):
        for i in range(len(self.pins)):
            #%%%self.pins[i].value(self.stop[i])
            continue
        print(f"stopping - {self.stop}")        

    def Set(self, speed=None, distance=None):
        if speed != None:
            try:
                if speed > 0:
                    self.speed = speed
                else:
                    print("Negitive Speed Error")
            except:
                print("Speed Error")
        if distance != None:
                try:
                    self.distance = distance        
                except:
                    print("Distance Error")

    def Get(self):
        return [self.ID, self.speed, self.distance]




class Stepper():

    def __init__(self, ID=[], time=0, currentSpeed=[], currentDistance=[], motors=[]):
        self.time=time
        self.ID = ID
        self.cSpeed=currentSpeed
        self.cDistance = currentDistance
        self.motors=motors
        self.count = 0

    def addMotor(self, pins=[], ID="a"):
        self.count += 1
        motor=Control(pins=pins, ID=ID)
        self.motors.append(motor)
        self.ID.append(ID)
        for i in range(self.count):
            if self.ID[i] == ID:
                data = self.motors[i]
                data = data.Get()
                self.cDistance.append(data[2])
                self.cSpeed.append(data[1])
    def Set(self, ID="a", speed=None, distance=None):   
              for i in range(self.count):
                   if self.ID[i] == ID:
                        motor=self.motors[i]
                        motor.Set(speed, distance)
                        

               
    def Run(self, ID=[], dis=[], sp=[]):
        index = []
        for i in range(self.count):
            if self.ID[i] in ID:
                index.append(i)
                for c in range(len(ID)):
                    if self.ID[i] == ID[c]:
                        data = self.motors[c]
                        self.Set(ID=self.ID[i], speed=sp[c], distance=dis[c])
                        data = data.Get()
                        self.cDistance[i] = dis[c]
                        self.cSpeed[i] = sp[c]
        done = 0
        while done < len(index):
            for i in index:
                
                if (self.cDistance[i]) != 0:
                    motor = self.motors[i]
                    motor = motor.Step()
                    self.cDistance[i] = motor
                elif (self.cDistance[i]) == 0:
                    done += 1
                    motor = self.motors[i]
                    motor = motor.Stop()
                    
    def Start(self, file="", ID=[], dis=[], sp=[]):
        
        
        def NumSort(sp=[]):
            copy_list = sp[:]
            newlist = []
            while len(copy_list) != 0:
                front = 0
                for i in copy_list:
                    if i >= front:
                        front = i
                newlist.append(front)
                copy_list.remove(front)
                
            return newlist

        def Check():
            
            wait=[]
            fastest = NumSort(sp)
            fastest = fastest[0]
            self.time = 1/fastest
            
            for i in sp:
                sleep = 1/i
                wait.append(sleep)
            return (wait)

        def Timer():
            print()

        def Read():
            f = open("Bcode.txt", "r")
            for i in f:
                line = i.split(",")
                print(line)

        Read()

test = Stepper() 
test.addMotor(pins=[1,2,3,4], ID="1")
test.addMotor(pins=[5,6,7,8], ID="2")
test.Set(ID="1",speed=100)

test.Start(ID=["1","2","3"], dis=[100,54,547], sp=[100, 500, 570])


#at speed 500 it must tick once every .002 seconds or 2 miliseconds
#at speed 100 ticks every .01 seconds or 10 miliseconds

#if 500 ticks first then 8 ms later 100 will tick, but that means 500 ticks another 4 times

#1000 is .001, 10 in the time for 100 to do one

#stop time = 1/ticksPerSecond
#find fastest stepper, 1000 and see how many times it gopes into the slowest by time

#.01/.001 = 10

#do the same for the middle

#.01/.002 = 5

#find how many times the fastest goes into that

#.002/.01 = 2

#find golobal smallest speed

#.001 = 1ms

#check motors every 1ms

#100 = 10ms
#500 = 2ms
#1000 = 1ms

#time scale

"""
Speed:Remaining
100:10
500:1
1000:0 *
______
100:9
500:0 *
1000:0
______
100:8
500:1
1000:0 *
______
100:7
500:0 *
1000:0 *

"""