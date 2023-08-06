import time
import math
import rtmidi
from .MidiPlus import MidiPlus

def main():
    # Port name we are looking for
    port_name = "FIT"
    in_port_num = -1
    out_port_num = -1

    midiin = rtmidi.MidiIn()
    available_ports = midiin.get_ports()
    for idx, name in enumerate(available_ports):
        if name[0:len(port_name)] == port_name:
            in_port_num = idx

    midiout = rtmidi.MidiOut()
    available_ports = midiout.get_ports()
    for idx, name in enumerate(available_ports):
        if name[0:len(port_name)] == port_name:
            out_port_num = idx

    if in_port_num == -1:
        raise BaseException("could not find midi in device")
    if out_port_num == -1:
        raise BaseException("could not find midi out device")

    mp = MidiPlus(in_port_num, out_port_num)
    mp.clear_screens()
    for fader in mp.faders:
        fader.set_fader(0)

    t = 0
    base = 16384
    def set_base(_, pos):
        nonlocal base
        base = pos
    mp.faders[16].register_callback("fader_move", set_base)
    while True:
        for idx, fader in enumerate(mp.faders):
            raw_val = math.sin(t+idx)
            val = int(base + ( raw_val * 16384) * 0.5)
            val = max(0, val)
            val = min(32768, val)
            fader.set_fader(val)
        t = t + 1
        time.sleep(0.05)
    # for cmd in range(0xAA, 0xAF):
    #     print
    #     for key in range(0x00, 0xFF+1):
    #         for vel in range(0x00, 0xFF+1):
    #             # mp.faders[0].set_row(1, "0x%02x" % cmd)
    #             # mp.faders[0].set_row(2, "0x%02x" % key)
    #             # mp.faders[0].set_row(3, "0x%02x" % vel)
    #             mp.midi_out.send_message([cmd, key, vel])
    # mp.clear_screens()
if __name__ == "__main__":
    main()