# Weasel program
# Lev Bernstein

import asyncio
from js import document
from math import log
from random import choice, randint


PHRASE = "METHINKS_IT_IS_LIKE_A_WEASEL"
LETTERS = "ABCDEFGHIJKLMNOPQRSTUVWXYZ_"
MAX_GENERATIONS = 10000
MUTATION_RATE = 5


def mutate() -> bool:
	return randint(1, 100) <= MUTATION_RATE


def fitness(survivor: str, target: str) -> int:
	if len(survivor) != len(target):
		raise Exception("Strings must be the same length!")
	return sum((int(survivor[i] == target[i]) for i in range(len(survivor))))


def strcmp(a: str, b: str, target: str) -> str:
	# Return string with higher fitness
	return a if fitness(a, target) > fitness(b, target) else b


def spawn(parent: str) -> str:
	return "".join(choice(LETTERS) if mutate() else letter for letter in parent)


def compete(parent: str, target: str, litter_size: int) -> str:
	# Spawn a litter of children, return the one with the highest fitness
	# Performance could probably be improved via use of a heap; however, I/O
	# is the biggest performance bottleneck, so not significant
	child = spawn(parent)
	for i in range(litter_size - 1):
		child = strcmp(child, spawn(parent), target)
	return strcmp(parent, child, target)


async def main():
	div = document.getElementById("box")
	div.innerHTML = ""
	seed = "".join(choice(LETTERS) for i in range(len(PHRASE)))
	for j in (1, 2, 5, 10, 20, 50, 100):
		survivor = seed
		await asyncio.sleep(.1)
		div.innerHTML += f"<br>{j}-child version:<br>Generation Child Score<br>"
		div.innerHTML += f"0 {survivor} {fitness(survivor, PHRASE)}"
		for i in range(1, MAX_GENERATIONS + 1):
			survivor = compete(survivor, PHRASE, j)
			if PHRASE == survivor:
				await asyncio.sleep(.1)
				div.innerHTML += f"<br>{i} {survivor} {fitness(survivor, PHRASE)}"
				await asyncio.sleep(.1)
				div.innerHTML += f"<br>{j}-child program successful on generation {i}.<br>"
				break
			if i % int(4 * (1 + (log(2 * MAX_GENERATIONS, 1.05 ** j)))) == 0:
				await asyncio.sleep(.1)
				div.innerHTML += f"<br>{i} {survivor} {fitness(survivor, PHRASE)}"


if __name__ == "__main__":
	asyncio.ensure_future(main())
