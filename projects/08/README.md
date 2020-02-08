# stackToAssembly

stackToAssembly takes a vm file as an input and returns a hack or asm file as an output. It parses the vm file to create the assembly representation of the virtual machine code.

## Usage

In a terminal, cd into the directory that contains stackToAssembly and run the following command.

```terminal
python stackToAssembly.py path_to_vm_file or path_of_directory_to_compile

```

This should call the function and convert the vm file into an asm file in the same directory as the vm file. If the asm file already exists, it will overwrite the existing file. If it is a directory that is being compiled, it will make sure that you have a Sys.vm file in the folder. If you do not, then it will ask you to add the file with the bootstrap code before continuing. The function will write a compiled asm file in the directory that you are compiling using the name of the basepath as the name for the file.
