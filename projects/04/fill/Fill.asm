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

@STATE //start the state at one 
M=0 

(LISTEN)
@KBD
D=M
@STATE0
D;JEQ

@STATE1 // jump to state one if the keyboard is not equal to one 
0;JMP


(STATE0)
@STATE 
D=M
@LISTEN //return to listening if keyboard is equal to zero and state is correct 
D;JEQ
//state is black and needs to be changed to white 
@STATE
M = 0
//send to go get filled 
@FILL
0;JMP
 
//This means that keyboard is not equal to 0. Need to check the state of the screen
(STATE1)
@STATE
D=M
@BLACK 
D;JEQ //go to change to black if state is not black
//if the screen is black then we want to keep it that way since keyboard != 0, we then want to continue listening 
@LISTEN
0;JMP 


(BLACK)//change state to black 
@STATE
M= -1


(FILL)//want to loop through number of rows and then number of columns (we get 16 at a time, so we need to fill 32 columns) 
//lets set R to 256
@256
D=A
@R
M=D

@SCREEN
D=A
@addr
M=D

(ROWS)
@R
D=M
@LISTEN
D;JEQ //if R is equal to 0 then all of the rows have been written, so we can return to listening 
//Otherwise we are going to fill a row 
@31
D=A
@C
M=D

(COLS)
//Going to fill the column of the row 
@STATE
D=M
@addr
A=M
M=D

@addr //add one to the addr
M = M + 1

@C //subtract one from C 
D=M
M = M - 1
@COLS
D;JNE //if we havent reached the end of the row continue to fill. 

//We have reached the end of the row. Need to remove one from the row element. 
@R
M = M - 1
@ROWS
0;JMP


//Incase we somehow get to this condition 
(END)
@END
0;JMP






 