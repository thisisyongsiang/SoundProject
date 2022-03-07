from pyo import *

s = Server().boot()


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


# We tell the Events object which instrument to use with the 'instr' argument.
e = Events(
    instr=MyInstrument,
    degree=EventSeq([5.00, 5.04, 5.07, 6.00]),
    beat=1 / 2.0,
    db=-12,
    attack=0.001,
    decay=0.05,
    sustain=0.5,
    release=0.005,
).play()

s.gui(locals())