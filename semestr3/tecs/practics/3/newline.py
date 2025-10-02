S, N = 1, 6

R1 = R2 = 2*(S+N)
R3 = R4 = 2*N
R5 = N + S
R6 = N

R12 = R1*R2/(R1+R2)
R34 = R3*R4/(R3+R4)

R125 = R12 + R5
R346 = R34 + R6

R_ALL = R125*R346/(R125+R346)

print(F"R_ALL: {R_ALL}")