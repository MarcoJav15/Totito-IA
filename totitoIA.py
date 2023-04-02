# Marco Javier de León Vasquez 1521719

# Librerías
import random
import math
import os


class Totito:
    def __init__(self):
        self.board = ['-' for _ in range(9)]
        if random.randint(0, 1) == 1:
            self.humanPLayer = 'X'
            self.botPlayer = "O"
        else:
            self.humanPLayer = "O"
            self.botPlayer = "X"

    def imprimirTablero(self):
        print("")
        for i in range(3):
            print("  ",self.board[0+(i*3)]," | ",self.board[1+(i*3)]," | ",self.board[2+(i*3)])
            print("")
            
    def tableroLleno(self,state):
        return not "-" in state

    def combinacionVictoria(self,state,player):
        if state[0]==state[1]==state[2] == player: return True
        if state[3]==state[4]==state[5] == player: return True
        if state[6]==state[7]==state[8] == player: return True
        if state[0]==state[3]==state[6] == player: return True
        if state[1]==state[4]==state[7] == player: return True
        if state[2]==state[5]==state[8] == player: return True
        if state[0]==state[4]==state[8] == player: return True
        if state[2]==state[4]==state[6] == player: return True

        return False

    def verificarVictoria(self):
        if self.combinacionVictoria(self.board,self.humanPLayer):
            os.system("cls")
            print(f"    {self.humanPLayer} ganó el juego!")
            return True
            
        if self.combinacionVictoria(self.board,self.botPlayer):
            os.system("cls")
            print(f"    {self.botPlayer} ganó el juego!")
            return True

        # Declara empate o no
        if self.tableroLleno(self.board):
            os.system("cls")
            print("   Empate!")
            return True
        return False

    def start(self):
        bot = ComputerPlayer(self.botPlayer)
        human = humanPLayer(self.humanPLayer)
        while True:
            os.system("cls")
            print(f"   Turno de {self.humanPLayer} ")
            self.imprimirTablero()
            
            #Humano
            square = human.human_move(self.board)
            self.board[square] = self.humanPLayer
            if self.verificarVictoria():
                break
            
            #Bot
            square = bot.machine_move(self.board)
            self.board[square] = self.botPlayer
            if self.verificarVictoria():
                break

       
        print()
        self.imprimirTablero()

class humanPLayer:
    def __init__(self,letter):
        self.letter = letter
    
    def human_move(self,state):
        # Elije la casilla a jugar
        while True:
            square =  int(input("Elija una casilla para colocar tu ficha (1-9): "))
            print()
            if state[square-1] == "-":
                break
        return square-1

class ComputerPlayer(Totito):
    def __init__(self,letter):
        self.botPlayer = letter
        self.humanPlayer = "X" if letter == "O" else "O"

    def players(self,state):
        n = len(state)
        x = 0
        o = 0
        for i in range(9):
            if(state[i] == "X"):
                x = x+1
            if(state[i] == "O"):
                o = o+1
        
        if(self.humanPlayer == "X"):
            return "X" if x==o else "O"
        if(self.humanPlayer == "O"):
            return "O" if x==o else "X"
    
    def actions(self,state):
        return [i for i, x in enumerate(state) if x == "-"]
    
    def result(self,state,action):
        newState = state.copy()
        player = self.players(state)
        newState[action] = player
        return newState
    
    def terminal(self,state):
        if(self.combinacionVictoria(state,"X")):
            return True
        if(self.combinacionVictoria(state,"O")):
            return True
        return False

    def minimax(self, state, player):
        max_player = self.humanPlayer  
        other_player = 'O' if player == 'X' else 'X'

        # Verifica si existe un ganador en el movimiento anterior
        if self.terminal(state):
            return {'posicion': None, 'puntuación': 1 * (len(self.actions(state)) + 1) if other_player == max_player else -1 * (
                        len(self.actions(state)) + 1)}
        elif self.tableroLleno(state):
            return {'posicion': None, 'puntuación': 0}

        if player == max_player:
            best = {'posicion': None, 'puntuación': -math.inf}  
        else:
            best = {'posicion': None, 'puntuación': math.inf}  
        for possible_move in self.actions(state):
            newState = self.result(state,possible_move)
            sim_score = self.minimax(newState, other_player)  

            sim_score['posicion'] = possible_move  

            if player == max_player:
                if sim_score['puntuación'] > best['puntuación']:
                    best = sim_score
            else:
                if sim_score['puntuación'] < best['puntuación']:
                    best = sim_score
        return best

    def machine_move(self,state):
        square = self.minimax(state,self.botPlayer)['posicion']
        return square

# Iniciando el juego
Totito = Totito()
Totito.start()