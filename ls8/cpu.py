"""CPU functionality."""

import sys

LDI = 0b10000010
PRN = 0b01000111
HLT = 0b00000001
MUL = 0b10100010
PUSH = 0b01000101
POP = 0b01000110
SP = 7

# 32  16  8 4 2 1
# 1   0  1 0 1 0

class CPU:
    """Main CPU class."""

    def __init__(self):
        """Construct a new CPU."""
        # 8 general-purpose registers
        self.reg = [0] * 8
        # stack pointer is 7, the last place of the reg
        # `R7` is set to `0xF4`.
        # 0xF4 == 244
        self.reg[SP] = 0xF4        
        # Program Counter, index of the current instruction
        self.pc = 0
        # CPU has a total of 256 bytes of memory
        self.ram = [0] * 256
        # exit the emulator
        self.halted = False

        self.LDI = LDI
        self.HLT = HLT
        self.PRN = PRN
        self.MUL = MUL
        self.PUSH = PUSH
        self.POP = POP


    # Step 2
    # add method `ram_read()
    def ram_read(self, pc):
        return self.ram[pc]

    # Step 2
    # add ram_write()
    def ram_write(self, pc, value):
        self.ram[pc] = value



    def load(self, program_name):
        """Load a program into memory."""
        
        address = 0        

        with open(program_name) as p:
            # for address, line in enumerate(p):
            for line in p:
                line_split = line.split("#")
                num = line_split[0].strip()

                if num == "":
                    continue

                try:
                    instruction = int(num, 2)
                except ValueError:
                    continue

                self.ram[address] = instruction
                address += 1

        # For now, we've just hardcoded a program:

        # program = [
        #     # From print8.ls8
        #     0b10000010, # LDI R0,8
        #     0b00000000,
        #     0b00001000,
        #     0b01000111, # PRN R0
        #     0b00000000,
        #     0b00000001, # HLT
        # ]


    def alu(self, op, reg_a, reg_b):
        """ALU operations."""

        if op == "ADD":
            self.reg[reg_a] += self.reg[reg_b]
        #elif op == "SUB": etc
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
        running = True

        # while loop
        # LDI
        # PRN
        # and HLT
        while running == True:
            ir = self.ram[self.pc]
            # >> means shift right
            number_of_bytes = (ir & 0b11000000) >> 6
            # if num of bytes == 2
            # then read both address 1 & address 2
            if number_of_bytes == 2:
                address_1 = self.ram[self.pc+1]
                address_2 = self.ram[self.pc+2]
            elif number_of_bytes == 1:
                address_1 = self.ram[self.pc+1]
                address_2 = None

            if ir == self.LDI:
                self.ldi(address_1, address_2)                

            elif ir == self.PRN:
                self.prn(address_1)                

            elif ir == self.MUL:
                self.mul(address_1, address_2)

            elif ir == self.PUSH:
                # minus SP
                self.reg[SP] -= 1

                # Get the value we want to store from the register
                reg_num = address_1
                value = self.reg[reg_num]

                # figure out where to store it
                top_of_stack_addr = self.reg[SP]

                # and then store it
                self.ram[top_of_stack_addr] = value

            elif ir == self.POP:

                top_of_stack_addr = self.reg[SP]

                value = self.ram[top_of_stack_addr]

                self.reg[address_1] = value

                self.reg[SP] += 1


            elif ir == self.HLT:
                running = self.hlt(running)
            
            self.pc += number_of_bytes + 1

                
        # LDI, PRN, HLT defs
        # LDI will have address, value, and ram_write
        # PRN will have address and value of ram_read
        # HLT will return false
    def ldi(self, address_1, value):        
        self.reg[address_1] = value       

    def prn(self, address):        
        value = self.reg[address]
        print(value)        

    def hlt(self, running):
        
        return False

    def mul(self, address_1, address_2):        

        value_1 = self.reg[address_1]
        value_2 = self.reg[address_2]
        self.reg[address_1] = value_1 * value_2
        print(value_1, value_2)
        print("reg", self.reg[address_1])
        
