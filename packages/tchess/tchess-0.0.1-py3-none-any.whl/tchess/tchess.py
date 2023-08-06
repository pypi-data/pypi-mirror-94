#!/usr/bin/env python3

""" Play the Chess in the terminal """

import pickle
import sys
import os
import copy
import time

class Ansi:
    """ The terminal ansi chars """

    GREEN = '\033[32m'
    RED = '\033[31m'
    RESET = '\033[0m'
    GRAY = '\033[37m'

    @staticmethod
    def disable():
        """ Disables the ansi chars """
        Ansi.GREEN = ''
        Ansi.RED = ''
        Ansi.RESET = ''
        Ansi.GRAY = ''

class Piece:
    """ Each piece in the chess board """

    PAWN = 'pawn'
    KING = 'king'
    QUEEN = 'queen'
    KNIGHT = 'knight'
    BISHOP = 'bishop'
    ROCK = 'rock'

    def __init__(self, name: str, color: str):
        self.name = name
        self.color = color
        self.id = id

    def __str__(self):
        return self.color + '-' + self.name

class Game:
    """ The running game handler """

    ROW_SEPARATOR = '|--------------|--------------|--------------|--------------|--------------|--------------|--------------|--------------|\n'

    def __init__(self):
        self.turn = 'white'
        self.logs = []

        # this item is used to validate saved games versions
        # if we load a file that created with old version of the game,
        # we can check it using this property
        # if we made backward IN-compatible changes on this class,
        # this number should be bumped.
        self.version = 1

        # initialize the board
        self.board = []
        for i in range(8):
            self.board.append([])
            for j in range(8):
                # handle default pieces location
                if i in (1, 6):
                    self.board[-1].append(
                        Piece(
                            name=Piece.PAWN,
                            color=('white' if i == 1 else 'black'),
                        )
                    )
                elif i in (0, 7):
                    name = Piece.PAWN
                    if j in (0, 7):
                        name = Piece.ROCK
                    elif j in (0, 3):
                        name = Piece.KING
                    elif j in (3 ,7):
                        name = Piece.QUEEN
                    elif j in (0, 4):
                        name = Piece.QUEEN
                    elif j in (4, 7):
                        name = Piece.KING
                    elif j in (2, 5):
                        name = Piece.BISHOP
                    elif j in (1, 6):
                        name = Piece.KNIGHT
                    self.board[-1].append(
                        Piece(
                            name=name,
                            color=('white' if i == 0 else 'black'),
                        )
                    )
                else:
                    self.board[-1].append(None)

    def change_turn(self):
        """ Changes the turn.

        If currently is white turn, set turn to black and reverse
        """
        self.turn = 'black' if self.turn == 'white' else 'white'

    def move(self, src, dst):
        """ Moves src to dst """
        # TODO : validate the move
        dst_p = copy.deepcopy(self.board[dst[0]][dst[1]])
        src_p = copy.deepcopy(self.board[src[0]][src[1]])

        if dst_p is not None:
            if dst_p.color == self.turn:
                # killing self!
                return False, 'Error: You cannot kill your self!'

        self.board[src[0]][src[1]] = None

        self.board[dst[0]][dst[1]] = src_p

        return True, ''

    def run_command(self, cmd: str) -> str:
        """ Gets a command as string and runs that on the game. Returns result message as string """
        cmd_parts = cmd.split()

        invalid_msg = 'Invalid Command!'

        result_msg = 'Runed'

        if len(cmd_parts) == 4:
            # the move operation
            if cmd_parts[0] in ('move', 'mv') and cmd_parts[2] == 'to':
                src = cmd_parts[1].replace('.', '-').split('-')
                dst = cmd_parts[3].replace('.', '-').split('-')
                if len(src) == 2 and len(dst) == 2:
                    try:
                        src[0] = int(src[0])-1
                        src[1] = int(src[1])-1
                        dst[0] = int(dst[0])-1
                        dst[1] = int(dst[1])-1

                        valid_range = list(range(0, 8))
                        if not (src[0] in valid_range and src[1] in valid_range and dst[0] in valid_range and dst[1] in valid_range):
                            return 'Error: Locations are out of range!'
                    except:
                        return 'Error: Invalid locations!'
                    result_msg = cmd_parts[1] + ' Moved to ' + cmd_parts[3]
                else:
                    return invalid_msg

                if self.board[src[0]][src[1]] is not None:
                    pass
                else:
                    return 'Error: source location is empty cell!'
                if src == dst:
                    return 'Error: source and target locations are not different!'
                if self.board[src[0]][src[1]].color != self.turn:
                    return 'Error: its ' + self.turn + ' turn, you should move ' + self.turn + ' pieces!'
                result = self.move(src, dst)
                if not result[0]:
                    return result[1]
            else:
                return invalid_msg
        else:
            return invalid_msg

        # add command to the log
        self.logs.append(cmd)

        # change the turn
        self.change_turn()

        return result_msg

    def render(self) -> str:
        """ Renders the board to show in the terminal """
        output = ''
        i = 0
        for row in self.board:
            output += self.ROW_SEPARATOR
            j = 0
            for column in row:
                if column is None:
                    column_str = ' ' + str(i+1) + '-' + str(j+1)
                    ansi_color = Ansi.GRAY
                    ansi_reset = Ansi.RESET
                else:
                    column_str = str(column)
                    ansi_color = Ansi.GREEN if column.color == 'white' else Ansi.RED
                    ansi_reset = Ansi.RESET
                output += '| ' + ansi_color + column_str + ansi_reset + (' ' * (13-len(column_str)))
                j += 1
            output += '|\n'
            i += 1
        output += self.ROW_SEPARATOR
        return output

def show_help():
    """ Prints the help message """
    print('''TChess - Play the chess in terminal

DESCRIPTION
    The TChess is a chess game in terminal.
    This software can handle saving the game in a file
    Then you can continue your game later by loading that file

SYNOPSIS
    $ '''+sys.argv[0]+''' [options...] [?game-file-name]

OPTIONS
    --help: shows this help
    --no-ansi: disable terminal ansi colors
    --play: play the saved game
    --play-speed: delay between play frame (for example `3`(secound) or `0.5`)

AUTHOR
    This software is created by Parsa Shahmaleki <parsampsh@gmail.com>
    And Licensed under MIT
''')

def load_game_from_file(path: str):
    """ Loads the game object from a file """
    tmp_f = open(path, 'rb')
    game = pickle.load(tmp_f)
    tmp_f.close()
    return game

def run(args=[]):
    """ The main cli entry point """

    game_file_name = 'game.tchess'

    # parse the arguments
    options = [arg for arg in args if arg.startswith('-')]
    arguments = [arg for arg in args if not arg.startswith('-')]

    # check the `--help` option
    if '--help' in options:
        options.remove('--help')
        show_help()
        sys.exit()

    # handle `--no-ansi` option
    if '--no-ansi' in options:
        options.remove('--no-ansi')
        Ansi.disable()

    # handle `--play` option
    is_play = False
    log_counter = 0
    if '--play' in options:
        options.remove('--play')
        is_play = True

    # handle `--play-speed` option
    play_speed = 1
    for option in options:
        if option.startswith('--play-speed='):
            options.remove(option)
            value = option.split('=', 1)[-1]
            try:
                play_speed = float(value)
            except:
                pass
            break

    # check the terminal size
    try:
        terminal_width = os.get_terminal_size().columns
    except:
        terminal_width = len(Game.ROW_SEPARATOR)
    if terminal_width < len(Game.ROW_SEPARATOR):
        print(
            'ERROR: your terminal width is less than ' + str(len(Game.ROW_SEPARATOR)) + '.',
            file=sys.stderr
        )
        sys.exit(1)

    if len(arguments) > 0:
        game_file_name = arguments[0]

    if os.path.isfile(game_file_name):
        # if file exists, load the game from that
        # (means user wants to open a saved game)
        try:
            game = load_game_from_file(game_file_name)

            # validate the game object
            if not isinstance(game, Game):
                raise

            # check the version
            if game.version != Game().version:
                print('ERROR: file `' + game_file_name + '` is created with OLD/NEW version of tchess and cannot be loaded', file=sys.stderr)
                raise
        except:
            # file is corrupt
            print('ERROR: file `' + game_file_name + '` is corrupt', file=sys.stderr)
            sys.exit(1)
    else:
        game = Game()

    game_logs = game.logs
    if is_play:
        game = Game()

    # last result of runed command
    last_message = ''

    while True:
        # render the game board on the terminal
        print('\033[H', end='')
        title = '*** Welcome to the TChess! ***'
        print(title, end='')
        print(' ' * (len(Game.ROW_SEPARATOR) - len(title)))
        print(' ' * len(Game.ROW_SEPARATOR))
        print(game.render())

        # get command from user and run it
        tmp_turn = game.turn
        ansi_color = Ansi.RED if tmp_turn == 'black' else Ansi.GREEN
        # fix whitespace
        print(last_message, end='')
        print(' ' * (len(Game.ROW_SEPARATOR)-len(last_message)))
        print(' ' * len(Game.ROW_SEPARATOR), end='\r')
        if is_play:
            time.sleep(play_speed)
            try:
                command = game_logs[log_counter]
            except:
                print('Finished.')
                sys.exit()
            log_counter += 1
        else:
            command = input(ansi_color + game.turn + Ansi.RESET + ' Turn >>> ').strip().lower()

        # check the empty command
        if command == '':
            last_message = ''
            continue

        # check the exit command
        if command in ['exit', 'quit', 'q']:
            game_file_name = os.path.abspath(game_file_name)
            print('Your game was saved in file `' + game_file_name + '`.')
            print(
                'To continue this game again, run `' + sys.argv[0] + ' '+repr(game_file_name)+'`.'
            )
            print('Good bye!')
            sys.exit()

        # run the command on the game to make effects
        last_message = game.run_command(command)

        # save the game
        # open a file
        # this file is used to save the game state
        # after any command on the game, game will be re-write on this file
        game_file = open(game_file_name, 'wb')
        pickle.dump(game, game_file)
        game_file.close()

if __name__ == '__main__':
    run(sys.argv[1:])
