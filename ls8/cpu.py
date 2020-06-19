"""CPU functionality."""

import sys



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
        self.sp = 7
        self.reg[self.sp] = 0xF4        
        # Program Counter, index of the current instruction
        self.pc = 0
        # CPU has a total of 256 bytes of memory
        self.ram = [0] * 256
        # exit the emulator
        self.halted = False        

        # flags
        self.flags = [0] * 8

        # instructions        
        self.instructions = {

            0b10000010: self.ldi,
            0b01000111: self.prn,
            0b00000001: self.hlt,
            0b10100010: self.mul,
            0b01000101: self.push,
            0b01000110: self.pop,
            0b00010001: self.ret,
            0b01010000: self.call,
            0b10100000: self.add,
            0b10100111: self.compare,
            0b01010101: self.jeq,
            0b01010110: self.jne,
            0b01010100: self.jmp
            
        }
        

    # Step 2
    # add method `ram_read()
    def ram_read(self, pc):
        return self.ram[pc]

    # Step 2
    # add ram_write()
    def ram_write(self, pc, value):
        self.ram[pc] = value



    def load(self):
        """Load a program into memory."""

        if len(sys.argv) < 2:
            raise NameError("no input")

        program_name = sys.argv[1]               
        address = 0        

        with open(program_name) as p:
            # for address, line in enumerate(p):
            for line in p:
                line = line.split("#")[0]

                try:
                    instruction = int(line, 2)
                except ValueError:
                    continue

                self.ram[address] = instruction
                address += 1


    def alu(self, op, reg_a, reg_b):
        """ALU operations."""

        if op == "ADD":
            self.reg[reg_a] += self.reg[reg_b]
        elif op == "SUB":
            self.reg[reg_a] -= self.reg[reg_b]
        elif op == "MUL":
            self.reg[reg_a] *= self.reg[reg_b]
        elif op == "DIV":
            self.reg[reg_a] /= self.reg[reg_b]
        elif op == "CMP":
            if self.reg[reg_a] == self.reg[reg_b]:
                self.flags[-1] = 1
            elif self.reg[reg_a] < self.reg[reg_b]:
                self.flags[-3] = 1
            else:
                self.flags[-2] = 1
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

            # changed = False
            # print("self.pc", self.pc)

            ir = self.ram[self.pc]
            instruction = self.instructions.get(ir)
            sets_pc = (ir >> 4) & 0b1

            if instruction and not sets_pc:
                inc = (ir >> 6) + 1
                self.instructions[ir]()
                self.pc += inc
            elif instruction:
                self.instructions[ir]()

            # >> means shift right
            #                       0b10000010
            # number_of_bytes = (ir & 0b11000000) >> 6
            # #                       0b10000000
            # # if num of bytes == 2
            # # then read both address 1 & address 2
            # if number_of_bytes == 2:
            #     address_1 = self.ram[self.pc+1]
            #     address_2 = self.ram[self.pc+2]
            # elif number_of_bytes == 1:
            #     address_1 = self.ram[self.pc+1]
            #     address_2 = None

            
                
        # LDI, PRN, HLT defs
        # LDI will have address, value, and ram_write
        # PRN will have address and value of ram_read
        # HLT will return false
    def ldi(self):        
        address = self.ram[self.pc+1]
        value = self.ram[self.pc+2]
        self.reg[address] = value

    def prn(self):       
        address = self.ram[self.pc+1]
        value = self.reg[address]
        print(value) 

    def hlt(self):        
        sys.exit(0)

    def add(self):
        addresses = self.get_operands()
        self.alu("ADD", *addresses)

    def mul(self):
        addesses = self.get_operands()
        self.alu("MUL", *addesses)

    def div(self):
        addresses = self.get_operands()
        self.alu("DIV", *addresses)

    def compare(self):
        addresses = self.get_operands()
        self.alu("CMP", *addresses)

    def get_operands(self):
        address_1 = self.ram[self.pc +1]
        address_2 = self.ram[self.pc + 2]

        return [address_1, address_2]

    def push(self, address_1):
        # minus SP
        self.sp -= 1

        address = self.ram[self.pc + 1]
        value = self.reg[address]
        self.ram[self.sp] = value

    def pop(self):
        address = self.ram[self.pc + 1]
        value = self.ram[self.sp]
        self.reg[address] = value

        self.sp += 1

    def call(self):
        return_addr = self.pc + 2

        # push onto stack
        self.pc -= 1
        self.ram[self.reg[self.sp]] = return_addr

        # get() addr to call
        reg_num = self.ram[self.pc + 1]
        subroutine_addr = self.reg[reg_num]

        # call subroutine
        self.pc = subroutine_addr

    def ret(self):
        self.pc = self.ram[self.reg[self.sp]]
        self.sp += 1

    def jeq(self):
        if self.flags[-1] == 1:
            address = self.ram[self.pc+1]
            jump_to = self.reg[address]
            self.pc = jump_to
        else:
            self.pc += 2

    def jne(self):
        if self.flags[-1] == 0:
            address = self.ram[self.pc+1]
            jump_to = self.reg[address]
            self.pc = jump_to
        else:
            self.pc += 2

    def jmp(self):
        address = self.ram[self.pc+1]
        jump_to = self.reg[address]
        self.pc = jump_to

    

# CALL
# what are some ways to effectivly get arg to a subroutine 
# stack, regs, ram
# bitwise operators => and
# results of bitwise and btw 2 sets of binary numbers
# binary to hex

#     1
#    10
#    11
#   100
#   101
#   110
#   111
#  1000
#  1001
#  1010
#  1011
#  1100
#  1111

# 10000
# 10001
# 10010
# 10011
# 10100
# 10101
# 10110
# 10111










