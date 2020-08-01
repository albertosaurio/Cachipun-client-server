# Alberto Salinas Muñoz

import tkinter as tk
from tkinter import PhotoImage
from tkinter import messagebox
import socket
from time import sleep
import threading

# MAIN GAME WINDOW
window_main = tk.Tk()
window_main.title("Cliente del juego")
your_name = ""
oponente_name = ""
game_round = 0
game_timer = 4
your_choice = ""
oponente_choice = ""
TOTAL_NO_OF_ROUNDS = 5
your_score = 0
oponente_score = 0

# cliente de red
client = None
HOST_ADDR = "0.0.0.0"
HOST_PORT = 8080


top_welcome_frame= tk.Frame(window_main)
lbl_name = tk.Label(top_welcome_frame, text = "Nombre:")
lbl_name.pack(side=tk.LEFT)
ent_name = tk.Entry(top_welcome_frame)
ent_name.pack(side=tk.LEFT)
btn_connect = tk.Button(top_welcome_frame, text="Coneccion", command=lambda : connect())
btn_connect.pack(side=tk.LEFT)
top_welcome_frame.pack(side=tk.TOP)

top_message_frame = tk.Frame(window_main)
lbl_line = tk.Label(top_message_frame, text="***********************************************************").pack()
lbl_welcome = tk.Label(top_message_frame, text="")
lbl_welcome.pack()
lbl_line_server = tk.Label(top_message_frame, text="***********************************************************")
lbl_line_server.pack_forget()
top_message_frame.pack(side=tk.TOP)


top_frame = tk.Frame(window_main)
top_left_frame = tk.Frame(top_frame, highlightbackground="green", highlightcolor="green", highlightthickness=1)
lbl_your_name = tk.Label(top_left_frame, text="Tu nombre: " + your_name, font = "Helvetica 13 bold")
lbl_oponente_name = tk.Label(top_left_frame, text="Tu oponente: " + oponente_name)
lbl_your_name.grid(row=0, column=0, padx=5, pady=8)
lbl_oponente_name.grid(row=1, column=0, padx=5, pady=8)
top_left_frame.pack(side=tk.LEFT, padx=(10, 10))


top_right_frame = tk.Frame(top_frame, highlightbackground="green", highlightcolor="green", highlightthickness=1)
lbl_game_round = tk.Label(top_right_frame, text="Ronda de juego (x) inicia en", foreground="blue", font = "Helvetica 14 bold")
lbl_timer = tk.Label(top_right_frame, text=" ", font = "Helvetica 24 bold", foreground="blue") #fuente de letra y fondos
lbl_game_round.grid(row=0, column=0, padx=5, pady=5)
lbl_timer.grid(row=1, column=0, padx=5, pady=5)
top_right_frame.pack(side=tk.RIGHT, padx=(10, 10))

top_frame.pack_forget()

middle_frame = tk.Frame(window_main)

lbl_line = tk.Label(middle_frame, text="***********************************************************").pack()
lbl_line = tk.Label(middle_frame, text="**** REGISTRO ****", font = "Helvetica 13 bold", foreground="blue").pack()
lbl_line = tk.Label(middle_frame, text="***********************************************************").pack()

round_frame = tk.Frame(middle_frame)
lbl_round = tk.Label(round_frame, text="Ronda")
lbl_round.pack()
lbl_your_choice = tk.Label(round_frame, text="Tu eleccion: " + "Ninguna", font = "Helvetica 13 bold")
lbl_your_choice.pack()
lbl_oponente_choice = tk.Label(round_frame, text="Eleccion del oponente: " + "Ninguna")
lbl_oponente_choice.pack()
lbl_result = tk.Label(round_frame, text=" ", foreground="blue", font = "Helvetica 14 bold")
lbl_result.pack()
round_frame.pack(side=tk.TOP)

final_frame = tk.Frame(middle_frame)
lbl_line = tk.Label(final_frame, text="***********************************************************").pack()
lbl_final_result = tk.Label(final_frame, text=" ", font = "Helvetica 13 bold", foreground="blue")
lbl_final_result.pack()
lbl_line = tk.Label(final_frame, text="***********************************************************").pack()
final_frame.pack(side=tk.TOP)

middle_frame.pack_forget()
# iconos de botones de piedra papel o tigeras (usurpados de internet)
button_frame = tk.Frame(window_main)
photo_piedra = PhotoImage(file=r"piedra.gif")
photo_papel = PhotoImage(file = r"papel.gif")
photo_tijera = PhotoImage(file = r"tijera.gif")
# creacion de botones para sus variables (deje el nombre asignado a la misma imagen)
btn_piedra = tk.Button(button_frame, text="piedra", command=lambda : choice("piedra"), state=tk.DISABLED, image=photo_piedra)
btn_papel = tk.Button(button_frame, text="papel", command=lambda : choice("papel"), state=tk.DISABLED, image=photo_papel)
btn_tijera = tk.Button(button_frame, text="tijera", command=lambda : choice("tijera"), state=tk.DISABLED, image=photo_tijera)
btn_piedra.grid(row=0, column=0)
btn_papel.grid(row=0, column=1)
btn_tijera.grid(row=0, column=2)
button_frame.pack(side=tk.BOTTOM)

# definicion de variables para los botones
def game_logic(tu, oponente):
    winner = ""
    piedra = "piedra"
    papel = "papel"
    tijera = "tijera"
    player0 = "tu"
    player1 = "oponente"
#logica del cachipun
    if tu == oponente:
        winner = "Empate"
    elif tu == piedra:
        if oponente == papel:
            winner = player1
        else:
            winner = player0
    elif tu == tijera:
        if oponente == piedra:
            winner = player1
        else:
            winner = player0
    elif tu == papel:
        if oponente == tijera:
            winner = player1
        else:
            winner = player0
    return winner


def enable_disable_buttons(todo):
    if todo == "disable":
        btn_piedra.config(state=tk.DISABLED)
        btn_papel.config(state=tk.DISABLED)
        btn_tijera.config(state=tk.DISABLED)
    else:
        btn_piedra.config(state=tk.NORMAL)
        btn_papel.config(state=tk.NORMAL)
        btn_tijera.config(state=tk.NORMAL)


def connect():
    global your_name
    if len(ent_name.get()) < 1:
        tk.messagebox.showerror(title="ERROR!!!", message="DEBES ingresar tu nombre <ej. Michael Miranda>")
    else:
        your_name = ent_name.get()
        lbl_your_name["text"] = "tu nombre: " + your_name
        connect_to_server(your_name)


def count_down(my_timer, nothing):
    global game_round
    if game_round <= TOTAL_NO_OF_ROUNDS:
        game_round = game_round + 1

    lbl_game_round["text"] = "Ronda de juego " + str(game_round) + " inicia en"

    while my_timer > 0:
        my_timer = my_timer - 1
        print("el timer es: " + str(my_timer))
        lbl_timer["text"] = my_timer
        sleep(1)

    enable_disable_buttons("enable")
    lbl_round["text"] = "Ronda - " + str(game_round)
    lbl_final_result["text"] = ""


def choice(arg):
    global your_choice, client, game_round
    your_choice = arg
    lbl_your_choice["text"] = "Tu eleccion: " + your_choice

    if client:
        client.send("Game_Round"+str(game_round)+your_choice)
        enable_disable_buttons("disable")


def connect_to_server(name):
    global client, HOST_PORT, HOST_ADDR, your_name
    try:
        client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        client.connect((HOST_ADDR, HOST_PORT))
        client.send(name) # Enviar nombre al servidor después de conectarse

        # deshabilitar widgets
        btn_connect.config(state=tk.DISABLED)
        ent_name.config(state=tk.DISABLED)
        lbl_name.config(state=tk.DISABLED)
        enable_disable_buttons("disable")

        # iniciar un hilo para seguir recibiendo mensajes del servidor
        # no bloquee el hilo principal :)
        threading._start_new_thread(receive_message_from_server, (client, "m"))
    except Exception as e:
        tk.messagebox.showerror(title="ERROR!!!", message="No se puede conectar al host: " + HOST_ADDR + " en puerto: " + str(HOST_PORT) + " El servidor puede no estar disponible. Intenta nuevamente más tarde")


def receive_message_from_server(sck, m):
    global your_name, oponente_name, game_round
    global your_choice, oponente_choice, your_score, oponente_score

    while True:
        from_server = sck.recv(4096)

        if not from_server: break

        if from_server.startswith("Bienvenido"):
            if from_server == "bienvenido1":
                lbl_welcome["text"] = "Servidor dice: bienvenido " + your_name + "! a la espera del jugador 2"
            elif from_server == "bienvenido2":
                lbl_welcome["text"] = "Servidor dice: bienvenido " + your_name + "! el juego iniciara pronto"
            lbl_line_server.pack()

        elif from_server.startswith("oponente_name$"):
            oponente_name = from_server.replace("oponente_name$", "")
            lbl_oponente_name["text"] = "Oponente: " + oponente_name
            top_frame.pack()
            middle_frame.pack()

            # sabemos que dos usuarios están conectados, por lo que el juego está listo para comenzar
            threading._start_new_thread(count_down, (game_timer, ""))
            lbl_welcome.config(state=tk.DISABLED)
            lbl_line_server.config(state=tk.DISABLED)

        elif from_server.startswith("$oponente_choice"):
            # obtener la opción del oponente del servidor
            oponente_choice = from_server.replace("$oponente_choice", "")

            # averiguar quién gana en esta ronda
            who_wins = game_logic(your_choice, oponente_choice)
            round_result = " "
            if who_wins == "tu":
                your_score = your_score + 1
                round_result = "Ganador"
            elif who_wins == "oponente":
                oponente_score = oponente_score + 1
                round_result = "Pierde"
            else:
                round_result = "EMPATE"

            # actualiza la GUI
            lbl_oponente_choice["text"] = "eleccion del oponente : " + oponente_choice
            lbl_result["text"] = "Resultado: " + round_result

            # Es esta la última ronda, ej. Ronda 5?
            if game_round == TOTAL_NO_OF_ROUNDS:
                # calcular el resultado final
                final_result = ""
                color = ""

                if your_score > oponente_score:
                    final_result = "(Tu ganas!!!)"
                    color = "green"
                elif your_score < oponente_score:
                    final_result = "(Tu pierdes!!!)"
                    color = "red"
                else:
                    final_result = "(Empate!!!)"
                    color = "black"

                lbl_final_result["text"] = "resultado final: " + str(your_score) + " - " + str(oponente_score) + " " + final_result
                lbl_final_result.config(foreground=color)

                enable_disable_buttons("disable")
                game_round = 0

            # inicia el timer
            threading._start_new_thread(count_down, (game_timer, ""))


    sck.close()


window_main.mainloop()
