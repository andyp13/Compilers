// Data will be loaded in R[100] and R[200] thru R[203]
// The outputs will be taken from R[200] thru R[203]

.EQU FLAG_REGISTER 16383
.EQU FLAG_VALUE 24242

@100
D=M
@200
M=D&M
@201
M=D|M
@202
M=D+M
@203
M=D-M

// Set the flag
@ FLAG_VALUE
D=A
@ FLAG_REGISTER
M=D

