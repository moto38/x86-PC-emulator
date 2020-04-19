# coding: utf-8
import os
import sys
from x86base import cpu,memory

class x86cpu(cpu):

    def Mrxrmy(self,dRT,sRT):
        modb=self.readNextMem(self.CS)
        self.ModRM(modb,sRT,dRT) # ro=dRT rm=sRT

        self.drm = 0b11 #dest is register
        self.dRT = dRT
        self.sRT = sRT

        self.srcO = self.rm #RMy
        self.srcV = self.rf[self.Mod](self.rm, self.dRT, self.seg) #RMy(value)

        self.dstO = self.ro #Rx
        self.dstV = self.rReg(self.ro) #Rx(value)

        self.opStr += ' R[{0}], RM(0x{1:02X})'.format(cpu.regp[self.dstO][2] , self.srcO)


    def Mrmyrx(self,dRT,sRT):
        modb=self.readNextMem(self.CS)
        self.ModRM(modb,sRT,dRT) # ro=sRT rm=dRT

        self.dRT = dRT
        self.sRT = sRT

        self.srcO = self.ro #Rx
        self.srcV = self.rReg(self.ro) #Rx(value)

        self.dstO = self.rm #RMy
        self.dstV = self.rf[self.Mod](self.rm, self.dRT, self.seg) #RMy(value)

        self.opStr += ' {0}, R[{1}]'.format(self.modstr[self.Mod](self.dstO) , cpu.regp[self.srcO][2])



    def Mrmyiz(self,dRT,sRT):
        modb=self.readNextMem(self.CS)
        self.ModRM(modb,sRT,dRT) # ro=nouse rm=dRT

        self.dRT = dRT
        self.sRT = sRT

        self.srcV = self.disp(self.sRT) #Iz(value)
        self.srcO = self.eip #Iz

        self.dstO = self.rm #RMy
        self.dstV = self.rf[self.drm](self.rm , self.dRT,self.seg) #RMy(value)

        self.opStr += ' {0}, Imm({1})'.format(self.modstr[self.drm](self.dstO) , self.srcV)


    def MrmySrx(self, dRT, sRT):
        #for sal rm , cl    etc..
        modb=self.readNextMem(self.CS)
        self.ModRM(modb,sRT,dRT) # rm=dRT , ro=nouse

        self.dRT = dRT
        self.sRT = sRT
        self.srcO = self.sRT # src is register
        self.srcV = self.rReg(self.sRT)

        self.dstO = self.rm # RMy
        self.dstV = self.rf[self.drm](self.dstO, self.dRT,self.seg)

        self.opStr += ' {0}({1}), R[{2}]({3})'.format(self.modstr[self.drm](self.dstO) , self.dstV, cpu.regp[self.srcO][2], self.srcV)



    def Mrmy(self, dRT, sRT):
        #for sal rm    etc..
        modb=self.readNextMem(self.CS)
        self.ModRM(modb,sRT,dRT) # rm=dRT , ro=nouse

        self.dRT = dRT
        self.sRT = -1
        self.srcO = self.sRT # src is register
        self.srcV = -1

        self.dstO = self.rm # RMy
        self.dstV = self.rf[self.drm](self.dstO, self.dRT,self.seg)

        self.opStr += ' {0}({1})'.format(self.modstr[self.drm](self.dstO) , self.dstV)




    def Mrxiz(self,dRT,sRT):
        modb=self.readNextMem(self.CS)
        self.ModRM(modb,sRT,dRT) # ro=sRT rm=nouse

        self.drm = 0b11 #dest is register

        self.dRT = dRT
        self.sRT = sRT

        self.srcV = self.disp(self.sRT) #Iz(value)
        self.srcO = self.eip #Iz

        self.dstO = self.ro #Rx
        self.dstV = self.rReg(self.ro) #Rx(value)

        self.opStr += ' {0}, Imm({1})'.format(self.modstr[self.drm](self.dstO), self.srcV)


    def Srxiz(self,dRT,sRT):
        '''
        specified register & Imm
        '''

        self.drm = 0b11
        self.Mod = 0b11
        self.ro = dRT #dest is specified register

        self.dRT = cpu.regp[dRT][1]
        self.sRT = sRT

        self.srcV = self.disp(self.sRT) #Iz(value)
        self.srcO = self.eip #Iz

        self.dstO = self.ro #Rx
        self.dstV = self.rReg(self.ro) #Rx(value)

        self.opStr += ' {0}, Imm({1})'.format(cpu.regp[self.ro][2], self.srcV)


    def Siz(self,dRT,sRT): # sRT no use
        '''
        trickey use
        dst = Imm
        '''
        self.Mod = -1 # Mod is no use
        self.drm = -1 # drm is no use

        self.dRT = dRT
        self.sRT = sRT

        self.dstV = self.disp(dRT) #Iz(value)
        self.dstO = self.eip #Iz

        self.srcO = -1 #Rx no set
        self.srcV = -1 #Rx(value) no set

        self.opStr += ' Imm({0})'.format(self.dstV)


    def Srx(self,dRT,sRT): # sRT no use
        '''
        trickey use
        dst = specified register number
        '''
        self.drm = 0b11 #drm is target register number
        self.Mod = 0b11 #Mod no use

        self.dRT = cpu.regp[dRT][1]
        self.sRT = sRT

        self.dstO = self.ro = dRT #Rx

        self.dstV = self.rReg(self.dstO) #Rx(value)

        self.srcO = -1 #RMy no use
        self.srcV = -1 #RMy(value) bo use
        cpu.dbgp('dstO={0}'.format(self.dstO))
        self.opStr += ' R[{0}]({1})'.format(cpu.regp[self.dstO][2] , self.dstV)


    def SSrx(self,dRT,sRT): # register and register type 
        '''
        trickey use
        dst = specified register number
        src = register resource type
        '''
        self.drm = 0b11 #drm target register number
        self.Mod = 0b11 #Mod no use

        #print(self.rexb,dRT,sRT)
        self.dstO = cpu.mod1164[self.rexb][dRT][sRT]
        self.dRT = sRT
        self.sRT = -1

        self.ro = self.dstO

        self.dstV = self.rReg(self.dstO) #Rx(value)

        self.srcO = -1 #RMy no use
        self.srcV = -1 #RMy(value) bo use
        cpu.dbgp('dstO={0}'.format(self.dstO))
        self.opStr += ' R[{0}]({1})'.format(cpu.regp[self.dstO][2] ,
        self.dstV)
    
    def Srxrx(self,dRT,sRT):
        '''
        trickey use
        dst = specified register number
        src = specified register number
        '''
        self.drm = 0b11 #drm is target register number
        self.Mod = 0b11 #Mod no use

        self.dRT = cpu.regp[dRT][1]
        self.sRT = cpu.regp[sRT][1]

        self.dstO = self.ro = dRT #Rx1

        self.dstV = self.rReg(self.dstO) #Rx1(value)

        self.srcO = self.rm = sRT #Rx2
        self.srcV = self.rReg(self.srcO) #Rx2(value)
        cpu.dbgp('dstO={0} srcO={1}'.format(self.dstO, self.srcO))
        self.opStr += ' R[{0}]({1}) R[{2}]({3})'.format(cpu.regp[self.dstO][2], self.dstV, cpu.regp[self.srcO][2], self.srcV)


    def noArgs(self, dRT, sRT):
        self.opStr = ''
        pass


    def Sarg(self , dstO, dstV):
        self.dstO = dstO
        self.dstV = dstV
        self.opStr += ' (0x{0:X}({0}))'.format(self.dstV)


    def op_mov(self , oprand , dRT , sRT):
        self.seg = self.segOVR(self.DS)
        oprand(dRT , sRT)

        v = self.srcV # move operation
        self.wf[self.drm](self.dstO , v , self.dRT,self.seg)
        # flag : no change

        self.opStr = 'mov' + self.opStr
        cpu.msg(self.opStr)



    def op_add(self , oprand , dRT , sRT):
        self.seg = self.segOVR(self.DS)
        oprand(dRT , sRT)
        #v = self.dstV + self.srcV # add operation

        v = self.addsub(self.dstV, self.srcV, dRT)

        self.wf[self.drm](self.dstO , v , self.dRT,self.seg)

        self.flagchk(cpu.OF|cpu.SF|cpu.ZF|cpu.AF|cpu.PF|cpu.CF, self.dstV, self.srcV , v , self.dRT)

        self.opStr = 'add' + self.opStr
        cpu.msg(self.opStr)


    def op_adc(self , oprand , dRT , sRT):
        self.seg = self.segOVR(self.DS)
        oprand(dRT , sRT)

        cflg = 1 if self.getflag(cpu.CF) else 0
        #v = self.dstV + self.srcV + cflg # add operation + 1
        v = self.addsub(self.dstV , (self.srcV + 1 ),self.sRT)

        self.wf[self.drm](self.dstO , v , self.dRT,self.seg)

        self.flagchk(cpu.OF|cpu.SF|cpu.ZF|cpu.AF|cpu.PF|cpu.CF , self.dstV, self.srcV + cflg , v , self.dRT)

        self.opStr = 'adc' + self.opStr + ' + CF:{0}'.format(cflg)
        cpu.msg(self.opStr)


    def op_sbb(self , oprand , dRT , sRT):
        self.seg = self.segOVR(self.DS)
        oprand(dRT , sRT)

        cflg = 1 if self.getflag(cpu.CF) else 0
        #v = self.dstV - self.srcV - cflg # sub operation with borrow
        v = self.addsub(self.dstV, self.tocomp(self.srcV + 1, self.sRT), self.dRT)

        self.wf[self.drm](self.dstO , v , self.dRT,self.seg)
        self.flagchk(cpu.OF|cpu.SF|cpu.ZF|cpu.AF|cpu.PF|cpu.CF , self.dstV, self.srcV - cflg , v , self.dRT)

        self.opStr = 'sbb' + self.opStr +' - CF:{0}'.format(cflg)
        cpu.msg(self.opStr)


    def op_sub(self , oprand , dRT , sRT):
        self.seg = self.segOVR(self.DS)
        oprand(dRT , sRT)

        #v = self.dstV - self.srcV # sub operation
        v = self.addsub(self.dstV, self.tocomp(self.srcV, self.sRT), self.dRT)

        cpu.dbgp('dstV:{0} - srcV:{1} = v:{2}'.format(self.dstV , self.srcV, v))

        self.wf[self.drm](self.dstO , v , self.dRT,self.seg)
        self.flagchk(cpu.OF|cpu.SF|cpu.ZF|cpu.AF|cpu.PF|cpu.CF , self.dstV, self.srcV , v , self.dRT)

        self.opStr = 'sub' + self.opStr
        cpu.msg(self.opStr)


    def op_cmp(self , oprand , dRT , sRT):
        self.seg = self.segOVR(self.DS)
        oprand(dRT , sRT)
        #v = self.dstV - self.srcV
        v = self.addsub(self.dstV, self.tocomp(self.srcV, self.sRT), self.dRT)

        cpu.dbgp('cmp: v({0}) = {1} - {2}'.format(v , self.dstV , self.srcV))

        self.flagchk(cpu.OF|cpu.SF|cpu.ZF|cpu.AF|cpu.PF|cpu.CF , self.dstV, self.srcV , v , self.dRT)

        self.opStr = 'cmp' + self.opStr
        cpu.msg(self.opStr)


    def op_or(self , oprand , dRT , sRT):
        self.seg = self.segOVR(self.DS)
        oprand(dRT , sRT)
        v = self.dstV  | self.srcV # or operation
        self.wf[self.drm](self.dstO , v , self.dRT,self.seg)

        self.flagchk(cpu.OF|cpu.SF|cpu.ZF|cpu.AF|cpu.PF|cpu.CF , self.dstV, self.srcV , v , self.dRT
        )
        self.opStr = 'or' + self.opStr
        cpu.msg(self.opStr)


    def op_xor(self , oprand , dRT , sRT):
        self.seg = self.segOVR(self.DS)
        oprand(dRT , sRT)
        v = self.dstV  ^ self.srcV # xor operation
        self.wf[self.drm](self.dstO , v ,self.dRT, self.seg)
        self.flagchk(cpu.OF|cpu.SF|cpu.ZF|cpu.AF|cpu.PF|cpu.CF , self.dstV, self.srcV , v , self.dRT)

        self.opStr = 'xor' + self.opStr
        cpu.msg(self.opStr)


    def op_push(self , oprand , dRT , sRT):
        self.seg = self.segOVR(self.DS)
        oprand(dRT , sRT)
        v = self.dstV
        sp = self.rReg(cpu.rsp_)
        ss = cpu.stacksize[self.DB]
        dstsp = sp - ss
        self.wMem(dstsp, v, self.DB, self.SS)
        self.wReg(cpu.rsp_ , dstsp)
        self.opStr = 'push' + self.opStr
        cpu.msg(self.opStr)


    def op_pop(self , oprand , dRT , sRT):
        self.seg = self.segOVR(self.DS)
        oprand(dRT , sRT)

        sp = self.rReg(cpu.rsp_)
        ss = cpu.stacksize[self.DB]
        v = self.rMem(sp , self.DB , self.SS)
        #self.wReg(self.dstO , v)
        self.wf[self.drm](self.dstO , v , self.dRT , self.seg)
        dstsp = sp + ss
        self.wReg(cpu.rsp_ , dstsp)
        self.opStr = 'pop' + self.opStr
        cpu.msg(self.opStr)


    def op_lea(self , oprand , dRT , sRT):
        self.seg = self.segOVR(self.DS)
        oprand(dRT , sRT)

        v = self.srcO # src address
        self.wf[self.drm](self.dstO , v , self.dRT,self.seg)
        # flag : no change

        self.opStr = 'lea' + self.opStr
        cpu.msg(self.opStr)



    def op_callRel8(self , oprand , dRT , sRT):
        self.seg = self.segOVR(self.CS)
        nexteip = self.eip + 2
        self.op_push(self.Sarg, nexteip, self.DB)

        self.opStr='callRel8'
        self.op_jmpRel8( oprand , dRT , sRT)
        cpu.msg(self.opStr)


    def op_ret(self , oprand , dRT , sRT):
        self.seg = self.segOVR(self.CS)
        sp = self.rReg(cpu.rsp_)
        ss = cpu.stacksize[self.DB]
        v = self.rMem(sp , self.DB,self.SS)

        dstsp = sp + ss
        self.wReg(cpu.rsp_ , dstsp)
        self.eip = v
        self.opStr = 'ret to [0x{0:X}({0})]'.format(self.eip)
        cpu.msg(self.opStr)




    def op_sal(self, oprand, dRT, sRT):
        self.seg = self.segOVR(self.DS)
        oprand(dRT , sRT)
        v = self.dstV
        s = self.srcV
        self._scf = 0

        for i in range(0,s):
            v = self.shift1L(v, self.dRT, AL=0)

        self.wf[self.drm](self.dstO, v, self.dRT, self.seg)

        self.flagchk(cpu.SF|cpu.ZF|cpu.AF|cpu.PF|cpu.CF , self.dstV, self.srcV , v , self.dRT)

        if cpu.chkMSB(v , self.dRT) :
            # msb = 1
            if self._scf != 0 :
                self.flagOff(cpu.OF)
            else:
                self.flagOn(cpu.OF)
        else:
            # msb = 0
            if self._scf != 0 :
                self.flagOn(cpu.OF)
            else:
                self.flagOff(cpu.OF)

        self.opStr = 'sal' + self.opStr
        cpu.msg(self.opStr)




    def op_sar(self, oprand, dRT, sRT):
        self.seg = self.segOVR(self.DS)
        oprand(dRT , sRT)
        v = self.dstV
        s = self.srcV
        self._scf = 0

        for i in range(0,s):
            v = self.shift1R(v, self.dRT, AL=1)

        self.wf[self.drm](self.dstO, v, self.dRT,self.seg)

        self.flagchk(cpu.SF|cpu.ZF|cpu.AF|cpu.PF|cpu.CF , self.dstV, self.srcV , v , self.dRT)

        self.flagOff(cpu.OF)

        self.opStr = 'sar' + self.opStr
        cpu.msg(self.opStr)




    def op_shr(self, oprand, dRT, sRT):
        self.seg = self.segOVR(self.DS)
        oprand(dRT , sRT)
        v = old = self.dstV
        s = self.srcV
        self._scf = 0

        for i in range(0,s):
            v = self.shift1R(v, self.dRT, AL=0)

        self.wf[self.drm](self.dstO, v, self.dRT,self.seg)

        self.flagchk(cpu.SF|cpu.ZF|cpu.AF|cpu.PF|cpu.CF , self.dstV, self.srcV , v , self.dRT)

        if old & cpu.maskMSB[self.dRT] != 0 :
            self.flagOn(cpu.OF)
        else:
            self.flagOff(cpu.OF)

        self.opStr = 'shr' + self.opStr
        cpu.msg(self.opStr)



    def op_shrd(self, oprand, dRT, sRT):
        self.seg = self.segOVR(self.DS)
        # dRT = dst & src
        # sRT = no use  fot imm8/cl_
        self.Mrmyrx(dRT , dRT)
        rm = self.rm
        dstO = self.dstO
        dstV = self.dstV
        ro = self.ro
        srcO = self.srcO
        srcV = self.srcV
        drm = self.drm

        oprand(sRT, sRT) # Siz or Srx

        v = vold = dstV
        x = xold = srcV
        s = sold = self.dstV
        self._scf = 0

        for i in range(0,s):
            x = self.shift1R(x, self.dRT, AL=0)  #shiftin
            if self._scf != 0:
                m = cpu.maskMSB[self.dRT]
            else:
                m = 0
            #cpu.dbgp(x)

            cpu.dbgp('shiftin:{0:b}\noperand:{1:b}'.format(m,v))
            if m != v & cpu.maskMSB[self.dRT]:
                self.flagOn(cpu.OF)
            else:
                self.flagOn(cpu.OF)

            v = self.shift1R(v, self.dRT, AL=0)  #shift
            v = v | m
            #cpu.dbgp(v)

        if s != 0:
            self.wf[drm](dstO, v, self.dRT,self.seg)

            self.flagchk(cpu.SF|cpu.ZF|cpu.AF|cpu.PF|cpu.CF , dstV, srcV , v , dRT)

        self.opStr = 'shrd' + self.opStr
        cpu.msg(self.opStr)



    def op_shld(self, oprand, dRT, sRT):
        self.seg = self.segOVR(self.DS)
        # dRT = dst & src
        # sRT = no use  fot imm8/cl_
        self.Mrmyrx(dRT , dRT)
        rm = self.rm
        dstO = self.dstO
        dstV = self.dstV
        ro = self.ro
        srcO = self.srcO
        srcV = self.srcV
        drm = self.drm

        oprand(sRT, sRT) # Siz or Srx

        v = vold = dstV
        x = xold = srcV
        s = sold = self.dstV
        self._scf = 0

        for i in range(0,s):
            x = self.shift1L(x, dRT, AL=0)  #shiftin
            if self._scf != 0:
                m = 1
            else:
                m = 0
            #cpu.dbgp(x)

            cpu.dbgp('shiftin:{0:b}({2:b})\noperand:{1:b}'.format(m,v,x))
            if m != v & cpu.maskMSB[dRT]:
                self.flagOn(cpu.OF)
            else:
                self.flagOn(cpu.OF)

            v = self.shift1L(v, dRT, AL=0)  #shift
            v = v | m
            #cpu.dbgp(v)

        if s != 0:
            self.wf[drm](dstO, v, dRT ,self.seg)

            self.flagchk(cpu.SF|cpu.ZF|cpu.AF|cpu.PF|cpu.CF , dstV, srcV , v , dRT)

        self.opStr = 'shld' + self.opStr
        cpu.msg(self.opStr)


    def op_rol(self, oprand, dRT, sRT):
        self.seg = self.segOVR(self.DS)
        # dRT = dst
        # sRT = src
        oprand(dRT, sRT)

        v = vold = self.dstV
        s = self.srcV
        self._scf = 0

        for i in range(0,s):
            v = self.shift1L(v, self.dRT, AL=0)
            if self._scf != 0:
                m = 1
            else:
                m = 0

            v = v | m
            #cpu.dbgp(v)

        if s != 0:
            self.wf[self.drm](self.dstO, v, self.dRT, self.seg)

            if self._scf != 0:
                self.flagOn(cpu.CF)
            else:
                self.flagOff(cpu.CF)

            m2 = 1 if v & cpu.maskMSB[self.dRT] !=0 else 0

            m = m ^ m2
            if m != 0:
                self.flagOn(cpu.OF)
            else:
                self.flagOff(cpu.OF)

        self.opStr = 'rol' + self.opStr
        cpu.msg(self.opStr)



    def op_ror(self, oprand, dRT, sRT):
        self.seg = self.segOVR(self.DS)
        # dRT = dst
        # sRT = src
        oprand(dRT, sRT)

        v = vold = self.dstV
        s = self.srcV
        self._scf = 0

        for i in range(0,s):

            v = self.shift1R(v, self.dRT, AL=0)
            if self._scf != 0:
                m = cpu.maskMSB[self.dRT]
            else:
                m = 0

            v = v | m
            #cpu.dbgp(v)

        if s != 0:
            self.wf[self.drm](self.dstO, v, self.dRT, self.seg)

            if self._scf != 0:
                self.flagOn(cpu.CF)
            else:
                self.flagOff(cpu.CF)

            m2 = v & (cpu.maskMSB[self.dRT] >> 1)

            m = m ^ ( m2 << 1)
            if m != 0:
                self.flagOn(cpu.OF)
            else:
                self.flagOff(cpu.OF)

        self.opStr = 'ror' + self.opStr
        cpu.msg(self.opStr)



    def op_rcl(self, oprand, dRT, sRT):
        self.seg = self.segOVR(self.DS)
        # dRT = dst
        # sRT = src
        oprand(dRT, sRT)

        v = vold = self.dstV
        s = self.srcV
        c = 1 if self.getflag(cpu.CF) else 0
        self._scf = 0

        for i in range(0,s):
            v = self.shift1L(v, self.dRT, AL=0)
            v = v | c
            if self._scf != 0:
                c = 1
            else:
                c = 0
            #cpu.dbgp(v)

        if s != 0:
            self.wf[self.drm](self.dstO, v, self.dRT, self.seg)

            if self._scf != 0:
                self.flagOn(cpu.CF)
            else:
                self.flagOff(cpu.CF)

            m2 = v & cpu.maskMSB[self.dRT]

            c = c ^ m2
            if c != 0:
                self.flagOn(cpu.OF)
            else:
                self.flagOff(cpu.OF)

        self.opStr = 'rcl' + self.opStr
        cpu.msg(self.opStr)


    def op_rcr(self, oprand, dRT, sRT):
        self.seg = self.segOVR(self.DS)
        # dRT = dst
        # sRT = src
        oprand(dRT, sRT)

        v = vold = self.dstV
        s = self.srcV
        c = cpu.maskMSB[self.dRT] if self.getflag(cpu.CF) else 0
        self._scf = 0

        for i in range(0,s):
            v = self.shift1R(v, self.dRT, AL=0)
            v = v | c
            if self._scf != 0:
                c = cpu.maskMSB[self.dRT]
            else:
                c = 0
            #cpu.dbgp(v)

        if s != 0:
            self.wf[self.drm](self.dstO, v, self.dRT, self.seg)

            if self._scf != 0:
                self.flagOn(cpu.CF)
            else:
                self.flagOff(cpu.CF)

            m2 = v & (cpu.maskMSB[self.dRT] >> 1)

            c = c ^ ( m2 << 1 )
            if c != 0:
                self.flagOn(cpu.OF)
            else:
                self.flagOff(cpu.OF)

        self.opStr = 'rcl' + self.opStr
        cpu.msg(self.opStr)




    def shift1L(self, v, rt, AL):
        '''
        AL is 1: Arithmetic
        AL is 0: Logical

        @x86
        arithmetic left shift = logical left shift...
        then Always AL=0
        '''
        old = v
        m = old & cpu.maskMSB[rt] #sign
        n = old & (cpu.maskMSB[rt]>>1) # new sign
        v <<= 1
        v &= cpu.mask[rt]

        if AL == 1:
            # Arithmetic  not use @x86
            v |= m
            if n != 0:
                self._scf = 1
            else:
                self._scf = 0
        else:
            # Logical
            if m != 0:
                self._scf = 1
            else:
                self._scf = 0
            pass

        cpu.dbgp('v:{0:b} << 1 -> {1:b} CF:{2}'.format(old, v, self._scf))
        return v


    def shift1R(self, v, rt, AL):
        '''
        AL is 1: Arithmetic
        AL is 0: Logical
        '''
        old = v
        m  = old & cpu.maskMSB[rt] #sign
        l = old & 0x1 #LSB
        v = old >> 1

        if l != 0:
            self._scf = 1
        else:
            self._scf = 0

        if AL == 1:
            # Arithmetic
            v |= m
        else:
            # Logical
            pass

        cpu.dbgp('v:{0:b} >> 1 -> {1:b} CF:{2}'.format(old, v, self._scf))
        return v


    def op_div(self, oprand , dRT, sRT):
        self.seg = self.segOVR(self.DS)
        # oprand = Mrxrmy : use rmy only
        # dRT = Divisor's RT
        # sRT = nouse
        oprand(dRT, sRT)

        dv = self.dstV # Divisor

        if dRT == cpu.RTr16:
            dx = cpu.dx_
            ax = cpu.ax_
        elif dRT == cpu.RTr32:
            dx = cpu.edx_
            ax = cpu.eax_
        elif dRT == cpu.RTr64:
            dx = cpu.rdx_
            ax = cpu.rax_
        else:
            # RTr8
            dx = cpu.ah_
            ax = cpu.al_

        dxv = self.rReg(dx)
        axv = self.rReg(ax)

        dst = (dxv << cpu.bits[dRT]) | axv

        if dv == 0:
            cpu.msg('Division by zero')
        else:
            #t,q = self.divsub(dst, dv, dRT)
            t,q = self.divsub2(dxv,axv,dv,dRT)
            if t > cpu.mask[dRT]:
                cpu.msg('Division Error')
            else:
                #q = dst % dv
                self.wReg(ax , t)
                self.wReg(dx , q)

                s = '[{0}:{1}]({2}) / [{3}]({4}) = {5}...{6}'.format(cpu.regp[dx][2], cpu.regp[ax][2], dst, cpu.regp[self.dstO][2], dv, t, q)
                cpu.dbgp(s)

        self.opStr = 'div' + self.opStr
        cpu.msg(self.opStr)



    def op_idiv(self, oprand , dRT, sRT):
        self.seg = self.segOVR(self.DS)
        # oprand = Mrxrmy : use rmy only
        # dRT = Divisor's RT
        # sRT = nouse
        oprand(dRT, sRT)

        dv = self.dstV # Divisor

        if dRT == cpu.RTr16:
            dx = cpu.dx_
            ax = cpu.ax_
        elif dRT == cpu.RTr32:
            dx = cpu.edx_
            ax = cpu.eax_
        elif dRT == cpu.RTr64:
            dx = cpu.rdx_
            ax = cpu.rax_
        else:
            # RTr8
            dx = cpu.ah_
            ax = cpu.al_

        dxv = self.rReg(dx)
        axv = self.rReg(ax)

        dst = (dxv << cpu.bits[dRT])| axv

        if dv == 0:
            cpu.msg('Division by zero')
        else:
            #t,q = self.idivsub(dst, dv, dRT)
            t,q = self.idivsub2(dxv, axv, dv, dRT)
            if t > cpu.mask[dRT]:
                cpu.msg('Division Error')
            else:
                #q = dst % dv
                self.wReg(ax , t)
                self.wReg(dx , q)

                s = '[{0}:{1}]({2}) / [{3}]({4}) = {5}...{6}'.format(cpu.regp[dx][2], cpu.regp[ax][2], dst, cpu.regp[self.dstO][2], dv, t, q)
                cpu.dbgp(s)

        self.opStr = 'idiv' + self.opStr
        cpu.msg(self.opStr)


    '''
    def divsub(self, d1, d2, d2RT):
        bitw = cpu.bits[d2RT]
        d2x = d2 << bitw
        d2 = 0
        cpu.dbgp('d1:{0},d2:{1},d2x:{2},bitw:{3}'.format(d1,d2,d2x,bitw))
        while bitw >= 0:
            d2 <<= 1
            dd = d1 - d2x
            if dd >= 0:
                d2 = d2 | 1
                cpu.dbgp('loop: d1:{0},d2:{1},d2x:{2},bitw:{3}'.format(d1,d2,d2x,bitw))
                d1 = dd
            else:
                cpu.dbgp('loop: d1:{0},d2:{1},d2x:{2},bitw:{3}'.format(d1,d2,d2x,bitw))
            bitw -= 1
            d2x >>= 1

        cpu.dbgp('d1:{0},d2:{1},d2x:{2},bitw:{3}'.format(d1,d2,d2x,bitw))

        return d2,d1  # syou / amari
    '''

    def divsub2(self, rd, ra, divs , d2RT):
        # rd = edx
        # ra = eax
        # dst is rd:ra
        # divs = divisor
        bitw = cpu.bits[d2RT]
        d2u = divs
        d2l = 0
        #d2x = d2 << bitw
        d2 = 0 #syou
        d1 = 0 #amari
        cpu.dbgp('rd:ra={0}:{1} divs={2}'.format(rd, ra, divs))
        while bitw >= 0:
            d2 <<= 1
            u = rd - d2u
            l = ra - d2l
            if l < 0:
                # borrow
                u -= 1
                l += cpu.mask[d2RT] + 1
                if u >= 0:        # ul >=0
                    d2 = d2 | 1
                    d1 = ( u << cpu.bits[d2RT]) + l
                    rd = u
                    ra = l
            else: # l>= 0
                if u >= 0:     # u>=0,l>=0
                    d2 = d2 | 1
                    d1 = ( u << cpu.bits[d2RT]) + l
                    rd = u
                    ra = l

            cpu.dbgp('loop: rd:ra={0}:{1}({2}),d2u:d2l={6}:{7}({8}),d1:{5},d2:{3},bitw:{4}'.format(rd, ra, (rd<<cpu.bits[d2RT])+ra, d2, bitw,d1,d2u,d2l,(d2u<<cpu.bits[d2RT])+d2l))

            bitw -= 1
            d2u = self.shift1R(d2u,d2RT,AL=0)
            c = self._scf
            d2l = self.shift1R(d2l,d2RT,AL=0)
            if c > 0:
                d2l = d2l | cpu.maskMSB[d2RT]

        cpu.dbgp('d1:{0},d2:{1},d2u:{2},d2l:{3},bitw:{4}'.format((rd<<cpu.bits[d2RT])+ra,d2,d2u,d2l,bitw))

        return d2,d1 # syou / amari


    '''
    def idivsub(self, od1, od2, d2RT):
        bitw = cpu.bits[d2RT]

        msd1 = cpu.chkMSB(od1,d2RT)
        msd2 = cpu.chkMSB(od2,d2RT)

        if msd1:
            d1 = self.tocomp(od1,d2RT)
        else:
            d1 = od1
        if msd2:
            d2 = cpu.tocomp(od2,d2RT)
        else:
            d2 = od2

        d2x = d2 << bitw

        cpu.dbgp('d1:{0},d2:{1},d2x:{2},bitw:{3}'.format(od1,od2,d2x,bitw))
        d2 = 0
        while bitw >= 0:
            d2 <<= 1
            dd = d1 - d2x
            if dd >= 0:
                d2 = d2 | 1
                cpu.dbgp('loop: d1:{0},d2:{1},d2x:{2},bitw:{3}'.format(d1,d2,d2x,bitw))
                d1 = dd
            else:
                cpu.dbgp('loop: d1:{0},d2:{1},d2x:{2},bitw:{3}'.format(d1,d2,d2x,bitw))
            bitw -= 1
            d2x >>= 1

        if msd1 != msd2:
            d2 = self.tocomp(d2,d2RT)

        cpu.dbgp('d1:{0}={4},d2:{1}={5},d2x:{2},bitw:{3}'.format(d1, d2, d2x, bitw, cpu.sb2sd(d1,d2RT), cpu.sb2sd(d2,d2RT)))
        return d2,d1  # syou / amari
    '''


    def idivsub2(self, rd , ra , divs ,d2RT):
        bitw = cpu.bits[d2RT]

        msd1 = cpu.chkMSB(rd,d2RT)
        msd2 = cpu.chkMSB(divs,d2RT)

        if msd1:
            rd1 = self.tocomp(rd,d2RT)
            ra1 = self.tocomp(ra,d2RT)
        else:
            rd1 = rd
            ra1 = ra
        if msd2:
            divs = cpu.tocomp(divs,d2RT)
        else:
            divs = divs

        d2,d1 = self.divsub2(rd1,ra1,divs,d2RT)

        if msd1 >= 0:
            d2 = self.tocomp(d2,d2RT)

        cpu.dbgp('d1:{0}={2},d2:{1}={3}'.format(d1, d2, cpu.sb2sd(d1,d2RT), cpu.sb2sd(d2,d2RT)))
        return d2,d1  # syou / amari


    def addsub(self, v1, v2, rt):
        if cpu.mask[rt] - v2 < v1:
            self._scf = 1
        else:
            self._scf = 0

        return (v1 + v2) & cpu.mask[rt]


    def mul2(self, d1, d2, dRT):
        cpu.dbgp('mul2 d1:{0},d2:{1}'.format(d1,d2))
        # d1 : multiplied
        # d2 : multiplier
        # d1&d2 RT
        # u : upper val
        # l : lower val

        if d2 & 1 :
            l = d1
        else:
            l = 0
        u = 0
        i = 0
        cpu.dbgp('mul2 loop: u:l={0}:{1}({2}),d2:{3},i:{4}'.format(u, l, (u<<cpu.bits[dRT])+l, d2, i))

        while d2 != 0 :
            d2 = self.shift1R(d2, dRT, AL=0)
            i += 1
            if (d2 & 1) == 1 :
                ii = i
                dl = d1
                du = 0
                c = 0
                while ii > 0:
                    dl = self.shift1L(dl, dRT, AL=0)
                    if self._scf != 0:
                        c = 1
                    else:
                        c = 0
                    du = self.shift1L(du, dRT, AL=0)
                    du |= c
                    ii -= 1
                u += du
                l += dl
            cpu.dbgp('loop: u:l={0}:{1}({2}),d2:{3},i:{4}'.format(u, l, (u<<cpu.bits[dRT])+l, d2, i))
        return u,l



    def imul(self, od1, od2, dRT):
        msd1 = cpu.chkMSB(od1,dRT)
        msd2 = cpu.chkMSB(od2,dRT)

        #tdst = cpu.sb2sd(od1, dRT) * cpu.sb2sd(od2, dRT)

        if msd1 != 0:
            d1 = self.tocomp(od1,dRT)
        else:
            d1 = od1
        if msd2 != 0:
            d2 = self.tocomp(od2,dRT)
        else:
            d2 = od2

        u,l = self.mul2(d1, d2, dRT)

        if msd1 != msd2:
            u,l= self.tocomp2(u,l,dRT)

        #cpu.dbgp('imul solve: {0}*{1}={2}'.format(cpu.sb2sd(od1, dRT) , cpu.sb2sd(od2, dRT) , tdst ))
        #cpu.dbgp('imul solve: u:l={0}:{1}'.format((tdst & (cpu.mask[dRT]<<cpu.bits[dRT]))>>cpu.bits[dRT], tdst & cpu.mask[dRT]))
        cpu.dbgp('imul: u:l={0}:{1}({2})'.format(u, l, cpu.sb2sd((u<<cpu.bits[dRT])+l, dRT+1)))
        return u,l


    def op_mul(self, oprand , dRT, sRT):
        self.seg = self.segOVR(self.DS)
        # oprand = Mrxrmy : use rmy only
        # dRT = multiplier's rt
        # sRT = nouse
        oprand(dRT, sRT)

        mlv = self.dstV # multiplier

        if dRT == cpu.RTr16:
            dx = cpu.dx_
            ax = cpu.ax_
        elif dRT == cpu.RTr32:
            dx = cpu.edx_
            ax = cpu.eax_
        elif dRT == cpu.RTr64:
            dx = cpu.rdx_
            ax = cpu.rax_
        else:
            # RTr8
            dx = cpu.ah_
            ax = cpu.al_

        dxv = self.rReg(dx)
        axv = self.rReg(ax)

        if mlv == 0:
            dv = 0
            av = 0
        else:
            dv,av = self.mul2(axv, mlv, dRT)
            self.wReg(ax , av)
            self.wReg(dx , dv)

        if dv == 0:
            self.flagOff(cpu.CF)
            self.flagOff(cpu.OF)
        else:
            self.flagOn(cpu.CF)
            self.flagOn(cpu.OF)

        s = 'op_mul: [{0}]:{1},[{2}]:({3})*[{4}]({5}) = {6}:{7}({8})'.format(cpu.regp[dx][2], dxv, cpu.regp[ax][2], axv, cpu.regp[self.dstO][2], mlv, dv, av,(dv<<cpu.bits[dRT])+av)
        cpu.dbgp(s)

        self.opStr = 'mul' + self.opStr
        cpu.msg(self.opStr)




    def op_imul(self, oprand , dRT, sRT):
        self.seg = self.segOVR(self.DS)
        # oprand = Mrxrmy : use rmy only
        # dRT = multiplier's rt
        # sRT = nouse
        oprand(dRT, sRT)

        mlv = self.dstV # multiplier

        if dRT == cpu.RTr16:
            dx = cpu.dx_
            ax = cpu.ax_
        elif dRT == cpu.RTr32:
            dx = cpu.edx_
            ax = cpu.eax_
        elif dRT == cpu.RTr64:
            dx = cpu.rdx_
            ax = cpu.rax_
        else:
            # RTr8
            dx = cpu.ah_
            ax = cpu.al_

        dxv = self.rReg(dx)
        axv = self.rReg(ax)

        if mlv == 0:
            dv = 0
            av = 0
        else:
            dv,av = self.imul(axv, mlv, dRT)
            self.wReg(ax , av)
            self.wReg(dx , dv)

        if dv == 0:
            self.flagOff(cpu.CF)
            self.flagOff(cpu.OF)
        else:
            self.flagOn(cpu.CF)
            self.flagOn(cpu.OF)

        s = 'op_imul: [{0}]:{1},[{2}]:({3})*[{4}]({5}) = {6}:{7}({8})'.format(cpu.regp[dx][2], dxv, cpu.regp[ax][2], axv, cpu.regp[self.dstO][2], mlv, dv, av,(dv<<cpu.bits[dRT])+av)
        cpu.dbgp(s)

        self.opStr = 'imul' + self.opStr
        cpu.msg(self.opStr)

    def op_and(self, oprand, dRT, sRT):
        # dRT = dest rt
        # sRT = src rt
        self.seg = self.segOVR(self.DS)
        oprand(dRT , sRT)
        v = self.dstV  & self.srcV # and operation
        self.wf[self.drm](self.dstO , v , self.dRT,self.seg)

        self.flagchk(cpu.SF|cpu.ZF|cpu.AF|cpu.PF, self.dstV, self.srcV , v , self.dRT)
        self.flagOff(cpu.CF)
        self.flagOff(cpu.OF)

        self.opStr = 'and' + self.opStr
        cpu.msg(self.opStr)
        
        
        
    def op_dbgp(self, op1, op2, op3):
    	print('==== {0}:{1},{2},{3}'.format(self.op,op1,op2,op3))
    	self.op_()
    	raise
    	
    def op_(self,x):
        print("error:", sys.exc_info()[0])
        print('===Error eip:{1:02X}:{2:02X} Opcode:0x{0:X}==='.format(x,self.CS,self.eip))
        # raise Exception
       
    def op_daa(self,x,y,z):
        self.op_(self.op)
    
    def op_das(self,x,y,z):
        self.op_(self.op)
    
    def op_aaa(self,x,y,z):
        self.op_(self.op)
    
    def op_aas(self,x,y,z):
        self.op_(self.op)
    
    def op_inc(self):
        self.op_(self.op)
        
    def op_dec(self):
        self.op_(self.op)
    
    def op_pusha(self,x,y,z):
        self.op_(self.op)
        
    def op_popa(self,x,y,z):
        self.op_(self.op)
        
    def op_bound(self,x,y,z):
        self.op_(self.op)
    
    def op_arpl(self,x,y,z):
        self.op_(self.op)
        
    def op_ins(self,x,y,z):
        self.op_(self.op)
    
    def op_outs(self,x,y,z):
        self.op_(self.op)
    
    
    def op_xchg(self, oprand, dRT, sRT):
        # dRT = dest rt
        # sRT = src rt
        self.seg = self.segOVR(self.DS)
        oprand(dRT , sRT)
        tempd = self.dstV
        temps = self.srcV
        
        self.wReg(self.dstO, temps)
        self.wReg(self.srcO, tempd)
        
        self.opStr = 'xchg' + self.opStr
        cpu.msg(self.opStr)
        
    
    def op_test(self, oprand, dRT, sRT):
        # dRT = dest rt
        # sRT = src rt
        self.seg = self.segOVR(self.DS)
        oprand(dRT , sRT)
        v = self.dstV  & self.srcV # and operation

        self.flagchk(cpu.SF|cpu.ZF|cpu.AF|cpu.PF, self.dstV, self.srcV , v , self.dRT)
        self.flagOff(cpu.CF)
        self.flagOff(cpu.OF)

        self.opStr = 'test' + self.opStr
        cpu.msg(self.opStr)
        
        
    def op_segoverride(self, oprand, dRT, sRT):  # dRT .. overrider(register)
        self.seg = self.rReg(dRT)
        
        self.opStr = '{0}'.format(cpu.regp[dRT][2])
        cpu.msg(self.opStr)
        
        
    def op_jz(self, oprand, dRT, flag): #jzshort
        flg = self.getflag(cpu.ZF)
        
        self.opStr = 'JZ' if flag else 'JNZ'
        
        if flg == flag:
            self.op_jmpRel8(self.Siz , cpu.RTr8 , cpu.RTr8)
            cpu.msg(self.opStr)
        else:
            self.Siz(cpu.RTr8 , cpu.RTr8)
            self.opStr += ' 0x{0:X} ZF:{1}'.format(self.dstV, flg)
            cpu.msg(self.opStr)
            
            
    def op_jo(self, oprand, dRT, flag): #joshort
        flg = self.getflag(cpu.OF)
        
        self.opStr = 'JO' if flag else 'JNO'
        
        if flg == flag:
            self.op_jmpRel8(self.Siz , cpu.RTr8 , cpu.RTr8)
            cpu.msg(self.opStr)
        else:
            self.Siz(cpu.RTr8 , cpu.RTr8)
            self.opStr += ' 0x{0:X} OF:{1}'.format(self.dstV, flg)
            cpu.msg(self.opStr)
    
    def op_jc(self, oprand, dRT, flag): #jcshort
        flg = self.getflag(cpu.CF)
        
        self.opStr = 'JC' if flag else 'JNC'
        
        if flg == flag:
            self.op_jmpRel8(self.Siz , cpu.RTr8 , cpu.RTr8)
            cpu.msg(self.opStr)
        else:
            self.Siz(cpu.RTr8 , cpu.RTr8)
            self.opStr += ' 0x{0:X} CF:{1}'.format(self.dstV, flg)
            cpu.msg(self.opStr)
    
    
    
    def op_jbe(self, oprand, dRT, flag): #jbeshort
        self.OF = self.getflag(cpu.OF) 
        self.CF = self.getflag(cpu.CF)
        
        flg = self.CF & self.OF
        
        self.opStr = 'JBE' if flag else 'JNBE'
        
        if flg == flag:
            self.op_jmpRel8(self.Siz , cpu.RTr8 , cpu.RTr8)
            cpu.msg(self.opStr)
        else:
            self.Siz(cpu.RTr8 , cpu.RTr8)
            self.opStr += ' 0x{0:X} OF:{1},CF:{2}'.format( self.dstV, self.OF, self.CF)
            cpu.msg(self.opStr)
            
            
    def op_js(self, oprand, dRT, flag): #jsshort
        flg = self.getflag(cpu.SF)
        
        self.opStr = 'JS' if flag else 'JNS'
        
        if flg == flag:
            self.op_jmpRel8(self.Siz , cpu.RTr8 , cpu.RTr8)
            cpu.msg(self.opStr)
        else:
            self.Siz(cpu.RTr8 , cpu.RTr8)
            self.opStr += ' 0x{0:X} SF:{1}'.format(self.dstV, flg)
            cpu.msg(self.opStr)
    
    
    def op_jp(self, oprand, dRT, flag): #jpshort
        flg = self.getflag(cpu.PF)
        
        self.opStr = 'JP' if flag else 'JNP'
        
        if flg == flag:
            self.op_jmpRel8(self.Siz , cpu.RTr8 , cpu.RTr8)
            cpu.msg(self.opStr)
        else:
            self.Siz(cpu.RTr8 , cpu.RTr8)
            self.opStr += ' 0x{0:X} PF:{1}'.format(self.dstV, flg)
            cpu.msg(self.opStr)
    
    
    def op_jl(self, oprand, dRT, flag): #jlshort
        self.OF = self.getflag(cpu.OF)
        self.SF = self.getflag(cpu.SF)
        
        flg = True if self.SF != self.OF else False
        
        self.opStr = 'JL' if flag else 'JNL'
        
        if flg == flag:
            self.op_jmpRel8(self.Siz , cpu.RTr8 , cpu.RTr8)
            cpu.msg(self.opStr)
        else:
            self.Siz(cpu.RTr8 , cpu.RTr8)
            self.opStr += ' 0x{0:X} OF:{1} != SF:{2} {3}'.format(self.dstV, self.OF, self.SF, flg)
            cpu.msg(self.opStr)
    
    def op_jle(self, oprand, dRT, flag): #jelshort
        self.OF = self.getflag(cpu.OF)
        self.SF = self.getflag(cpu.SF)
        self.ZF = self.getflag(cpu.ZF)
        
        flg = True if ( self.ZF == True ) or ( self.SF != self.OF ) else False
        
        self.opStr = 'JLE' if flag else 'JNLE'
        
        if flg == flag:
            self.op_jmpRel8(self.Siz , cpu.RTr8 , cpu.RTr8)
            cpu.msg(self.opStr)
        else:
            self.Siz(cpu.RTr8 , cpu.RTr8)
            self.opStr += ' 0x{0:X} ( ZF:{3} == True ) or ( OF:{1} != SF:{2} ) {4}'.format(self.dstV, self.OF, self.SF, self.ZF, flg)
            cpu.msg(self.opStr)
    
    
    def op_8x(self, oprand, dRT, sRT):
        modb=self.readNextMem(self.CS)
        self.ModRM(modb,dRT,sRT)
        # ro : opcode selecter
        # rm : dst register or memory
        if self.Mro == 0 :
        	f = self.op_add
        elif self.Mro == 1 :
        	f = self.op_or
        elif self.Mro == 2 :
        	f = self.op_adc
        elif self.Mro == 3 :
        	f = self.op_sbb
        elif self.Mro == 4 :
        	f = self.op_and
        elif self.Mro == 5 :
        	f = self.op_sub
        elif self.Mro == 6 :
        	f = self.op_xor
        else:
        	f = self.op_cmp
        	
        self.eip -= 1
        
        f(oprand, dRT, sRT)
        

    '''
    def movR8RM8(self):
        self.op_mov(self.Mrxrmy , cpu.RTr8 , cpu.RTr8)

    def addRM16Imm8(self):
        self.op_add(self.Mrmyiz , cpu.RTr16 , cpu.RTr8)

    def orRM8R8(self):
          self.op_or(self.Mrmyrx , cpu.RTr8 , cpu.RTr8)

    def xorRM8R8(self):
        self.op_xor(self.Mrmyrx , cpu.RTr8 , cpu.RTr8)

    def movALImm8(self):
        self.op_mov(self.Srxiz , cpu.al_ , cpu.RTr8)

    def movAHImm8(self):
        self.op_mov(self.Srxiz , cpu.ah_ , cpu.RTr8)

    def movSIImm16(self):
        self.op_mov(self.Srxiz , cpu.si_ , cpu.RTr16)

    def addALImm8(self):
        self.op_add(self.Srxiz , cpu.al_ , cpu.RTr8)


    def cmpALImm8(self):
        self.op_cmp(self.Srxiz , cpu.al_ , cpu.RTr8)

    def jmpRel8(self):  #jmpshort 0xEB
        self.opStr = 'JMP'
        self.op_jmpRel8(self.Siz , cpu.RTr8 , cpu.RTr8)
        cpu.msg(self.opStr)


    def jzRel8(self): #jzshort 0x74
        flg = self.getflag(cpu.ZF)
        self.opStr = 'JZ'
        if flg :
            self.op_jmpRel8(self.Siz , cpu.RTr8 , cpu.RTr8)
            cpu.msg(self.opStr)
        else:
            self.Siz(cpu.RTr8 , cpu.RTr8)
            self.opStr += '0x{0:X} ZF:{1}'.format(self.dstV, self.ZF)
            cpu.msg(self.opStr)
    '''

    def op_jmpRel8(self , oprand , dRT , sRT):
        oprand(dRT , sRT)
        ip = self.eip
        jmp = self.dstV
        v = ((ip + jmp) & 0xFF) & (self.mem.segment - 1)
        self.eip = v
        s1='eip:[{3}:{0}] + 0x{1:X}({1})-> eip[{3}:{2}]'.format(ip, jmp , v, self.seg)
        cpu.dbgp(s1)
        input()


    def repn(self):
        pass

    def rep(self):
        pass


    def clearPrefix(self):
        self.setrex(0)
        self.DB = self.defaultDB
        self.CS = self.rReg(cpu.cs_)
        self.DS = self.rReg(cpu.ds_)
        self.SS = self.rReg(cpu.ss_)
        self.ES = self.rReg(cpu.es_)
        self.segOV = 0
        self.override = False
        self.LOCK= False


    def prefix(self):
        prefixed = 0
        op = self.op
        opmaskh = op & 0xF0

        # prefix group 1
        if op == 0xF0 :
           '''
           for atomic operation
           '''
           self.LOCK = True
           prefixed = 1


        if op == 0xF2:
           '''
           repeat non zero(NE)
           '''
           self.repn()
           prefixed = 1

        if op == 0xF3:
           '''
           repeat zero(equal)
           '''
           self.rep()
           prefixed = 1


        # rex prefix
        if opmaskh == 0x40 and self.cpumode == cpu.modeIA32e :
          '''
          rex prefix
          '''
          self.setrex(op)
          prefixed = 1
        # else:
        #   self.op_exec()


        # prefix group 4
        if op == 0x67 :
          '''
          address override prefix
          '''
          pass
          prefixed = 1


        # prefix group 3
        if op == 0x66 :
           '''
           precision/operand size prefix
           '''
           self.chDB()
           prefixed = 1


        # prefix group 2
        # segment selector override
        if op == 0x2E :
           # CS override  @real mode ?
           self.segOV = self.rReg(cpu.cs_)
           prefixed = 1
           self.override = True
           # if protected...

        if op == 0x36 :
           # SS override
           self.segOV = self.rReg(cpu.ss_)
           prefixed = 1
           self.override = True

        if op == 0x3E :
           # DS override
           self.segOV = self.rReg(cpu.ds_)
           prefixed = 1
           self.override = True

        if op == 0x26 :
           # ES override
           self.segOV = self.rReg(cpu.es_)
           prefixed = 1
           self.override = True

        if op == 0x64 :
           # FS override
           self.segOV = self.rReg(cpu.fs_)
           prefixed = 1
           self.override = True

        if op == 0x65 :
           # GS override
           self.segOV = self.rReg(cpu.gs_)
           prefixed = 1
           self.override = True

        if op == 0x2E :
           # condition may not be true
           pass
           prefixed = 1

        if op == 0x2F :
           # condition may be true
           pass
           prefixed = 1

        cpu.msg('prefixed:{0} op:0x{1:02X}({1})'.format(prefixed , op))
        if prefixed == 0:
          '''
          prefixed == 0 -> op is not prefix
          operation execution
          '''
          self.op_exec()
        else:
          '''
          if op is prefix
          -> next prefix check
          '''
          self.op = self.readNextMem(self.CS)
          self.prefix()


    def op_exec(self):
        op = self.op
        
        try:
            print('@op_exec == op:{0}'.format(op))
            self.opcode[op](op)
            self.opStr=''
        except:
            print("error:", sys.exc_info()[0])
            cpu.msg('=== Error eip:{1:02X}:{2:02X} Opcode:0x{0:X} ==='.format(op,self.CS,self.eip))
            raise Exception

        '''
        if op == 0xB0:
            self.movALImm8()
        elif op == 0x04:
            self.addALImm8()
        elif op == 0xEB:
            self.jmpRel8()
        elif op == 0x3C:
            self.cmpALImm8()
        elif op == 0x74:
            self.jzRel8()
        elif op == 0x30:
            self.xorRM8R8()
        elif op == 0xCD:
            self.intImm8()
        elif op == 0xBE:
            self.movSIImm16()
        elif op == 0xB4:
            self.movAHImm8()
        elif op == 0x8A:
            self.movR8RM8()
        elif op == 0x08:
            self.orRM8R8()
        elif op == 0x83:
            self.addRM16Imm8()
        else:
            print("Not Implemented 0x%X" % op)
            s='[0x{0:02X}]:0x{1:02X}'.format(self.eip,op)
            input(s)
        
        '''

        # parameter initialize
        self.clearPrefix()
        
        





    def execute(self,op):
        self.op = op
        #check prefix
        self.prefix()



    # SIB bytes
    #
    # disp + base + index * scale
    # -> disp + SIB2(regB,regI,scale)
    #
    # code = scale76 + regB543 + regI210
    # scale76 -> 0,64,128,192 (2bit*64)
    # regB543 -> 0, 8,16,24,32,40,48,56 (3bit*8)
    # regI210 -> 0, 1, 2, 3, 4, 5, 6, 7
    #
    def SIB32(self , sibByte):

        maskB=0b00111000
        shftB=3
        maskI=0b00000111
        maskS=0b11000000
        shftS=6

        regB = (sibByte & maskB)>>shftB
        regI = (sibByte & maskI)
        scal = (sibByte & maskS)>>shftS
        print("sibByte:0x{3:X}=0b{3:8b} regB:{0} regI:{1} Scale:{2} ->regB+regI*Scale".format(regB , regI , scal , sibByte) )
        return self.rReg(regB)+ self.rReg(regI)*scal

   
