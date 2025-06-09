s1 = """{figflnFCTr*Dz|4HGEc<jdyM`N?"v@R7A!6%b,O\\x$o[=~3Z1we;V/W&h8s^+Ku_9'#aU0:)t(XY-2]ISpkQqmLB5PJ>.}"""
s2 = """{figfl0FCTr*o&wD:G7@=V'n5J-p^yhK~A;b_?c)k+daUL3tmPe/Qq[HI](sO"\ZBW1$j!#|4uEMY<xS>9z%vNX68,2.`R}"""

# solving the 79-cycle
s3 = ''.join([c1 if c1 != c2 else ' ' for c1, c2 in zip(s1, s2)]) # 79-cycle, A^17 S
s4 = ''.join([c2 if c1 != c2 else ' ' for c1, c2 in zip(s1, s2)]) # 79-cycle, A^528 S
s5 = {c1: c2 for c1, c2 in zip(s3, s4)} # 79-cycle, A^511
s6 = s5.copy()
for _ in range(47 - 1): # (A^511)^47 = A
    s6 = {c1: s5[s6[c1]] for c1 in s5.keys()} # 79-cycle, A
for _ in range(25): # A^25 A^528 S = S
    s4 = ''.join([s6[c1] for c1 in s4]) # 79-cycle, S

# solving the 1- and 7-cycles
s7 = "grifflesCTF{                                                                                  }"
s8 = ''.join([c1 if c1 == c2 else ' ' for c1, c2 in zip(s1, s2)]) # 1- or 7-cycle
s9 = ''.join([c1 if c1 == c2 else ' ' for c1, c2 in zip(s7, s8)]) # definitely 1-cycle (6/9)
s10 = ''.join([c1 if c1 != ' ' else c2.replace('s', '*') for c1, c2 in zip(s7, s8)]) # 1- and 7-cycles

s11 = ''.join([c1 if c1 != ' ' else c2 for c1, c2 in zip(s10, s4)])

# print(s1)
# print(s2)
# print(s3)
# print(s4)
# print(s7)
# print(s8)
# print(s9)
# print(s10)
print(s11)