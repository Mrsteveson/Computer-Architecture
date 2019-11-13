"""CPU functionality."""

import sys
# Set Instructions
HLT = 0b00000001
LDI = 0b10000010
PRN = 0b01000111
MUL = 0b10100010
PUSH = 0b01000101
POP = 0b01000110

class CPU:
    """Main CPU class."""

    def __init__(self):
        """Construct a new CPU."""
        self.ram = [0] * 256
        self.reg = [0] * 8
        self.pc = 0
        self.sp = 244
        self.branchtable = {}
        self.branchtable[HLT] = self.hlt
        self.branchtable[LDI] = self.ldi
        self.branchtable[PRN] = self.prn
        self.branchtable[MUL] = self.mul
        self.branchtable[POP] = self.pop
        self.branchtable[PUSH] = self.push
        self.running = True


    def hlt(self, operand_a, operand_b):
        self.running = False
        self.pc += 1

    def ldi(self, operand_a, operand_b):
        self.reg[operand_a] = operand_b
        self.pc += 3

    def prn(self, operand_a, operand_b):
        print(self.reg[operand_a])
        self.pc += 2

    def mul(self, operand_a, operand_b):
        self.alu("MUL", operand_a, operand_b)
        self.pc += 3

    def pop(self, operand_a, operand_b):
        self.reg[operand_a] = self.ram[self.sp]
        self.sp += 1
        self.pc += 2

    def push(self, operand_a, operand_b):
        self.sp -= 1
        self.ram[self.sp] = self.reg[operand_a]
        self.pc += 2

    def ram_read(self, MAR):
        "should accept the address to read and return the value stored"
        return self.ram[MAR]

    def ram_write(self, MAR, MDR):
        "should accept a value to write, and the address to write it to"
        self.ram[MAR] = MDR

    def load(self):
        """Load a program into memory."""
        address = 0
        try:
            with open(sys.argv[1]) as file:
                for line in file:
                    if line[0].startswith('0') or line[0].startswith('1'):
                        split = line.split('#')
                        number = split[0].strip()
                        self.ram[address] = int(number, 2)
                        address += 1
        except FileNotFoundError:
            print("Attempted to load an invalid file.")
            sys.exit(1)

    def alu(self, op, reg_a, reg_b):
        """ALU operations."""

        if op == "ADD":
            self.reg[reg_a] += self.reg[reg_b]
        #elif op == "SUB": etc
        if op == "MUL":
            self.reg[reg_a] *= self.reg[reg_b]
        else:
            raise Exception("Unsupported ALU operation")

    def trace(self):
        """
        Handy function to print out the CPU state. You might want to call this
        from run() if you need help debugging.
        """

        print(f"TRACE: %02X | %02X %02X %02X |" % (
            self.pc,
            #self.fl,
            #self.ie,
            self.ram_read(self.pc),
            self.ram_read(self.pc + 1),
            self.ram_read(self.pc + 2)
        ), end='')

        for i in range(8):
            print(" %02X" % self.reg[i], end='')

        print()

    def run(self):
        """Run the CPU."""
        while self.running:
            IR = self.ram[self.pc]
            operand_a = self.ram_read(self.pc + 1)
            operand_b = self.ram_read(self.pc + 2)
            self.branchtable[IR](operand_a, operand_b)