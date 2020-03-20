// Data will be loaded in R[100] and R[200] thru R[203]
// The outputs will be taken from R[200] thru R[203]

// & commands
@100
D=M
@200
M=D&A
@201
M=D&!A
@202
M=!D&A
@203
M=!D&!A

// Set the trigger flag
@24242
D=A
@16383
M=D

// !& commands
@100
D=M
@200
M=!(D&A)
@201
M=!(D&!A)
@202
M=!(!D&A)
@203
M=!(!D&!A)

// Set the trigger flag
@24242
D=A
@16383
M=D

// | commands
@100
D=M
@200
M=D|A
@201
M=D|!A
@202
M=!D|A
@203
M=!D|!A

// Set the trigger flag
@24242
D=A
@16383
M=D

// !| commands
@100
D=M
@200
M=!(D|A)
@201
M=!(D|!A)
@202
M=!(!D|A)
@203
M=!(!D|!A)

// Set the trigger flag
@24242
D=A
@16383
M=D

//======================

// & commands
@100
D=M
@200
M=D&M
@201
M=D&!M
@202
M=!D&M
@203
M=!D&!M

// Set the trigger flag
@24242
D=A
@16383
M=D

// !& commands
@100
D=M
@200
M=!(D&M)
@201
M=!(D&!M)
@202
M=!(!D&M)
@203
M=!(!D&!M)

// Set the trigger flag
@24242
D=A
@16383
M=D

// | commands
@100
D=M
@200
M=D|M
@201
M=D|!M
@202
M=!D|M
@203
M=!D|!M

// Set the trigger flag
@24242
D=A
@16383
M=D

// !| commands
@100
D=M
@200
M=!(D|M)
@201
M=!(D|!M)
@202
M=!(!D|M)
@203
M=!(!D|!M)

// Set the trigger flag
@24242
D=A
@16383
M=D

