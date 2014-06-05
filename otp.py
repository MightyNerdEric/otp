#!/usr/bin/python
# otp.py
# One-time pad encrypter/decrypter
# Author: Eric Ball, on behalf of some pretend criminal
# Note: This software has no real-world uses. It is the Rube Goldberg machine of cryptography.
# Use at your own peril.

# Usage: otp.py (-e | --encrypt | -d | --decrypt) -i <inputfile> [-k <keyfile>] [-o <outputfile>]

import os
import sys		# Necessary for getting arguments
import time		# Necessary for time-based filename

infile = ''
outfile = ''
key = ''
decrypt = False
encrypt = False
usageMsg = "Usage: python otp.py (-e | --encrypt | -d | --decrypt) -i <inputfile> [-k <keyfile>] [-o <outputfile>]\n\t" \
+ "Choose either encrypt or decrypt. For decrypt, a keyfile is required."

# Parse arguments
for i in range(1, len(sys.argv)): 
	if (sys.argv[i] == "-d" or sys.argv[i] == "--decrypt"):
		decrypt = True
	elif (sys.argv[i] == "-e" or sys.argv[i] == "--encrypt"):
		encrypt = True
	elif (sys.argv[i] == "-i"):
		infile = sys.argv[i+1]
	elif (sys.argv[i] == "-o"):
		outfile = sys.argv[i+1]
	elif (sys.argv[i] == "-k"):
		key = sys.argv[i+1]

# Validate arguments
if ((decrypt == False and encrypt == False) or (decrypt == True and encrypt == True) or infile == ''):
	print usageMsg
	exit()
elif (decrypt == True and key == ''):
	key = raw_input("Please enter name for the keyfile, or q to quit: ")
	if (key == 'q'):
		exit()
elif (encrypt == True and key != ''):
	print "It's not really a \"one-time\" pad if you use an old keyfile. Exiting..."
	exit()
   
# Encrypt function
if (encrypt == True):
	# Get input file as bytearray, and make a copy so "otp" (one-time pad buffer) is same length
	buf = bytearray(open(infile, "rb").read())
	otp = bytearray(buf)
	# For each byte in file, generate 1 random byte. Copy that to "otp," and then XOR it with buf, and store
	# the result over the old buf byte.
	for i in range (len(buf)):
		rand = bytearray(os.urandom(1))
		otp[i] = rand[0]
		buf[i] ^= otp[i]
	# If filename is not specified, the output will simply be the input filename with -out concatenated on the end
	if (outfile == ''):
		outfp = open(infile + "-out", "wb")
	else:
		outfp = open(outfile, "wb")
	outfp.write(buf)
	outfp.close()
	open(str(time.clock()), "wb").write(otp)
	
# Decrypt function
elif (decrypt == True):
	buf = bytearray(open(infile, "rb").read())
	otp = bytearray(open(key, "rb").read())
	for i in range (len(buf)):
		# By XORing each byte from the encrypted file with the key (one-time pad) used for encryption, the
		# original message is output.
		buf[i] ^= otp[i]
	# If filename is not specified, the output will simply be the input filename with -dc concatenated on the end
	if (outfile == ''):
		outfp = open(infile + "-dc", "wb")
	else:
		outfp = open(outfile, "wb")
	outfp.write(buf)
	outfp.close()
	exit()

else:
	print "Something went horribly, horribly wrong."
	exit()