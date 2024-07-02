import random

class Parchis:
    def __init__(self):
        self.board = self.create_board()
        self.players = self.initialize_players()
        self.turn = 0

    def create_board(self):
        # Crear el tablero con las casillas
        board = ['empty'] * 68  # Suponiendo que el tablero tiene 68 casillas
        return board

    def initialize_players(self):
        # Inicializar jugadores y sus fichas
        players = {
            'red': {'home': 4, 'board': [], 'goal': 0},
            'blue': {'home': 4, 'board': [], 'goal': 0},
            'green': {'home': 4, 'board': [], 'goal': 0},
            'yellow': {'home': 4, 'board': [], 'goal': 0}
        }
        return players

    def roll_dice(self):
        return random.randint(1, 6)

    def move_piece(self, player, piece_index, steps):
        # Lógica para mover una ficha
        if piece_index < len(self.players[player]['board']):
            current_position = self.players[player]['board'][piece_index]
            new_position = current_position + steps
            if new_position < 68:  # Suponiendo que la última casilla es la 67
                self.players[player]['board'][piece_index] = new_position
                # Verificar capturas y aplicar recompensas
                self.check_capture(player, new_position)
                self.check_goal_entry(player, new_position)
            else:
                self.players[player]['goal'] += 1
                self.players[player]['board'].pop(piece_index)
                print(f"Player {player} moved piece to goal!")
        else:
            print(f"Player {player} has no piece at index {piece_index}")

    def check_capture(self, player, position):
        # Verificar si hay una ficha en la posición que puede ser capturada
        for other_player in self.players:
            if other_player != player:
                if position in self.players[other_player]['board']:
                    self.players[other_player]['board'].remove(position)
                    self.players[other_player]['home'] += 1
                    self.apply_rewards(player, 'capture')
                    print(f"Player {player} captured a piece from {other_player}!")

    def check_goal_entry(self, player, position):
        # Verificar si una ficha ha entrado en la meta
        if position == 67:  # Suponiendo que la meta está en la posición 67
            self.players[player]['goal'] += 1
            self.apply_rewards(player, 'goal_entry')
            print(f"Player {player} entered a piece to goal!")

    def apply_rewards(self, player, reward_type):
        if reward_type == 'capture':
            steps = 20
        elif reward_type == 'goal_entry':
            steps = 10
        else:
            return False

        for piece_index in range(len(self.players[player]['board'])):
            if self.can_move(player, piece_index, steps):
                self.move_piece(player, piece_index, steps)
                return True
        return False

    def can_move(self, player, piece_index, steps):
        current_position = self.players[player]['board'][piece_index]
        new_position = current_position + steps
        return new_position < 68  # Suponiendo que la última casilla es la 67

    def play_turn(self):
        current_player = list(self.players.keys())[self.turn]
        dice_result = self.roll_dice()
        print(f"{current_player} rolled a {dice_result}")

        if self.players[current_player]['home'] > 0:
            # Sacar una ficha de la casa al tablero
            self.players[current_player]['board'].append(0)
            self.players[current_player]['home'] -= 1
            print(f"{current_player} moved a piece from home to the board")
        else:
            # Mover una ficha existente
            self.move_piece(current_player, 0, dice_result)

        self.turn = (self.turn + 1) % len(self.players)

    def check_victory(self):
        for player, status in self.players.items():
            if status['goal'] == 4:
                return player
        return None

    def play_game(self):
        while not self.check_victory():
            self.play_turn()

        winner = self.check_victory()
        print(f"The winner is {winner}!")

# Crear una instancia del juego y jugar
game = Parchis()
game.play_game()
