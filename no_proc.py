# authors
# Jose Gabriel de Oliveira Santana 620459
# William Giacometti Dutra de Oliveira 743606

import socket, sys, struct, threading, pickle, time, random

multicast_group = '225.0.0.1'    

def create_multicast():

    sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM, socket.IPPROTO_UDP)
    sock.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
    sock.bind(('', multicast_port))
    mreq = struct.pack("4sl", socket.inet_aton(multicast_group), socket.INADDR_ANY)
    sock.setsockopt(socket.IPPROTO_IP, socket.IP_ADD_MEMBERSHIP, mreq)
    
    return sock


def send_req(s_t, msg):
    s_t.sendto(pickle.dumps(msg), (multicast_group, 2020)
    s_t.sendto(pickle.dumps(msg), (multicast_group, 2021)
    s_t.sendto(pickle.dumps(msg), (multicast_group, 2022)

def send(s_t, msg, port):
    s_t.sendto(pickle.dumps(msg), (multicast_group, port))


                
def listen (p_id, msg_list, clock):

    s_t = create_multicast()

    while True:
        

        msg = pickle.loads(s_t.recv( 1024 ))

        prev_clock = (clock[0], p_id)
       
        if(msg[1] > clock[0]):
            clock[0] = msg[1]+1
        else:
            clock[0] = clock[0]+1

        print("Mensagem: ", msg)

        if(msg[3] == True):
            msg_list.append(msg)

            msg_list.sort(key = lambda x: (x[1], x[2]))
            
            print("Lista de msgs: ----->")
            print(msg_list)
            print("-------------------->")

       
        
        if (rec_want[0] == True):

                ack_counter = 0
                while ack_counter < 2:
                    ack = pickle.loads(s_t.recv( 1024 ))
                    if (ack[3] == False):
                        ack_counter += 1

                port_to_use = "202" + str(msg[2])
                ack = ["ACK", clock[0], p_id, False]
                send(s_t, ack, port_to_use)
        else: 
                ack = ["ACK", clock[0], p_id, False]
                if(p_id == 0):
                    port1 = "2021"
                    port2 = "2022"
                elif (p_id == 1):
                    port1 = "2020"
                    port2 = "2022"
                else:
                    port1 = "2020"
                    port2 = "2021"
                send(s_t, ack, port1)
                send(s_t, ack, port2)
            

def Main(argv):

    global multicast_port = argv[0] 

    s_t = create_multicast()

    msg_list = []


    p_id = input("Id do processo: ")
    clock = input("Clock inicial: ")

    p_id = int(p_id)
    clock = [int(clock)]
    
    rec_want = [False]

    t_proc = threading.Thread(target=listen, args=(p_id, msg_list, clock))

    t_proc.start()

    while True:
        input()
        msg = input("Usar recurso? (s/n): ")
        if msg == "s":
            rec_want[0] = True
            msg = ["REC WANT", clock[0]+1, p_id, True]
            send_rec(s_t, msg)
            print(msg)




if __name__ == '__main__':
    Main(sys.argv)
