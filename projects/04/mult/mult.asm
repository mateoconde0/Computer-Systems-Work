// This file is part of www.nand2tetris.org
// and the book "The Elements of Computing Systems"
// by Nisan and Schocken, MIT Press.
// File name: projects/04/Mult.asm

// Multiplies R0 and R1 and stores the result in R2.
// (R0, R1, R2 refer to RAM[0], RAM[1], and RAM[2], respectively.)

// Put your code here.

@R0 //store R0 in addressing register 
D = M // store whatever is in M into D 
@N 
M=D //store D into M 

@R1 // store R1 in addressing register 
D = M 
@W
M=D

@Z
M = 0

@SUM // defining a zero value 
M = 0

//check if n or m is zero, if it is go to ZERO 
@W
D=M
@ZERO
D;JEQ

@N
D=M
@ZERO
D;JEQ


(LOOP)
@W
D=M
@STOP
D;JEQ // go to stop if W is 0, otherwise continue

//Need to add N to R2 and return to loop 
@SUM
D=M
@N
D = D + M
@SUM
M = D

//Need to subtract 1 from W
@W
M = M - 1
@LOOP
0;JMP 
 
(ZERO) // sets the output to zero 
@Z
D=M
@R2
M=D
@END
0;JMP

(STOP)
@SUM
D=M
@R2
M=D

(END)
@END
0;JMP 