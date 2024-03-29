machine_code = []
reg_file = [0]*32
mem = []

data = "data"
reg_file[18] = 5 #key for encryption

a = 2 #function selector
reg_file[8] = 5 # n for factorial
reg_file[9] = 1

if a== 1:f = open('xor.txt', 'r')
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
            return rs+rt
        if(func == "100010"): #sub
            return rs-rt
        if(func == "100110"): #xor
            return chr(ord(rs)^rt)
        if(func == "011000"): #mul
            return rs*rt
    if(op =="001000"):
        return rs + imm
    if(op == "100011"):
        return mem[rs + imm]
    if(op == "000010"):
        return int((Integer(jimm,False)-(1048576+1)))
    if(op == "011100"):
        return rs*rt
    if(op=="000100"):
        return imm
    if(op=="100000"):
        return mem[rs+imm]
    if(op == "101000"):
        return rs+imm
    
def control_unit(ins):
    rw = False
    mr = False
    mw = False
    branch = False
    isb = False

    if(ins[0:6] == "000100"):
        if(reg_read(Integer(ins[6:11],False))==reg_read(Integer(ins[11:16],False)) or chr(reg_file[Integer(ins[6:11],False)]) == reg_file[Integer(ins[11:16],False)]):
            branch = True
    if(ins[0:6] == "000000"):
        rw = True
    if(ins[0:6] == "001000"):
        rw = True
    if(ins[0:6] == "011100"):
        rw = True
    if(ins[0:6] == "100000"):
        rw=True
    if(ins[0:6] == "000010"):
        branch = True
        isb = True
    if(ins[0:6]=="101000"):
        mw = True
    return [rw,mr,mw,branch,isb]
    

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
res = None
while i < (len(machine_code)):
    clock+=5
    ins = ins_fetch(i)
    regs = ins_decode(ins)
    res = ALU(reg_read(Integer(regs[0],False)),reg_read(Integer(regs[1],False)),Integer(ins[16:32],True),ins[0:6],ins[26:32],ins[6:32])
    rw,mr,mw,branch,isb = control_unit(ins)
    mem_write(res,reg_read(Integer(regs[1],False)),mw)
    write_back(Integer(regs[2],False),res,rw)
    #print(control_signals[0])
    if(branch):
        if(isb):
            i = res
        else:
            i += res
    i+=1
    b+=1

print("Clock Cycles: "+ str(clock))
if a==1:
    print("modified data :")
    for i in mem:
        print(i,end='')
    
else:
    print("factorial = " +str(reg_file[9]))
