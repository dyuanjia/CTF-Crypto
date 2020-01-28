from Crypto.Util.number import long_to_bytes

def GCD(p1, p2):
    while True:
        if p1.degree() > p2.degree():
            tmp_p1 = p1
            p1 = p2
            p2 = tmp_p1

        c1 = p1.coefficients()
        c2 = p2.coefficients()
        print p1.degree(), p2.degree()

        if p1.degree() <= 1 and p2.degree() <= 1:
            print (-1*(1/c1[1])*c1[0])
            print long_to_bytes(-1*(1/c1[1])*c1[0])
            print (-1*(1/c2[1])*c2[0])
            print long_to_bytes(-1*(1/c2[1])*c2[0])
            return
        to_mul = (1 / c1[-1])*c2[-1] 
        to_mul *= y^(p2.degree()-p1.degree())
        p2 -= to_mul*p1

ans = ''
ZM = Zmod(n)
P.<x> = PolynomialRing(ZM)

f1=((x2-x)^4097-(x1-x)^4097-4040)
f2=((x3-y)^4097-(x2-y)^4097-4040)
GCD(x1, x2)