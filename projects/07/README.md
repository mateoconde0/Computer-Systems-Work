# stackToAssembly

stackToAssembly takes a vm file as an input and returns a hack or asm file as an output. It parses the vm file to create the assembly representation of the virtual machine code.

## Usage

In a terminal, cd into the directory that contains stackToAssembly and run the following command.

```terminal
python stackToAssembly.py path_to_vm_file

```

This should call the function and convert the vm file into an asm file in the same directory as the vm file. If the asm file already exists, it will overwrite the existing file.
