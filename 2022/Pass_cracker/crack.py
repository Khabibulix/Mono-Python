#!python3
# coding:utf-8

import time, string, hashlib, sys, argparse, atexit

class Layout:
    ROUGE = '\033[91m'
    VERT = '\033[92m'
    FIN = '\033[0m'
    UNDERLINE = "\x1B[4m"
    FIN_UNDERLINE = "\x1B[0m"
    BOLD = '\033[1m'

class Cracker:
    @staticmethod
    def crack_dict(hash_provided, file):
        """
        Cracking using a wordlist
        :param hash_provided: hash to crack
        :param file: wordlist to use
        :return found: we want to know if it was efficient
        """
        try:
            found = False
            opened_file = open(file, "r")
            for mot in opened_file.readlines():
                mot = mot.strip("\n").encode("utf8")
                hash = hashlib.md5(mot).hexdigest()
                hash_sha = hashlib.sha256(mot).hexdigest()
                if hash == hash_provided:
                    print(Layout.VERT + "Password found", str(mot).replace("b'", "")[:-1], "--", hash + Layout.FIN)
                    found = True
                    return found
                if hash_sha == hash_provided:
                    print(Layout.VERT + "Password found", str(mot).replace("b'", "")[:-1], "--", hash_sha + Layout.FIN)
                    found = True
                    return found
            if not found:
                print(Layout.ROUGE + "Not found" + Layout.FIN)
                return found
            opened_file.close()

        except FileNotFoundError as fnfe:
            print(Layout.ROUGE + "File does not exist:", str(fnfe) + Layout.FIN)
            sys.exit(1)

    @staticmethod
    def crack_smart(hash_provided, pattern, _index=0):
        """
        :param hash_provided: hash to crack
        :param pattern:
        :param _index: private variable
        :return:
        """
        MAJ = string.ascii_uppercase
        CHIFFRES = string.digits
        MIN = string.ascii_lowercase
        found = False
        if _index < len(pattern):
            if pattern[_index] in MAJ + CHIFFRES + MIN:
                cracker.crack_smart(hash_provided, pattern, _index+1)
            if "^" == pattern[_index]:
                for c in MAJ:
                    p = pattern.replace("^", c, 2)
                    if len(hash_provided) == 32:
                        currhash = hashlib.md5(p.encode("utf8")).hexdigest()
                    if len(hash_provided) == 64:
                        currhash = hashlib.sha256(p.encode("utf8")).hexdigest()
                    if currhash == hash_provided:
                        print(Layout.VERT + "Found in maj: " + p + Layout.FIN)
                        found = True
                        return found
                    else:
                        cracker.crack_smart(hash_provided, p, _index + 1)

            if "*" == pattern[_index]:
                for c in MIN:
                    p = pattern.replace("*", c, 2)
                    if len(hash_provided) == 32:
                        currhash = hashlib.md5(p.encode("utf8")).hexdigest()
                    if len(hash_provided) == 64:
                        currhash = hashlib.sha256(p.encode("utf8")).hexdigest()
                    if currhash == hash_provided:
                        print(Layout.VERT + "Found in min: " + p + Layout.FIN)
                        found = True
                        return found
                    else:
                        cracker.crack_smart(hash_provided, p, _index + 1)

            if "²" == pattern[_index]:
                for c in CHIFFRES:
                    p = pattern.replace("²", c, 2)
                    if len(hash_provided) == 32:
                        currhash = hashlib.md5(p.encode("utf8")).hexdigest()
                    if len(hash_provided) == 64:
                        currhash = hashlib.sha256(p.encode("utf8")).hexdigest()
                    if currhash == hash_provided:
                        print(Layout.VERT + "Found: " + p + Layout.FIN)
                        found = True
                        return found
                    else:
                        cracker.crack_smart(hash_provided, p, _index + 1)

    @staticmethod
    def generate_the_hack(arg, pwd_to_encrypt):
        if arg == 1:
            return hashlib.md5(pwd_to_encrypt.encode("utf8")).hexdigest()
        if arg == 2:
            return hashlib.sha256(pwd_to_encrypt.encode("utf8")).hexdigest()
        else:
            return None

cracker = Cracker()
print(cracker.crack_smart("56f27dc9bb026e86ee241fa197d00fb0", "*^3*"))

"""
def display_time():
    print("Durée :", str(time.time() - debut), "secondes")

parser = argparse.ArgumentParser(
               description="████████████████████████████"
                +Layout.BOLD+Layout.UNDERLINE+
               "Password Cracker"+Layout.FIN+
               "█████████████████████████████████",
                epilog="██████████████████████████████████████████████████████████████████████████████")

parser.add_argument("-f", "--file", dest="file", help="Path to wordlist file", required=False)
parser.add_argument("-g", "--gen", dest="gen", help="Choose hashing of password (1 for md5, 2 for sha-256",required=False, type=int)
parser.add_argument("-pwd", "--password", dest="pwd", help="Password")
parser.add_argument("-l", dest="plength", help="Password Length", type=int, required=False)
parser.add_argument("-p", dest="pattern", help="Using pattern of password (^=Maj, *=Min, ²=Chiffre)",required=False)


args = parser.parse_args()

debut = time.time()
atexit.register(display_time)



if args.pwd:
    if args.file and not args.plength:
       print("[Cracking using wordlist", args.file,"]")
       cracker.crack_dict(args.pwd, args.file)
    elif args.plength and not args.file:
       print("[Cracking using incremental mode for", str(args.plength), "letter(s)]")
       cracker.crack_incr(args.pwd, args.plength)
    elif args.pattern:
       print("[Cracking using pattern mode for", str(args.pattern),"]")
       cracker.crack_smart(args.pwd, args.pattern)
    elif args.gen: #if no hash, we create one
       pwd = args.pwd
       args = vars(parser.parse_args())
       if args["gen"] == 1:  # md5
             print("[MD5 hash is:", cracker.generate_the_hack(1, pwd), "]")
       if args["gen"] == 2:  # sha-256
             print("[SHA-256 hash is", cracker.generate_the_hack(2, pwd), "]")
       args = parser.parse_args()

    elif not args.gen:
        while True:
         algo = input(Layout.ROUGE+ "In which algorithm do you want to encrypt the password?"+ Layout.FIN)
         if algo == 1:
            print(Layout.UNDERLINE+"[The MD5 hash is:",Layout.FIN_UNDERLINE, cracker.generate_the_hack(1, args.pwd))
            break
         if algo == 2:
            print(Layout.UNDERLINE+"[SHA-256 hash is",Layout.FIN_UNDERLINE, cracker.generate_the_hack(2, args.pwd))
            break
         else:
            print(Layout.ROUGE, "Invalid input, please enter 1 for MD5, or 2 for sha-256)", Layout.FIN)
            continue

if args.gen and not args.pwd:
    print(Layout.ROUGE +
   "You must provide a password to encrypt, dummy. Use -pwd for that. "
   #+Layout.FIN+
   +Layout.UNDERLINE +
   "Example:"+
   Layout.FIN+
   Layout.FIN_UNDERLINE+
   " -pwd 'password' where password will be encrypted",)

if not args.file and not args.plength and not args.gen and not args.pattern:
    print(Layout.ROUGE + "Enter -h to display help" + Layout.FIN)
"""