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
from optparse import OptionParser

infile = ''
outfile = ''
key = ''
decrypt = False
encrypt = False
usage = "Usage: otp.py {-e | --encrypt | -d | --decrypt} -i <INPUTFILE> [-k <KEYFILE>] [-o <OUTPUTFILE>]\n" \
+ "       Choose either encrypt or decrypt. For decrypt, a keyfile is required."

# Parse arguments
parser = OptionParser(usage=usage)
parser.add_option("-d", "--decrypt", action="store_true", dest="decrypt", default=False,
                  help="Decrypt a file")
parser.add_option("-e", "--encrypt", action="store_true", dest="encrypt", default=False,
                  help="Encrypt a file")
parser.add_option("-i", action="store", type="string", dest="infile", metavar="INPUTFILE",
                  default='', help="Input file for encryption or decryption")
parser.add_option("-k", action="store", type="string", dest="key", metavar="KEYFILE", default='', 
                  help="Decryption keyfile")
parser.add_option("-o", action="store", type="string", dest="outfile", metavar="OUTPUTFILE",
                  default='', help="File name for output of encryption or decryption")

(options, args) = parser.parse_args()
decrypt = options.decrypt
encrypt = options.encrypt
infile  = options.infile
outfile = options.outfile
key     = options.key

# Validate arguments
if ((decrypt == False and encrypt == False) or (decrypt == True and encrypt == True) or infile == ''):
	print usage
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
