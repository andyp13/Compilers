// Data will be loaded in R[100] and R[200] thru R[203]
// The outputs will be taken from R[200] thru R[203]

// & commands
@ 100
D=M
@ 0X00C8
M=D&M
@ 0B000011001001
M=D|M
@ 0xca
M=D+M
@ 0b11001011
M=D-M

// Set the trigger flag
@ 0B0101111010110010
D=A
@ 0X3FFF
M=D
