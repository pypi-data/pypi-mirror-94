import random

class TicTacToe:

    def __init__(self):
        """ Tic-tac-toe class

        Attributes:
            board (string) representing the tic-tac-toe board
            first_player (int) representing the first player 
            second_player (int) representing the second player 
            first_player_marker (string) representing the marker of the first player
            second_player_marker (string) representing the marker of the second player
            first_player_turn (bool) that keeps track of whose turn it is
        """

        self.board = ['#'] + 9 * [' ']
        self.first_player = 0
        self.second_player = 0
        self.first_player_marker = ' '
        self.second_player_marker = ' '
        self.first_player_turn = True

    def init_game(self):
        """Function to initialize the game. A tic-tac-toe board is displayed with position 
        numbers. The first player, chosen randomly gets to choose their marker.

        Args:
            None

        Returns:
            None

        """
        
        print('     |     |     ')
        print('  7  |  8  |  9  ')
        print('_ _ _|_ _ _|_ _ _')
        print('     |     |     ')
        print('  4  |  5  |  6  ')
        print('_ _ _|_ _ _|_ _ _')
        print('     |     |     ')
        print('  1  |  2  |  3  ')
        print('     |     |     ')

        print('\nThe game requires 2 players.')
        print('Please assign a number (1 or 2) to uniquely identify the players.')
        print('Hit Enter to continue...')
        input()

        self.choose_first()
        print(
            f'Player {self.first_player}, you have been randomly chosen to go first.')
        self.choose_marker()

    def play_game(self):
        """Function to play the game where the players take turns placing their markers on 
        the board until one of them wins or the game is a draw.

        Args:
            None

        Returns:
            None

        """
        
        self.init_game()
        print(f'The game begins...\n')

        while True:
            if self.first_player_turn:
                player = self.first_player
                marker = self.first_player_marker
            else:
                player = self.second_player
                marker = self.second_player_marker

            print(f'\nPlayer {player}:')
            print('_________')
            position = self.choose_board_position()
            self.place_marker(marker, position)
            self.display_board()

            if self.full_board_check():
                print('Tough game! The result is a draw.')
                break
            if self.win_check(marker):
                print(
                    f'Congratulations player {player}! You have won the game.')
                break

            self.first_player_turn = not(self.first_player_turn)

    def display_board(self):
        """Function to display tic-tac-toe board.

        Args:
            None

        Returns:
            None

        """

        print('     |     |     ')
        print(f'  {self.board[7]}  |  {self.board[8]}  |  {self.board[9]}  ')
        print('_ _ _|_ _ _|_ _ _')
        print('     |     |     ')
        print(f'  {self.board[4]}  |  {self.board[5]}  |  {self.board[6]}  ')
        print('_ _ _|_ _ _|_ _ _')
        print('     |     |     ')
        print(f'  {self.board[1]}  |  {self.board[2]}  |  {self.board[3]}  ')
        print('     |     |     ')

    def choose_first(self):
        """Function to choose the first player between players 1 and 2.

        Args:
            None

        Returns:
            None

        """
        
        self.first_player = random.randint(1, 2)
        
        if self.first_player == 1:
            self.second_player = 2
        else:
            self.second_player = 1

    def choose_marker(self):
        """Function for first player to choose marker 'X' or 'O'. The second player is 
        assigned the other marker.

        Args:
            None

        Returns:
            None

        """
        
        marker = 'wrong'
        acceptable_markers = ['X', 'O']
        
        while marker not in acceptable_markers:
            
            marker = input('Enter your marker choice (X or O): ')
            marker = marker.upper()

            if marker not in acceptable_markers:
                print('Sorry, input marker can only be X or O. Please try again.')
            else:
                self.first_player_marker = marker
                if self.first_player_marker == 'X':
                    self.second_player_marker = 'O'
                else:
                    self.second_player_marker = 'X'

    def choose_board_position(self):
        """Function for player to choose board position for marker placement.

        Args:
            None

        Returns:
            position (int): board position chosen by player for marker placement

        """
        
        acceptable_positions = range(1, 10)
        position = 0
        
        while (position not in acceptable_positions) or (not space_check(board, position)):
            try:
                position = int(input('Select a free position (1-9): '))

                if position not in acceptable_positions:
                    print('Sorry, invalid position! Please try again.')
                elif not self.space_check(position):
                    print('Sorry, this position is occupied. Choose another position.')
                else:
                    return position
            except:
                print('Sorry, you need to enter an integer value between 1 and 9.')

    def space_check(self, position):
        """Function to check if a board position is occupied.

        Args:
            position (int): board position chosen by player for marker placement

        Returns:
            is_occupied (bool): boolean that tells if the board position is occupied
                                or not

        """
        
        acceptable_markers = ['X', 'O']
        is_occupied = self.board[position] not in acceptable_markers
        return is_occupied

    def place_marker(self, marker, position):
        """Function that assigns player marker to board position specified.

        Args:
            marker (string): 'X' or 'O' player marker
            position (int): board position chosen by player for marker placement

        Returns:
            None

        """
        
        self.board[position] = marker

    def full_board_check(self):
        """Function that tells if the board is completely filled with 'X' and 'O' markers

        Args:
            None

        Returns:
            is_full (bool): boolean that tells if the board is completely filled with 'X' 
                            and 'O' markers

        """
        
        is_full = list(set(self.board[1:10])) == ['O', 'X']
        return is_full

    def win_check(self, marker):
        """Function that checks if player using marker has won the game.

        Args:
            marker (string): 'X' or 'O' player marker

        Returns:
            has_won (bool): boolean that determines if a player has won

        """
        
        win_series = [marker] * 3
        
        win_1 = win_series == [self.board[1], self.board[2], self.board[3]]
        win_2 = win_series == [self.board[4], self.board[5], self.board[6]]
        win_3 = win_series == [self.board[7], self.board[8], self.board[9]]
        win_4 = win_series == [self.board[1], self.board[4], self.board[7]]
        win_5 = win_series == [self.board[2], self.board[5], self.board[8]]
        win_6 = win_series == [self.board[3], self.board[6], self.board[9]]
        win_7 = win_series == [self.board[1], self.board[5], self.board[9]]
        win_8 = win_series == [self.board[3], self.board[5], self.board[7]]
        
        has_won = win_1 or win_2 or win_3 or win_4 or win_5 or win_6 or win_7 or win_8
        return has_won
