from Tkinter import *
import time

canv_width=640
canv_height=480

cart_width=100
cart_height=100

pole_height=150


class cartObj(object):

    def __init__(self,p1_x,p1_y,p2_x,p2_y):
        print "Creating cart"
        self.p1_x=p1_x
        self.p1_y=p1_y
        self.p2_x=p2_x
        self.p2_y=p2_y

    def apple(self):
        #print self.tangerine
        print "I AM CLASSY APPLES!"

class poleObj(object):

    def __init__(self,p1_x,p1_y,p2_x,p2_y):
        print "Creating pole"
        self.p1_x=p1_x
        self.p1_y=p1_y
        self.p2_x=p2_x
        self.p2_y=p2_y



def main():
    root = Tk()
    canv = Canvas(root, width=canv_width, height=canv_height)
    canv.pack(fill='both', expand=True)

    #Create objects
    cart = cartObj(canv_width/2-cart_width/2, canv_height-cart_height, canv_width/2+cart_width/2, canv_height) #top_left corner x and y, right bottom point x and y
    pole = poleObj(canv_width/2, canv_height-cart_height, canv_width/2, canv_height-cart_height-pole_height) #point 1 x and y, point 2 x and y
    #pole = poleObj(canv_width/2, 0, canv_width/2, 640)

    #Draw objects
    middle = canv.create_line(canv_width/2, 0, canv_width/2, 640, fill='red')
    right = canv.create_line(canv_width, 0, canv_width, canv_height, fill='blue')
    left = canv.create_line(0, 0, 0, canv_height, fill='red')

    #cart = canv.create_rectangle(cart.p1_x, cart.p1_y , cart.p2_x, cart.p2_y, outline='black', fill='gray40', tags=('rect'))
    pole = canv.create_line(pole.p1_x, pole.p1_y, pole.p2_x, pole.p1_y, fill='red')
    #pole = canv.create_line(canv_width/2, 0, canv_width/2, 640, fill='red')


    #cart.apple()



    while True:
        time.sleep(0.025)

        #canv.move(cart, 3, 0)
        #canv.move(pole,0,3)
        canv.update()



    root.geometry('%sx%s+%s+%s' %(canv_width, canv_height, 100, 100))
    root.resizable(0, 0)
    root.mainloop()





if __name__ == "__main__":
    main()
