// Data will be loaded in R[100] and R[200] thru R[203]
// The outputs will be taken from R[200] thru R[203]

@ 0xFFFF
D=M
@ 0B201
M = D*M
@ 0X3FFH
R0 = D|M
@ 202
M = D+M; JFS
@ 203
M = D-M

/ R[16383] = 24242
@24242
D = A
@16383 /* This is just before the start of SCREEN memory */
M = D

