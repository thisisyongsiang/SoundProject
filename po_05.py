from pyo import *
import random

s = Server().boot()

# # A python integer (or float).
# anumber = 100

# # Conversion from number to an audio stream (vector of floats).
# astream = Sig(anumber)

# # Use a Print (capital "P") object to print an audio stream.
# pp = Print(astream, interval=0.1, message="Audio stream value")

# # Use the get() method to extract a float from an audio stream.
# print("Float from audio stream : ", astream.get())
# 2 seconds linear ramp starting at 0.0 and ending at 0.3.
# amp = SigTo(value=0.3, time=2.0, init=0.0)

# # Pick a new value four times per second.
# pick = Choice([200, 250, 300, 350, 400], freq=4)

# # Print the chosen frequency
# pp = Print(pick, method=1, message="Frequency")

# # Add a little portamento on an audio target and detune a second frequency.
# freq = SigTo(pick, time=0.01, mul=[1, 1.005])
# # Play with portamento time.
# freq.ctrl([SLMap(0, 0.25, "lin", "time", 0.01, dataOnly=True)])

# # Play a simple wave.
# sig = RCOsc(freq, sharp=0.7, mul=amp).out()

# 2 seconds linear ramp starting at 0.0 and ending at 0.3.
# amp = SigTo(value=0.3, time=2.0, init=0.0)

# # Pick a new value four times per second.
# pick = Choice([200, 250, 300, 350, 400], freq=4)

# # Print the chosen frequency
# pp = Print(pick, method=1, message="Frequency")

# # Add an exponential portamento on an audio target and detune a second frequency.
# # Sharp attack for rising notes and long release for falling notes.
# freq = Port(pick, risetime=0.001, falltime=0.25, mul=[1, 1.005])
# # Play with portamento times.
# freq.ctrl()

# # Play a simple wave.
# sig = RCOsc(freq, sharp=0.7, mul=amp).out()

# Infinite sustain for the global envelope.
# globalamp = Fader(fadein=2, fadeout=2, dur=0).play()

# # Envelope for discrete events, sharp attack, long release.
# env = Adsr(attack=0.01, decay=0.1, sustain=0.5, release=1.5, dur=2, mul=0.5)
# # setExp method can be used to create exponential or logarithmic envelope.
# env.setExp(0.75)

# # Initialize  a simple wave player and apply both envelopes.
# sig = SuperSaw(freq=[100, 101], detune=0.6, bal=0.8, mul=globalamp * env).out()


# def play_note():
#     "Play a new note with random frequency and jitterized envelope."
#     freq = random.choice(midiToHz([36, 38, 41, 43, 45]))
#     # sig.freq = [freq, freq * 1.005]
#     env.attack = random.uniform(0.002, 0.01)
#     env.decay = random.uniform(0.1, 0.5)
#     env.sustain = random.uniform(0.3, 0.6)
#     env.release = random.uniform(0.8, 1.4)
#     # Start the envelope for the event.
#     env.play()


# # Periodically call a function.
# pat = Pattern(play_note, time=2).play()

s = Server().boot()

# Randomly built 10-points amplitude envelope.
t = 0
points = [(0.0, 0.0), (2.0, 0.0)]
for i in range(8):
    t += random.uniform(0.1, 0.2)
    v = random.uniform(0.1, 0.9)
    points.insert(-1, (t, v))

amp = Expseg(points, exp=3, mul=0.3)
amp.graph(title="Amplitude envelope")

sig = RCOsc(freq=[150, 151], sharp=0.85, mul=amp)

# A simple linear function to vary the amount of frequency shifting.
sft = Linseg([(0.0, 0.0), (0.5, 20.0), (2, 0.0)])
sft.graph(yrange=(0.0, 20.0), title="Frequency shift")

fsg = FreqShift(sig, shift=sft).out()

rev = WGVerb(sig + fsg, feedback=0.9, cutoff=3500, bal=0.3).out()


def playnote():
    "Start the envelopes to play an event."
    amp.play()
    sft.play()


# Periodically call a function.
pat = Pattern(playnote, 2).play()
s.gui(locals())