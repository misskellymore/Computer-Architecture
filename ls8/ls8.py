#!/usr/bin/env python3

"""Main."""

import sys
from cpu import *

cpu = CPU()

# cpu.load(sys.argv[1])
# cpu.load("/home/kelly/Kelly/Desktop/LambdaProjects/Computer-Architecture/ls8/examples/mult.ls8")
# cpu.load("/home/kelly/Kelly/Desktop/LambdaProjects/Computer-Architecture/ls8/examples/stack.ls8")
# cpu.load("/home/kelly/Kelly/Desktop/LambdaProjects/Computer-Architecture/ls8/examples/call.ls8")
# cpu.load("/home/kelly/Kelly/Desktop/LambdaProjects/Computer-Architecture/ls8/examples/stack.ls8")
cpu.load()
cpu.run()