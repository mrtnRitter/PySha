# (c) Martin Ritter, 2020

# ---------- Import Dependencies
#
#

import os
import sys
import hashlib
import itertools
import math
from tkinter import filedialog, Tk
from pathlib import Path


# ---------- Global variables
#
#

version = "1.1"
Buf_size = 1024*1024													# 1024 = 1KB ... * 1024 = 1MB ...



# ---------- Print box
#
#
def printbox (layout, width, height, box_halign, box_valign, content, c_halign, c_valign):
	terminalsize = os.get_terminal_size()
	box = []
	i = 0
	
	cwidth = width-2
	content_height = len(content.splitlines())
		
	if c_valign == "top":
		cheight_upper = 0
		cheight_lower = height - content_height
	elif c_valign == "bottom":
		cheight_upper = height - content_height
		cheight_lower = 0
	elif c_valign == "center":
		cheight_upper = math.floor((height - content_height)/2)
		cheight_lower = math.ceil((height - content_height)/2)
	
	box.append(layout[0] + cwidth*layout[4] + layout[1])
	
	while cheight_upper > 0:
		box.append(layout[5] + cwidth*layout[6] + layout[5])
		cheight_upper -= 1
	for line in content.splitlines():
		if line == "":
			box.append(layout[5] + cwidth*layout[6] + layout[5])
		elif c_halign == "left":
			box.append(layout[5] + line.ljust(cwidth) + layout[5])
		elif c_halign == "right":
			box.append(layout[5] + line.rjust(cwidth) + layout[5])
		elif c_halign == "center":
			box.append(layout[5] + line.center(cwidth) + layout[5])
	while cheight_lower > 0:
		box.append(layout[5] + cwidth*layout[6] + layout[5])
		cheight_lower -= 1	
	box.append(layout[2] + cwidth*layout[4] + layout[3])

		
	if box_valign == "top":
		printer_h = 0
		printer_l = (terminalsize[1]-2) - (height + 2)
	elif box_valign == "bottom":
		printer_h = (terminalsize[1]-2) - (height + 2)
		printer_l = 0
	elif box_valign == "center":
		printer_h = math.floor(((terminalsize[1]-2) - (height+2))/2)
		printer_l = math.ceil(((terminalsize[1]-2) - (height+2))/2)		
		
		
				
	while printer_h > 0:
		print ("")
		printer_h -= 1

	for entry in box:
		if box_halign == "left":
			print(entry.ljust(terminalsize[0]))
		elif box_halign == "right":
			print(entry.rjust(terminalsize[0]))
		elif box_halign == "center":
			print(entry.center(terminalsize[0]))
			
	while printer_l > 0:
		print ("")
		printer_l -= 1

# ========================================================================================================================

os.system("cls")

starttext = """\
* * * PySHA {version} * * *

Your friendly Python SHA3-512 Hasher.
""".format(version = version)

printbox("╭╮╰╯─│ ", 50, 8, "center", "top", starttext, "center", "center")

Tk().withdraw()
startpath = Path("\\\\?\\" + filedialog.askdirectory(title = "Select folder"))

filesdone = 0
hashes = []

print ("Hashing recursivly from " + str(startpath))
print ("Counting all files...", end = "\t")
sys.stdout.flush

allfiles = str(f"{(sum(len(files) for _, _, files in os.walk(startpath))):,}")

print (allfiles + " files found!\n")

for root, dirs, files in os.walk(startpath):
	
	for filename in files:

		filepath = Path(root).joinpath(filename)
				
		#filesize = str("{:.2f}".format(os.path.getsize(filepath)/(1024**3)))
		
		filesize = str("{:.2f}".format((filepath.stat().st_size)/(1024**3)))
				
		file_hash = hashlib.sha3_512()
		
		filesdone += 1
		
		print ("Processing file " + str(f"{filesdone:,}") + " of " + allfiles)
				
		with open(filepath, "rb") as file: 
			
			for i in itertools.count():
				data = file.read(Buf_size)
				
				currentsize = str("{:.2f}".format(i*(Buf_size/(1024**3)),2))
				
				print ("Reading " + currentsize + "GB of " + filesize + "GB from " + filename, end="\r")
				
				if not data:
					break

				file_hash.update(data)
				
		print ("\n")
		hashes.append(file_hash.hexdigest() + " *" + str(filepath.relative_to(startpath)))

with open(os.path.join(startpath, "checksums.sha3-512"), "w+", encoding="utf-8") as file:
	for hash in hashes:
		file.write(hash + "\n")
