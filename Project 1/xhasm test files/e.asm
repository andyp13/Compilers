// Data will be loaded in R[100] and R[200] thru R[203]
// The outputs will be taken from R[200] thru R[203]

.EQU OP1 100
.EQU OP2.1 200
.EQU OP2.2 201
.EQU OP2.3 202
.EQU OP2.4 203
.EQU FLAG$reg 16383
.EQU FLAG$value 24242

// & commands
@ OP1
D=M
@ OP2.1
M=D&M
@ OP2.2
M=D|M
@ OP2.3
M=D+M
@ OP2.4
M=D-M

// Set the trigger flag
@ FLAG_value
D=A
@ FLAG_register
M=D
