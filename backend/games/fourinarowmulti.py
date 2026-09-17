import random

class Connect4Game:
    def __init__(self):
        self.reset()

    def reset(self):
        self.board = [[0]*7 for _ in range(6)]
        self.current_player = 1
        self.game_over = False
        self.winner = 0

    def is_valid(self, c):
        return 0 <= c < 7 and self.board[0][c] == 0

    def next_row(self, c):
        for r in range(5, -1, -1):
            if self.board[r][c] == 0:
                return r
        return -1

    def drop(self, c):
        if self.game_over or not self.is_valid(c):
            return False

        r = self.next_row(c)
        self.board[r][c] = self.current_player

        if self.win(r, c, self.current_player):
            self.game_over = True
            self.winner = self.current_player

        self.current_player = 3 - self.current_player
        return True

    def win(self, r, c, p):
        for dr, dc in [(0,1),(1,0),(1,1),(1,-1)]:
            cnt = 1
            for d in [1,-1]:
                rr, cc = r + dr*d, c + dc*d
                while 0 <= rr < 6 and 0 <= cc < 7 and self.board[rr][cc] == p:
                    cnt += 1
                    rr += dr*d
                    cc += dc*d
            if cnt >= 4:
                return True
        return False

    def ai_move(self):
        valid = [c for c in range(7) if self.is_valid(c)]

        for c in valid:
            r = self.next_row(c)
            self.board[r][c] = 2
            if self.win(r, c, 2):
                self.board[r][c] = 0
                return c
            self.board[r][c] = 0

        for c in valid:
            r = self.next_row(c)
            self.board[r][c] = 1
            if self.win(r, c, 1):
                self.board[r][c] = 0
                return c
            self.board[r][c] = 0

        return random.choice(valid)
