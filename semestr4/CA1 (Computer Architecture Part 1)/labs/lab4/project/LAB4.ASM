\===========================================================
\ LAB4
\ F = (X & Y) * Z
\ X -> RD zovnishnoho prystroiu
\ Y, Z -> OP
\ op_xy, multiply -> priamа rehistrova adresatsiia
\ multiply -> 3-y sposob
\===========================================================

link l1:ct
link l2:rdm
link l3:rdd
link ewh:10
link M: z,z,z,z,z,z,z,z,14,13,12,11
link ra:3,2,1,0

accept rdm_delay:3

accept dev[0]:I, 02h, 04h, 6, 2
accept dev_buf[0]:000Eh          \ X = 14

accept R1:0000h                  \ stan portu
accept R2:0000h                  \ X
accept R3:0020h                  \ adresa potochnoi komandy v OP
accept R4:0003h                  \ adresa pershoho slova rezultatu v OP
accept R5:0000h                  \ Y
accept R6:0000h                  \ Z
accept R7:0000h                  \ X & Y
accept R8:0000h                  \ mnozhene (nerukhome)
accept R9:0000h                  \ registr komandy
accept R10:0000h                 \ starsha chastyna rezultatu
accept R11:0000h                 \ molodsha chastyna rezultatu
accept R12:0000h                 \ lichylnyk cykliv

\------------------- dany v OP -----------------------------

dw 1h:000Bh                      \ Y = 11
dw 2h:0005h                      \ Z = 5
dw 3h:0000h                      \ result high
dw 4h:0000h                      \ result low

\------------------- prohrama v OP -------------------------

dw 20h:0802h                     \ test RS
dw 21h:1002h                     \ ready_test RS
dw 22h:1804h                     \ input RD
dw 23h:2001h                     \ load_y [1h]
dw 24h:2802h                     \ load_z [2h]
dw 25h:3405h                     \ op_xy R5
dw 26h:3C06h                     \ multiply R6
dw 27h:4003h                     \ write [3h]
dw 28h:4800h                     \ end

\------------------- vektory komand ------------------------

ORG 0h {cjp nz, start;}
ORG 1h {cjp nz, test;}
ORG 2h {cjp nz, ready_test;}
ORG 3h {cjp nz, input;}
ORG 4h {cjp nz, load_y;}
ORG 5h {cjp nz, load_z;}
ORG 6h {cjp nz, op_xy;}
ORG 7h {cjp nz, multiply;}
ORG 8h {cjp nz, write_res;}
ORG 9h {cjp nz, end;}

\------------------- makrosy -------------------------------

macro next_com: {cjp nz, next;}
macro inc reg: {add reg, z, nz;}
macro op_addr: {or nil, R9, z; oey; ewl;}

\===========================================================
\ Start / fetch
\===========================================================

start
{xor nil, R0, R0; oey; ewh;}         \ ochystyty starshi rozriady adresy
{cjp nz, read_com;}

read_com
{xor nil, R0, R0; oey; ewh;}
{or nil, R3, z; oey; ewl;}           \ adresa potochnoi komandy
{cjp rdm, cp; R; or R9, bus_d, z;}   \ R9 <- komanda
{cjp nz, check;}

check
{and nil, R9, 8000h; load RM, flags;} \ odnoadresna komanda?
{cjp not RM_z, end;}
{or nil, R9, z; oey; jmap;}           \ perexid na mikoprohramu operatsii

next
{inc R3;}                             \ nastupna komanda
{cjp nz, read_com;}

\===========================================================
\ test RS
\===========================================================

test
{op_addr;}
{cjp rdd, cp; I; or R1, bus_d, z;}    \ R1 <- RS
{next_com;}

\===========================================================
\ ready_test
\===========================================================

ready_test
{and nil, R1, 0080h; load RM, flags;} \ bit gotovnosti
{cjp not RM_z, ready_ok;}
{op_addr;}
{cjp rdd, cp; I; or R1, bus_d, z;}    \ povtorno chytaiemo RS
{cjp nz, ready_test;}

ready_ok
{next_com;}

\===========================================================
\ input RD -> R2
\===========================================================

input
{op_addr;}
{cjp rdd, cp; I; or R2, bus_d, z;}    \ R2 <- X
{next_com;}

\===========================================================
\ load_y
\===========================================================

load_y
{op_addr;}
{cjp rdm, cp; R; or R5, bus_d, z;}    \ R5 <- Y
{next_com;}

\===========================================================
\ load_z
\===========================================================

load_z
{op_addr;}
{cjp rdm, cp; R; or R6, bus_d, z;}    \ R6 <- Z
{next_com;}

\===========================================================
\ op_xy : R7 := R2 AND R[A]
\ dla komandy 3405h A=5 -> R5
\===========================================================

op_xy
{or nil, R9, z; oey; ewa;}            \ zavantazhyty nomer rehistra v RA
{xor R7, R7;}
{or R7, R2, z;}
{and R7, ra;}
{next_com;}

\===========================================================
\ multiply : 3-y sposob
\ multiplicand = R7 -> R8 (nerukhome)
\ multiplier   = R[A] -> R11
\ result pair  = R10:R11
\===========================================================

multiply
{or nil, R9, z; oey; ewa;}              \ A -> RA
{or R8, R7, z;}                         \ R8 := X & Y
{xor R10, R10;}                         \ high := 0
{xor R11, R11;}
{or R11, ra;}                           \ low := Z
{or R12, 0010h, z;}                     \ CT := 16

M1
{and nil, R11, 0001h; load RM, flags;}  \ test low bit
{cjp RM_z, M2;}
{add R10, R10, R8, z;}                  \ high := high + multiplicand

M2
{or srl, R10, z;}                       \ high >>= 1
{or sr.9, R11, z;}                      \ low >>= 1 with carry from high
{sub R12, R12, z, z; load RM, flags; cem_c;}
{cjp not RM_z, M1;}
{next_com;}

\===========================================================
\ write result to OP
\===========================================================

write_res
{xor nil, R0, R0; oey; ewh;}
{or nil, R4, z; oey; ewl;}            \ adresa 3h
{or nil, R10, z; oey; cjp rdm, cp; W;} \ M[3h] <- high
{inc R4;}
{xor nil, R0, R0; oey; ewh;}
{or nil, R4, z; oey; ewl;}            \ adresa 4h
{or nil, R11, z; oey; cjp rdm, cp; W;} \ M[4h] <- low
{next_com;}

\===========================================================
\ end
\===========================================================

end
{}