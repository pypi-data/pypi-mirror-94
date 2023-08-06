import hashlib

def encode(s,length):
    try:
        if(length>32 or length<0):
            raise ValueError('length must not be greater than than 32 and less than 0')
        else:

            l = len(s) // 3
            inc = count = 0
            inc = len(s) % 3
            temp = ""

            while (count < l):
                temp += chr(ord(s[count]) + 7)
                count += 1
            while (count < 2 * l):
                temp += chr(ord(s[count]) + 17)
                count += 1
            while (count < 3 * l + inc):
                temp += chr(ord(s[count]) + 13)
                count = count + 1

            enca = (hashlib.sha256(s.encode())).hexdigest()
            encb = hashlib.new('ripemd160', s.encode())
            encb = encb.hexdigest()
            encc = enca[47:55] + encb[14:22]
            encd = ((hashlib.sha256(encc.encode()).hexdigest())[11:11 + length]).capitalize()
            encd = encd[0:length // 2] + encd[length // 2:length + 1].upper()
            encd = encd.replace(encd[len(encd) // 2], "$")
            i = ord(encd[2])
            if (i > 99):

                encd = encd.replace(encd[i // 100], "_", 1)
            else:
                re = i // 100
                if (re > len(encd) - 1):
                    encd = encd.replace(encd[len(encd) - 1], "_", 1)
                else:
                    encd = encd.replace(encd[re], "@", 1)
            return(encd)
    except ValueError:
        raise

encode(string,length)