import socket

port = 53
ip = '127.0.0.1'

socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
socket.bind((ip, port))

def question_domain(data):
    state = 0
    length = 0
    domain = ''
    domain_part = []
    step = 0
    y = 0
    for byte in data:
        y+=1
        if state == 1:
            step += 1
            domain += chr(byte)
            if step == length:
                state = 0
                domain_part.append(domain)
                domain = ''
                step = 0
            elif byte == 0:
                break
        else:
            state = 1
            length = byte
    
    print(domain_part)
    question_type = data[y:y+2]
    print(question_type)
    return (domain_part, question_type)

def get_flags(flags):
    byte1 = bytes(flags[:1])
    byte2 = bytes(flags[1:2])
    rflags = ''
    QR = '1'
    OPCODE = ''

    for bit in range(1,5):
        OPCODE += str(ord(byte1)&(1<<bit))
    AA = '1'
    TC = '0'
    RD = '0'
    RA = '0'
    Z = '000'
    RCODE = '0000'

    return (int(QR+OPCODE+AA+TC+RD, 2).to_bytes(1, byteorder='big')+ int(RA+Z+RCODE,2).to_bytes(1,byteorder='big'))


def build_response(data):
    
    # get id transation
    transationID = data[:2]
    TID =''
    for byte in transationID:
        TID += hex(byte)[2:]

    # get flags
    flags = get_flags(data[2:4])
    
    QDCOUNT = b'\x00\x01' # Two bytes 
    
    get_question_domain = question_domain(data[12:])


while True:
    data, addr = socket.recvfrom(512)
    
    response = build_response(data)
    socket.sendto(response,addr)
