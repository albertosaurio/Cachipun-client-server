# Alberto Salinas Muñoz
import tkinter as tk
import socket
import threading
from time import sleep


window = tk.Tk()
window.title("Sevidor")

# Marco superior que consta de dos botones de widgets (i.e. btnStart, btnStop)
topFrame = tk.Frame(window)
btnStart = tk.Button(topFrame, text="iniciar", command=lambda : start_server())
btnStart.pack(side=tk.LEFT)
btnStop = tk.Button(topFrame, text="Parar", command=lambda : stop_server(), state=tk.DISABLED)
btnStop.pack(side=tk.LEFT)
topFrame.pack(side=tk.TOP, pady=(5, 0))

# media ventana consiste en 2 etiquetas para mostrar el host y la información del puerto
middleFrame = tk.Frame(window)
lblHost = tk.Label(middleFrame, text = "Direccion: X.X.X.X")
lblHost.pack(side=tk.LEFT)
lblPort = tk.Label(middleFrame, text = "Puerto:XXXX")
lblPort.pack(side=tk.LEFT)
middleFrame.pack(side=tk.TOP, pady=(5, 0))

# la ventana del cliente muestra su area
clientFrame = tk.Frame(window)
lblLine = tk.Label(clientFrame, text="**********lista de clientes**********").pack()
scrollBar = tk.Scrollbar(clientFrame)
scrollBar.pack(side=tk.RIGHT, fill=tk.Y)
tkDisplay = tk.Text(clientFrame, height=10, width=30)
tkDisplay.pack(side=tk.LEFT, fill=tk.Y, padx=(5, 0))
scrollBar.config(command=tkDisplay.yview)
tkDisplay.config(yscrollcommand=scrollBar.set, background="#F4F6F7", highlightbackground="grey", state="disabled")
clientFrame.pack(side=tk.BOTTOM, pady=(5, 10))

#variables
server = None
HOST_ADDR = "0.0.0.0"
HOST_PORT = 8080
client_name = " "
clients = []
clients_names = []
player_data = []


# inicia la funcion del servidor
def start_server():
    global server, HOST_ADDR, HOST_PORT # el código está bien sin esto
    btnStart.config(state=tk.DISABLED)
    btnStop.config(state=tk.NORMAL)

    server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    print (socket.AF_INET)
    print (socket.SOCK_STREAM)

    server.bind((HOST_ADDR, HOST_PORT))
    server.listen(5)  # el servidor está esperando por la conexión del cliente

    threading._start_new_thread(accept_clients, (server, " "))

    lblHost["text"] = "Direccion: " + HOST_ADDR
    lblPort["text"] = "Puerto: " + str(HOST_PORT)


# detiene la funcion del server
def stop_server():
    global server
    btnStart.config(state=tk.NORMAL)
    btnStop.config(state=tk.DISABLED)


def accept_clients(the_server, y):
    while True:
        if len(clients) < 2:
            client, addr = the_server.accept()
            clients.append(client)

            # aqui se usa un hilo para no obstruir el hilo de la interfaz gráfica de usuario
            threading._start_new_thread(send_receive_client_message, (client, addr))

# Función para recibir mensajes del cliente actual Y
# Enviar ese mensaje a otros clientes
def send_receive_client_message(client_connection, client_ip_addr):
    global server, client_name, clients, player_data, player0, player1

    client_msg = " "

    # envia el mensaje de bienvenida al cliente, para que se den cuenta que ya se conectaron 
    client_name = client_connection.recv(4096)
    if len(clients) < 2:
        client_connection.send("bienvenido usuario1")
    else:
        client_connection.send("bienvenido usuario2")

    clients_names.append(client_name)
    update_client_names_display(clients_names)  # actualiza nombres de los clientes

    if len(clients) > 1:
        sleep(1)

        # enviar nombre del oponente
        clients[0].send("oponente_name$" + clients_names[1])
        clients[1].send("oponente_name$" + clients_names[0])
        # va a dormir
#estos datos hacia abajo son los del cliente-servidor que vi en stackoverflow,pero perdi el enlace, entonces NO TOCAR
    while True:
        data = client_connection.recv(4096)
        if not data: break

        # obtener la elección del jugador a partir de los datos recibidos
        player_choice = data[11:len(data)]

        msg = {
            "choice": player_choice, 
            "socket": client_connection
        }

        if len(player_data) < 2:
            player_data.append(msg)

        if len(player_data) == 2:
            # enviar la eleccion del player1 al player2 y vice versa
            player_data[0].get("socket").send("$oponente_choice" + player_data[1].get("choice"))
            player_data[1].get("socket").send("$oponente_choice" + player_data[0].get("choice"))

            player_data = []

    # busque el índice del cliente y luego elimínelo de ambas listas (lista de nombres de clientes y lista de conexiones)
    idx = get_client_index(clients, client_connection)
    del clients_names[idx]
    del clients[idx]
    client_connection.close()

    update_client_names_display(clients_names)  # actualiza nombres de los clientes


# Devuelve el índice del cliente actual en la lista de clientes
def get_client_index(client_list, curr_client):
    idx = 0
    for conn in client_list:
        if conn == curr_client:
            break
        idx = idx + 1

    return idx


# Actualizar la visualización del nombre del cliente cuando un nuevo cliente se conecta O
# Cuando un cliente conectado se desconecta
def update_client_names_display(name_list):
    tkDisplay.config(state=tk.NORMAL)
    tkDisplay.delete('1.0', tk.END)

    for c in name_list:
        tkDisplay.insert(tk.END, c+"\n")
    tkDisplay.config(state=tk.DISABLED)


window.mainloop()
