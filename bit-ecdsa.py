"""
椭圆曲线加密
Elliptic curve digital signature algorithm 椭圆曲线数字签名算法
"""
import ecdsa
import os

# secp256k1, http://www.oid-info.com/get/1.3.132.0.10
_p = 0xFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFEFFFFFC2F
_r = 0xFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFEBAAEDCE6AF48A03BBFD25E8CD0364141
_b = 0x0000000000000000000000000000000000000000000000000000000000000007
_a = 0x0000000000000000000000000000000000000000000000000000000000000000
_Gx = 0x79BE667EF9DCBBAC55A06295CE870B07029BFCDB2DCE28D959F2815B16F81798
_Gy = 0x483ada7726a3c4655da4fbfc0e1108a8fd17b448a68554199c47d08ffb10d4b8
# 通过 p、a、b 定义一条曲线
curve_secp256k1 = ecdsa.ellipticcurve.CurveFp(_p, _a, _b)
# 定义一个生成点：曲线、x、y、序号
generator_secp256k1 = ecdsa.ellipticcurve.Point(curve_secp256k1, _Gx, _Gy, _r)
oid_secp256k1 = (1, 3, 132, 0, 10)
SECP256k1 = ecdsa.curves.Curve("SECP256k1", curve_secp256k1,
                               generator_secp256k1, oid_secp256k1)
ec_order = _r

curve = curve_secp256k1
generator = generator_secp256k1


def random_secret():
    # 从系统中获得密码安全的随机值，转换成 int 返回
    # Collect 256 bits of random data from the OS's cryptographically secure
    # random number generator
    byte_array = os.urandom(32).hex()

    return int(byte_array, 16)


def get_point_pubkey(point):
    if (point.y() % 2) == 1:
        # 把 x 转换成十六进制填进去，长度保持 64，不足高位用 0 补齐
        key = '03' + '%064x' % point.x()
    else:
        key = '02' + '%064x' % point.x()

    return key


def get_point_pubkey_uncompressed(point):
    key = ('04' +
           '%064x' % point.x() +
           '%064x' % point.y())
    return key


# 密钥
secret = random_secret()
print("密钥：", secret)

# 生成公钥点
point = secret * generator
print("椭圆曲线算出的公钥点", point)

print(f"压缩公钥：{get_point_pubkey(point)}")
print(f"非压缩公钥：{get_point_pubkey_uncompressed(point)}")

# 通过曲线、x、y、顺序值也能直接计算出点
point1 = ecdsa.ellipticcurve.Point(curve, point.x(), point.y(), ec_order)
assert(point1 == point)
