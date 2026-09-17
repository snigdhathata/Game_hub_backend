import random

# =========================
# BOARD SETUP
# =========================

puzzles = {
    "easy": [[
        ['r','n','b','q','k','b','n','r'],
        ['p','p','p','p','p','p','p','p'],
        ['.','.','.','.','.','.','.','.'],
        ['.','.','.','.','.','.','.','.'],
        ['.','.','.','.','.','.','.','.'],
        ['.','.','.','.','.','.','.','.'],
        ['P','P','P','P','P','P','P','P'],
        ['R','N','B','Q','K','B','N','R']
    ]]
}

board = []
turn = "white"
winner = None
difficulty = "easy"
game_mode = "pvp"

# =========================
# GAME CONTROL
# =========================

def load_game(diff="easy", mode="pvp"):
    global board, turn, winner, difficulty, game_mode

    difficulty = diff
    game_mode = mode

    board = [row[:] for row in puzzles["easy"][0]]

    turn = "white"
    winner = None


def get_state():
    return {
        "board": board,
        "turn": turn,
        "winner": winner,
        "mode": game_mode
    }

load_game()

# =========================
# HELPERS
# =========================

def inside(x,y):
    return 0 <= x < 8 and 0 <= y < 8


def enemy(piece,color):
    return piece.islower() if color=="white" else piece.isupper()

# =========================
# MOVE GENERATION
# =========================

def get_moves(piece,x,y,color):

    moves=[]
    directions=[]

    if piece.lower()=="p":

        d=-1 if color=="white" else 1

        if inside(x+d,y) and board[x+d][y]==".":
            moves.append((x+d,y))

        for dy in [-1,1]:
            if inside(x+d,y+dy) and board[x+d][y+dy]!="." and enemy(board[x+d][y+dy],color):
                moves.append((x+d,y+dy))

    elif piece.lower()=="r":
        directions=[(-1,0),(1,0),(0,-1),(0,1)]

    elif piece.lower()=="b":
        directions=[(-1,-1),(-1,1),(1,-1),(1,1)]

    elif piece.lower()=="q":
        directions=[(-1,0),(1,0),(0,-1),(0,1),(-1,-1),(-1,1),(1,-1),(1,1)]

    elif piece.lower()=="n":

        for dx,dy in [(-2,-1),(-2,1),(-1,-2),(-1,2),(1,-2),(1,2),(2,-1),(2,1)]:

            tx=x+dx
            ty=y+dy

            if inside(tx,ty) and (board[tx][ty]=="." or enemy(board[tx][ty],color)):
                moves.append((tx,ty))

    elif piece.lower()=="k":

        for dx,dy in [(-1,0),(1,0),(0,-1),(0,1),(-1,-1),(-1,1),(1,-1),(1,1)]:

            tx=x+dx
            ty=y+dy

            if inside(tx,ty) and (board[tx][ty]=="." or enemy(board[tx][ty],color)):
                moves.append((tx,ty))

    for dx,dy in directions:

        tx=x+dx
        ty=y+dy

        while inside(tx,ty):

            if board[tx][ty]==".":
                moves.append((tx,ty))

            else:

                if enemy(board[tx][ty],color):
                    moves.append((tx,ty))

                break

            tx+=dx
            ty+=dy

    return moves

# =========================
# CHECK DETECTION
# =========================

def find_king(color):

    king='K' if color=="white" else 'k'

    for i in range(8):
        for j in range(8):

            if board[i][j]==king:
                return (i,j)

    return None


def in_check(color):

    king_pos=find_king(color)

    if not king_pos:
        return False

    kx,ky=king_pos

    enemy_color="black" if color=="white" else "white"

    for i in range(8):
        for j in range(8):

            piece=board[i][j]

            if piece==".":
                continue

            if enemy(piece,color):

                moves=get_moves(piece,i,j,enemy_color)

                if (kx,ky) in moves:
                    return True

    return False

# =========================
# LEGAL MOVE SEARCH
# =========================

def has_legal_moves(color):

    for i in range(8):
        for j in range(8):

            piece=board[i][j]

            if piece==".":
                continue

            if color=="white" and not piece.isupper():
                continue

            if color=="black" and not piece.islower():
                continue

            moves=get_moves(piece,i,j,color)

            for tx,ty in moves:

                temp=board[tx][ty]

                board[tx][ty]=piece
                board[i][j]="."

                if not in_check(color):

                    board[i][j]=piece
                    board[tx][ty]=temp

                    return True

                board[i][j]=piece
                board[tx][ty]=temp

    return False

# =========================
# CHECKMATE
# =========================

def checkmate(color):

    if not in_check(color):
        return False

    if has_legal_moves(color):
        return False

    return True

# =========================
# PLAYER MOVE
# =========================

def player_move(data):

    global turn,winner

    fx,fy=data["from"]
    tx,ty=data["to"]

    piece=board[fx][fy]

    if piece==".":
        return {"error":"empty"},400

    if turn=="white" and not piece.isupper():
        return {"error":"not your piece"},400

    if turn=="black" and not piece.islower():
        return {"error":"not your piece"},400

    if (tx,ty) not in get_moves(piece,fx,fy,turn):
        return {"error":"illegal move"},400

    board[tx][ty]=piece
    board[fx][fy]="."

    turn="black" if turn=="white" else "white"

    if checkmate(turn):
        winner="white" if turn=="black" else "black"

    return {"status":"ok","turn":turn,"winner":winner},200


# =========================
# AGENT MOVE
# =========================

def agent_move():

    global turn,winner

    moves=[]

    for i in range(8):
        for j in range(8):

            if board[i][j].islower():

                for tx,ty in get_moves(board[i][j],i,j,"black"):

                    moves.append((i,j,tx,ty))

    if not moves:
        return {"status":"stalemate"}

    fx,fy,tx,ty=random.choice(moves)

    board[tx][ty]=board[fx][fy]
    board[fx][fy]="."

    turn="white"

    if checkmate("white"):
        winner="black"

    return {"status":"ok","turn":"white","winner":winner}