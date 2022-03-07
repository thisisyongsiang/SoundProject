import math
import numpy as np
import matplotlib.pyplot as plt
import itertools
from abc import ABC,abstractmethod

class Oscillator(ABC):
    def __init__(self,freq=440,phase=0,amp=1,
        sampleRate=44100,waveRange=(-1,1)):
        self._freq = freq
        self._amp = amp
        self._phase = phase
        self._sampleRate = sampleRate
        self._waveRange = waveRange
        # Properties that will be changed
        self._f = freq
        self._a = amp
        self._p = phase
    @property
    def InitFreq(self):
        return self._freq
    @property
    def InitAmp(self):
        return self._amp
    @property
    def InitPhase(self):
        return self._phase
    @property
    def freq(self):
        return self._f
    
    @freq.setter
    def freq(self, value):
        self._f = value
        self._postFreqSet()
    @property
    def amp(self):
        return self._a
    
    @amp.setter
    def amp(self, value):
        self._a = value
        self._postAmpSet()
        
    @property
    def phase(self):
        return self._p
    
    @phase.setter
    def phase(self, value):
        self._p = value
        self._postPhaseSet()
        
    def _postFreqSet(self):
        pass
    
    def _postAmpSet(self):
        pass
    
    def _postPhaseSet(self):
        pass
    
    @abstractmethod
    def _initializeOsc(self):
        pass    
    
    @staticmethod
    def squish_val(val, min_val=0, max_val=1):
        return (((val + 1) / 2 ) * (max_val - min_val)) + min_val

    @abstractmethod
    def __next__(self):
        return None
    
    def __iter__(self):
        self.freq = self._freq
        self.phase = self._phase
        self.amp = self._amp
        self._initializeOsc()
        return self
        
class SineOscillator(Oscillator):
    def _postFreqSet(self):
        self._step = (2 * math.pi * self._f) / self._sampleRate
        
    def _postPhaseSet(self):
        self._p = (self._p / 360) * 2 * math.pi
        
    def _initializeOsc(self):
        self._i = 0
        
    def  __next__(self):
        val = math.sin(self._i + self._p)
        self._i = self._i + self._step
        if self._waveRange is not (-1, 1):
            val = self.squish_val(val, *self._waveRange)
        return val * self._a

class SquareOscillator(SineOscillator):

    def __init__(self,freq=440,phase=0,amp=1,
        sampleRate=44100,waveRange=(-1,1), threshold=0):
        super().__init__(freq, phase, amp, sampleRate, waveRange)
        self.threshold = threshold

    def __next__(self):
        val = math.sin(self._i + self._p)
        self._i = self._i + self._step
        if val < self.threshold:
            val = self._waveRange[0]
        else:
            val = self._waveRange[1]
        return val * self._a


class SawtoothOscillator(Oscillator):
    def _postFreqSet(self):
        self._period = self._sampleRate / self._f
        self._postPhaseSet
        
    def _postPhaseSet(self):
        self._p = ((self._p + 90)/ 360) * self._period
    
    def _initializeOsc(self):
        self._i = 0
    
    def __next__(self):
        div = (self._i + self._p )/self._period
        val = 2 * (div - math.floor(0.5 + div))
        self._i = self._i + 1
        if self._waveRange is not (-1, 1):
            val = self.squish_val(val, *self._waveRange)
        return val * self._a

class TriangleOscillator(SawtoothOscillator):

    def __next__(self):
        div = (self._i + self._p )/self._period
        val = 2 * (div - math.floor(0.5 + div))
        val=(abs(val)-0.5)*2
        self._i = self._i + 1
        if self._waveRange is not (-1, 1):
            val = self.squish_val(val, *self._waveRange)
        return val * self._a


class WaveAdder:
    def __init__(self, *oscillators):
        self.oscillators = oscillators
        self.n = len(oscillators)
    
    def __iter__(self):
        [iter(osc) for osc in self.oscillators]
        return self
    
    def __next__(self):
        return sum(next(osc) for osc in self.oscillators) / self.n