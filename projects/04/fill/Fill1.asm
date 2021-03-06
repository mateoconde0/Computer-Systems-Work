// This file is part of www.nand2tetris.org
// and the book "The Elements of Computing Systems"
// by Nisan and Schocken, MIT Press.
// File name: projects/04/Fill.asm

// Runs an infinite loop that listens to the keyboard input.
// When a key is pressed (any key), the program blackens the screen,
// i.e. writes "black" in every pixel;
// the screen should remain fully black as long as the key is pressed. 
// When no key is pressed, the program clears the screen, i.e. writes
// "white" in every pixel;
// the screen should remain fully clear as long as no key is pressed.

// Put your code here.
// we want to make sure that we are listening to the keyboard 
@STATE
M = 0 // start state set to 0 

(RESET)
@255 
D=A
@N //initialize the number of rows to be equal rowmax
M=D  

@32
D=A
@W
M=D

@SCREEN // we are going to get the screen address 
D=A
@addr 
M=D 

(LISTEN)
@KBD
D=M
@LISTEN
D;JEQ //if keyboard is equal to 0 then continue listening 

//Now we are going to change all of the rows to be the opposite of what it is now. 
//Check state 
@STATE
D=M 
@BLACK
D;JEQ

//if state does not equal zero then it equals black so we go to white 
(WHITE)
@STATE
M = 0 //set state equal to white 
@FILL //now lets fill
0;JMP

(BLACK)
@STATE 
M=-1 //set state to black (-1 sets all bits to 1) 

(FILL)
@N
D=M
@RESET
D;JEQ // if N is equal to 0 then reset the variables and go back to listening to the keyboard 

//lets start filling some rows 
(ROWS)
@STATE //get the state and store in D 
D=M
@addr //get the row address 
A=M
M=D //set the row to the state

@addr
M = M + 1

@W
D=M
M = D - 1 //subtract 1 from W  
@ROWS
D;JNE // if we haven't reached the end of the row continue to fill. 


//subtract one from N and add one row to addr 
@31
D=A
@W
M = D
@N
M=M-1

@FILL
0;JMP

//Incase we somehow get to this condition 
(END)
@END
0;JMP

 