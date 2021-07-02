'p4a example service using oscpy to communicate with main application.'
import os
os.environ['KIVY_AUDIO'] = 'android'


from oscpy.server import OSCThreadServer



class Service(object):

    SERVER = OSCThreadServer()
    SERVER.listen('localhost', port=3000, default=True)

    a = 0





    def __init__(self):




        while True:
            pass






































                

if __name__ == '__main__':
    service = Service()



