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
N=1000

def drawcircle(canv,x,y,rad):
    canv.create_oval(x-rad,y-rad,x+rad,y+rad,width=0,fill='blue')



class cartObj(object):

    def __init__(self,p1_x,p1_y,p2_x,p2_y,speed):
        #print "Creating cart"
        self.p1_x=p1_x
        self.p1_y=p1_y
        self.p2_x=p2_x
        self.p2_y=p2_y
        self.speed=speed
        self.acceleration=0.0

        self.mass=cart_mass

    def position(self):
        pos = (self.p2_x+self.p1_x)/2 -canv_width/2
        #pos=pos/100

        return pos



    def draw(self,canv):
        self.cart_draw = canv.create_rectangle(self.p1_x, self.p1_y , self.p2_x, self.p2_y, outline='black', fill='gray40', tags=('rect'))

    def move (self,pole,x,y):
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

    def __init__(self,p1_x,p1_y,p2_x,p2_y,angle,angular_velocity):
        #print "Creating pole"
        self.p1_x=p1_x
        self.p1_y=p1_y
        self.p2_x=p2_x
        self.p2_y=p2_y
        self.angle=0.0
        self.angle_drawing=deg_90
        self.rotate (angle)

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




    def rotate (self,theta):
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



def simulate_timestep(cart,pole,time_step,F):

    #angle_degrees=degrees(pole.angle)
    #print "pole angle in degrees is" + str(angle_degrees)

    angle_acceleration=(g*sin(pole.angle)*(cart.mass +pole.mass ) - (F+pole.mass*pole.half_length*pole.angle*pole.angle*sin(pole.angle))*cos(pole.angle)    )/ (  (4/3)*pole.half_length*(cart.mass + pole.mass) - pole.mass*pole.half_length*cos(pole.angle)*cos(pole.angle)   )

    cart_acceleration=(F-pole.mass*pole.half_length* (angle_acceleration*cos(pole.angle) - pole.angular_speed*pole.angular_speed*sin(pole.angle) ) )/ (cart.mass + pole.mass)

    #cart Stuff
    cart.acceleration=cart_acceleration
    cart.speed=cart.speed + cart.acceleration*time_step
    distance = (cart.speed * time_step) #+ (cart.acceleration * time_step * time_step) / 2
    cart.move(pole,distance,0)



    #Pole stuff
    pole.angular_acc=angle_acceleration
    pole.angular_speed=pole.angular_speed + pole.angular_acc*time_step
    angle_increase = (pole.angular_speed * time_step) #+ (pole.angular_acc * time_step * time_step) / 2
    pole.rotate(angle_increase)


    #s = s + u * dt;
    #u = u + a * dt;

    #angle_increase= pole.angular_speed * time_step;
    #pole.angular_speed=pole.angular_speed + pole.angular_acc*time_step



    #print "angle acceleration is" + str(angle_acceleration)
    #print "angle we need to increase= " + str(angle_increase)
    #print "pole angular speed= " + str(pole.angular_speed)
    #print "current angle" + str(pole.angle)


def F_func(cart,pole,k1,k2,k3,k4):

    position=cart.position()
    velocity=cart.speed
    angle=pole.angle
    angular_velocity=pole.angular_speed

    inner= max(-30,k1*position + k2*velocity + k3*angle + k4*angular_velocity )
    #print "inner is "  + str (k1*position + k2*velocity + k3*angle + k4*angular_velocity)

    F=min (30, inner)

    #print "F=" +str(F)

    return F



def part_6_1():
    root = Tk()
    canv = Canvas(root, width=canv_width, height=canv_height)
    canv.pack(fill='both', expand=True)


    #Create objects
    cart = cartObj(100, canv_height-cart_height, 100+cart_width, canv_height,0.2)
    pole = poleObj(100+cart_width/2, canv_height-cart_height, 100+cart_width/2, canv_height-cart_height-pole_length, 0.2, -0.5) #point 1 x and y, point 2 x and y , angle and angular speed




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
        #cart.move(pole,3,0)
        #pole.rotate(0.1)
        simulate_timestep(cart,pole,time_step,0.0)

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



def brute_force():
    #k1=1
    #k2=-1.0
    #k3=5.0
    #k4=4.0
    #step_size=0.75

    k1_best=0.0
    k2_best=0.0
    k3_best=0.0
    k4_best=0.0
    step_size=1

    highest_reward=-999999

    #-1276 -7 2 -10 7

    #-1273 -8.0 1.9 -11.0 7.8

    #-1265 6.0 1.0 -1.0 14.0


    for i in [float(j)/10 for j in range(-10, 10, 1)]:
        print i

    #return

    for k1 in [float(u)/1 for u in range(-15, 15, 1)]:
        for k2 in [float(p)/1 for p in range(-15, 15, 1)]:
            for k3 in [float(j)/1 for j in range(-15, 15, 1)]:
                for k4 in [float(k)/1 for k in range(-15, 15, 1)]:
                    reward_episode=episode(k1,k2,k3,k4)
                    print "reward is " + str(reward_episode) + " " + str(k1) + " " + str(k2) + " " + str(k3) + " " + str(k4)

                    if reward_episode > highest_reward:
                        print "updating the best"
                        highest_reward=reward_episode
                        k1_best=k1
                        k2_best=k2
                        k3_best=k3
                        k4_best=k4


    print "finished"
    reward_episode=run_6_2_episode(k1_best,k2_best,k3_best,k4_best)
    print "reward is " + str(reward_episode) + " " + str(k1_best) + " " + str(k2_best) + " " + str(k3_best) + " " + str(k4_best)

def part_6_2():

    #-718 doing normal on each step
    #k1=-0.3
    #k2=-1.0
    #k3=-1.0
    #k4=-1.0
    #step_size=0.5

    #-716 doing normal on each step
    #k1=0.3
    #k2=-1.0
    #k3=-1.0
    #k4=-1.0
    #step_size=0.75

    #-716 doing normal only once
    #k1=0.3
    #k2=-1.0
    #k3=-1.0
    #k4=-1.0
    #step_size=0.75

    #-718 doing normal only once
    #k1=0.3
    #k2=0.5
    #k3=4.0
    #k4=1.0
    #step_size=0.25



    #All of these are with the bug of the position being in pixels and not in meters

    #converges prtty ok, probably the one that I will submit
    #k1=0.3
    #k2=-1.0
    #k3=5.0
    #k4=-2.0
    #step_size=0.75

    #1108
    #k1=-1.3
    #k2=4.0
    #k3=7.0
    #k4=5.0
    #step_size=0.75

    #1104
    #k1=-1.3
    #k2=4.0
    #k3=-1.0
    #k4=5.0
    #step_size=0.75

    #1100
    #k1=-1.3
    #k2=4.0
    #k3=-7.0
    #k4=5.0
    #step_size=0.75

    #1098
    #k1=-1.3
    #k2=4.0
    #k3=-15.0
    #k4=5.0
    #step_size=0.75

    k1=-1.3
    k2=4.0
    k3=-16.0
    k4=5.0
    step_size=0.75

    #Here I stop the ones that have the position bug

    '''
    #One given to me
    k1=30
    k2=19
    k3=+300.0
    k4=30.0
    step_size=0.75

    #use now with the correct positon

    k1=1
    k2=-1.0
    k3=5.0
    k4=4.0
    step_size=0.75


    k1=13
    k2=19.0
    k3=300.0
    k4=30.0
    step_size=0.7
    '''


    reward_episode_initial=run_6_2_episode(k1,k2,k3,k4)
    print "episode had reward" + str(reward_episode_initial)

    #run episode with plus and minus step_size of k_x
    # see which one has the bigges reward, that is the new k

    iter =0

    while iter < 100:
        k1_new=k1
        k2_new=k2
        k3_new=k3
        k4_new=k4

        slope_k1_plus=0.0
        slope_k1_minus=0.0
        slope_k2_plus=0.0
        slope_k2_minus=0.0
        slope_k3_plus=0.0
        slope_k3_minus=0.0
        slope_k4_plus=0.0
        slope_k4_minus=0.0


        reward_episode_initial=run_6_2_episode(k1,k2,k3,k4)
        #K1
        k1_minus=k1-step_size
        k1_plus=k1+step_size
        reward_episode_minus=episode(k1_minus,k2,k3,k4)
        reward_episode_plus=episode(k1_plus,k2,k3,k4)
        reward_episode_normal=episode(k1,k2,k3,k4)


        slope_k1_plus=(reward_episode_plus- reward_episode_initial)/step_size
        slope_k1_minus=(reward_episode_minus- reward_episode_initial)/step_size

        #print "rewardplus is ",reward_episode_plus, "reward episode minus is ", reward_episode_minus, "normal is " ,reward_episode_initial, "slope plus is ",slope_k1_plus, "slope minus is ", slope_k1_minus

        '''
        if (reward_episode_plus- reward_episode_initial)/step_size > 0:
            k1_new=k1_plus
        if (reward_episode_minus- reward_episode_initial)/step_size > 0:
            k1_new=k1_minus
        '''

        '''
        if reward_episode_minus > reward_episode_normal:
            k1=k1_minus
        if reward_episode_plus > reward_episode_normal:
            k1=k1_plus
        '''

        #K2
        k2_minus=k2-step_size
        k2_plus=k2+step_size
        reward_episode_minus=episode(k1,k2_minus,k3,k4)
        reward_episode_plus=episode(k1,k2_plus,k3,k4)
        #reward_episode_normal=run_6_2_episode(k1,k2,k3,k4)

        slope_k2_plus=(reward_episode_plus- reward_episode_initial)/step_size
        slope_k2_minus=(reward_episode_minus- reward_episode_initial)/step_size

        '''
        if (reward_episode_plus- reward_episode_initial)/step_size > 0:
            k2_new=k2_plus
        if (reward_episode_minus- reward_episode_initial)/step_size > 0:
            k2_new=k2_minus
        '''

        '''
        if reward_episode_minus > reward_episode_normal:
            k2=k2_minus
        if reward_episode_plus > reward_episode_normal:
            k2=k2_plus
        '''

        #K3
        k3_minus=k3-step_size
        k3_plus=k3+step_size
        reward_episode_minus=episode(k1,k2,k3_minus,k4)
        reward_episode_plus=episode(k1,k2,k3_plus,k4)
        #reward_episode_normal=run_6_2_episode(k1,k2,k3,k4)

        slope_k3_plus=(reward_episode_plus- reward_episode_initial)/step_size
        slope_k3_minus=(reward_episode_minus- reward_episode_initial)/step_size

        '''
        if (reward_episode_plus- reward_episode_initial)/step_size > 0:
            k3_new=k3_plus
        if (reward_episode_minus- reward_episode_initial)/step_size > 0:
            k3_new=k3_minus
        '''

        '''
        if reward_episode_minus > reward_episode_normal:
            k3=k3_minus
        if reward_episode_plus > reward_episode_normal:
            k3=k3_plus
        '''

        #K4
        k4_minus=k4-step_size
        k4_plus=k4+step_size
        reward_episode_minus=episode(k1,k2,k3,k4_minus)
        reward_episode_plus=episode(k1,k2,k3,k4_plus)
        #reward_episode_normal=run_6_2_episode(k1,k2,k3,k4)

        slope_k4_plus=(reward_episode_plus- reward_episode_initial)/step_size
        slope_k4_minus=(reward_episode_minus- reward_episode_initial)/step_size

        '''
        if (reward_episode_plus- reward_episode_initial)/step_size > 0:
            k4_new=k4_plus
        if (reward_episode_minus- reward_episode_initial)/step_size > 0:
            k4_new=k4_minus
        '''

        '''
        if reward_episode_minus > reward_episode_normal:
            k4=k4_minus
        if reward_episode_plus > reward_episode_normal:
            k4=k4_plus
        '''


        '''
        k1=k1_new
        k2=k2_new
        k3=k3_new
        k4=k4_new
        '''


        ##new way of doing it by only choosing the highes slope and updating that one
        x = np.array([slope_k1_plus,slope_k1_minus,slope_k2_plus,slope_k2_minus,slope_k3_plus,slope_k3_minus,slope_k4_plus,slope_k4_minus])
        if np.all(x==0):
            #no more slope, we Converged
            print "CONVERGENCE: reward is " + str(reward_episode_normal) + " " + str(k1) + " " + str(k2) + " " + str(k3) + " " + str(k4)
            break;

        maximum= x.tolist().index(max(x))
        #print maximum


        if maximum==0:
            k1=k1+step_size
        if maximum==1:
            k1=k1-step_size
        if maximum==2:
            k2=k2+step_size
        if maximum==3:
            k2=k2-step_size
        if maximum==4:
            k3=k3+step_size
        if maximum==5:
            k3=k3-step_size
        if maximum==6:
            k4=k4+step_size
        if maximum==7:
            k4=k4-step_size



        iter = iter+1
        reward_episode_normal=episode(k1,k2,k3,k4)
        print "reward is " + str(reward_episode_normal) + " " + str(k1) + " " + str(k2) + " " + str(k3) + " " + str(k4)
    reward_episode_normal=run_6_2_episode(k1,k2,k3,k4)



def run_6_2_episode(k1,k2,k3,k4):

    #reward= episode (k1,k2,k3,k4)
    #return reward

    root = Tk()
    canv = Canvas(root, width=canv_width, height=canv_height)
    canv.pack(fill='both', expand=True)


    #Create objects
    cart = cartObj(250, canv_height-cart_height, 250+cart_width, canv_height,0.2)
    pole = poleObj(250+cart_width/2, canv_height-cart_height, 250+cart_width/2, canv_height-cart_height-pole_length, 0.2, -0.5) #point 1 x and y, point 2 x and y , angle and angular speed

    #Draw objects
    #middle = canv.create_line(canv_width/2, 0, canv_width/2, 640, fill='red')
    right = canv.create_line(canv_width, 0, canv_width, canv_height, fill='blue')
    left = canv.create_line(0, 0, 0, canv_height, fill='red')

    cart.draw(canv)
    pole.draw(canv)

    iters=0
    total_reward=0

    while iters < 1000:

        #time.sleep(time_step)

        canv.delete("all")

        #Move and rotate
        #cart.move(pole,3,0)
        #pole.rotate(0.1)
        F=F_func(cart,pole,k1,k2,k3,k4)
        simulate_timestep(cart,pole,time_step,F)

        #draw
        #circ1=drawcircle(canv,100+cart_width/2,canv_height-cart_height,pole_length)
        cart.draw(canv)
        pole.draw(canv)
        right = canv.create_line(canv_width, 0, canv_width, canv_height, fill='blue')
        left = canv.create_line(0, 0, 0, canv_height, fill='red')


        #noise
        #cart.apply_noise()
        #pole.apply_noise()


        #give rewards
        if pole.angle > -0.1 and pole.angle < 0.1 and cart.position() > -0.1 and cart.position() < 0.1:
            total_reward = total_reward +0
        else:
            total_reward = total_reward -1

        #check boundaries and critical angle
        hit=cart.check_border()
        if hit or abs(pole.angle) >0.8:
            total_reward=total_reward+ (-2* (N-iters) )
            root.destroy()
            return total_reward



        canv.update()
        iters=iters+1



    total_reward=total_reward+ (-2* (N-iters) )
    root.destroy()
    return total_reward


    #root.geometry('%sx%s+%s+%s' %(canv_width, canv_height, 100, 100))
    #root.resizable(0, 0)
    #root.mainloop()



def episode(k1,k2,k3,k4):
    cart = cartObj(250, canv_height-cart_height, 250+cart_width, canv_height,0.2)
    pole = poleObj(250+cart_width/2, canv_height-cart_height, 250+cart_width/2, canv_height-cart_height-pole_length, 0.2, -0.4) #point 1 x and y, point 2 x and y , angle and

    iters=0
    total_reward=0

    while iters < 1000:
        F=F_func(cart,pole,k1,k2,k3,k4)
        simulate_timestep(cart,pole,time_step,F)

        #give rewards
        if pole.angle > -0.1 and pole.angle < 0.1 and cart.position() > -0.1 and cart.position() < 0.1:
            total_reward = total_reward +0
        else:
            total_reward = total_reward -1


        #check boundaries and critical angle
        hit=cart.check_border()
        if hit or abs(pole.angle) >0.8:
            total_reward=total_reward+ (-2* (N-iters) )
            return total_reward

        iters=iters+1

    total_reward=total_reward+ (-2* (N-iters) )
    return total_reward


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
        cart.move(pole,3,0)
        pole.rotate(0.1)

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
    #part_6_1()
    part_6_2()
    #brute_force()
    #main()
