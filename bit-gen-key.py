import bitcoin

msgs = [
    '所有的压缩，都表示公钥坐标转换为公钥值时的压缩',
    '压缩密钥不是把密钥压缩，而是指仅用来生成压缩公钥的密钥',
    '压缩地址也不是把地址压缩，而是用压缩公钥生成的地址'
]
print('='*80)
print('\n'.join(m.center(60, ' ') for m in msgs))
print('='*80)

# 生成一个随机的密钥
while True:
    # 生成一个用十六进制表示的长 256 位的私钥（str类型）
    private_key = bitcoin.random_key()
    # 解码为十进制的整形密钥
    decoded_private_key = bitcoin.decode_privkey(private_key, 'hex')
    if 0 < decoded_private_key < bitcoin.N:
        break

print(f'密钥（十六进制）：{private_key} （长 256 位）')
print(f'密钥（十进制）：{decoded_private_key} （0 到 1.158*10**77 之间）')

# 用 WIF 格式编码密钥
wif_encoded_private_key = bitcoin.encode_privkey(decoded_private_key, 'wif')
print(f'密钥（WIF）：{wif_encoded_private_key} （5 开头，长 51 字符）')

# 用 01 标识的压缩密钥
compressed_private_key = private_key + '01'
print(f'压缩密钥（十六进制）：{compressed_private_key} （01 结尾，长 264 位）')

# 生成 WIF的压缩格式
wif_compressed_private_key = bitcoin.encode_privkey(
    bitcoin.decode_privkey(compressed_private_key, 'hex'), 'wif')
print(f'压缩密钥（WIF）：{wif_compressed_private_key} （L/K 开头）')

# 计算公钥坐标 K = k * G
public_key = bitcoin.fast_multiply(bitcoin.G, decoded_private_key)
print(f'公钥（坐标）：{public_key}')
# 转十六也可用 bitcoin.encode(xxx, 16)
print(f'公钥（坐标的十六进制）：{tuple(hex(i) for i in public_key)}')

# 计算公钥
hex_encoded_public_key = bitcoin.encode_pubkey(public_key, 'hex')
print(f'公钥（十六进制）：{hex_encoded_public_key} （04 x y）')

# 计算压缩公钥
# if public_key[1] % 2 == 0:  # 两种方式均可
if public_key[1] & 1 == 0:
    compressed_prefix = '02'
else:
    compressed_prefix = '03'
# 转十六也可用 bitcoin.encode(xxx, 16)
hex_compressed_public_key = compressed_prefix + hex(public_key[0])[2:]
print(f'压缩公钥（十六进制）{hex_compressed_public_key} '
      '（02 开头代表 y 是偶数，03 开头代表 y 是奇数）')

# 计算地址
# 传入公钥坐标对象/十六进制公钥值，输出同样的地址
# 传入压缩公钥值，输出与⬆️不同的地址
print(f'地址（b58check）：{bitcoin.pubkey_to_address(public_key)} （1 开头）')
print('压缩地址（b58check）：'
      f'{bitcoin.pubkey_to_address(hex_compressed_public_key)} （1 开头）')
