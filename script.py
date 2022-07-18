import time

while True:
	f = open("demofile.txt", "r")
	print(f.read())
	print("I am working!")
	time.sleep(2)
