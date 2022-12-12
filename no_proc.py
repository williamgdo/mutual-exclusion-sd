# authors
# Jose Gabriel de Oliveira Santana 620459
# William Giacometti Dutra de Oliveira 743606

# Tanenbaum example (page 256)

# python3 no_proc.py 2020 0 8
# python3 no_proc.py 2021 1 9
# python3 no_proc.py 2022 2 12

import socket, sys, struct, threading, pickle, time, random

multicast_group = '225.0.0.1'    
rec_using = [False]
rec_want = [False]
resource_queue = []
MAX_NODES = 3
acks_count = 0


def create_multicast():

    sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM, socket.IPPROTO_UDP)
    sock.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
    sock.bind(('', multicast_port))
    mreq = struct.pack("4sl", socket.inet_aton(multicast_group), socket.INADDR_ANY)
    sock.setsockopt(socket.IPPROTO_IP, socket.IP_ADD_MEMBERSHIP, mreq)
    
    return sock


def send_req(s_t, msg):
    s_t.sendto(pickle.dumps(msg), (multicast_group, 2020))
    s_t.sendto(pickle.dumps(msg), (multicast_group, 2021))
    s_t.sendto(pickle.dumps(msg), (multicast_group, 2022))

def send(s_t, msg, port):
    s_t.sendto(pickle.dumps(msg), (multicast_group, int(port)))

def useResource(p_id, clock, s_t):
  global acks_count
  
  print("Usando o recurso...")
  # simula utilizacao do recurso 
  time.sleep(5)
  rec_want = [False]
  rec_using = [False]
  acks_count = 0
  
  length = len(resource_queue)
  i = 0
  
  print("length : " + str(length))
  print("Parando de usar o recurso, notificando processos...")
  while i < length:
    port_to_use = "202" + str(resource_queue[i][2])
    ack = ["ACK", clock[0] + i + 1, p_id, False]
    send(s_t, ack, port_to_use)
    i += 1
    
  clock[0] = clock[0] + length # ?????
    
  print("Limpando fila e voltando ao estado inicial.")
  resource_queue.clear()
  return
  
def listen (p_id, msg_list, clock):
    global acks_count
    s_t = create_multicast()

    while True:
        print(acks_count)

        msg = pickle.loads(s_t.recv( 1024 ))
        # msg = ["REC WANT", clock atualizado, p_id, isMessage]

        prev_clock = (clock[0], p_id)
       
        if(msg[1] > clock[0]):
            clock[0] = msg[1]+1
        else:
            clock[0] = clock[0]+1

        print("Mensagem: ", msg)

        # checar se eh um ack do proprio processo
        if (p_id == msg[2]):
            print("recebeu o proprio ack")
            continue

        if(msg[3] == True): # se for mensagem
          msg_list.append(msg)  

          msg_list.sort(key = lambda x: (x[1], x[2]))
          
          print("Lista de msgs: ----->")
          print(msg_list)
          print("-------------------->")
          
          # port of connection received
          port_to_use = "202" + str(msg[2])
                  
          if(rec_using[0] == True):
            resource_queue.append(msg)
            nack = ["NACK", clock[0], p_id, False]
            send(s_t, nack, port_to_use)
          elif (rec_want[0] == True):
            time.sleep(2)
            print("rec_want[0] == True")
            # ack_counter = 0
            # while ack_counter < 2:
            #     ack = pickle.loads(s_t.recv( 1024 ))
            #     if (ack[3] == False):
            #         ack_counter += 1
            
            if (prev_clock[0] > msg[1]):
              time.sleep(2)
              # resource_queue.append(["REC WANT", clock[0], p_id, True])
              print("clock[0] > msg[1]")
              ack = ["ACK", clock[0], p_id, False]
              send(s_t, ack, port_to_use)
            else:
              time.sleep(2)
              print("clock[0] <= msg[1]")
              resource_queue.append(msg)
              nack = ["NACK", clock[0], p_id, False]
              send(s_t, nack, port_to_use)
          else: 
            time.sleep(2)
            print("rec_using[0] == False && rec_want[0] == False")
            ack = ["ACK", clock[0], p_id, False]
            send(s_t, ack, port_to_use)
            
            # if(p_id == 0):
            #     port1 = "2021"
            #     port2 = "2022"
            # elif (p_id == 1):
            #     port1 = "2020"
            #     port2 = "2022"
            # else:
            #     port1 = "2020"
            #     port2 = "2021"
            # send(s_t, ack, port1)
            # send(s_t, ack, port2)
        else: # se nao for mensagem
            if msg[1] != "NACK":
              print(msg[1])
              acks_count += 1
              print("recebeu um ack do processo " + str(msg[2]))
            else:
              print("recebeu um nack do processo " + str(msg[2]))
            print(resource_queue)
            
        if (acks_count == MAX_NODES - 1 and p_id != msg[2]):
          rec_using[0] = True
          
          useResource(p_id, clock, s_t)
          # t_resource = threading.Thread(target=useResource, args=(p_id, clock, s_t))
          # t_resource.start()

        
            

def Main(argv):
    global multicast_port
    
    # print(argv[1], argv[2], argv[3])
    
    if len(sys.argv) == 4:
      multicast_port = int(argv[1])
      p_id = int(argv[2])
      clock = [int(argv[3])]
    else:
      # print("Usage: python3 no_proc.py <port> <p_id> <base_clock>")
      multicast_port = input("Id do processo: ")
      p_id = input("Id do processo: ")
      clock = input("Clock inicial: ")

      multicast_port = int(multicast_port)
      p_id = int(p_id)
      clock = [int(clock)]
    
    s_t = create_multicast()

    msg_list = []

    
    
    # rec_want = [False]

    t_proc = threading.Thread(target=listen, args=(p_id, msg_list, clock))

    t_proc.start()

    while True:
        input()
        msg = input("Usar recurso? (s/n): ")
        if (msg == "s" and rec_want[0] != True): 
            rec_want[0] = True
            msg = ["REC WANT", clock[0]+1, p_id, True]
            send_req(s_t, msg)




if __name__ == '__main__':
    Main(sys.argv)
