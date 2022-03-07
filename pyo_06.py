# from pyo import *

# s = Server().boot()

# ### Using multichannel-expansion to create a square wave ###

# # Sets fundamental frequency.
# # freq = 100
# # # Sets the highest harmonic.
# # high = 20

# # # Generates the list of harmonic frequencies (odd only).
# # harms = [freq * i for i in range(1, high) if i % 2 == 1]
# # # Generates the list of harmonic amplitudes (1 / n).
# # amps = [0.33 / i for i in range(1, high) if i % 2 == 1]

# # # Creates all sine waves at once.
# # a = Sine(freq=harms, mul=amps).out()
# # # Prints the number of streams managed by "a".
# # print(len(a))

# # # The mix(voices) method (defined in PyoObject) mixes
# # # the object streams into `voices` streams.
# # b = a.mix(voices=2).out()

# # # Displays the waveform.

# a = SumOsc(
#     freq=[100, 150.2, 200.5, 250.7],
#     ratio=[0.501, 0.753, 1.255],
#     index=[0.3, 0.4, 0.5, 0.6, 0.7, 0.4, 0.5, 0.3, 0.6, 0.7, 0.3, 0.5],
#     mul=0.05,
# )

# # Adds a stereo reverberation to the signal
# rev = Freeverb(a.mix(2), size=0.80, damp=0.70, bal=0.30)
# rev.out()
# # a=a.mix(2).out()
# print(len(a))
# sc = Scope(rev)

# # Sets fundamental frequency and highest harmonic.
# # freq = 100
# # high = 20

# # # Generates lists for frequencies and amplitudes
# # harms = [freq * i for i in range(1, high) if i % 2 == 1]
# # amps = [0.33 / i for i in range(1, high) if i % 2 == 1]

# # # Creates a square wave by additive synthesis.
# # a = Sine(freq=harms, mul=amps)
# # print("Number of Sine streams: %d" % len(a))

# # # Mix down the number of streams of "a" before computing the Chorus.
# # b = Chorus(a.mix(2), feedback=0.5).out()
# # print("Number of Chorus streams: %d" % len(b))

# # Creates a Server with 8 channels
# # s = Server(nchnls=8).boot()

# # Generates a sine wave
# # amps = [0.05, 0.1, 0.15, 0.2, 0.25, 0.3, 0.35, 0.4]
# # a = Sine(freq=500, mul=amps)

# # # Mixes it up to four streams
# # # b = a.mix(4)
# # Outputs to channels 0, 2, 4 and 6
# s.gui(locals())