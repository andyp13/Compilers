// Data will be loaded in R[100] and R[200] thru R[203]
// The outputs will be taken from R[200] thru R[203]

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

// R[16383] = 24242
@24242
D=A
@16383
M=D

