machine_code = []
reg_file = [0]*32
mem = []

data = "data"
reg_file[18] = 5 #key for encryption

a = 1 #function selector
reg_file[8] = 2 # n for factorial
reg_file[9] = 1

if a== 1:
    f = open('xor.txt', 'r')
    reg_file[20] = 10
else:f = open('fact_mc.txt', 'r')

for i in range (len(data)):
    mem.append(data[i])
mem.append('\n')

def Integer(bString,signed):
    result = int(bString, 2)
    if (bString[0] == '1') & signed:
        result -= 2 ** len(bString)
    return result

def get_reg(str):
    Integer(str,False)


def ALU(rs,rt,imm,op,func,jimm):
    if(op == "000000"):
        if(func == "100000"): #add
            return [rs+rt,False]
        if(func == "100010"): #sub
            return [rs-rt,False]
        if(func == "100110"): #xor
            return [chr(ord(rs)^rt),False]
        if(func == "011000"): #mul
            return [rs*rt,False]
    if(op =="001000"):
        return [rs + imm,False]
    if(op == "100011"):
        return [mem[rs + imm],False]
    if(op == "000010"):
        return [int((Integer(jimm,False)-(1048576))),True]
    if(op == "011100"):
        return [rs*rt,False]
    if(op=="000100"):
        if(rs == rt or chr(rs)==rt):
            return [imm,True]
        else:
            return [imm,False]
    if(op=="100000"):
        return [mem[rs+imm],False]
    if(op == "101000"):
        return [rs+imm,False]
    
def control_unit(ins):
    rw = False
    mr = False
    mw = False
    isb = False

    if(ins[0:6] == "000000"):
        rw = True
    if(ins[0:6] == "001000"):
        rw = True
    if(ins[0:6] == "011100"):
        rw = True
    if(ins[0:6] == "100000"):
        rw=True
    if(ins[0:6] == "000010"):
        isb = True
    if(ins[0:6]=="101000"):
        mw = True
    return [rw,mr,mw,isb]
    

def write_back(reg,val,wr):
    if(wr):
        reg_file[reg] = val

def reg_read(i):
    return reg_file[i]

def mem_write(i,val,mw):
    if(mw):
        mem[i] = val

def mem_read(i):
    return mem[i]

def ins_fetch(i):
    return machine_code[i]

def ins_decode(ins):
    opcode = ins[0:6]
    func = ins[26:32]
    rs = ins[6:11]
    rt = ins[11:16]
    rd = ins[16:21]
    if opcode == "100011" or opcode == "001000" or opcode =="100000" or opcode=="101000":
        rd = rt
    return [rs,rt,rd]


for line in f.readlines():
    machine_code.append(line[:-1])

f.close()

i = 0
b = 0
clock = 0
IF_ID={}
ID_EX={}
EX_MEM={}
MEM_WB={}
res = None
ins = None
rw,mr,mw,branch,isb = None,None,None,None,None
while (i < (len(machine_code)+3)) :
    if MEM_WB != {}:
        write_back(Integer(MEM_WB["rd"],False),MEM_WB["res"],MEM_WB["rw"])
    if EX_MEM != {}:
        MEM_WB["ins"] = EX_MEM["ins"]
        MEM_WB["res"],MEM_WB["rd"] = EX_MEM["res"],EX_MEM["rd"]
        MEM_WB["rw"] = EX_MEM["rw"]
        mem_write(MEM_WB["res"],reg_read(Integer(MEM_WB["rd"],False)),EX_MEM["mw"])
    else:
        MEM_WB = {}
    if ID_EX != {}:
        EX_MEM["ins"] = ID_EX["ins"]
        EX_MEM["rs"],EX_MEM["rt"],EX_MEM["rd"] = ID_EX["rs"],ID_EX["rt"],ID_EX["rd"]
        res,branch =  ALU(reg_read(Integer(ID_EX["rs"],False)),reg_read(Integer(ID_EX["rt"],False)),Integer(ID_EX["ins"][16:32],True),ID_EX["ins"][0:6],ID_EX["ins"][26:32],ID_EX["ins"][6:32])
        if MEM_WB!={}:
            if MEM_WB["rd"]==EX_MEM["rs"] :
                res,branch =  ALU(MEM_WB["res"],reg_read(Integer(ID_EX["rt"],False)),Integer(ID_EX["ins"][16:32],True),ID_EX["ins"][0:6],ID_EX["ins"][26:32],ID_EX["ins"][6:32])
            elif MEM_WB["rd"]==EX_MEM["rt"]:
                res,branch =  ALU(reg_read(Integer(ID_EX["rs"],False)),MEM_WB["res"],Integer(ID_EX["ins"][16:32],True),ID_EX["ins"][0:6],ID_EX["ins"][26:32],ID_EX["ins"][6:32])
        rw,mr,mw,isb = control_unit(EX_MEM["ins"])
        if(branch):
            if(isb):
                i = res
            else:
                i+= res
        EX_MEM["res"],EX_MEM["rw"],EX_MEM["mw"] = res,rw,mw

    else:
        EX_MEM = {}
    if IF_ID != {}:
        ID_EX["ins"] = IF_ID["ins"]
        regs = ins_decode(IF_ID["ins"])
        ID_EX["rs"],ID_EX["rt"],ID_EX["rd"] = regs[0],regs[1],regs[2]
    else:
        ID_EX = {}
    if ins != None:
        IF_ID["ins"] = ins
    else:
        IF_ID = {} 
    if i< len(machine_code):
        ins = ins_fetch(i)
    else:
        ins = None
    i+=1
    b+=1

if a == 1:
    print("Clock cycles: " + str(b+1))
else:
    print("Clock cycles: " + str(((b+1))))

if a==1:
    print("modified data :")
    for i in mem:
        print(i,end='')
else:
    print("factorial = " +str(reg_file[9]))