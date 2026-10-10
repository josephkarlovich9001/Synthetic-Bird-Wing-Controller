import StepperController

WingCTL=StepperController.Steppers()
WingCTL.addStepper(pins=[1,2,3,4], ID="a")
WingCTL.addStepper(pins=[5,6,7,8], ID="B")



#This code is specilized for moving the wing

def rotate():
    WingCTL.runM(ID=["a", "b"], dis=[200,-200], speed=[None, None, None])
    WingCTL.runM(ID=["a", "b"], dis=[-200, 200], speed=[None, None, None])

def UpDown():
    WingCTL.runM(ID=["a", "b"], dis=[200,200], speed=[None, None, None])
    WingCTL.runM(ID=["a", "b"], dis=[-200,-200], speed=[None, None, None])

def UpDown():
    WingCTL.runM(ID=["a", "b"], dis=[200,200], speed=[None, None, None])
    WingCTL.runM(ID=["a", "b"], dis=[-200,-200], speed=[None, None, None])
