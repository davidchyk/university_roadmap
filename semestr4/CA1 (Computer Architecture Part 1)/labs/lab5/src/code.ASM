link L1: ct
link L2: rdm
link L3: rdd

link ewh: 10
link RB: 7, 6, 5, 4
link RA: 3, 2, 1, 0
link M: z, z, z, z, z, z, z, z, 14, 13, 12, 11

\ Variant: a7 a6 a5 a4 a3 a2 a1 = 0 0 0 1 0 1 0
\ a5 a3 a1 = 000 -> operatsii 0, 1, 2
\ F1 = X + Y
\ F2 = X - Y
\ F3 = X and Y
\ a7 a6 a5 = 000 -> RS = 02h, RD = 04h

accept dev[0]: I, 02h, 04h, 3, 3
accept dev_buf[0]: 0FFFEh \ X = -2 u DK

accept R1: 0000h \ X u DK
accept R2: 0000h \ Y u DK
accept R3: 0000h \ RK - reiestr komandy
accept R4: 0010h \ LK - lichylnyk komand
accept R5: 0000h \ stan ZP
accept R6: 0000h \ F1 = X + Y
accept R7: 0000h \ F2 = X - Y
accept R8: 0000h \ F3 = X and Y

\ Dani v OP
dw 0h: 0000h \ rezerv
dw 1h: 0034h \ Y = 52 u DK
dw 2h: 0000h \ F1
dw 3h: 0000h \ F2
dw 4h: 0000h \ F3

\ Programa v OP, pochatok z 10h
dw 10h: 0000100000000010% \ TEST_ZP, kod 1, adres RS = 02h
dw 11h: 0001000000010000% \ Z_JUMP, kod 2, adres 10h
dw 12h: 0001100000000100% \ INPUT_X, kod 3, adres RD = 04h
dw 13h: 0010000000000001% \ GET_Y, kod 4, adres OP 1h

dw 14h: 1010110001100010% \ X_ADD_Y, kod 5, RA=R2, RB=R6
dw 15h: 0011000000000010% \ WRITE_F1, kod 6, adres OP 2h

dw 16h: 1011110001110010% \ X_SUB_Y, kod 7, RA=R2, RB=R7
dw 17h: 0100000000000011% \ WRITE_F2, kod 8, adres OP 3h

dw 18h: 1100110010000010% \ X_AND_Y, kod 9, RA=R2, RB=R8
dw 19h: 0101000000000100% \ WRITE_F3, kod Ah, adres OP 4h

dw 1Ah: 0101100000000000% \ END, kod Bh

\ Vektory komand u PMK
org 0h  {cjp nz, START;}

org 1h  {cjp nz, TEST_ZP;}
org 2h  {cjp nz, Z_JUMP;}
org 3h  {cjp nz, INPUT_X;}
org 4h  {cjp nz, GET_Y;}
org 5h  {cjp nz, X_ADD_Y;}
org 6h  {cjp nz, WRITE_F1;}
org 7h  {cjp nz, X_SUB_Y;}
org 8h  {cjp nz, WRITE_F2;}
org 9h  {cjp nz, X_AND_Y;}
org 0Ah {cjp nz, WRITE_F3;}
org 0Bh {cjp nz, END;}

macro INC REG: {add REG, REG, z, nz;}
macro ADDRESS: {or nil, R3, z; oey; ewl;}
macro NEXT_COM: {cjp nz, NEXT;}

NEXT
{INC R4;} \ LK = LK + 1

START
{xor nil, R0, R0; oey; ewh;}          \ starshi rozriady adresy = 0
{or nil, R4, z; oey; ewl;}            \ adres potochnoi komandy z LK
{cjp rdm, cp; R; or R3, BUS_D, z;}    \ chytannia komandy v RK
{or nil, R3, z; oey; jmap;}           \ perekhid za kodom operatsii

TEST_ZP
{ADDRESS;}                            \ adres RS z adresnoho polia komandy
{cjp rdd, cp; I; or R5, BUS_D, z;}     \ chytannia RS u R5
{and nil, R5, 0080h; load RM, flags;}  \ perevirka bita hotovnosti
{NEXT_COM;}

Z_JUMP
{cjp not RM_Z, ZJ_NEXT;}               \ yakshcho ZP hotovyi, idemo dali
{and R4, R3, 03FFh;}                   \ LK = adres z komandy
{cjp nz, START;}

ZJ_NEXT
{NEXT_COM;}

INPUT_X
{ADDRESS;}                            \ adres RD z adresnoho polia komandy
{cjp rdd, cp; I; or R1, BUS_D, z;}     \ R1 = X
{NEXT_COM;}

GET_Y
{ADDRESS;}                            \ adres Y v OP
{cjp rdm, cp; R; or R2, BUS_D, z;}     \ R2 = Y
{NEXT_COM;}

X_ADD_Y
{ADDRESS; ewa; ewb;}                  \ RA=R2, RB=R6
{or RB, R1, z;}                       \ RB = X, tobto R6 = X
{add RB, RB, RA, z;}                  \ RB = RB + RA, tobto R6 = X + Y
{NEXT_COM;}

WRITE_F1
{ADDRESS;}                            \ adres F1 v OP
{cjp rdm, cp; or nil, R6, z; oey; W;}  \ zapis R6 v OP
{NEXT_COM;}

X_SUB_Y
{ADDRESS; ewa; ewb;}                  \ RA=R2, RB=R7
{or RB, R1, z;}                       \ RB = X, tobto R7 = X
{sub RB, RB, RA, nz;}                 \ RB = RB - RA, tobto R7 = X - Y
{NEXT_COM;}

WRITE_F2
{ADDRESS;}                            \ adres F2 v OP
{cjp rdm, cp; or nil, R7, z; oey; W;}  \ zapis R7 v OP
{NEXT_COM;}

X_AND_Y
{ADDRESS; ewa; ewb;}                  \ RA=R2, RB=R8
{or RB, R1, z;}                       \ RB = X, tobto R8 = X
{and RB, RB, RA;}                     \ RB = RB and RA, tobto R8 = X and Y
{NEXT_COM;}

WRITE_F3
{ADDRESS;}                            \ adres F3 v OP
{cjp rdm, cp; or nil, R8, z; oey; W;}  \ zapis R8 v OP
{NEXT_COM;}

END
{}