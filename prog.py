from pyo import*
class MyInstrument(EventInstrument):
    def __init__(self, **args):
        EventInstrument.__init__(self, **args)

        # self.freq is derived from the 'degree' argument.
        self.phase = Phasor([self.freq, self.freq * 1.003])

        # self.dur is derived from the 'beat' argument.
        self.duty = Expseg([(0, 0.05), (self.dur, 0.5)], exp=4).play()

        self.osc = Compare(self.phase, self.duty, mode="<", mul=1, add=-0.5)

        # EventInstrument created the amplitude envelope as self.env.
        self.filt = ButLP(self.osc, freq=5000, mul=self.env).out()
        self.ended=False


s=Server().boot()
# freq=SigTo(440)
numberOfEvents=10
eventList=[Events() for i in range(numberOfEvents)]
eEndedList=[True for i in range(numberOfEvents)]

eEnded=False
e=Events()
def EventEnded():
    print('hello')
    print( EventKey("instr",e))
    global eEnded
    eEnded=True
freq=Sig(100)
e = Events(
instr=MyInstrument,
freq=EventSeq([freq],occurrences=1),
db=-10,
attack=0.1,
decay=0.05,
sustain=1,
release=1,
dur=2,
atend= EventEnded
).play()

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
        global eEnded
        # print(e.getCurrentDict())
        # freq.setValue(args[0])
        # print(eEnded)'
        # if eEnded:
        eEnded=False
        freq.setValue(args[0])
        # print(args[0])
        e.play()

port = 9900

s.amp=0.25

rec =OscDataReceive(port=port,address="/data/*",function = GetData)



# Sends new frequencies to the resonator filters.
sender2 = OscDataSend(types="ffff", port=9900, address="/data/main", host="127.0.0.1")
def change():
    "Randomly chooses new frequencies and sends them to the filters."
    sender2.send([random.uniform(250, 1000) for i in range(4)])
# Call the change() function every 2 seconds.
pat2 = Pattern(change,Sine(0.1,mul=1,add=1.5)).play()
s.gui(locals())