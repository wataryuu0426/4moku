# -*- coding: utf-8 -*-
"""4目並べ（コンソール版）

起動方法:
python w144moku.py
"""

import sys
import time


ROWS = 6
COLUMNS = 7
EMPTY = "."


def create_board():
    """空の盤面を作る。"""
    return [[EMPTY for _ in range(COLUMNS)] for _ in range(ROWS)]


def show_board(board):
    """盤面を表示する。"""
    print()
    for row in board:
        print(" ".join(row))
    print(" ".join(str(column) for column in range(1, COLUMNS + 1)))


def can_drop(board, column):
    """指定した列に石を置けるか判定する。"""
    return board[0][column] == EMPTY


def drop_piece(board, column, piece):
    """石を上から落とし、列の一番下の空きマスに置く。"""
    landing_row = None
    for row in range(ROWS - 1, -1, -1):
        if board[row][column] == EMPTY:
            landing_row = row
            break
    if landing_row is None:
        return None

    if sys.stdout.isatty():
        for row in range(landing_row + 1):
            frame = [board_row[:] for board_row in board]
            frame[row][column] = piece
            print("\033[2J\033[H", end="")
            show_board(frame)
            time.sleep(0.12)

    board[landing_row][column] = piece
    return landing_row


def count_direction(board, row, column, dr, dc, piece):
    """指定方向に連続する石の数を数える。"""
    count = 0
    r = row + dr
    c = column + dc
    while 0 <= r < ROWS and 0 <= c < COLUMNS:
        if board[r][c] != piece:
            break
        count += 1
        r += dr
        c += dc
    return count


def has_won(board, row, column, piece):
    """最後に置いた石を中心として4目があるか判定する。"""
    directions = ((0, 1), (1, 0), (1, 1), (1, -1))
    for dr, dc in directions:
        total = 1
        total += count_direction(board, row, column, dr, dc, piece)
        total += count_direction(board, row, column, -dr, -dc, piece)
        if total >= 4:
            return True
    return False


def is_full(board):
    """盤面が埋まっているか判定する。"""
    return all(board[0][column] != EMPTY for column in range(COLUMNS))


def read_column():
    """列番号、リスタート、終了の入力を受け取る。"""
    while True:
        text = input("置く列（1〜7）、R=リスタート、Q=終了 > ").strip()
        if text.upper() == "Q":
            return None
        if text.upper() == "R":
            return "restart"
        if text.isdigit():
            column = int(text) - 1
            if 0 <= column < COLUMNS:
                return column
        print("1から7までの数字を入力してください。")


def ask_restart():
    """ゲーム終了後にもう一度遊ぶか確認する。"""
    while True:
        choice = input("R=もう一度遊ぶ、Q=終了 > ").strip().upper()
        if choice == "R":
            return True
        if choice == "Q":
            return False
        print("RまたはQを入力してください。")


def main():
    board = create_board()
    players = ("X", "O")
    turn = 0

    print("===== 4目並べ =====")
    print("縦・横・斜めに同じマークを4つ並べたプレイヤーの勝ちです。")

    while True:
        show_board(board)
        piece = players[turn]
        print("プレイヤー " + piece + " の番です。")

        column = read_column()
        if column is None:
            print("ゲームを終了しました。")
            break
        if column == "restart":
            board = create_board()
            turn = 0
            print("新しいゲームを始めます。")
            continue

        if not can_drop(board, column):
            print("その列はいっぱいです。別の列を選んでください。")
            continue

        row = drop_piece(board, column, piece)
        if has_won(board, row, column, piece):
            show_board(board)
            print("プレイヤー " + piece + " の勝ちです！")
            if not ask_restart():
                break
            board = create_board()
            turn = 0
            continue

        if is_full(board):
            show_board(board)
            print("引き分けです！")
            if not ask_restart():
                break
            board = create_board()
            turn = 0
            continue

        turn = (turn + 1) % 2


if __name__ == "__main__":
    main()