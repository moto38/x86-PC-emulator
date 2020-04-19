from x86cpu import x86cpu
from x86base import cpu,memory
import sys

#Memorysize
MEMSIZE=100 #(64kB)

c=x86cpu(memory(MEMSIZE))

#c.load('HelloWorld')

c.wReg(cpu.ds_,0x7c0)
c.wReg(cpu.cs_,0x7c0)
c.CS = c.rReg(cpu.cs_)
c.DS = c.rReg(cpu.ds_)

'''
for i in range(0x90,0xC0):
	c.opStr=''
	c.op = i
	c.eip = 0
	c.wMem(c.eip+1, 0b11001011, cpu.RTr8, c.CS)
	print('== No:{0:X} == '.format(i),end='')
	c.opcode[i](i)
input('ready')
'''
#c.run(0,c.load('HelloWorld'))


def reginit():
    for i in range(0,cpu.r_NREG):
        c.wReg(i , i % 3)
        c.initReg()

def meminit():
    for i in range(0,c.mem.memmax):
        c.mem.set(i,i)

def testopcode():
    print('=== test opcode ===')
    c.eip=0
    c.dumpRegister(-2)
    for i in range(0,0xff):
        try:
            c.eip = 0
            c.wMem(c.eip+1, 0b11001011, cpu.RTr8, c.CS)
            print('=== opcode:0x{0:02X} ==='.format(i))
            c.opcode[i](i)
            c.opStr=''
        except:
            print("error:", sys.exc_info()[0])
            #raise error
            print('=== Error Opcode:0x{0:X}==='.format(i))

    input()

testopcode()


def testpushsrx():
    c.eip=0
    c.dumpMemory(c.rReg(cpu.rsp_)-10,c.rReg(cpu.rsp_))
    c.dumpRegister(cpu.ss_)
    c.dumpRegister(cpu.rsp_)
    c.dumpRegister(cpu.rax_)
    c.op_push(c.Srx , cpu.ax_ , cpu.RTr8)
    c.opcode[0x50](0x50)
    c.dumpMemory(c.rReg(cpu.sp_)-10 , c.rReg(cpu.sp_))

    print()

testpushsrx()

x,y=65535,0
u,l=c.tocomp2(x,y,cpu.RTr16)
input()

'''
print(c.tocomp(1 , cpu.RTr16))

c.divsub(0x11110000,22222,cpu.RTr16)
input()


c.divsub2(0x1111,0,22222,cpu.RTr16)
input()

c.idivsub2(-0x1111,-0,22222,cpu.RTr16)
input()
#c.idivsub(-3652, 2161, cpu.RTr16)

c.mul2(0xffff,12,cpu.RTr16)
input()
c.mul2(0xffff,0xffff,cpu.RTr16)

input()
c.mul(0xffff,0xffff,cpu.RTr16)

input()
'''

def testmulmrmy():
    print('mul Mrmy test')
    c.seg=0
    c.eip=0
    c.wMem(1,0b11000011,cpu.RTr8,c.CS)
    c.wMem(2,3,cpu.RTr8 ,c.CS)
    c.wReg(cpu.ax_ , 3120)
    c.wReg(cpu.bx_ , 0x30)
    c.wReg(cpu.dx_ , 0x0)
    c.dumpMemory(0,10)
    c.dumpRegister(-2)
    c.op_mul(c.Mrmy, cpu.RTr16, cpu.RTr16)
    print('result:{1}:{0}'.format(cpu.sb2sd(c.rReg(cpu.ax_), cpu.RTr16), cpu.sb2sd(c.rReg(cpu.dx_), cpu.RTr16)))
    c.dumpMemory(0,10)
    c.dumpRegister(-2)
    input()

def testimulmrmy():
    c.opStr = ''
    print('imul Mrmy test')
    c.seg=0
    c.eip=0
    c.wMem(1,0b11000011,cpu.RTr8 ,c.CS)
    c.wMem(2,3,cpu.RTr8 ,c.CS)
    c.wReg(cpu.ax_ , -3120)
    c.wReg(cpu.bx_ , 0x30)
    c.wReg(cpu.dx_ , 0x0)
    c.dumpMemory(0,10)
    c.dumpRegister(-2)
    c.op_imul(c.Mrmy, cpu.RTr16, cpu.RTr16)
    print('result:{1}:{0}'.format(cpu.sb2sd(c.rReg(cpu.ax_), cpu.RTr16), cpu.sb2sd(c.rReg(cpu.dx_), cpu.RTr16)))
    c.dumpMemory(0,10)
    c.dumpRegister(-2)
    input()


#testmulmrmy()
#testimulmrmy()


def testidivmrmy():
    print('idiv Mrmy test')
    c.seg=0
    c.eip=0
    c.wMem(1,0b11000011,cpu.RTr8 ,c.CS)
    c.wMem(2,3,cpu.RTr8 ,c.CS)
    c.wReg(cpu.ax_ , -3120)
    c.wReg(cpu.bx_ , 0x30)
    c.wReg(cpu.dx_ , 0x0)
    c.dumpMemory(0,10)
    c.dumpRegister(-2)
    c.op_idiv(c.Mrmy, cpu.RTr16, cpu.RTr16)
    print('result:{0}...{1}'.format(cpu.sb2sd(c.rReg(cpu.ax_), cpu.RTr16), cpu.sb2sd(c.rReg(cpu.dx_), cpu.RTr16)))
    c.dumpMemory(0,10)
    c.dumpRegister(-2)
    input()




def testdivmrmy():
    print('div Mrmy test')
    c.seg=0
    c.eip=0
    c.wMem(1,0b11000011,cpu.RTr8 ,c.CS)
    c.wMem(2,3,cpu.RTr8 ,c.CS)
    c.wReg(cpu.ax_ , 0xc)
    c.wReg(cpu.bx_ , 0x3)
    c.wReg(cpu.dx_ , 0x0)
    c.dumpMemory(0,10)
    c.dumpRegister(-2)
    c.op_div(c.Mrmy, cpu.RTr16, cpu.RTr16)
    print('result:{0}...{1}'.format(cpu.sb2sd(c.rReg(cpu.ax_), cpu.RTr16), cpu.sb2sd(c.rReg(cpu.dx_), cpu.RTr16)))
    c.dumpMemory(0,10)
    c.dumpRegister(-2)
    input()

#testidivmrmy()
#testdivmrmy()

def testmulmrm():
    print('mul Mrmy test')
    c.seg=0
    c.eip=0
    c.wMem(1,0b11000011,cpu.RTr8 ,c.CS)
    c.wMem(2,3,cpu.RTr8 ,c.CS)
    c.wReg(cpu.ax_ , 0xc)
    c.wReg(cpu.bx_ , 0x3)
    c.wReg(cpu.dx_ , 0x0)
    c.dumpMemory(0,10)
    c.dumpRegister(-2)
    c.op_mul(c.Mrmy, cpu.RTr16, cpu.RTr16)
    print('result:{0}...{1}'.format(cpu.sb2sd(c.rReg(cpu.ax_), cpu.RTr16), cpu.sb2sd(c.rReg(cpu.dx_), cpu.RTr16)))
    c.dumpMemory(0,10)
    c.dumpRegister(-2)
    input()

def testimulmrm():
    print('imul Mrmy test')
    c.seg=0
    c.eip=0
    c.wMem(1,0b11000011,cpu.RTr8 ,c.CS)
    c.wMem(2,3,cpu.RTr8 ,c.CS)
    c.wReg(cpu.ax_ , 0xc)
    c.wReg(cpu.bx_ , 0x3)
    c.wReg(cpu.dx_ , 0x0)
    c.dumpMemory(0,10)
    c.dumpRegister(-2)
    c.op_imul(c.Mrmy, cpu.RTr16, cpu.RTr16)
    print('result:{0}...{1}'.format(cpu.sb2sd(c.rReg(cpu.ax_), cpu.RTr16), cpu.sb2sd(c.rReg(cpu.dx_), cpu.RTr16)))
    c.dumpMemory(0,10)
    c.dumpRegister(-2)
    input()




def testrclmrmyrx():
    print('rcl Mrmyrx test')
    c.seg=0
    c.eip=0
    c.wMem(1,0b11011000,cpu.RTr8 ,c.CS)
    c.wMem(2,3,cpu.RTr8 ,c.CS)
    c.wReg(cpu.ax_ , 0xf0f5)
    c.wReg(cpu.bx_ , 0x4)
    c.wReg(cpu.cl_ , 0x0)
    c.dumpMemory(0,10)
    c.dumpRegister(-2)
    c.op_rcl(c.Mrmyrx, cpu.RTr16, cpu.RTr16)
    c.dumpMemory(0,10)
    c.dumpRegister(-2)
    input()



def testrcrmrmyrx():
    print('rcr Mrmyrx test')
    c.seg=0
    c.eip=0
    c.wMem(1,0b11011000,cpu.RTr8 ,c.CS)
    c.wMem(2,3,cpu.RTr8 ,c.CS)
    c.wReg(cpu.ax_ , 0xf0f5)
    c.wReg(cpu.bx_ , 0x4)
    c.wReg(cpu.cl_ , 0x0)
    c.dumpMemory(0,10)
    c.dumpRegister(-2)
    c.op_rcr(c.Mrmyrx, cpu.RTr16, cpu.RTr16)
    c.dumpMemory(0,10)
    c.dumpRegister(-2)
    input()





def testrormrmyrx():
    print('ror Mrmyrx test')
    c.seg=0
    c.eip=0
    c.wMem(1,0b11011000,cpu.RTr8 ,c.CS)
    c.wMem(2,3,cpu.RTr8 ,c.CS)
    c.wReg(cpu.ax_ , 0xf0f5)
    c.wReg(cpu.bx_ , 0x4)
    c.wReg(cpu.cl_ , 0x0)
    c.dumpMemory(0,10)
    c.dumpRegister(-2)
    c.op_ror(c.Mrmyrx, cpu.RTr16, cpu.RTr16)
    c.dumpMemory(0,10)
    c.dumpRegister(-2)
    input()




def testrolmrmyrx():
    print('rol Mrmyrx test')
    c.seg=0
    c.eip=0
    c.wMem(1,0b11011000,cpu.RTr8 ,c.CS)
    c.wMem(2,3,cpu.RTr8 ,c.CS)
    c.wReg(cpu.ax_ , 0xf0f0)
    c.wReg(cpu.bx_ , 0x4)
    c.wReg(cpu.cl_ , 0x0)
    c.dumpMemory(0,10)
    c.dumpRegister(-2)
    c.op_rol(c.Mrmyrx, cpu.RTr16, cpu.RTr8)
    c.dumpMemory(0,10)
    c.dumpRegister(-2)
    input()




def testshldmrmyrxsrx():
    print('shld Mrmyrx Srx test')
    c.seg=0
    c.eip=0
    c.wMem(1,0b11011000,cpu.RTr8 ,c.CS)
    c.wMem(2,3,cpu.RTr8 ,c.CS)
    c.wReg(cpu.al_ , 0x0)
    c.wReg(cpu.bx_ , 0xaaaa)
    c.wReg(cpu.cl_ , 0x0)
    c.dumpMemory(0,10)
    c.dumpRegister(-2)
    c.op_shld(c.Srx, cpu.RTr16, cpu.cl_)
    c.dumpMemory(0,10)
    c.dumpRegister(-2)
    input()



def testshrdmrmyrxsrx():
    print('shrd Mrmyrx Srx test')
    c.seg=0
    c.eip=0
    c.wMem(1,0b11011000,cpu.RTr8 ,c.CS)
    c.wMem(2,3,cpu.RTr8 ,c.CS)
    c.wReg(cpu.al_ , 0x0B)
    c.wReg(cpu.bx_ , 0x5555)
    c.wReg(cpu.cl_ , 0x5)
    c.dumpMemory(0,10)
    c.dumpRegister(-2)
    c.op_shrd(c.Srx, cpu.RTr16, cpu.cl_)
    c.dumpMemory(0,10)
    c.dumpRegister(-2)
    input()



def testshrmrmysrx():
    print('shr MrmySrx test')
    c.seg=0
    c.eip=0
    c.wMem(1,0b11100000,cpu.RTr8 ,c.CS)
    c.wReg(cpu.al_ , 0xff)
    c.wReg(cpu.ah_ , 0xf)
    c.wReg(cpu.cl_ , 0x2)
    c.dumpMemory(0,10)
    c.dumpRegister(-2)
    c.op_shr(c.MrmySrx, cpu.RTr8 , cpu.cl_)
    c.dumpMemory(0,10)
    c.dumpRegister(-2)
    input()


def testsarmrmysrx():
    print('sar MrmySrx test')
    c.seg=0
    c.eip=0
    c.wMem(1,0b11100000,cpu.RTr8 ,c.CS)
    c.wReg(cpu.al_ , 0x5)
    c.wReg(cpu.ah_ , 0x3)
    c.wReg(cpu.cl_ , 0x2)
    c.dumpMemory(0,10)
    c.dumpRegister(-2)
    c.op_sar(c.MrmySrx, cpu.RTr8 , cpu.cl_)
    c.dumpMemory(0,10)
    c.dumpRegister(-2)
    input()

def testsalmrmysrx():
    print('sal MrmySrx test')
    c.seg=0
    c.eip=0
    c.wMem(1,0b11100000,cpu.RTr8 ,c.CS)
    c.wReg(cpu.al_ , 0x5)
    c.wReg(cpu.ah_ , 0x3)
    c.wReg(cpu.cl_ , 0x5)
    c.dumpMemory(0,10)
    c.dumpRegister(-2)
    c.op_sal(c.MrmySrx, cpu.RTr8 , cpu.cl_)
    c.dumpMemory(0,10)
    c.dumpRegister(-2)
    input()

'''
testrclmrmyrx()
testrcrmrmyrx()
testrormrmyrx()
testrolmrmyrx()
testshldmrmyrxsrx()
testshrdmrmyrxsrx()
testshrmrmysrx()
testsalmrmysrx()
testsarmrmysrx()
'''


def testcallrel8():
    print('call rel8 test')
    c.seg=0
    c.eip=0
    c.wMem(1,0x5,cpu.RTr8 ,c.CS)
    c.dumpMemory(0,10)
    c.dumpRegister(-2)
    c.op_callRel8(c.Siz , cpu.RTr8 , cpu.RTr8)
    c.dumpMemory(0,10)
    c.dumpRegister(-2)
    input()
    c.op_ret(c.Siz , 0 , 0)
    c.dumpRegister(-2)


def testpopsrx():
    c.eip=0
    c.dumpMemory(c.rReg(cpu.rsp_)-10,c.rReg(cpu.rsp_))
    c.dumpRegister(cpu.ss_)
    c.dumpRegister(cpu.rsp_)
    c.dumpRegister(cpu.rax_)
    c.op_pop(c.Srx , cpu.ax_ , cpu.RTr8)
    c.dumpMemory(c.rReg(cpu.sp_)-10 , c.rReg(cpu.sp_))
    c.dumpRegister(cpu.ax_)

    print()


def testmovrxiz():
    c.eip=0
    c.dumpMemory(0,5)
    c.dumpRegister(-2)
    c.wMem(1,0b00000001,cpu.RTr8 ,c.CS)
    c.op_mov(c.Mrxiz , cpu.RTr8 , cpu.RTr8)
    c.dumpMemory(0,5)
    c.dumpRegister(-2)


def testaddrmyrx():
    print()
    print('test add rmyrx')
    c.opStr=''
    c.eip=0
    c.dumpMemory(2051,2057)
    c.dumpRegister(-2)
    c.op_add(c.Mrmyrx , c.DB , c.DB)
    c.dumpMemory(2051,2057)
    c.dumpRegister(-2)

def testadcrmyrx():
    print()
    print('test adc rmyrx')
    c.eip=0
    c.opStr=''
    c.flagOn(cpu.CF)
    c.dumpMemory(2051,2057)
    c.dumpRegister(-2)
    c.op_adc(c.Mrmyrx , c.DB , c.DB)
    c.dumpMemory(2051,2057)
    c.dumpRegister(-2)

def testsubrmyrx():
    print()
    print('test sub rmyrx')
    c.opStr=''
    c.eip=0
    c.wReg(cpu.ax_,0x810)
    c.dumpMemory(2051,2057)
    c.dumpMemory(0,5)
    c.dumpRegister(-2)
    c.op_sub(c.Mrmyrx , cpu.RTr8 , cpu.RTr8)
    c.dumpMemory(2051,2057)
    c.dumpMemory(0,5)
    c.dumpRegister(-2)

def testsbbrmyrx():
    print()
    print('test sbb rmyrx')
    c.eip=0
    c.opStr=''
    c.flagOn(cpu.CF)
    c.dumpMemory(2051,2057)
    c.dumpRegister(-2)
    c.op_sbb(c.Mrmyrx , c.DB , c.DB)
    c.dumpMemory(2051,2057)
    c.dumpRegister(-2)


def testleaR16RM16():
    print()
    print('test lea R16 RM16')
    for i in [0,1,2,3,4,5,6,7]:
        c.eip=0
        c.mem.set(0,0x8a)
        c.mem.set(1 , 0b10000000+(~i&0x7)*8+i)
        c.mem.set(2,0x01)
        c.mem.set(3,0x02)
        c.mem.set(4,0x03)
        print()
        print('Check {0}:{1:08b}'.format(i,c.mem.get(1)))
        c.dumpMemory(c.rm,c.rm+5)
        c.dumpRegister(-2)
        c.op_lea(c.Mrxrmy , cpu.RTr16 , cpu.RTr16)
        c.dumpMemory(c.rm,c.rm+5)
        c.dumpRegister(-2)


def testmovR8RM8():
    print('test mov R8 RM8')
    for i in [0,1,2,3,4,5,6,7]:
        c.eip=0
        c.mem.set(0,0x8a)
        c.mem.set(1 , 0b10000000+(~i&0x7)*8+i)
        c.mem.set(2,0x01)
        c.mem.set(3,0x02)
        c.mem.set(4,0x03)
        print()
        print('Check {0}:{1:08b}'.format(i,c.mem.get(1)))
        c.dumpMemory(c.rm,c.rm+5)
        c.dumpRegister(-2)
        c.movR8RM8()()
        c.dumpMemory(c.rm,c.rm+5)
        c.dumpRegister(-2)


def testmovALImm8():
    print()
    print('test mov AL Imm8')
    c.wReg(cpu.rax_,0x1111111111111111)
    c.eip=0
    c.dumpRegister(cpu.al_)
    c.mem.set(1,0xFF)
    #c.movALImm8()
    c.op_mov(c.Srxiz , cpu.al_ ,cpu.RTr8)
    c.dumpRegister(cpu.al_)
    print()


def testmovSIImm16():
    print('test mov SI Imm8')
    c.wReg(cpu.rsi_,0x1111111111111111)
    c.eip=0
    c.dumpRegister(cpu.rsi_)
    c.mem.set(1,0xFF)
    c.mem.set(2,0x02)
    c.movSIImm16()
    c.dumpRegister(cpu.rsi_)
    print()



def testmovAHImm8():
    print('test mov AH Imm8')
    c.wReg(cpu.rax_,0x1111111111111111)
    c.eip=0
    c.dumpRegister(cpu.rax_)
    c.mem.set(1,0xFF)
    c.movAHImm8()
    c.dumpRegister(cpu.rax_)
    print()



def testaddALImm8():
    print('test add ALI Imm8')
    c.wReg(cpu.rax_,0x1111111111111180)
    c.eip=0
    c.dumpRegister(cpu.al_)
    c.mem.set(1,0xFF)
    c.addALImm8()
    c.dumpRegister(cpu.al_)
    print()


def testcmpALImm8():
    print('test cmp AL Imm8')
    c.wReg(cpu.rax_,0x111111111111180)
    c.eip=0
    c.dumpRegister(cpu.al_)
    c.mem.set(1,0x80)
    c.cmpALImm8()
    c.dumpRegister(cpu.al_)
    print()


def testjmpRel8():
    print('test jmp Imm8 (short jmp:Rel)')
    c.eip=c.mem.memmax-0xf0-1
    c.mem.set(c.eip+1,0xf0)
    c.jmpRel8()
    c.dumpRegister(-1)
    print()



def testjzRel8():
    print('test jz Imm8 (short jmp:Rel)')
    c.flagOn(cpu.ZF)
    s= 'ZF={0}'.format(c.getflag(cpu.ZF))
    c.eip=c.mem.memmax-2
    c.mem.set(c.eip+1, 0x5)
    c.jzRel8()
    c.dumpRegister(-1)
    print()


def testorRM8R8():
    print('test or RM8,R8')
    c.eip=0 #c.mem.memmax-2
    c.mem.set(c.eip+1, 0b10000011)
    c.dumpMemory(771,777)
    c.orRM8R8()
    c.dumpRegister(-2)
    c.dumpMemory(c.rm,c.rm+5)
    print()



def testxorRM8R8():
    print('test xor RM8,R8')
    c.eip=0 #c.mem.memmax-2
    c.mem.set(c.eip+1, 0b11000101)
    c.xorRM8R8()
    c.dumpRegister(-2)
    c.dumpMemory(c.rm,c.rm+5)
    print()


def testrwReg():
    print('test rReg,wReg')
    rn=cpu.xmm0_
    val=0xf7f6f5f4f0f2f3ff
    c.wReg(rn, val)
    c.dumpRegister(rn)
    r=c.rReg(rn)
    s='reg[{0}] = 0x{1:X}({1})'.format(cpu.regp[rn][2], r)
    cpu.msg(s)
    print()
    val=0x33333333
    c.wReg(rn, val)
    c.dumpRegister(rn)
    r=c.rReg(rn)
    s='r32 reg[{0}]({1}) = 0x{2:X}({2})'.format(rn, cpu.regp[rn][2], r)
    cpu.msg(s)
    print()
    val=0xf2222
    c.wReg(rn, val)
    c.dumpRegister(rn)
    r=c.rReg(rn)
    s='r16 reg[{0}]({1}) = 0x{2:X}({2})'.format(rn, cpu.regp[rn][2], r)
    cpu.msg(s)
    print()
    val=0x11
    c.wReg(rn, val)
    c.dumpRegister(rn)
    r=c.rReg(rn)
    s='rH reg[{0}]({1}) = 0x{2:X}({2})'.format(rn, cpu.regp[rn][2], r)
    cpu.msg(s)
    print()
    val=0x00
    c.wReg(rn, val)
    c.dumpRegister(rn)
    r=c.rReg(rn)
    s='r8 reg[{0}]({1}) = 0x{2:X}({2})'.format(rn, cpu.regp[rn][2], r)
    cpu.msg(s)
    print()
    c.dumpRegister(rn)

    print()



def testregsel():
    print('test jmp Imm8 (short jmp:Rel)')
    for rb in [0,1]:
        for r in range(0,7):
            for t in [cpu.r8, cpu.r16, cpu.r32, cpu.r64, cpu.mm, cpu.xmm, cpu.sreg, cpu.eee0, cpu.eee1]:
                reg=cpu.regsel16[rb][r][t]
                print('rex:{0} reg:{1} type:{2} register:{3}({4})'.format(rb, r, t, reg, cpu.regp[reg][2]))
    print()


def testdisp():
    bits=32
    start=c.eip
    end=c.eip + 5 + int(bits / 8)
    print('test disp()')
    c.dumpMemory(start, end)
    print('disp({2}):0x{0:X}({0}), eip:0x{1:X}({1})'.format(c.disp(bits), c.eip, bits))
    c.dumpMemory(start, end)
    print()


def testgetflag():
    print('test getflag')
    for f in [cpu.CF , cpu.ZF , cpu.OF ]:
        print('flag:0b{0:b} -> {1}'.format(f,c.getflag(f)))
    c.dumpRegister(-1)
    print()

def testregp():
    for i in range(0,cpu.NREG):
        print('{0}:[{1}]:real={2}({3})'.format(i , cpu.regp[i][2] , cpu.regp[i][0] , cpu.regp[cpu.r2reg[cpu.regp[i][0]]][2]))

def testmem():
    c.dumpMemory(0,10)
    c.wMem(2,0x12345678, cpu.RTr32 , c.CS)
    print(c.rMem(2,cpu.RTr32 ,c.CS))
    print(hex(c.rMem(2,cpu.RTr32)))
    c.dumpMemory(0,10)


def testaddRM16Imm8():
    c.wMem(0,0x83,cpu.RTr8 ,c.CS)
    c.wMem(1,0b10001001,cpu.RTr8 ,c.CS)
    c.wMem(2,0x90,cpu.RTr8 ,c.CS)
    c.wMem(4,0x81,cpu.RTr8 ,c.CS)
    c.wMem(772,0x7fff,cpu.RTr16 ,c.CS)
    c.wReg(cpu.ax_ , 0x7fff)
    c.eip=0
    c.dumpRegister(-2)
    c.dumpMemory(915,916)
    c.addRM16Imm8()
    c.dumpRegister(-2)
    c.dumpMemory(0,10)
    c.dumpMemory(915,916)
    cpu.msg(c.rMem(915,cpu.RTr16))


'''
v=170
for i in range(0,1):
    r = c.shift1L(v , cpu.RTr8, 1 )
    print(cpu.sb2sd(r,cpu.RTr8))
    v = r
    #c.LrotateL(0b10010101,i,cpu.RTr8)
    #c.LshiftR( 0b10010101,i,cpu.RTr8)
input()
'''


print('tocomp(-10)={0}'.format(c.tocomp(10,cpu.RTr8)))

#testcallrel8()

input()

reginit()
meminit()
testregp()
input()

testpushsrx()
testpushsrx()
testpopsrx()
testleaR16RM16()

testmovrxiz()
testaddrmyrx()
testadcrmyrx()
testsubrmyrx()
testsbbrmyrx()
#print(cpu.regsel16[0][cpu.rsp_][cpu.r64])
#testmem()
#testrwReg()

#testaddRM16Imm8()
##input()

#testmovRM8R8()
#input()

#testNewmovR8RM8()
#input()

reginit()
meminit()
#testmovR8RM8()

'''
testmovALImm8()
testmovAHImm8()
testmovSIImm16()
testaddALImm8()
testcmpALImm8()
#testregsel()
#testjmpRel8()
#testjzRel8()
testorRM8R8()
testxorRM8R8()
#testdisp()
#testgetflag()
'''

#print(cpu.regsel)
#print(cpu.regdict[0])

#print(hex(c.mem.memmax))

#print(cpu.sb2sd(0x1fe,8))

