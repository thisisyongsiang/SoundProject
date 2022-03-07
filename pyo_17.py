from pyo import *

s = Server().boot()

# The sound table to granulate.
# table = SndTable("C:\\Users\\yongsiang\\Desktop\\Work\\Sound\\scripts\\.venv\\Lib\\site-packages\\pyo\\examples\\snds\\flute.aif")

# Listen addresses '/density', '/position', '/pitch_rand' and '/duration' on port 9000.
# rec = OscReceive(port=9000, address=["/density", "/position", "/pitch_rand", "/duration","/leftChannel","/rightChannel"])

# # Sets initial values for the OSC streams. This allow the program to run with
# # minimal behaviour even if no message have been sent on these addresses.
# rec.setValue("/density", 0.5)
# rec.setValue("/position", 0.5)
# rec.setValue("/pitch_rand", 0.0)
# rec.setValue("/duration", 0.5)
# rec.setValue("/leftChannel", 0.1)
# rec.setValue("/rightChannel", 0.1)
# # Density of grains, between 1 and 250 grains per second.
# dens = SigTo(rec["/density"], time=0.05, mul=249, add=1)
# print(rec["/density"])
# print(rec.get("/density"))
# print(dens)
# # Reading position, in samples, in the table + little jitter noise.
# pos = SigTo(rec["/position"], time=0.05, mul=table.getSize(), add=Noise(100))

# # Amplitude of a jitter noise around 1.0 to control the pitch of individual grains.
# rpit = SigTo(rec["/pitch_rand"], time=0.05, mul=0.2, add=0.001)
# pit = Noise(mul=rpit, add=1)

# # Grain duration, between 0.025 and 0.5 second.
# dur = SigTo(rec["/duration"], time=0.05, mul=0.475, add=0.025)


# leftC = SigTo(rec["/leftChannel"], time=0.05, mul=1, add=0)
# rightC = SigTo(rec["/rightChannel"], time=0.05, mul=1, add=0)

# grain = Particle(
#     table=table,  # table to read samples from.
#     env=HannTable(),  # grain envelope.
#     dens=dens,  # density of grains per second.
#     pitch=pit,  # pitch of grains.
#     pos=pos,  # position in the table where to start the grain.
#     dur=dur,  # grain duration.
#     dev=0.01,  # Maximum deviation of the starting time of the grain.
#     pan=Noise(0.5, 0.5),  # Panning factor of the grain.
#     mul=[leftC,rightC],
# ).out()

def getDataMessage(address,*args):
    print(len(args))

source = SfPlayer("C:\\Users\\yongsiang\\Desktop\\Work\\Sound\\scripts\\.venv\\Lib\\site-packages\\pyo\\examples\\snds\\flute.aif",loop=True,mul=0.7)

rec=OscDataReceive(port = 9002,address='/4/xy',function=getDataMessage)


rec = OscListReceive(port=9002, address='/4/xy',num=2)
rec.setValue("/4/xy", [0.5, 0.5])
disto = Disto(source, drive=Sqrt(rec["/4/xy"][0]), slope=Sqrt(rec["/4/xy"][1]), mul=0.5).mix(2).out()
s.gui(locals())