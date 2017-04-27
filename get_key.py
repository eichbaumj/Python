import sys
from os import path
import struct
from bruteforce_stdcrypto import *


def getDecryptionKey(footer, pin):
	cryptoFooter = getCryptoData(footer)

	# make the decryption key from the password
	decKey = ''
	if cryptoFooter.kdf == KDF_PBKDF: 
		decKey = decryptDecodePbkdf2Key(cryptoFooter, pin)
	elif cryptoFooter.kdf == KDF_SCRYPT:
		decKey = decryptDecodeScryptKey(cryptoFooter, pin)
	else:
		raise Exception("Unknown or unsupported KDF: " + str(cryptoFooter.kdf))

	return decKey


def main(args):

	if len(args) < 2:
		print 'Usage: python getkey.py [footer file] [pin]'
		print '[] = Mandatory'
		print ''
	else:
		# use inputed filenames for the two files
		footerFile  = args[1]
		pin 		= args[2]

		assert path.isfile(footerFile), "Footer file '%s' not found." % footerFile
		footerSize = path.getsize(footerFile)

		assert (footerSize >= 16384), "Input file '%s' must be at least 16384 bytes" % footerFile

		decKey = getDecryptionKey(footerFile, pin)
		print 'Key: ', decKey.encode('hex').upper()
		open('/home/santoku/Desktop/DecKey.key','wb').write(decKey)
	
if __name__ == "__main__": 
	main(sys.argv)
