import random
from pyo import *
#Set-ExecutionPolicy -ExecutionPolicy RemoteSigned -Scope Process
#.venv\scripts\activate

s=Server().boot()

# Infinite sustain for the global envelope.
globalamp = Fader(fadein=2, fadeout=2, dur=0).play()

# Envelope for discrete events, sharp attack, long release.
env = Adsr(attack=0.01, decay=0.1, sustain=0.5, release=1.5, dur=100, mul=0.5)
# setExp method can be used to create exponential or logarithmic envelope.
env.setExp(0.75)


sig = SuperSaw(freq=[100, 101], detune=0.6, bal=0.8, mul=globalamp*env ).out()
# soundS=Mix(Sine(freq1),2,mul=globalamp * env).out()

def GetData(address,*args):
    print(args)
    print(address)
    '''
    needs to receive certain info.
    type of sound (controls the ATTACK DECAY RELEASE)
    duration
    amplitude
    frequency
    '''
    if "/main" in address:
        print(sig.get(True))
        if sig.get(True)[0]!=0:
            print(sig.getBaseObjects()[0]._getStream())
            print('hi')
        else:
            sig.freq=[args[0],args[1]]

            env.attack = random.uniform(0.002, 0.01)
            env.decay = random.uniform(0.1, 0.5)
            env.sustain = random.uniform(0.3, 0.6)
            env.release = random.uniform(0.8, 1.4)
            env.dur=100
            env.play()
            sig.out()
port = 9900


rec =OscDataReceive(port=port,address="/data/*",function = GetData)



# Sends new frequencies to the resonator filters.
sender2 = OscDataSend(types="ffff", port=port, address="/data/main", host="127.0.0.1")
def change():
    "Randomly chooses new frequencies and sends them to the filters."
    sender2.send([random.uniform(100, 1000) for i in range(4)])
# Call the change() function every 2 seconds.
pat2 = Pattern(change,Sine(0.1,mul=1,add=2)).play()
s.gui(locals())