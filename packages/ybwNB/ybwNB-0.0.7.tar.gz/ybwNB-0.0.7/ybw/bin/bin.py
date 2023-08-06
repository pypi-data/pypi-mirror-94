def Xor(a: bytes, b: bytes):
    res = b''
    def func(x): return 1 if x == 0 else 0
    data, lens = [a, b], [len(a), len(b)]
    idx = lens.index(min(lens))
    print(idx, func(idx))
    mini = data[idx]
    big = data[func(idx)]
    for i in range(len(big)):
        res += bytes(chr(big[i] ^ mini[i % len(mini)]), encoding='gb2312')

    return res


abc = b'qwertyuiopasdfghjklzxcvbnm'

ABC = b'QWERTYUIOPASDFGHJKLZXCVBNM'

num = b'1234567890'

chSet = range(32, 128)
