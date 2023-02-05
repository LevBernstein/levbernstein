# Simple Python implementation of Conway's Game of Life. Browser version.
# Author: Lev Bernstein

import asyncio
from random import randint
from os import name, system
from js import document

# Board size
WIDTH = 30
HEIGHT = 18

# Number of generations to simulate
TICKS = 5000


def clear():
  div = document.getElementById("box")
  div.innerHTML = ''


async def status(board):
	clear()
	div = document.getElementById("box")
	div.innerHTML = "<br>".join("   ".join(("O" if num == 1 else "_" for num in row)) for row in board)
	await asyncio.sleep(.2)
	return


def alive(board, y, x):
	left = (x - 1) % WIDTH
	right = (x + 1) % WIDTH
	up = (y - 1) % HEIGHT
	down = (y + 1) % HEIGHT
	neighbors = sum([
		board[up][left],
		board[y][left],
		board[down][left],
		board[up][x],
		board[down][x],
		board[up][right],
		board[y][right],
		board[down][right]
	])
	return (board[y][x] == 0 and neighbors == 3) or (board[y][x] == 1 and neighbors in (2, 3))


async def game(board, generations):
	await status(board)
	oldBoard = board
	for n in range(generations):
		newBoard = [[0 for a in range(WIDTH)] for b in range(HEIGHT)]
		for i in range(HEIGHT):
			for j in range(WIDTH):
				newBoard[i][j] = int(alive(board, i, j))
		await status(newBoard)
		if newBoard in (board, oldBoard) or sum(row.count(1) for row in board) == 0:
			break
		oldBoard = board
		board = newBoard
	div = document.getElementById("box")
	div.innerHTML += (f"<br>Ended on generation {n+1}. Reload to generate a new seed.")
	return


if __name__ == "__main__":
	asyncio.ensure_future(game([[randint(0,1) for i in range(WIDTH)] for j in range(HEIGHT)], TICKS))
