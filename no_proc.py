# authors
# Jose Gabriel de Oliveira Santana 620459
# William Giacometti Dutra de Oliveira 743606

import socket, sys, struct, threading, pickle, time, random

multicast_group = '225.0.0.1'    	# configura o ip hospedeiro para a conexao
multicast_port = 2022           # porta de comunicacao (a mesma que a do servidor)

def create_multicast():

    sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM, socket.IPPROTO_UDP)
    sock.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
    sock.bind(('', multicast_port))
    mreq = struct.pack("4sl", socket.inet_aton(multicast_group), socket.INADDR_ANY)
    sock.setsockopt(socket.IPPROTO_IP, socket.IP_ADD_MEMBERSHIP, mreq)
    
    return sock


def send(s_t, msg):
    time.sleep(random.randint(3, 10))
    s_t.sendto(pickle.dumps(msg), (multicast_group, multicast_port))

def listen (p_id, msg_list, clock):

    s_t = create_multicast()

    while True:
        
        time.sleep(random.randint(3, 10))

        msg = pickle.loads(s_t.recv( 1024 ))
       
        if(msg[1] > clock[0]):
            clock[0] = msg[1]+1
        else:
            clock[0] = clock[0]+1

        if(msg[3] == True):
            print("Mensagem: ", msg)
            msg_list.append(msg)

            msg_list.sort(key = lambda x: (x[1], x[2]))
            
            time.sleep(3)
            print("Lista de msgs: ----->")
            print(msg_list)
            print("-------------------->")
            ack = ["ACK", clock[0], p_id, False]
            send(s_t, ack)
        else:
            print("ACK: ", msg)

def Main():

    s_t = create_multicast()

    msg_list = []


    p_id = input("Id do processo: ")
    clock = input("Clock inicial: ")

    p_id = int(p_id)
    clock = [int(clock)]


    t_proc = threading.Thread(target=listen, args=(p_id, msg_list, clock))

    t_proc.start()

    while True:
        input()
        msg = input("Mensagem: ")
        msg = [msg, clock[0]+1, p_id, True]
        send(s_t, msg)
        print(msg)




if __name__ == '__main__':
    Main()
