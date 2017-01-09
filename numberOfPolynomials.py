
def numberOfPolynomials(m, q = 2):
    d = divisors(m)
    sum_moebius = 0;
    for i in d:
        to_moebius = 1/i
        r = moebius(to_moebius)*(q**i)
        sum_moebius = sum_moebius + r
    number = (1/m)*sum_moebius
    print "Number of irreducible polynomials over ", q, "with degree ", m, " is ", number
    return number