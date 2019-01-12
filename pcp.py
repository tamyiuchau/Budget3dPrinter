import serial
import struct
import math
#Constants
R_MAX = 400 #max rotation
R_MIN = 0
R_STEP = 2
R_RATIO = math.pi*(R_MAX/2)
H_MAX = 800
H_MIN = 0
H_STEP = 1
H_RATIO = 1
D_MAX = 100
D_MIN = 0
D_RATIO = 1
#Formating
TX_FMT = 'LL'
RX_FMT = 'LLL' # l: signed long, L: unsigned long, f float
RX_L = struct.calcsize(RX_FMT)

def calculate(r,h,d):
    dd = d*D_RATIO
    rr = r*R_RATIO
    x = dd*cos(rr)
    y = dd*sin(rr)
    z = h*H_RATIO
    return x,y,z
def condition(r,h,d):
    return d>D_MIN
def pattern():
    for th in range(H_MIN,H_MAX,H_STEP):
        for tr in range(R_MIN,R_MAX,R_STEP):
            yield th,tr
def main():
    r = b''
    with serial.Serial("COM5",115200,timeout=1) as s:
        print(".")
        p = pattern()
        for th,tr in p:
            s.write(struct.pack  (TX_FMT,tr,th))
            while len(r)<RX_L:
                r += s.read(RX_L)
            print(r)
            (rr,rh,rd) = struct.unpack(RX_FMT,r[:RX_L])
            r = r[RX_L:]
            if condition(rr,rh,rd):
                break
            else:
                yield calculate(rr,rh,rd)
if __name__ == "__main__":
    for i in main():
        print(i)
