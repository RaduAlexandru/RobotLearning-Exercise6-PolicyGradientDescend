from Tkinter import *
import time
from math import cos, sin, atan2, degrees, radians
import numpy as np

deg_90= -1.57079633

canv_width=600
canv_height=400

cart_width=100
cart_height=70
cart_mass=1.5

pole_length=150
pole_mass=0.5

g=9.81

time_step=0.01

def drawcircle(canv,x,y,rad):
    canv.create_oval(x-rad,y-rad,x+rad,y+rad,width=0,fill='blue')



class cartObj(object):

    def __init__(self,p1_x,p1_y,p2_x,p2_y,speed):
        print "Creating cart"
        self.p1_x=p1_x
        self.p1_y=p1_y
        self.p2_x=p2_x
        self.p2_y=p2_y
        self.speed=speed
        self.acceleration=0.0

        self.mass=cart_mass




    def draw(self,canv):
        self.cart_draw = canv.create_rectangle(self.p1_x, self.p1_y , self.p2_x, self.p2_y, outline='black', fill='gray40', tags=('rect'))

    def move (self,canv,pole,x,y):
        self.p1_x=self.p1_x+x
        self.p1_y=self.p1_y+y
        self.p2_x=self.p2_x+x
        self.p2_y=self.p2_y+y

        #move fixed point of pole
        pole.p1_x=pole.p1_x+x
        pole.p1_y=pole.p1_y+y

        #Move also the other point altough I don't know if its correct
        pole.p2_x=pole.p2_x+x
        pole.p2_y=pole.p2_y+y

    def apply_noise(self):
        #apply noise to position
        position_noise=np.random.normal(0.0, 0.001)
        self.p1_x=self.p1_x+position_noise
        self.p1_y=self.p1_y+position_noise
        self.p2_x=self.p2_x+position_noise
        self.p2_y=self.p2_y+position_noise

        speed_noise=np.random.normal(0.0, 0.001)
        self.speed=self.speed+speed_noise

    def check_border(self):
        if self.p1_x <= 0:
            return True
        if self.p2_x >=canv_width:
            return True

        return False


class poleObj(object):

    def __init__(self,canv,p1_x,p1_y,p2_x,p2_y,angle,angular_velocity):
        print "Creating pole"
        self.p1_x=p1_x
        self.p1_y=p1_y
        self.p2_x=p2_x
        self.p2_y=p2_y
        self.angle=0.0
        self.angle_drawing=deg_90
        self.rotate (canv,angle)

        self.angular_speed=angular_velocity
        self.angular_acc=0.0
        self.length=pole_length
        self.half_length=pole_length/2
        self.mass=pole_mass


    def draw(self,canv):
        self.pole_draw = canv.create_line(self.p1_x, self.p1_y, self.p2_x, self.p2_y, fill='red')

    def move (self,canv,x,y):
        self.p1_x=self.p1_x+x
        self.p1_y=self.p1_y+y
        self.p2_x=self.p2_x+x
        self.p2_y=self.p2_y+y
        #canv.move(self.pole_draw, x, y)




    def rotate (self,canv,theta):
        #print "pole.roate: to angle" +str(theta)
        #self.p2_x=pole_length*cos(theta)
        #self.p2_y=pole_length*sin(theta)
        #self.angle=self.angle+theta

        '''
        #better to calculate everytime the actual angle between the two points
        x1=self.p1_x
        x2=self.p2_x
        y1=self.p1_y
        y2=self.p2_y
        angle = atan2(y1 - y2, x1 - x2)
        angle=angle-deg_90
        print "computed angles is " + str(angle)
        '''

        self.angle_drawing=self.angle_drawing + theta
        self.angle=self.angle+theta
        #print "new angle of the pole is" + str(self.angle)
        #print "new angle:drawing of the pole is" + str(self.angle_drawing)


        #original coordinates
        x_bak=self.p1_x
        y_bak=self.p1_y

        #move to origin
        self.p1_x=self.p1_x-x_bak
        self.p1_y=self.p1_y-y_bak
        self.p2_x=self.p2_x-x_bak
        self.p2_y=self.p2_y-y_bak

        #self.p2_x=self.p2_x*cos(theta) - self.p2_y*sin(theta)
        #self.p2_y=self.p2_y*cos(theta) - self.p2_x*sin(theta)

        self.p2_x=pole_length*cos(self.angle_drawing)
        self.p2_y=pole_length*sin(self.angle_drawing)

        self.p1_x=self.p1_x+x_bak
        self.p1_y=self.p1_y+y_bak
        self.p2_x=self.p2_x+x_bak
        self.p2_y=self.p2_y+y_bak

    def apply_noise(self):
        angle_noise=np.random.normal(0.0, 0.001)
        self.angle=self.angle+angle_noise

        angular_speed_noise=np.random.normal(0.0, 0.001)
        self.angular_speed=self.angle+angular_speed_noise



def simulate_timestep(canv,cart,pole,time_step,F):

    #angle_degrees=degrees(pole.angle)
    #print "pole angle in degrees is" + str(angle_degrees)

    angle_acceleration=(g*sin(pole.angle)*(cart.mass +pole.mass ) - (F+pole.mass*pole.half_length*pole.angle*pole.angle*sin(pole.angle))*cos(pole.angle)    )/ (  (4/3)*pole.half_length*(cart.mass + pole.mass) - pole.mass*pole.half_length*cos(pole.angle)*cos(pole.angle)   )


    cart_acceleration=(F-pole.mass*pole.half_length* (angle_acceleration*cos(pole.angle) - pole.angular_speed*pole.angular_speed*sin(pole.angle) ) )/ (cart.mass + pole.mass)

    cart.acceleration=cart_acceleration
    pole.angular_acc=angle_acceleration

    distance = (cart.speed * time_step) + (cart.acceleration * time_step * time_step) / 2

    #print "distance the we need to move= " + str(distance)

    #cart.move(canv,pole,distance,0)




    angle_increase = (pole.angular_speed * time_step) + (pole.angular_acc * time_step * time_step) / 2

    #
    pole.angular_speed=pole.angular_speed + pole.angular_acc*time_step
    #


    #s = s + u * dt;
    #u = u + a * dt;

    #angle_increase= pole.angular_speed * time_step;
    #pole.angular_speed=pole.angular_speed + pole.angular_acc*time_step



    print "angle acceleration is" + str(angle_acceleration)
    #print "angle we need to increase= " + str(angle_increase)
    #print "pole angular speed= " + str(pole.angular_speed)
    #print "current angle" + str(pole.angle)



    pole.rotate(canv,angle_increase)


def part_6_1():
    root = Tk()
    canv = Canvas(root, width=canv_width, height=canv_height)
    canv.pack(fill='both', expand=True)


    #Create objects
    cart = cartObj(100, canv_height-cart_height, 100+cart_width, canv_height,0.2)
    pole = poleObj(canv,100+cart_width/2, canv_height-cart_height, 100+cart_width/2, canv_height-cart_height-pole_length, 0.2, 0.0) #point 1 x and y, point 2 x and y , angle and angular speed




    #Draw objects
    #middle = canv.create_line(canv_width/2, 0, canv_width/2, 640, fill='red')
    right = canv.create_line(canv_width, 0, canv_width, canv_height, fill='blue')
    left = canv.create_line(0, 0, 0, canv_height, fill='red')

    cart.draw(canv)
    pole.draw(canv)

    #cart_draw = canv.create_rectangle(cart.p1_x, cart.p1_y , cart.p2_x, cart.p2_y, outline='black', fill='gray40', tags=('rect'))
    #pole_draw = canv.create_line(pole.p1_x, pole.p1_y, pole.p2_x, pole.p2_y, fill='red')



    #cart.apple()



    while True:

        time.sleep(time_step)
        #time.sleep(0.01)

        canv.delete("all")

        #Move and rotate
        #cart.move(canv,pole,3,0)
        #pole.rotate(canv,0.1)
        simulate_timestep(canv,cart,pole,time_step,0.0)

        #draw
        circ1=drawcircle(canv,100+cart_width/2,canv_height-cart_height,pole_length)
        cart.draw(canv)
        pole.draw(canv)
        right = canv.create_line(canv_width, 0, canv_width, canv_height, fill='blue')
        left = canv.create_line(0, 0, 0, canv_height, fill='red')


        #noise
        #cart.apply_noise()
        #pole.apply_noise()

        #check boundaries
        hit=cart.check_border()
        if hit:
            break

        canv.update()



    root.geometry('%sx%s+%s+%s' %(canv_width, canv_height, 100, 100))
    root.resizable(0, 0)
    root.mainloop()


'''
def part_6_2():

    root = Tk()
    canv = Canvas(root, width=canv_width, height=canv_height)
    canv.pack(fill='both', expand=True)

    #Create objects
    #cart = cartObj(canv_width/2-cart_width/2, canv_height-cart_height, canv_width/2+cart_width/2, canv_height) #top_left corner x and y, right bottom point x and y
    pole = poleObj(canv_width/2, canv_height-cart_height, canv_width/2, canv_height-cart_height-pole_length) #point 1 x and y, point 2 x and y

    #Draw objects
    #middle = canv.create_line(canv_width/2, 0, canv_width/2, 640, fill='red')
    right = canv.create_line(canv_width, 0, canv_width, canv_height, fill='blue')
    left = canv.create_line(0, 0, 0, canv_height, fill='red')

    cart.draw(canv)
    pole.draw(canv)

    #cart_draw = canv.create_rectangle(cart.p1_x, cart.p1_y , cart.p2_x, cart.p2_y, outline='black', fill='gray40', tags=('rect'))
    #pole_draw = canv.create_line(pole.p1_x, pole.p1_y, pole.p2_x, pole.p2_y, fill='red')



    #cart.apple()



    while True:
        time.sleep(0.01)

        canv.delete("all")

        #Move and rotate
        cart.move(canv,pole,3,0)
        pole.rotate(canv,0.1)

        #draw
        cart.draw(canv)
        pole.draw(canv)
        right = canv.create_line(canv_width, 0, canv_width, canv_height, fill='blue')
        left = canv.create_line(0, 0, 0, canv_height, fill='red')


        #noise
        cart.apply_noise()
        pole.apply_noise()

        #check boundaries
        hit=cart.check_border()
        if hit:
            break

        canv.update()



    root.geometry('%sx%s+%s+%s' %(canv_width, canv_height, 100, 100))
    root.resizable(0, 0)
    root.mainloop()
'''


if __name__ == "__main__":
    part_6_1()
    #main()
