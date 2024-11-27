#Kyrylo Krocha, OM-4

#Modules
import numpy as np
import matplotlib
import scipy
import math
import time
import Drawer
import pylab


#Some parametres
num_of_searchers = 1
num_of_food = 40
time_limit = 30 #limit on the time of simulation
vision = 5 #radius of vision of searchers
tau = 0.5  #number for determining wait time
move_speed = 1
width = [-50., 50.]
height = [-50., 50.]
start_x = 0.0
start_y = 0.0
mu = 1.4
x_m = 1 # scale for Lévy flight
levy_walk = 1 # 1 - levy walk, else brownian motion
if not levy_walk:
    sigma = 50.0
classic_model = 1 # 1 - classic model, else chamged model


#init of Drawer
def init():
    global steps, searchers, list_of_x_dest, list_of_y_dest, start_time, food
    start_time = time.time()
    list_of_x_dest = []
    list_of_y_dest = []
    steps = 0
    searchers = []


    food = []
    for k in range(num_of_food):  # - uniform distribution
        #Structure of food:
        #   1.X
        #   2.Y
        #   3.Energy value of food
        #
        new_food = [np.random.uniform(width[0],width[1]), np.random.uniform(height[0],height[1]),1]
        food.append(new_food)

    #for k in range(12):                         # - surface distribution
    #    new_food = [np.random.uniform(-25, 25), np.random.uniform(-25, 25), 1]
    #    food.append(new_food)
    #for j in range(8):
    #    ch = np.random.uniform(0,100)
    #    if ch <= 25:
    #        new_food = [np.random.uniform(-25, 25), np.random.uniform(25, 50), 1]
    #    elif ch > 25 and ch <=50:
    #        new_food = [np.random.uniform(25, 50), np.random.uniform(-50, 50), 1]
    #    elif ch > 50 and ch <= 75:
    #        new_food = [np.random.uniform(-25, 25), np.random.uniform(-25, -50), 1]
    #    elif ch > 75:
    #        new_food = [np.random.uniform(-25, -50), np.random.uniform(-50, 50), 1]
    #    food.append(new_food)





    for i in range(num_of_searchers):
        init_x = start_x
        init_y = start_y

        #Structure of searcher:
        #   0.present x
        #   1.present y
        #   2.destination x
        #   3.destination y
        #   4.angle
        #   5.state(str)
        #   6.has reached destination(0 or 1)
        #   7.time of waiting
        #   8.at what time it stopped
        #   9.How much it ate
        #

        new_searcher = [init_x, init_y, 0.0, 0.0, 0.0, "stop", 0, 0.0, 0.0, 0.0]
        searchers.append(new_searcher)
        list_of_x_dest.append([start_x])
        list_of_y_dest.append([start_y])




def draw():
    global steps, searchers, food
    pylab.cla()
    x_dest = []
    y_dest = []
    x_current = []
    y_current = []
    x_visited = []
    y_visited = []
    x_food = []
    y_food = []
    counter = 0


    for f in food:
        x_food.append(f[0])
        y_food.append(f[1])
        pylab.scatter(x_food,y_food,color = 'violet')



    for s in searchers:
        x_dest.append(s[2])
        y_dest.append(s[3])
        if steps > 0:
            pylab.plot([s[0],s[2]],[s[1],s[3]],'g-')
            pylab.plot(list_of_x_dest[counter],list_of_y_dest[counter], color='gray', linestyle=':')
        if s[6]:
            x_visited.append(s[0])
            y_visited.append(s[1])
            s[6] = 0
        else:
            x_current.append(s[0])
            y_current.append(s[1])
        counter += 1
        pylab.plot(start_x,start_y, 'ro', label="Home", markersize=9)
        pylab.plot(x_dest, y_dest, 'k.')
        pylab.plot(x_visited, y_visited, 'ro')
        pylab.plot(x_current, y_current, 'go')



        #circle_of_visibility = pylab.Circle((x_current, y_current), radius=vision, fill=False)
        #pylab.gca().add_artist(circle_of_visibility)

        pylab.axis('scaled')
        pylab.axis([width[0], width[1], height[0], height[1]])
        pylab.title('Крок: ' + str(steps))


def clip(dest_x, dest_y, angle, width_min, width_max, height_min, height_max):
  if dest_x < width_min:
    dest_y += (width_min-dest_x)*math.tan(angle)
    dest_x = width_min
  elif dest_x > width_max:
    dest_y -= (dest_x-width_max)*math.tan(angle)
    dest_x = width_max

  if angle == math.pi/2.0 and dest_y >= height_max:
    dest_y = height_max
  elif angle == -math.pi/2.0 and dest_y <= height_min:
    dest_y = height_min
  else:
    if dest_y < height_min:
      dest_x += (height_min-dest_y)/math.tan(angle)
      dest_y = height_min
    elif dest_y > height_max:
      dest_x -= (dest_y-height_max)/math.tan(angle)
      dest_y = height_max
  return dest_x, dest_y


def step():
    global steps, searchers, food

    steps += 1
    counter = 0
    for s in searchers:
        if s[5] == "stop":
            #Choose next destination
            if (levy_walk):
                s[4] = np.random.uniform(-math.pi, math.pi)
                distance = scipy.stats.pareto.rvs(mu,scale=x_m)       #np.random.pareto(mu)
            else:
                b1 = np.random.normal(0.0, sigma)
                b2 = np.random.normal(0.0, sigma)
                distance = math.sqrt((b1-s[0])**2 + (b2-s[1])**2)
                if distance:
                    co = (b1 - s[0]) / distance
                    si = (b2 - s[1]) / distance
                    s[4] = math.atan2(si,co)

            #look for food
            for f in food:
                if (f[0] - s[0]) ** 2 + (f[1] - s[1]) ** 2 <= vision * vision and (f[0] - s[0]) ** 2 + (f[1] - s[1]) ** 2 >= move_speed * move_speed:
                    distance = math.sqrt((f[0] - s[0]) ** 2 + (f[1] - s[1]) ** 2)
                    if distance:
                        co1 = (f[0] - s[0]) / distance
                        si1 = (f[1] - s[1]) / distance
                        s[4] = math.atan2(si1, co1)
                else:
                    s[5] = 'move'

            s[2] = s[0] + distance * math.cos(s[4])
            s[3] = s[1] + distance * math.sin(s[4])
            s[2], s[3] = clip(s[2], s[3], s[4], width[0], width[1], height[0], height[1])
            list_of_x_dest[counter].append(s[2])
            list_of_y_dest[counter].append(s[3])
            s[5] = 'move'
        elif s[5] == 'move':
            if (s[3] - s[1]) * (s[3] - s[1]) + (s[2] - s[0]) * (s[2] - s[0]) > move_speed * move_speed:

                #find and eat the food
                for f in food:
                    if (f[0] - s[0]) ** 2 + (f[1] - s[1]) ** 2 <= vision * vision and (f[0] - s[0]) ** 2 + (f[1] - s[1]) ** 2 >= move_speed * move_speed:
                        list_of_x_dest[counter][max(0,len(list_of_x_dest[counter])-1)] = s[0]
                        list_of_y_dest[counter][max(0,len(list_of_y_dest[counter])-1)] = s[1]
                        s[5] = 'stop'
                    elif (f[0] - s[0]) ** 2 + (f[1] - s[1]) ** 2 < move_speed * move_speed:
                        s[0] = f[0]
                        s[1] = f[1]
                        s[9] += f[2]
                        food.remove(f)

                # make one step
                s[0] += move_speed * math.cos(s[4])
                s[1] += move_speed * math.sin(s[4])
            else:
                s[0] = s[2]
                s[1] = s[3]
                s[7] = np.random.exponential(tau)  # time of stay
                s[8] = time.time()
                s[5] = 'stay'
        elif s[5] == 'stay':
            if abs(s[8] - time.time()) >= s[7]:
                s[5] = 'stop'
        counter += 1


def classic_step():
    global steps, searchers, food

    steps += 1
    counter = 0
    for s in searchers:
        if s[5] == "stop":
            #Choose next destination
            if (levy_walk):
                s[4] = np.random.uniform(-math.pi, math.pi)
                distance = scipy.stats.pareto.rvs(mu,scale=x_m)       #scipy.stats.pareto.rvs(mu,scale=x_m)       #np.random.pareto(mu)
                if distance > 1000:
                    distance = 1000
            else:
                b1 = np.random.normal(0.0, sigma)
                b2 = np.random.normal(0.0, sigma)
                distance = math.sqrt((b1-s[0])**2 + (b2-s[1])**2)
                if distance:
                    co = (b1 - s[0]) / distance
                    si = (b2 - s[1]) / distance
                    s[4] = math.atan2(si,co)

            #look for food
            flag = False #food found

            for f in food:
                if flag:
                    pass
                else:
                    if (f[0] - s[0]) ** 2 + (f[1] - s[1]) ** 2 <= vision * vision and not(flag):
                        distance = math.sqrt((f[0] - s[0]) ** 2 + (f[1] - s[1]) ** 2)
                        if distance:
                            co1 = (f[0] - s[0]) / distance
                            si1 = (f[1] - s[1]) / distance
                            s[4] = math.atan2(si1, co1)
                        flag = True
            if not (flag):
                i = 0
                while i <= distance and not (flag):
                    for f in food:
                        if (s[0] + i * math.cos(s[4]) - f[0]) ** 2 + (s[1] + i * math.sin(s[4]) - f[1]) ** 2 <= vision * vision:
                                distance = i
                                flag = True
                    i += vision/2

            s[2] = s[0] + distance * math.cos(s[4])
            s[3] = s[1] + distance * math.sin(s[4])
            s[2], s[3] = clip(s[2], s[3], s[4], width[0], width[1], height[0], height[1])
            list_of_x_dest[counter].append(s[2])
            list_of_y_dest[counter].append(s[3])
            s[5] = 'move'
        elif s[5] == 'move':
            eated = False
            for f in food:
                if s[0] == f[0] and s[1] == f[1]:
                    s[9] += f[2]
                    eated = True
                    food.remove(f)
            if not(eated):
                s[0] = s[2]
                s[1] = s[3]
            s[7] = np.random.exponential(tau)  # time of stay
            s[8] = time.time()
            s[5] = 'stay'
        elif s[5] == 'stay':
            if abs(s[8] - time.time()) >= s[7]:
                s[5] = 'stop'
        counter += 1




#Start
if classic_model==1:
    Drawer.UI(time_limit=time_limit).start(func=[init,draw,classic_step])
else:
    Drawer.UI(time_limit=time_limit).start(func=[init,draw,step])

#Summary
global searchers,steps, list_of_x_dest,list_of_y_dest
print("Summary of simulation: ")

print("Total steps: "+str(steps))
print()
for i in range(num_of_searchers):
    print("Searcher number "+str(i+1))
    print("Energy consumed: "+str(searchers[i][9]))
    total_distance = 0.0
    for k in range(len(list_of_x_dest[i])-1):
        if k==0:
            total_distance += math.sqrt(list_of_x_dest[i][k]**2+list_of_y_dest[i][k]**2)
        else:
            total_distance += math.sqrt((list_of_x_dest[i][k]-list_of_x_dest[i][k-1]) ** 2 + (list_of_y_dest[i][k]-list_of_y_dest[i][k-1]) ** 2)
    print("Distance traveled: "+str(total_distance))
    print()

