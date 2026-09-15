\z = x * y, g = 1
\z = 4x - 0.5y, g = 0
\x, y zadani v PK
\z u DK

\_________nalashtuvannya shemy___________
link L1:ct
link L2:rdm
link ewh:16

accept R14:0004h \g v 3-mu biti, g=1 dlya testu
accept R0:0005h  \adres x
accept R1:0008h  \adres z
accept R4:0010h  \CT := 16
accept R5:0000h  \znak x
accept R6:0000h  \znak y
accept R7:0000h  \znak z
accept R8:0000h  \temp
accept R9:0000h  \temp
accept R10:0000h \temp

accept R2:0000h  \x
accept R3:0000h  \y

accept R11:0000h \RES starshi rozryadi
accept R12:0000h \RES molodshi rozryadi

accept rdm_delay:3

dw 5h:00009h \x = 9 (PK)
dw 6h:0C005h \y = -5 (PK)
dw 8h:00000h \z

\_______zavantazhennya danyh z OP___________
{ewh; oey; xor nil, R0, R0;} \adres (19-16)
{ewl; oey; or nil, R0, z;} \adres x
{cjp rdm, cp; R; or R2, bus_d, z;} \R2 := x (PK)

{add R0, R0, 1, z;} \adres y = adres x + 1
{ewl; oey; or nil, R0, z;} \adres y
{cjp rdm, cp; R; or R3, bus_d, z;} \R3 := y (PK)

\_______vydilennya znakiv___________
sign_x
{and R5, R2, 0C000h; load RM, flags;} \znak x

sign_y
{and R6, R3, 0C000h; load RM, flags;} \znak y

\_______analiz g___________
analyze_g
{and nil, R14, 0004h; load RM, flags;} \analiz 3-go bita
{cjp RM_Z, FORM_PREP;} \yakshcho g = 0 -> formula

\========================================================
\ MNOZHENNYA: beremo moduli z PK
\========================================================
MULT_PREP
{and nil, R5, 0C000h; load RM, flags;} \x vidyemne?
{cjp RM_Z, mult_y_prep;}
{xor R2, R2, 0C000h;} \R2 := |x| z PK

mult_y_prep
{and nil, R6, 0C000h; load RM, flags;} \y vidyemne?
{cjp RM_Z, mult_sign;}
{xor R3, R3, 0C000h;} \R3 := |y| z PK

mult_sign
{or R7, R5;} \R7 := znak x
{xor R7, R6;} \R7 := znak rezultatu
{xor R11, R11, z;} \starshi rozryady = 0
{xor R12, R12, z;} \molodshi rozryady = 0
{load RM, z;} \obnulennya oznak

\operatsiya mnozhennya moduliv
{or srl, nil, R2, z;} \otrymaly molodshyy bit mnozhnyka

M1
{cjp not RM_C, M2;} \R2[1] = 1?
{add R11, R11, R3, z;} \R11 := R11 + R3

M2
{or srl, R11, z;} \R11 := 0.R(R11)
{or sr.9, R2, z;} \R2 := R11[1].R(R2)
{or srl, nil, R2, z;} \znovu otrymaly R2[1]
{sub R4, R4, z, z; load RM, flags; cem_c;} \CT := CT - 1
{cjp not RM_Z, M1;} \CT = 0?

{or R12, R2, z;} \molodshi rozryady rezultatu

\_______nakladannya znaku na rezultat mnozhennya___________
{and nil, R7, 0C000h; load RM, flags;}
{cjp RM_Z, RES1;} \yakshcho rezultat dodatniy

\vidyemnyy rezultat -> perehid do DK
{xor R12, R12, 3FFFh;}
{add R12, R12, z, nz;} \+1
{or R11, 0FFFFh, z;} \sign extension dlya starshoho slova

\_______zapys rezultatu mnozhennya___________
RES1
{ewh; oey; xor nil, R1, R1;} \adres (19-16)
{ewl; oey; or nil, R1, z;} \adres z
{cjp rdm, cp; W; or nil, R12, z; oey;} \z -> OP
{cjp nz, END;}

\========================================================
\ FORMULA: peretvoryuyemo X,Y z PK u DK
\========================================================
FORM_PREP
{and nil, R5, 0C000h; load RM, flags;} \x vidyemne?
{cjp RM_Z, form_y_prep;}
{xor R2, R2, 0C000h;} \znyaly znakovI bity
{sub R2, z, R2, nz;} \R2 := x v DK

form_y_prep
{and nil, R6, 0C000h; load RM, flags;} \y vidyemne?
{cjp RM_Z, FORM;}
{xor R3, R3, 0C000h;} \znyaly znakovI bity
{sub R3, z, R3, nz;} \R3 := y v DK

\__________obchyslennya formuly___________
FORM
{or sll, R2, R2, z;} \2x
{or sll, R2, R2, z;} \4x
{or sra, R3, R3, z;} \0.5y

{or R12, R2, z;} \R12 := 4x
{sub R12, R12, R3, nz;} \R12 := 4x - 0.5y

\____________zapys rezultatu formuly_______________
RES2
{ewh; oey; xor nil, R1, R1;} \adres (19-16)
{ewl; oey; or nil, R1, z;} \adres z
{cjp rdm, cp; W; or nil, R12, z; oey;} \z -> OP

END
{} \end