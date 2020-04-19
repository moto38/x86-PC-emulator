# coding: utf-8
import os
import sys
import copy
#import register


class memory():
    def __init__(self,k64): # mem=64k*64
        '''
        if 64KB : k64 = 1
        if 640KB : k64 = 10
        if 1MB : k64 = 16
        if 1GB : k64 = 16384
        '''
        self.segment=65536
        memorysize = self.segment*k64
        self._memory = [0 for i in range(0,memorysize)]
        self.memmax = memorysize-1 #final address
        print('memmax={0}'.format(self.memmax))

    def set(self,addr,v):
        self._memory[addr] = v & 0xff

    def get(self,addr):
        return self._memory[addr]


class cpu():
    def msg(str):
        print(str)
        pass

    def dbgp(str):
        #print(str)
        pass

    # define register label
    rax_=0
    eax_=1
    ax_=2
    ah_=3
    al_=4

    rcx_=5
    ecx_=6
    cx_=7
    ch_=8
    cl_=9

    rdx_=10
    edx_=11
    dx_=12
    dh_=13
    dl_=14

    rbx_=15
    ebx_=16
    bx_=17
    bh_=18
    bl_=19

    rsp_=20
    esp_=21
    sp_=22
    spl_=23

    rbp_=24
    ebp_=25
    bp_=26
    bpl_=27

    rsi_=28
    esi_=29
    si_=30
    sil_=31

    rdi_=32
    edi_=33
    di_=34
    dil_=35

    mm0_=36
    mm1_=37
    mm2_=38
    mm3_=39
    mm4_=40
    mm5_=41
    mm6_=42
    mm7_=43

    xmm0_=44
    xmm1_=45
    xmm2_=46
    xmm3_=47
    xmm4_=48
    xmm5_=49
    xmm6_=50
    xmm7_=51
    xmm8_=52
    xmm9_=53
    xmm10_=54
    xmm11_=55
    xmm12_=56
    xmm13_=57
    xmm14_=58
    xmm15_=59

    r8_=60
    r8d_=61
    r8w_=62
    r8b_=63

    r9_=64
    r9d_=65
    r9w_=66
    r9b_=67

    r10_=68
    r10d_=69
    r10w_=70
    r10b_=71

    r11_=72
    r11d_=73
    r11w_=74
    r11b_=75

    r12_=76
    r12d_=77
    r12w_=78
    r12b_=79

    r13_=80
    r13d_=81
    r13w_=82
    r13b_=83

    r14_=84
    r14d_=85
    r14w_=86
    r14b_=87

    r15_=88
    r15d_=89
    r15w_=90
    r15b_=91

    es_=92
    cs_=93
    ss_=94
    ds_=95
    fs_=96
    gs_=97

    cr0_=98
    cr1_=99 #invd
    cr2_=100
    cr3_=101
    cr4_=102
    cr5_=103 #invd
    cr6_=104 #invd
    cr7_=105 #invd
    cr8_=106

    dr0_=107
    dr1_=108
    dr2_=109
    dr3_=110
    dr4_=111
    dr5_=112
    dr6_=113
    dr7_=114
    INVD=115
    RESERVED=116
    NREG=115

    r_rax=0
    r_rcx=1
    r_rdx=2
    r_rbx=3
    r_rsp=4
    r_rbp=5
    r_rsi=6
    r_rdi=7

    r_mm0=8
    r_mm1=9
    r_mm2=10
    r_mm3=11
    r_mm4=12
    r_mm5=13
    r_mm6=14
    r_mm7=15

    r_xmm0=16
    r_xmm1=17
    r_xmm2=18
    r_xmm3=19
    r_xmm4=20
    r_xmm5=21
    r_xmm6=22
    r_xmm7=23
    r_xmm8=24
    r_xmm9=25
    r_xmm10=26
    r_xmm11=27
    r_xmm12=28
    r_xmm13=29
    r_xmm14=30
    r_xmm15=31

    r_r8=32
    r_r9=33
    r_r10=34
    r_r11=35
    r_r12=36
    r_r13=37
    r_r14=38
    r_r15=39

    r_es=40
    r_cs=41
    r_ss=42
    r_ds=43
    r_fs=44
    r_gs=45

    r_cr0=46
    r_cr1=47 #invd
    r_cr2=48
    r_cr3=49
    r_cr4=50
    r_cr5=51 #invd
    r_cr6=52 #invd
    r_cr7=53 #invd
    r_cr8=54

    r_dr0=55
    r_dr1=56
    r_dr2=57
    r_dr3=58
    r_dr4=59
    r_dr5=60
    r_dr6=61
    r_dr7=62

    r_INDV=63
    r_RESERVED=64
    r_NREG=63

    # resource type
    RTr8=0 # AL
    RTrH=1 # AH
    RTr16=2 # AX
    RTr32=3 # EAX
    RTr64=4 # RAX
    RTr128=6 # XMM

    regp=[
    # realreg , rtype , name
    [r_rax, RTr64,'rax_'], #0 rax
    [r_rax, RTr32,'eax_'],
    [r_rax, RTr16,'ax_'],
    [r_rax, RTrH ,'ah_'],
    [r_rax, RTr8 ,'al_'],
    [r_rcx, RTr64,'rcx_'], #5 rcx
    [r_rcx, RTr32,'ecx_'],
    [r_rcx, RTr16,'cx_'],
    [r_rcx, RTrH ,'ch_'],
    [r_rcx, RTr8 ,'cl_'],
    [r_rdx, RTr64,'rdx_'], #10 rdx
    [r_rdx, RTr32,'edx_'],
    [r_rdx, RTr16,'dx_'],
    [r_rdx, RTrH ,'dh_'],
    [r_rdx, RTr8 ,'dl_'],
    [r_rbx, RTr64,'rbx_'], #15 rbx
    [r_rbx, RTr32,'ebx_'],
    [r_rbx, RTr16,'bx_'],
    [r_rbx, RTrH ,'bh_'],
    [r_rbx, RTr8 ,'bl_'],
    [r_rsp, RTr64,'rsp_'], #20 rsp
    [r_rsp, RTr32,'esp_'],
    [r_rsp, RTr16,'sp_'],
    [r_rsp, RTr8 ,'spl_'],
    [r_rbp, RTr64,'rbp_'], #24 rbp
    [r_rbp, RTr32,'ebp_'],
    [r_rbp, RTr16,'bp_'],
    [r_rbp, RTr8 ,'bpl_'],
    [r_rsi, RTr64,'rsi_'], #28 rsi
    [r_rsi, RTr32,'esi_'],
    [r_rsi, RTr16,'si_'],
    [r_rsi, RTr8 ,'sil_'],
    [r_rdi, RTr64,'rdi_'], #32 rdi
    [r_rdi, RTr32,'edi_'],
    [r_rdi, RTr16,'di_'],
    [r_rdi, RTr8 ,'dil_'],
    [r_mm0, RTr64,'mm0_'], #36 mm0
    [r_mm1, RTr64,'mm1_'],
    [r_mm2, RTr64,'mm2_'],
    [r_mm3, RTr64,'mm3_'],
    [r_mm4, RTr64,'mm4_'],
    [r_mm5, RTr64,'mm5_'],
    [r_mm6, RTr64,'mm6_'],
    [r_mm7, RTr64,'mm7_'],
    [r_xmm0,RTr128,'xmm0_'], #44 xmm0
    [r_xmm1,RTr128,'xmm1_'],
    [r_xmm2,RTr128,'xmm2_'],
    [r_xmm3,RTr128,'xmm3_'],
    [r_xmm4,RTr128,'xmm4_'],
    [r_xmm5,RTr128,'xmm5_'],
    [r_xmm6,RTr128,'xmm6_'],
    [r_xmm7,RTr128,'xmm7_'],
    [r_xmm8,RTr128,'xmm8_'],
    [r_xmm9,RTr128,'xmm9_'],
    [r_xmm10,RTr128,'xmm10_'],
    [r_xmm11,RTr128,'xmm11_'],
    [r_xmm12,RTr128,'xmm12_'],
    [r_xmm13,RTr128,'xmm13_'],
    [r_xmm14,RTr128,'xmm14_'],
    [r_xmm15,RTr128,'xmm15_'],
    [r_r8 , RTr64 ,'r8_'], #60 r8
    [r_r8 , RTr32 ,'r8d_'],
    [r_r8 , RTr16 ,'r8w_'],
    [r_r8 , RTr8 ,'[r8b_'],
    [r_r9 , RTr64 ,'r9_'], #64 r9
    [r_r9 , RTr32 ,'r9d_'],
    [r_r9 , RTr16 ,'r9w_'],
    [r_r9 , RTr8 ,'r9b_'],
    [r_r10, RTr64 ,'r10_'], #68 r10
    [r_r10, RTr32 ,'r10d_'],
    [r_r10, RTr16 ,'r10w_'],
    [r_r10, RTr8 ,'r10b_'],
    [r_r11, RTr64 ,'r11_'], #72 r11
    [r_r11, RTr32 ,'r11d_'],
    [r_r11, RTr16 ,'r11w_'],
    [r_r11, RTr8 ,'r11b_'],
    [r_r12, RTr64 ,'r12_'], #76 r12
    [r_r12, RTr32 ,'r12d_'],
    [r_r12, RTr16 ,'r12w_'],
    [r_r12, RTr8 ,'r12b_'],
    [r_r13, RTr64 ,'r13_'], #80 r13
    [r_r13, RTr32 ,'r13d_'],
    [r_r13, RTr16 ,'r13w_'],
    [r_r13, RTr8 ,'r13b_'],
    [r_r14, RTr64 ,'r14_'], #84 r14
    [r_r14, RTr32 ,'r14d_'],
    [r_r14, RTr16 ,'r14w_'],
    [r_r14, RTr8 ,'r14b_'],
    [r_r15, RTr64 ,'r15_'], #88 r15
    [r_r15, RTr32 ,'r15d_'],
    [r_r15, RTr16 ,'r15w_'],
    [r_r15, RTr8 ,'r15b_'],
    [r_es , RTr16 ,'es_'], #92 es
    [r_cs , RTr16 ,'cs_'], #93
    [r_ss , RTr16 ,'ss_'], #94
    [r_ds , RTr16 ,'ds_'], #95
    [r_fs , RTr16 ,'fs_'], #96
    [r_gs , RTr16 ,'gs_'], #97
    [r_cr0 , RTr32 ,'cr0_'],
    [r_cr1 , RTr32 ,'cr1_'], #invd
    [r_cr2 , RTr32 ,'cr2_'],
    [r_cr3 , RTr32 ,'cr3_'],
    [r_cr4 , RTr32 ,'cr4_'],
    [r_cr5 , RTr32 ,'cr5_'], #invd
    [r_cr6 , RTr32 ,'cr6_'], #invd
    [r_cr7 , RTr32 ,'cr7_'], #invd
    [r_cr8 , RTr32 ,'cr8_'],
    [r_dr0 , RTr32 ,'dr0_'],
    [r_dr1 , RTr32 ,'dr1_'],
    [r_dr2 , RTr32 ,'dr2_'],
    [r_dr3 , RTr32 ,'dr3_'],
    [r_dr4 , RTr32 ,'dr4_'],
    [r_dr5 , RTr32 ,'dr5_'],
    [r_dr6 , RTr32 ,'dr6_'],
    [r_dr7 , RTr32 ,'dr7_']
    ]

    r2reg=[0 for x in range(0, r_NREG)]
    x=0
    for y in range(0, NREG):
        if regp[y][0] != x:
            x += 1
            r2reg[x] = y

    mod1164 = [
        [ # rex.b = 0
            [ # rax
                al_,None,
                ax_ ,
                eax_ ,
                rax_ ,
                mm0_ ,
                xmm0_ ,
                es_ ,
                cr0_ ,
                dr0_
            ] ,
            [ # rcx
                cl_ , None,
                cx_ ,
                ecx_ ,
                rcx_ ,
                mm1_ ,
                xmm1_ ,
                cs_ ,
                INVD ,
                dr1_
            ] ,
            [ # rdx_
                dl_ , None,
                dx_ ,
                edx_ ,
                rdx_ ,
                mm2_ ,
                xmm2_ ,
                ss_ ,
                cr2_ ,
                dr2_
            ] ,
            [ # rbx_
                bl_ , None,
                bx_ ,
                ebx_ ,
                rbx_ ,
                mm3_ ,
                xmm3_ ,
                ds_ ,
                cr3_ ,
                dr3_
            ] ,
            [ # rsp_
                spl_ , None, #@16 ah_
                sp_ ,
                esp_ ,
                rsp_ ,
                mm4_ ,
                xmm4_ ,
                fs_ ,
                cr4_ ,
                dr4_
            ] ,
            [ # rbp_
                bpl_ , None, #@16 ch_
                bp_ ,
                ebp_ ,
                rbp_ ,
                mm5_ ,
                xmm5_ ,
                gs_ ,
                INVD ,
                dr5_
            ] ,
            [ # rsi_
                sil_ , None, #@16 dh_
                si_ ,
                esi_ ,
                rsi_ ,
                mm6_ ,
                xmm6_ ,
                RESERVED ,
                INVD ,
                dr6_
            ] ,
            [ # rdi_
                dil_ , None, #@16 bh_
                di_ ,
                edi_ ,
                rdi_ ,
                mm7_ ,
                xmm7_ ,
                RESERVED ,
                INVD ,
                dr7_
            ]
        ] ,
        [ # rex.b = 1
            [ # r8
                r8b_, None,
                r8w_ ,
                r8d_ ,
                r8_ ,
                mm0_ ,
                xmm8_ ,
                es_ ,
                cr8_ ,
                INVD
            ] ,
            [ # r9
                r9b_ , None,
                r9w_ ,
                r9d_ ,
                r9_ ,
                mm1_ ,
                xmm9_ ,
                cs_ ,
                INVD ,
                INVD
            ] ,
            [ # r10_
                r10b_ , None,
                r10w_ ,
                r10d_ ,
                r10_ ,
                mm2_ ,
                xmm10_ ,
                ss_ ,
                INVD ,
                INVD
            ] ,
            [ # r11
                r11b_ , None,
                r11w_ ,
                r11d_ ,
                r11_ ,
                mm3_ ,
                xmm11_ ,
                ds_ ,
                INVD ,
                INVD
            ] ,
            [ # r12_
                r12b_ , None,
                r12w_ ,
                r12d_ ,
                r12_ ,
                mm4_ ,
                xmm12_ ,
                fs_ ,
                INVD ,
                INVD
            ] ,
            [ # r13
                r13b_ , None,
                r13w_ ,
                r13d_ ,
                r13_ ,
                mm5_ ,
                xmm13_ ,
                gs_ ,
                INVD ,
                INVD
            ] ,
            [ # r14
                r14b_ , None,
                r14w_ ,
                r14d_ ,
                r14_ ,
                mm6_ ,
                xmm14_ ,
                RESERVED ,
                INVD ,
                INVD ,
            ] ,
            [ # r15
                r15b_ , None,
                r15w_ ,
                r15d_ ,
                r15_ ,
                mm7_ ,
                xmm15_ ,
                RESERVED ,
                INVD ,
                INVD ,
            ]
        ]
    ]

    mod1116 = copy.deepcopy(mod1164)
    mod1116[0][r_rsp][RTr8] = ah_
    mod1116[0][r_rbp][RTr8] = ch_
    mod1116[0][r_rsi][RTr8] = dh_
    mod1116[0][r_rdi][RTr8] = bh_

    ID=2**21 #Identification Flag
    VIP=2**20 #Virtual Interrupt Pending
    VIF=2**19 #Virtual Interrupt
    AC=2**18 #Alignment check
    VM=2**17 #Virtual8086 mode
    RF=2**16 #Resume Flag
    NT=2**14 #Nested Task
    IOPL13=2**13 #I/O Privillege Level
    IOPL12=2**12
    OF=2**11 #status:overflow
    DF=2**10 #control:direction
    IF=2**9 #control:interrupt
    TF=2**8 #control:trap
    SF=2**7 #status:sign
    ZF=2**6 #status:zero
    AF=2**4 #status:auxiliary carry
    PF=2**2 #statis:parity
    CF=2**0 #status:carry

    maskRG=0b00111000
    shftG=3
    maskRM=0b00000111
    maskMB=0b11000000
    shftM=6

    mask=[
        0x00000000000000FF , #RTr8
        0x00000000000000FF , #RTrH
        0x000000000000FFFF , #RTr16
        0x00000000FFFFFFFF , #RTr32
        0xFFFFFFFFFFFFFFFF , #RTr64
        0xFFFFFFFFFFFFFFFF , #RTr64
         0xFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFF #RTr128
        ]

    maskRead=[
        0x00000000000000FF , #RTr8
        0x000000000000FF00 , #RTrH
        0x000000000000FFFF , #RTr16
        0x00000000FFFFFFFF , #RTr32
        0xFFFFFFFFFFFFFFFF , #RTr64
        0xFFFFFFFFFFFFFFFF , #RTr64
         0xFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFF #RTr128
        ]

    maskL=[
     mask[RTr128]^mask[RTr8], #RTr8
     mask[RTr128]^mask[RTrH], #RTrH
     mask[RTr128]^mask[RTr16],#RTr16
     mask[RTr128]^mask[RTr32],#RTr32
     mask[RTr128]^mask[RTr64],#RTr64
     mask[RTr128]^mask[RTr64],
     0x0 #RTr128
    ]

    maskAL=maskRead[RTr8]
    maskAH=maskRead[RTrH]

    maskMSB=[
        1<<7, #RTr8
        1<<7, #RTrH treated as rtr8
        1<<15,#RTr16
        1<<31,#RTr32
        1<<63,#RTr64
        1<<63,
        1<<127 #RTr128
    ]

    maskMSBR=[
        mask[RTr8] - maskMSB[RTr8],
        mask[RTr8] - maskMSB[RTr8],  # attention
        mask[RTr16] - maskMSB[RTr16],
        mask[RTr32] - maskMSB[RTr32],
        mask[RTr64] - maskMSB[RTr64],
        mask[RTr64] - maskMSB[RTr64],
        mask[RTr128]- maskMSB[RTr128]
    ]

    r8=0
    rH=1
    r16=2
    r32=3
    r64=4
    mm=5
    xmm=6
    sreg=7
    eee0=8
    eee1=9

    bits = [
        8, #r8
        8, #rH
        16, #r16
        32, #r32
        64, #r64
        64, #r64 mm
        128, #r128 xmm
        16, #r16 segment register
        32, #r32 control register
        32  #r32 debug register
    ]

    REX = [
      0x0 , #REX
      0x1 , #REX.B
      0x2 , #REX.X
      0x3 , #REX.XB
      0x4 , #REX.R
      0x5 , #REX.RB
      0x6 , #REX.RX
      0x7 , #REX.RXB
      0x8 , #REX.W
      0x9 , #REX.WB
      0xA , #REX.WX
      0xB , #REX.WXB
      0xC , #REX.WR
      0xD , #REX.WRB
      0xE , #REX.WRX
      0xF   #REX.WRXB
    ]

    REXb=1
    REXx=2
    REXr=4
    REXw=8

    modeREAL = 0 #0 real mode
    modeIA32 = 1 #1 IA32 mode(protedted)
    modeV8086 = 2 #2 V8086 mode
    modeIA32e = 3 #3 IA32e mode(64bit)

    stacksize = [
        1 , # cpu.RTr8
        1 , # cpu.RTrH
        2 , # cpu.RTr16
        4 , # cpu.RTr32
        8   # cpu.RTr64
     ]

    LOGIC = 1 #Logical
    ARITH = 0 #Arithmetic



    def rReg(self,reg):
        r = cpu.regp[reg][0]
        rt= cpu.regp[reg][1]
        rv = self.register[r] & cpu.maskRead[rt]
        if rt == cpu.RTrH :
            rv >>= 8
        return rv


    def wReg(self,reg,val):
        r = cpu.regp[reg][0]
        rt= cpu.regp[reg][1]
        dmask = cpu.maskRead[rt]
        maskL = cpu.maskRead[cpu.RTr128] ^ dmask
        old = self.register[r]

        if rt == cpu.RTrH:
            val <<= 8
            #print(hex(val))

        old &= maskL
        val &= dmask
        self.register[r] = old | val
        return self.register[r]

    def disp(self,rt): #displacement
        r=0
        c=0
        bits = cpu.bits[rt]
        while bits > 0:
            r += self.readNextMem(self.CS) << (cpu.bits[cpu.RTr8]*c)
            c += 1
            bits -= 8
        return r


    def wMem(self,addr,v,rt,seg):
        c=0
        bits = int(cpu.bits[rt]>>3) #Division by 8 = bits2bytes
        while bits > c:
            bt = v & 0xff #lowest 1 byte
            self.mem.set(addr + (seg<<4), bt)
            s='wMem [0x{2:04X}:0x{0:04X}]:0x{1:02X}'.format(addr, bt, seg)

            cpu.dbgp(s)
            v >>= 8
            c += 1
            addr += 1



    def rMem(self,addr,rt,seg):
        r=0
        c=0
        bits = int(cpu.bits[rt]>>3) #Division by 8 -> bits2bytes
        while bits > c:
            bt = self.mem.get(addr + (seg<<4))
            r += bt << (8*c)
            s='rMem [0x{2:04X}:0x{0:04X}]:0x{1:02X}'.format(addr, bt, seg)
            #s='c={0} r={1:X}'.format(c, r)
            cpu.dbgp(s)
            c += 1
            addr += 1
        return r


    def initReg(self):
        self.wReg(cpu.cs_ , 0)
        self.wReg(cpu.ds_ , 0)
        self.wReg(cpu.es_ , 0)
        self.wReg(cpu.fs_ , 0)
        self.wReg(cpu.gs_ , 0)

        #self.SS = self.mem.memmax - (self.mem.segment - 1)
        self.SS = 0

        self.wReg(cpu.ss_ , self.SS)

        #rsp = self.SS + self.mem.segment - 1
        rsp = self.mem.segment - 1
        self.wReg(cpu.rsp_ , rsp)
        #cpu.dbgp('seg:{0} reg:{1}'.format(self.mem.segment , self.rReg(cpu.rsp_)))


    def __init__(self,memory):
        self.eip=0
        self.eflags=0
        self.mem=memory
        self.register = [0 for x in range(0,cpu.r_NREG)]

        self.SS = 0 # stack segment
        self.CS = 0 # code segment
        self.DS = 0 # data segment
        self.ES = 0 # extra segment
        self.seg = 0 # Overrided segment value
        self.override = False


        self.Mod=0 # ModRM's Mod
        self.Mrm=0 # ModRM's RM
        self.rm=0  # rm pointer
        self.Mro=0 # ModRM's reg/op
        self.ro=0  # r/o value


        self.defaultDB = cpu.RTr16
        self.DB = cpu.RTr16
        #16bit = cpu.RTr16
        #32bit = cpu.RTr32
        #64bit = cpu.RTr64


        self.cpumode = cpu.modeREAL
        #0 REAL mode
        #1 IA32 mode(protedted)
        #2 V8086 mode
        #3 IA32e mode(64bit)

        self.rexw = self.rexr = self.rexx = self.rexb = 0

        self.dstO=self.dstV=0
        self.srcO=self.srcV=0
        self.drm=0
        self.dRT=self.sRT=0
        # dstO = dest Operand
        # dstV = value of dest
        # dRT = resource type of dest
        # drm = dest type, register or memory(its meaning is same as Mod)
        # srvO = src Operand
        # srcV = value of src
        # sRT = resource type of src

        self.opStr = ''
        self._scf = 0  # temporary ShiftCarry
        self._ccf = 0  # temporary CompletionCarry
        self.displaytext=''

        self.ftbl16=[
        # [modbit][rg or rm]
        # modbit 0b00
        [
        lambda : self.rReg(cpu.bx_) + self.rReg(cpu.si_) , #000
        lambda : self.rReg(cpu.bx_) + self.rReg(cpu.di_) , #001
        lambda : self.rReg(cpu.bp_) + self.rReg(cpu.si_) , #010
        lambda : self.rReg(cpu.bp_) + self.rReg(cpu.di_) , #011
        lambda : self.rReg(cpu.si_) , #100
        lambda : self.rReg(cpu.di_) , #101
        lambda : self.disp(cpu.RTr16) , #110
        lambda : self.rReg(cpu.bx_) #111
        ],

        # modbit 0b01. disp8 series
        [
        lambda : self.rReg(cpu.bx_) + self.rReg(cpu.si_) + self.disp(cpu.RTr8) , #000
        lambda : self.rReg(cpu.bx_) + self.rReg(cpu.di_) + self.disp(cpu.RTr8) , #001
        lambda : self.rReg(cpu.bp_) + self.rReg(cpu.si_) + self.disp(cpu.RTr8) , #010
        lambda : self.rReg(cpu.bp_) + self.rReg(cpu.di_) + self.disp(cpu.RTr8) , #011
        lambda : self.rReg(cpu.si_) + self.disp(cpu.RTr8) , #100
        lambda : self.rReg(cpu.di_)+ self.disp(cpu.RTr8) , #101
        lambda : self.rReg(cpu.bp_)+ self.disp(cpu.RTr8) , #110
        lambda : self.rReg(cpu.bx_)+ self.disp(cpu.RTr8) , #111
        ],

        # modbit 0b10  disp16 series
        [
        lambda : self.rReg(cpu.bx_) + self.rReg(cpu.si_) + self.disp(cpu.RTr16) , #000
        lambda : self.rReg(cpu.bx_) + self.rReg(cpu.di_) + self.disp(cpu.RTr16) , #001
        lambda : self.rReg(cpu.bp_) + self.rReg(cpu.si_) + self.disp(cpu.RTr16) , #010
        lambda : self.rReg(cpu.bp_) + self.rReg(cpu.di_) + self.disp(cpu.RTr16) , #011
        lambda : self.rReg(cpu.si_) + self.disp(cpu.RTr16) , #100
        lambda : self.rReg(cpu.di_) + self.disp(cpu.RTr16) , #101
        lambda : self.rReg(cpu.bp_) + self.disp(cpu.RTr16) , #110
        lambda : self.rReg(cpu.bx_) + self.disp(cpu.RTr16)   #111
        ]
        ]

        self.rf=[ #mod=0,1,2,3
         lambda d,dR,seg: self.rMem(d,dR,seg) ,
         lambda d,dR,seg : self.rMem(d,dR,seg) ,
         lambda d,dR,seg : self.rMem(d,dR,seg) ,
         lambda d,dR,seg : self.rReg(d)
         ]

        self.wf=[ #mod=0,1,2,3
         lambda d,v,dR,seg: self.wMem(d,v,dR,seg),
         lambda d,v,dR,seg: self.wMem(d,v,dR,seg),
         lambda d,v,dR,seg: self.wMem(d,v,dR,seg),
         lambda d,v,dR,seg: self.wReg(d,v)
         ]

        self.modstr=[ #mod 0,1,2,3
         lambda x : "M[{0}]".format(x),
         lambda x : "M[{0}]".format(x),
         lambda x : "M[{0}]".format(x),
         lambda x : "R[{0}]".format(cpu.regp[x][2])
        ]

        self.opcode = [
        lambda x : self.op_add(
        self.Mrmyrx, cpu.RTr8, cpu.RTr8),#00
        lambda x : self.op_add(
        self.Mrmyrx, self.DB, self.DB),#01
        lambda x : self.op_add(
        self.Mrxrmy, cpu.RTr8, cpu.RTr8),#02
        lambda x : self.op_add(
        self.Mrxrmy, self.DB, self.DB),#03
        lambda x : self.op_add(
        self.Srxiz, cpu.al_, cpu.RTr8),#04
        lambda x : self.op_add(
        self.Srxiz, cpu.rax_, self.DB),#05
        lambda x : self.op_push(
        self.Srx, cpu.es_, 0),#06   #16bit
        lambda x : self.op_pop(
        self.Srx, cpu.es_, 0),#07   #16bit


        lambda x : self.op_or(
        self.Mrmyrx, cpu.RTr8, cpu.RTr8),#08
        lambda x : self.op_or(
        self.Mrmyrx, self.DB, self.DB),#09
        lambda x : self.op_or(
        self.Mrxrmy, cpu.RTr8, cpu.RTr8),#0A
        lambda x : self.op_or(
        self.Mrxrmy, self.DB, self.DB),#0B
        lambda x : self.op_or(
        self.Srxiz, cpu.al_, cpu.RTr8),#0C
        lambda x : self.op_or(
        self.Srxiz, cpu.rax_, self.DB),#0D
        lambda x : self.op_push(
        self.Srx, cpu.cs_, 0),#0E   #16bit
        lambda x : self.op_(x),
        #self.Srx, cpu.es_, 0),#0F

        lambda x : self.op_adc(
        self.Mrmyrx, cpu.RTr8, cpu.RTr8),#10
        lambda x : self.op_adc(
        self.Mrmyrx, self.DB, self.DB),#11
        lambda x : self.op_adc(
        self.Mrxrmy, cpu.RTr8, cpu.RTr8),#12
        lambda x : self.op_adc(
        self.Mrxrmy, self.DB, self.DB),#13
        lambda x : self.op_adc(
        self.Srxiz, cpu.al_, cpu.RTr8),#14
        lambda x : self.op_adc(
        self.Srxiz, cpu.rax_, self.DB),#15
        lambda x : self.op_push(
        self.Srx, cpu.ss_, 0),#16   #16bit
        lambda x : self.op_pop(
        self.Srx, cpu.ss_, 0),#17   #16bit

        lambda x : self.op_sbb(
        self.Mrmyrx, cpu.RTr8, cpu.RTr8),#18
        lambda x : self.op_sbb(
        self.Mrmyrx, self.DB, self.DB),#19
        lambda x : self.op_sbb(
        self.Mrxrmy, cpu.RTr8, cpu.RTr8),#1A
        lambda x : self.op_sbb(
        self.Mrxrmy, self.DB, self.DB),#1B
        lambda x : self.op_sbb(
        self.Srxiz, cpu.al_, cpu.RTr8),#1C
        lambda x : self.op_sbb(
        self.Srxiz, cpu.rax_, self.DB),#1D
        lambda x : self.op_push(
        self.Srx, cpu.ds_, 0),#1E   #16bit
        lambda x : self.op_pop(
        self.Srx, cpu.ds_, 0),#1F   #16bit

        lambda x : self.op_and(
        self.Mrmyrx, cpu.RTr8, cpu.RTr8),#20
        lambda x : self.op_and(
        self.Mrmyrx, self.DB, self.DB),#21
        lambda x : self.op_and(
        self.Mrxrmy, cpu.RTr8, cpu.RTr8),#22
        lambda x : self.op_and(
        self.Mrxrmy, self.DB, self.DB),#23
        lambda x : self.op_and(
        self.Srxiz, cpu.al_, cpu.RTr8),#24
        lambda x : self.op_and(
        self.Srxiz, cpu.rax_, self.DB),#25
        lambda x : self.op_push(
        self.Srx, cpu.es_, 0),#26   #16bit
        lambda x : self.op_daa(
        self.Srx, cpu.al_, 0),#27   #16bit

        lambda x : self.op_sub(
        self.Mrmyrx, cpu.RTr8, cpu.RTr8),#28
        lambda x : self.op_sub(
        self.Mrmyrx, self.DB, self.DB),#29
        lambda x : self.op_sub(
        self.Mrxrmy, cpu.RTr8, cpu.RTr8),#2A
        lambda x : self.op_sub(
        self.Mrxrmy, self.DB, self.DB),#2B
        lambda x : self.op_sub(
        self.Srxiz, cpu.al_, cpu.RTr8),#2C
        lambda x : self.op_sub(
        self.Srxiz, cpu.rax_, self.DB),#2D
        lambda x : self.op_segoverride(
        self.Srx, cpu.cs_,0),#2E   #16bit
        lambda x : self.op_das(
        self.Srx, cpu.al_, 0),#2F   #16bit

        lambda x : self.op_xor(
        self.Mrmyrx, cpu.RTr8, cpu.RTr8),#30
        lambda x : self.op_xor(
        self.Mrmyrx, self.DB, self.DB),#31
        lambda x : self.op_xor(
        self.Mrxrmy, cpu.RTr8, cpu.RTr8),#32
        lambda x : self.op_xor(
        self.Mrxrmy, self.DB, self.DB),#33
        lambda x : self.op_xor(
        self.Srxiz, cpu.al_, cpu.RTr8),#34
        lambda x : self.op_xor(
        self.Srxiz, cpu.rax_, self.DB),#35
        lambda x : self.op_segoverride(
        self.Srx, cpu.ss_, 0),#36   #16bit
        lambda x : self.op_aaa(
        self.Srxrx, cpu.al_, cpu.ah_),#37


        lambda x : self.op_cmp(
        self.Mrmyrx, cpu.RTr8, cpu.RTr8),#38
        lambda x : self.op_cmp(
        self.Mrmyrx, self.DB, self.DB),#39
        lambda x : self.op_cmp(
        self.Mrxrmy, cpu.RTr8, cpu.RTr8),#3A
        lambda x : self.op_cmp(
        self.Mrxrmy, self.DB, self.DB),#3B
        lambda x : self.op_cmp(
        self.Srxiz, cpu.al_, cpu.RTr8),#3C
        lambda x : self.op_cmp(
        self.Srxiz, cpu.rax_, self.DB),#3D
        lambda x : self.op_segoverride(
        self.Srx, cpu.ds_, 0),#3E
        lambda x : self.op_aas(
        self.Srxrx, cpu.al_, cpu.ah_),#3F

        lambda x : self.op_inc(),#40
        lambda x : self.op_inc(),#41
        lambda x : self.op_inc(),#42
        lambda x : self.op_inc(),#43
        lambda x : self.op_inc(),#44
        lambda x : self.op_inc(),#45
        lambda x : self.op_inc(),#46
        lambda x : self.op_inc(),#47
        lambda x : self.op_dec(),#48
        lambda x : self.op_dec(),#49
        lambda x : self.op_dec(),#4A
        lambda x : self.op_dec(),#4B
        lambda x : self.op_dec(),#4C
        lambda x : self.op_dec(),#4D
        lambda x : self.op_dec(),#4E
        lambda x : self.op_dec(),#4F

        lambda x : self.op_push(
        self.SSrx, cpu.r_rax, self.DB),#50
        lambda x : self.op_push(
        self.SSrx, cpu.r_rcx, self.DB),#51
        lambda x : self.op_push(
        self.SSrx, cpu.r_rdx, self.DB),#52
        lambda x : self.op_push(
        self.SSrx, cpu.r_rbx, self.DB),#53
        lambda x : self.op_push(
        self.SSrx, cpu.r_rsp, self.DB),#54
        lambda x : self.op_push(
        self.SSrx, cpu.r_rbp, self.DB),#55
        lambda x : self.op_push(
        self.SSrx, cpu.r_rsi, self.DB),#56
        lambda x : self.op_push(
        self.SSrx, cpu.r_rdi, self.DB),#57

        lambda x : self.op_pop(
        self.SSrx, cpu.r_rax, self.DB),#58
        lambda x : self.op_pop(
        self.SSrx, cpu.r_rcx, self.DB),#59
        lambda x : self.op_pop(
        self.SSrx, cpu.r_rdx, self.DB),#5A
        lambda x : self.op_pop(
        self.SSrx, cpu.r_rbx, self.DB),#5B
        lambda x : self.op_pop(
        self.SSrx, cpu.r_rsp, self.DB),#5C
        lambda x : self.op_pop(
        self.SSrx, cpu.r_rbp, self.DB),#5D
        lambda x : self.op_pop(
        self.SSrx, cpu.r_rsi, self.DB),#5E
        lambda x : self.op_pop(
        self.SSrx, cpu.r_rdi, self.DB),#5F

        lambda x : self.op_pusha(
        self.noArgs,0,0),#60
        lambda x : self.op_popa(
        self.noArgs,0,0),#61
        lambda x : self.op_bound(
        self.Mrxrmy, self.DB, self.DB),#62
        lambda x : self.op_arpl(
        self.Mrmyrx, cpu.RTr16, cpu.RTr16),#63
        lambda x : self.op_segoverride(
        self.Srx, cpu.fs_, 0),#64
        lambda x : self.op_segoverride(
        self.Srx, cpu.gs_, 0),#65
        
        lambda x : self.prefix(),#66
        lambda x : self.prefix(),#67
        lambda x : self.prefix(),#68
        
        lambda x : self.op_push(
        self.Siz, self.DB,0),#69
        
        lambda x : self.op_imul(
        self.Mrmy, self.DB, self.DB),#6A
        
        lambda x : self.op_push(
        self.Siz, cpu.RTr8, 0),#6B
        
        lambda x : self.op_ins(
        	self.Sarg, cpu.RTr8, 0),#6C
        lambda x : self.op_ins(
        	self.Sarg, self.DB, 0),#6D
        
        lambda x : self.op_outs(
        	self.Sarg, cpu.RTr8, 0),#6E
        lambda x : self.op_outs(
        	self.Sarg, self.DB, 0),#6F
        
        lambda x : self.op_jo(
        	self.Siz, cpu.RTr8, True),#70 jo
        lambda x : self.op_jo(
        	self.Siz, cpu.RTr8, False),#71 jno
        lambda x : self.op_jc(
        	self.Siz, cpu.RTr8, True),#72 jc
        lambda x : self.op_jc(
        	self.Siz, cpu.RTr8, False),#73 jnc
        lambda x : self.op_jz(
        	self.Siz, cpu.RTr8, True),#74 jz
        lambda x : self.op_jz(
        	self.Siz, cpu.RTr8, False),#75 jnz
        lambda x : self.op_jbe(
        	self.Siz, cpu.RTr8, True),#76 jbe
        lambda x : self.op_jbe(
        	self.Siz, cpu.RTr8, False),#77 jnbe
        lambda x : self.op_js(
        	self.Siz, cpu.RTr8, True),#78 js
        lambda x : self.op_js(
        	self.Siz, cpu.RTr8, False),#79 jns
        lambda x : self.op_jp(
        	self.Siz, cpu.RTr8, True),#7A jp
        lambda x : self.op_jp(
        	self.Siz, cpu.RTr8, False),#7B jnp
        lambda x : self.op_jl(
        	self.Siz, cpu.RTr8, True),#7C jl
        lambda x : self.op_jl(
        	self.Siz, cpu.RTr8, False),#7D jnl
        lambda x : self.op_jle(
        	self.Siz, cpu.RTr8, True),#7E jle
        lambda x : self.op_jle(
        	self.Siz, cpu.RTr8, False),#7F jnle
        	
        lambda x : self.op_8x(
        	self.Mrmyiz, cpu.RTr8, cpu.RTr8),#80
        lambda x : self.op_8x(
        	self.Mrmyiz, self.DB, self.DB),#81
        lambda x : self.op_8x(
        	self.Mrmyiz, cpu.RTr8, cpu.RTr8),#82
        lambda x : self.op_8x(
        	self.Mrmyiz, self.DB, cpu.RTr8),#83
        
        lambda x : self.op_test(
        	self.Mrmyrx, cpu.RTr8, cpu.RTr8),#84
        lambda x : self.op_test(
        	self.Mrmyrx, self.DB, self.DB),#85
        
        lambda x : self.op_xchg(
        	self.Mrxrmy, cpu.RTr8, cpu.RTr8),#86
        lambda x : self.op_xchg(
        	self.Mrmyrx, self.DB, self.DB),#87
        	
        lambda x : self.op_mov(
        	self.Mrmyrx, cpu.RTr8, cpu.RTr8),#88
        lambda x : self.op_mov(
        	self.Mrmyrx, self.DB, self.DB),#89
        lambda x : self.op_mov(
        	self.Mrxrmy, cpu.RTr8, cpu.RTr8),#8A
        lambda x : self.op_mov(
        	self.Mrxrmy, self.DB, self.DB),#8B
        
        lambda x : self.op_mov(
        	self.Mrmyrx, self.DB, cpu.sreg),#8C
        
        lambda x : self.op_lea(
        	self.Mrxrmy, self.DB, self.DB),#8D
        
        lambda x : self.op_mov(
        	self.Mrxrmy, cpu.sreg, cpu.RTr16),#8E
        
        lambda x : self.op_pop(
        	self.Mrmy, self.DB, self.DB),#8F
        
        lambda x : self.op_ ,#90
        lambda x : self.op_ ,#91
        lambda x : self.op_ ,#92
        lambda x : self.op_ ,#93
        lambda x : self.op_ ,#94
        lambda x : self.op_ ,#95
        lambda x : self.op_ ,#96
        lambda x : self.op_ ,#97
        lambda x : self.op_ ,#98
        lambda x : self.op_ ,#99
        lambda x : self.op_ ,#9A
        lambda x : self.op_ ,#9B
        lambda x : self.op_ ,#9C
        lambda x : self.op_ ,#9D
        lambda x : self.op_ ,#9E
        lambda x : self.op_ ,#9F
        lambda x : self.op_ ,#A0
        lambda x : self.op_ ,#A1
        lambda x : self.op_ ,#A2
        lambda x : self.op_ ,#A3
        lambda x : self.op_ ,#A4
        lambda x : self.op_ ,#A5
        lambda x : self.op_ ,#A6
        lambda x : self.op_ ,#A7
        lambda x : self.op_ ,#A8
        lambda x : self.op_ ,#A9
        lambda x : self.op_ ,#AA
        lambda x : self.op_ ,#AB
        lambda x : self.op_ ,#AC
        lambda x : self.op_ ,#AD
        lambda x : self.op_ ,#AE
        lambda x : self.op_ ,#AF
        
        lambda x : self.op_mov(
        	self.Srxiz, cpu.al_, cpu.RTr8),#B0
        lambda x : self.op_mov(
        	self.Srxiz, cpu.cl_, cpu.RTr8) ,#B1
        lambda x : self.op_mov(
        	self.Srxiz, cpu.dl_, cpu.RTr8) ,#B2
        lambda x : self.op_mov(
        	self.Srxiz, cpu.bl_, cpu.RTr8) ,#B3
        lambda x : self.op_mov(
        	self.Srxiz, cpu.ah_, cpu.RTr8) ,#B4
        lambda x : self.op_mov(
        	self.Srxiz, cpu.ch_, cpu.RTr8) ,#B5
        lambda x : self.op_mov(
        	self.Srxiz, cpu.dh_, cpu.RTr8) ,#B6
        lambda x : self.op_mov(
        	self.Srxiz, cpu.bh_, cpu.RTr8) ,#B7
        
        lambda x : self.op_mov(
        	self.Srxiz, cpu.mod1116[self.rexb][cpu.r_rax][self.DB], self.DB),#B8
        lambda x : self.op_mov(
        	self.Srxiz, cpu.mod1116[self.rexb][cpu.r_rcx][self.DB], self.DB) ,#B9
        lambda x : self.op_mov(
        	self.Srxiz, cpu.mod1116[self.rexb][cpu.r_rdx][self.DB], self.DB) ,#BA
        lambda x : self.op_mov(
        	self.Srxiz, cpu.mod1116[self.rexb][cpu.r_rbx][self.DB], self.DB) ,#BB
        lambda x : self.op_mov(
        	self.Srxiz, cpu.mod1116[self.rexb][cpu.r_rsp][self.DB], self.DB) ,#BC
        lambda x : self.op_mov(
        	self.Srxiz, cpu.mod1116[self.rexb][cpu.r_rbp][self.DB], self.DB) ,#BD
        lambda x : self.op_mov(
        	self.Srxiz, cpu.mod1116[self.rexb][cpu.r_rsi][self.DB], self.DB) ,#BE
        lambda x : self.op_mov(
        	self.Srxiz, cpu.mod1116[self.rexb][cpu.r_rdi][self.DB], self.DB) ,#BF
        	
        lambda x : self.op_ ,#C0
        lambda x : self.op_ ,#C1
        lambda x : self.op_ ,#C2
        lambda x : self.op_ ,#C3
        lambda x : self.op_ ,#C4
        lambda x : self.op_ ,#C5
        lambda x : self.op_ ,#C6
        lambda x : self.op_ ,#C7
        lambda x : self.op_ ,#C8
        lambda x : self.op_ ,#C9
        lambda x : self.op_ ,#CA
        lambda x : self.op_ ,#CB
        lambda x : self.op_ ,#CC
        lambda x : self.intImm8() ,#CD
        lambda x : self.op_ ,#CE
        lambda x : self.op_ ,#CF
        lambda x : self.op_ ,#D0
        lambda x : self.op_ ,#D1
        lambda x : self.op_ ,#D2
        lambda x : self.op_ ,#D3
        lambda x : self.op_ ,#D4
        lambda x : self.op_ ,#D5
        lambda x : self.op_ ,#D6
        lambda x : self.op_ ,#D7
        lambda x : self.op_ ,#D8
        lambda x : self.op_ ,#D9
        lambda x : self.op_ ,#DA
        lambda x : self.op_ ,#DB
        lambda x : self.op_ ,#DC
        lambda x : self.op_ ,#DD
        lambda x : self.op_ ,#DE
        lambda x : self.op_ ,#DF
        lambda x : self.op_ ,#E0
        lambda x : self.op_ ,#E1
        lambda x : self.op_ ,#E2
        lambda x : self.op_ ,#E3
        lambda x : self.op_ ,#E4
        lambda x : self.op_ ,#E5
        lambda x : self.op_ ,#E6
        lambda x : self.op_ ,#E7
        lambda x : self.op_ ,#E8
        lambda x : self.op_ ,#E9
        lambda x : self.op_ ,#EA
        lambda x : self.op_jmpRel8() ,#EB
        lambda x : self.op_ ,#EC
        lambda x : self.op_ ,#ED
        lambda x : self.op_ ,#EE
        lambda x : self.op_ ,#EF
        lambda x : self.op_ ,#F0
        lambda x : self.op_ ,#F1
        lambda x : self.op_ ,#F2
        lambda x : self.op_ ,#F3
        lambda x : self.op_ ,#F4
        lambda x : self.op_ ,#F5
        lambda x : self.op_ ,#F6
        lambda x : self.op_ ,#F7
        lambda x : self.op_ ,#F8
        lambda x : self.op_ ,#F9
        lambda x : self.op_ ,#FA
        lambda x : self.op_ ,#FB
        lambda x : self.op_ ,#FC
        lambda x : self.op_ ,#FD
        lambda x : self.op_ ,#FE
        
        ]

        self.initReg()


    def tocomp(self,r1,rt):
        t = (~r1) + 1
        if r1 == 0 or t > cpu.mask[rt]:
            self._ccf = 1
        else:
            self._ccf = 0
        #cpu.dbgp('tocomp: {0} -> {1}'.format(r1,t&cpu.mask[rt]))
        return t & cpu.mask[rt]


    def tocomp2(self,ru,rl,rt):
        rl2 = self.tocomp(rl,rt)
        if self._ccf == 1:
            ru2 = self.tocomp(ru,rt)
        else:
            ru2 = (~ru) & cpu.mask[rt]

        #s = 'tocomp2: u:l={0}:{1}={8}:{9}=val:{2}|{3} -> ru:rl={4}:{5}={10}:{11}=val:{6}|{7}'.format(ru, rl, (ru<<cpu.bits[rt])+rl, cpu.sb2sd((ru<<cpu.bits[rt])+rl , rt+1), ru2, rl2, (ru2<<cpu.bits[rt])+rl2, cpu.sb2sd((ru2<<cpu.bits[rt])+rl2,rt+1), cpu.sb2sd(ru, rt), cpu.sb2sd(rl, rt), cpu.sb2sd(ru2, rt), cpu.sb2sd(rl2, rt))
        #cpu.dbgp(s)

        return ru2,rl2




    def sb2sd(val,rt):
        '''
        Signed Binary
        to Signed Decimal
        '''
        m = -(val & cpu.maskMSB[rt])
        s =   val & cpu.maskMSBR[rt]
        return m | s


    def signex(val,rtf,rtt):
        '''
        Sign Extend
        from rtf to rtt
        '''
        m = cpu.sb2sd(val, rtf)
        return m & cpu.mask[rtt]




    def chkOF(v1,v2,v3,rt):
        '''
        v1 & v2=msb 1 & v3=msb 0 ->T
        v1 & v2=msb 0 & v3=msb 1 ->T
        '''
        c1 = cpu.chkMSB(v1,rt)
        c2 = cpu.chkMSB(v2,rt)
        c3 = cpu.chkMSB(v3,rt)
        s='chkOF: op1MSB[{0}] op2MSB[{1}] resultMSB[{2}] ->'.format(c1,c2,c3)
        if ( c1 and c2 and (not c3)) or ( (not c1) and (not c2) and c3 ):
            s=s+'True'
            cpu.dbgp(s)
            return True
        else:
            s=s+'False'
            cpu.dbgp(s)
            return False


    def chkCF(val):
        s='chkCF:{0}'.format(val)
        cpu.dbgp(s)
        return True if val == 1 else False

    def chkZF(val,rt):
        '''
        val is all 0 -> T
        '''
        mask = cpu.mask[rt]
        v = val & mask
        retval = True if v == 0 else False
        s='chkZF:{0:b}({0}) & mask({1:b})({1}) -> {2:b}({2})  ZF:{3}'.format(val,mask,v,retval)
        cpu.dbgp(s)
        return retval


    def chkMSB(val,rt):
        mask = cpu.maskMSB[rt]
        v = val & mask
        retval = True if v >0 else False
        s='chkMSB/SF[mask({2:0b})({2})]:{0:b}({0}) -> MSB:{1:b}({1})  SF:{3}'.format(val , v, mask, retval)
        cpu.dbgp(s)
        return retval


    def chkPF(val,rt):
        v = val & 0x0F # least byte
        # 0,3,5,9,10,12,15(0,2,2,2,2,2,4)
        if v == 0b0011 or v == 0b0101 or v == 0b1001 or v == 0b1010 or v == 0b1100 or v == 0x00 or v == 0x1111:
           retval = True
        else:
           retval = False
        s='chkPF:{0:b}({0}) -> mask(1111)(15):{1:b}({1})  PF:{2}'.format(val , v, retval)
        cpu.dbgp(s)
        return retval



    def chkAF(v1,v2,v3):
        '''
        example
                             5b 5b 5b
        00100 + 01000 = 01100 0 0 0  nc
        01000 + 01000 = 10000 0 0 1  c
        10000 + 01000 = 11000 1 0 1  nc
        11000 + 01000 =100000 1 0 0  c
        01000 + 10000 = 11000 0 1 1  nc
        10000 + 10000 =100000 1 1 0  nc
        11000 + 10000 =101000 1 1 0  nc
        01000 + 11000 =100000 0 1 0  c
        10000 + 11000 =101000 1 1 0  nc
        11000 + 11000 =110000 1 1 1  c

        5bit's pattern
        s s   d
        0 0 = 0 n   no carried
        0 0 = 1 c   carried
        0 1 = 0 c   carried
        0 1 = 1 n   no carried
        1 0 = 0 c   carried
        1 0 = 1 n   no carried
        1 1 = 0 n   no carried
        1 1 = 1 c   carried

        TRue's pattern(carried)
        v1+v2=0 and v3=1
        v1+v2=1 and v3=0
        v1+v2=2 and v3=1
        '''
        v12 = (v1 & 0x10) + (v2 & 0x10)
        v33 = v3 & 0x10
        if (v12 == 0 and v33 == 0x10) or (v12 == 0x10 and v33 == 0) or (v12 == 0x20 and v33 == 0x10):
           retval = True
        else:
           retval = False
        s='chkAF:{0:09b}({0}) , {1:09b}({1}) -> {2:09b}({2})  AF:{3}'.format(v1,v2,v3,retval)
        cpu.dbgp(s)
        return retval


    def flagchk(self,flg,o1,o2,r,rt):
        if flg & cpu.CF:
            if cpu.chkCF(self._scf):
                self.flagOn(cpu.CF)
            else:
                self.flagOff(cpu.CF)

        if flg & cpu.ZF :
            if cpu.chkZF(r,rt):
                self.flagOn(cpu.ZF)
            else:
                self.flagOff(cpu.ZF)

        if flg & cpu.OF :
            if cpu.chkOF(o1,o2,r,rt):
                self.flagOn(cpu.OF)
            else:
                self.flagOff(cpu.OF)

        if flg & cpu.SF :
            if cpu.chkMSB(r,rt):
                self.flagOn(cpu.SF)
            else:
                self.flagOff(cpu.SF)

        if flg & cpu.AF :
            if cpu.chkAF(o1,o2,r):
                self.flagOn(cpu.AF)
            else:
                self.flagOff(cpu.AF)

        if flg & cpu.PF :
            if cpu.chkPF(r,rt):
                self.flagOn(cpu.PF)
            else:
                self.flagOff(cpu.PF)
        pass


    def getflag(self,flg):
        return True if self.eflags & flg else False


    def flagOff(self,flag):
        v = self.eflags & ( ~flag )
        self.eflags = v
        #cpu.dbgp('flagOff:{1:b} eflags:{0:b}'.format(self.eflags,flag))
        return self.eflags



    def flagOn(self,flag):
        v = self.eflags | flag
        self.eflags = v
        #cpu.dbgp('flagOn:{1:b} eflags:{0:b}'.format(self.eflags,flag))
        return self.eflags



    def dumpRegister(self,index):
        if index == -1 :
            print('DumpRegister')
            for i in range(0, cpu.r_NREG):
                rp=cpu.r2reg[i]
                s='[{0}]:{1} '.format(cpu.regp[rp][2], hex(self.rReg(rp)))
                print(s,end="")
            print()
        elif index < -1 :
            print('DumpRegister Main')
            for i in range(0, 8):
                rp=cpu.r2reg[i]
                s='[{0}]:{1} '.format(cpu.regp[rp][2], hex(self.rReg(rp)))
                print(s,end="")
            print()
        else:
            s='[{0}]:{1}'.format(cpu.regp[index][2] , hex(self.rReg(index)))
            print(s)

        s='DB:{0}'.format(self.DB)
        cpu.dbgp(s)

        print('eip:0x{0:X}({0})'.format(self.eip))
        s='eflags:{0:b}'.format(self.eflags)
        print(s)

        '''
        OF=2**11 #status:overflow
        DF=2**10 #control:direction
        IF=2**9 #control:interrupt
        TF=2**8 #control:trap
        SF=2**7 #status:sign
        ZF=2**6 #status:zero
        AF=2**4 #status:auxiliary carry
        PF=2**2 #statis:parity
        CF=2**0 #status:carry
        '''
        s='OB:{0} DA:{1} I9:{2} T8:{3} S7:{4} Z6:{5} A4:{6} P2:{7} C0:{8}'.format(
        True if self.eflags & cpu.OF else False ,
        True if self.eflags & cpu.DF else False ,
        True if self.eflags & cpu.IF else False ,
        True if self.eflags & cpu.TF else False ,
        True if self.eflags & cpu.SF else False ,
        True if self.eflags & cpu.ZF else False ,
        True if self.eflags & cpu.AF else False ,
        True if self.eflags & cpu.PF else False ,
        True if self.eflags & cpu.CF else False)
        print(s)



    def dumpMemory(self,start,finish):
        for i in range(start,finish+1):
            m = i % (self.mem.memmax + 1)
            print('mem[{2}:{0}]:0x{1:X}({1})'.format(m, self.rMem(m, cpu.RTr8,0),0))

    def opstat(o1,o2,r,rt):
        s='opstat OP1:0x{0:X}({0})({1}) OP2:0x{2:X}({2})({3}) -> RESULT:0x{4:X}({5})({3})'.format(o1 , cpu.sb2sd(o1,rt) , o2 , cpu.sb2sd(o2,rt) , r , cpu.sb2sd(r,rt))
        cpu.dbgp(s)



    def readMem(self,seg):
        #v = self.mem.get(self.eip)
        v = self.rMem(self.eip, cpu.RTr8, seg)
        s = 'readM[{2}:{0}]:0x{1:X}({1})'.format(self.eip , v & cpu.mask[cpu.RTr8], seg)
        cpu.dbgp(s)
        return (v & cpu.mask[cpu.RTr8])


    def readNextMem(self,seg):
        self.eip += 1
        #v = self.mem.get(self.eip)
        v = self.rMem(self.eip, cpu.RTr8, seg)
        s = 'readNM[{2}:{0}]:0x{1:X}({1})'.format(self.eip , v & cpu.mask[cpu.RTr8] ,seg)
        cpu.dbgp(s)
        return (v & cpu.mask[cpu.RTr8])



    def ModRM(self, mod, RTro, RTrm):
        self.Mro = (mod & cpu.maskRG)>>cpu.shftG
        self.Mrm = (mod & cpu.maskRM)
        self.Mod = (mod & cpu.maskMB)>>cpu.shftM
        s='ModRM:0x{0:02X} Mod:{1:02b}({1}) Reg:{2:03b}({2}) rm:{3:03b}({3})'.format(mod, self.Mod, self.Mro, self.Mrm)
        #self.dumpMemory(self.eip,self.eip+3)
        cpu.dbgp(s)

        if not self.Mod == 0b11:
            self.ro = cpu.mod1116[self.rexb][self.Mro][RTro]

            self.rm = (self.ftbl16[self.Mod][self.Mrm])()
            s='ModRM: reg={0} rm=M[{1}]:{2}'.format(cpu.regp[self.ro][2], self.rm, self.rMem(self.rm,RTrm,self.CS))
            cpu.dbgp(s)
        else:
            self.rm = cpu.mod1116[self.rexb][self.Mrm][RTrm]
            self.ro = cpu.mod1116[self.rexb][self.Mro][RTro]
            s='ModRM: reg={0} rm={1}({2})'.format(cpu.regp[self.ro][2], cpu.regp[self.rm][2],self.rReg(self.rm))
            cpu.dbgp(s)

        self.drm = self.Mod

        return self.Mod, self.Mro, self.Mrm



    def segOVR(self,defaultseg):
        return self.segOV if self.override == True else defaultseg



    def intImm8(self):
        Imm8 = self.readNextMem(self.CS)

        if Imm8 == 0x10 :
            ah=self.rReg(cpu.ah_)
            al=self.rReg(cpu.al_)
            s='INT 0x{0:X}'.format(Imm8)
            cpu.msg(s)
            if ah == 0 and al == 0x03:
                pass
            elif ah == 0x0E :
                if al == ord('\n') :
                    cpu.msg(
                    self.displaytext
                    )
                    self.dumpMemory(self.eip, self.eip)
                else:
                    cpu.msg(
                    chr(al)
                    )
                    self.displaytext += chr(al)
            else:
                s='Not Implemented data'.format(self.rReg(cpu.rax_))
                cpu.msg(s)
                raise Exception
        else:
            s='Not Implemented Imm={0}'.format(Imm8)
            cpu.msg(s)
            raise Exception


    def run(self,eip,size):
        self.eip=eip
        runflag = True
        while runflag == True :
            self.op = self.rMem(self.eip, cpu.RTr8, self.CS)
            s='=== run [{2}:{0}]:op=0x{1:02X}'.format(self.eip, self.op, self.CS)
            #cpu.msg(s)
            cpu.dbgp(s)
            if not self.eip == size:
                self.execute(self.op)
                self.opStr = ''
            else:
                runflag = False
                cpu.msg('End')
                raw=input('hit any')
                sys.exit(0)
            self.eip += 1



    def execute(self,op):
        '''
        show operand
        '''
        s = 'execute [{0}]:op=0x{0:02X} '.format( self.eip , op )
        cpu.msg(s)


    def load(self,filename):
        try:
            with open(filename,'rb') as f:
                i = 0
                b = f.read(1)
                while not b == b'' :
                    self.wMem(i, cpu.b2i(b), cpu.RTr8, self.CS)
                    b = f.read(1)
                    i += 1
            return i
        except:
            s='{0} open error'.format(filename)
            cpu.msg(s)
            raise Exception


    def b2i(val):
        return int.from_bytes(val , byteorder = 'little')

    def setrex(self,op):
        self.rexw = self.rexr = self.rexx = self.rexb = 0

        self.rexb = op & cpu.REXb
        self.rexx = op & cpu.REXx
        self.rexr = op & cpu.REXr
        self.rexw = op & cpu.REXw


    def chDB(self):  #16 or 32
        db = ((self.DB + 1) % cpu.RTr16) + cpu.RTr16
        self.DB = db


    def chDB_R(self): #32 or 64
        db =((self.DB + 1) % cpu.RTr32) + cpu.RTr32
        self.DB = db


if __name__ == '__main__':
    c=cpu(memory(1))
    print('Reprensative Register')
    print(cpu.r2reg)
    input()

    print(cpu.regp[c.mod1116[0][cpu.rax_][cpu.RTr8]][2])
    input()

    c.dumpRegister(-2)
    c.wReg(cpu.rax_,0x1234557890)
    c.wReg(cpu.ah_,0x20)
    c.wReg(cpu.ch_,0xff)
    c.wReg(cpu.xmm7_,0xfffdffdfd)
    c.dumpRegister(cpu.ah_)
    c.dumpRegister(-2)
    s=cpu.signex(0xff01, cpu.RTr16, cpu.RTr32)
    print(hex(s),cpu.sb2sd(s,cpu.RTr32))


    c.wReg(cpu.eax_,0x0E00+ord('a'))
    c.wMem(1,0x10, cpu.RTr8, c.CS)
    c.dumpMemory(0,10)
    c.eip=0
    c.intImm8()

    size=c.load('HelloWorld')
    #c.run(0,size)

    c.dumpMemory(0,10)
    c.dumpMemory(940,944)
    c.dumpRegister(-2)
    m = c.ModRM(0b10101110, cpu.RTr8, cpu.RTr8)
    print(c.Mod,c.Mro,c.Mrm, c.rReg(c.ro),c.rm)

    def testModRM():
        print()
        print('test ModRM')
        c.eip=0
        modp=[
            0b00000000,
            0b01000000,
            0b10000000,
            0b11000000
        ]
        pt=[
            ['bx+si',
            'bx+di',
            'bp+si',
            'bp+di',
            'si',
            'di',
            'disp16',
            'bx'],
            ['bx+si+disp8',
            'bx+di+disp8',
            'bp+si+disp8',
            'bp+di+disp8',
            'si+disp8',
            'di+disp8',
            'bp+disp16',
            'bx+disp8'],
            ['bx+si+disp16',
            'bx+di+disp16',
            'bp+si+disp16',
            'bp+di+disp16',
            'si+disp16',
            'di+disp16',
            'bp+disp16',
            'bx+disp16'],
            ['al ax',
            'cl cx',
            'dl dx',
            'bl bx',
            'ah sp',
            'ch bp',
            'dh si',
            'bh di']
            ]

        for i in range(0,35):
            c.wReg(i,i)

        #for i in range(0,c.mem.memmax):
            #c.wMem(i,i,cpu.RTr8,0)

        j=0
        for p in modp[0:3]:
            for i in range(0,8):
                mod = p |(i<<3)|i
                c.ModRM(mod,cpu.RTr8,cpu.RTr8)

                s='{0:08b}:'.format(mod)+pt[j][i]+':'+str(c.rm)
                print(s)
                c.dumpRegister(-2)
                c.dumpMemory(c.eip,c.eip+5)
                c.dumpMemory(c.rm,c.rm+5)

            j += 1




    testModRM()

    def rexp():
        print('rex.b:{0}'.format(c.rexb))
        print('rex.x:{0}'.format(c.rexx))
        print('rex.r:{0}'.format(c.rexr))
        print('rex.w:{0}'.format(c.rexw))

    def testrex():
        for i in range(0x40,0x50):
            c.setrex(i)
            print('rex:{0:08b}'.format(i))

    def testchdb():
        print('DB={0} 2=>16 3=>32'.format(c.DB))
        c.chDB()
        print('changed DB:{0}'.format(c.DB))
        c.chDB()
        print('changed DB:{0}'.format(c.DB))
        c.chDB()
        print('changed DB:{0}'.format(c.DB))

    testrex()
    c.setrex(0)
    rexp()

    testchdb()

    def testflagchk():
        flg = cpu.CF|cpu.AF
        c.flagchk(flg,127,127,254,cpu.RTr8)
        c.dumpRegister(-2)
        flg = cpu.CF|cpu.AF|cpu.ZF|cpu.PF
        c.flagchk(flg,127,202,329,cpu.RTr8)
        c.dumpRegister(-2)
        cpu.msg(cpu.sb2sd(256,cpu.RTr8))

    testflagchk()
