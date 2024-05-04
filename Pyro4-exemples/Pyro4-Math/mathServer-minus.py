import Pyro4 as pyro
import sys
import os
@pyro.expose
class Math1(object):
    def subst(self,a,b):
        print('subst {} - {} '.format(a,b))
        return int(a)-int(b)
def main():
    server = Math1()
    daemon = pyro.Daemon()
    '''ns = pyro.locateNS(host=os.environ['NS_HOST'],
                       port=int(os.environ['NS_PORT']))'''

    uri = daemon.register(server)

    ns = pyro.locateNS(host="localhost", port=9091)
    ns.register('Math1',uri)
    print('Ready object : ',uri)
    daemon.requestLoop()
#if __name__ == '__main__':
    '''if 'NS_HOST' not in os.environ or 'NS_PORT' not in os.environ:
        print('You have to set VARS NS_HOST and NS_PORT')
        sys.exit(1)'''
main()