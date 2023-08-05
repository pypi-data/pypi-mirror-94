import keyboard
import subprocess

keyMap = {
	"f1": 11,
	"f2": 12,
	"f3": 13,
	"f4": 14,
	"f5": 15,
	"ctrl": 21,
	"f6": 22,
	"delete": 23,
	"left": 24,
	"up": 25,
	"right": 26,
	"alt": 31,
	"f10": 32,
	"f7": 33,
	"down": 34,
	"a": 41,
	"b": 42,
	"c": 43,
	"f8": 44,
	"f9": 45,
	"d": 51,
	"e": 52,
	"f": 53,
	"g": 54,
	"h": 55,
	"^": 5,
	"i": 61,
	",": 62,
	"j": 62,
	"(": 63,
	"k": 63,
	")": 64,
	"l": 64,
	"/": 65,
	"m": 65,
	"÷": 65,
	"n": 71,
	"7": 72,
	"o": 72,
	"8": 73,
	"p": 73,
	"9": 74,
	"q": 74,
	"×": 75,
	"*": 75,
	"r": 75,
	"s": 81,
	"4": 82,
	"t": 82,
	"5": 83,
	"u": 83,
	"6": 84,
	"v": 84,
	"-": 85,
	"−": 85,
	"w": 85,
	"=": 91,
	"x": 91,
	"1": 92,
	"y": 92,
	"2": 93,
	"z": 93,
	"3": 94,
	"+": 95,
	"\"": 95,
	"0": 102,
	"space": 102,
	".": 103,
	":": 103,
	"-": 104,
	"?": 104,
	"−": 104,
	"enter": 105
}

def getKey():
	subprocess.check_call(["stty", "-echo"], stdout=subprocess.DEVNULL, stderr=subprocess.STDOUT)
	currentKey = keyboard.read_key().lower()
	if currentKey in keyMap:
		subprocess.check_call(["stty", "echo"], stdout=subprocess.DEVNULL, stderr=subprocess.STDOUT)
		return keyMap[currentKey]
	else:
		subprocess.check_call(["stty", "echo"], stdout=subprocess.DEVNULL, stderr=subprocess.STDOUT)
		return 0