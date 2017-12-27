import crypt
import sys
import itertools

if(len(sys.argv)!=2):
    print("Usage: python crack.py hash")
    quit()

hash1 = sys.argv[1]
salt = '50'

def findstring(hash1):

    charset = 'abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ'
    for i in range(1,5):
        for xs in itertools.product(charset, repeat=i):
                str1 = ''.join(xs)
                if crypt.crypt(str1,salt) == hash1:
                        return str1



password = findstring(hash1)
print(password)
