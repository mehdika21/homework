import Pyro4 as pyro

if __name__ == '__main__':
    #uri = input('Insert the Pyro Server : ').strip()
    ns = pyro.locateNS(host="localhost", port=9090)
    uri = ns.lookup('Math')
    ns1 = pyro.locateNS(host="localhost", port=9091)
    uri1 = ns1.lookup('Math1')
    a = input('Enter integer value a  : ').strip()
    b = input('Enter integer value b  : ').strip()

    math = pyro.Proxy(uri)  # we will use Math object
    math1 = pyro.Proxy(uri1)
    result = math.sum(a, b)  # we call the sum method
    result1 = math1.subst(a, b)
    print('Sum >>> {} + {} = {}'.format(a, b, result))
    print('Subst >>> {} - {} = {}'.format(a, b, result1))