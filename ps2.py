# 6.00.2x Problem Set 2: Simulating robots

import math
import random

import ps2_visualize
import pylab

##################
## Comment/uncomment the relevant lines, depending on which version of Python you have
##################

# For Python 3.5:
#from ps2_verify_movement35 import testRobotMovement
# If you get a "Bad magic number" ImportError, you are not using Python 3.5 

# For Python 3.6:
# from ps2_verify_movement36 import testRobotMovement
# If you get a "Bad magic number" ImportError, you are not using Python 3.6

# For Python 3.7:
from ps2_verify_movement37 import testRobotMovement
# If you get a "Bad magic number" ImportError, you are not using Python 3.6
##################


# === Provided class Position
class Position(object):
    """
    A Position represents a location in a two-dimensional room.
    """
    def __init__(self, x, y):
        """
        Initializes a position with coordinates (x, y).
        """
        self.x = x
        self.y = y
        
    def getX(self):
        return self.x
    
    def getY(self):
        return self.y
    
    def getNewPosition(self, angle, speed):
        """
        Computes and returns the new Position after a single clock-tick has
        passed, with this object as the current position, and with the
        specified angle and speed.

        Does NOT test whether the returned position fits inside the room.

        angle: number representing angle in degrees, 0 <= angle < 360
        speed: positive float representing speed

        Returns: a Position object representing the new position.
        """
        old_x, old_y = self.getX(), self.getY()
        angle = float(angle)
        # Compute the change in position
        delta_y = speed * math.cos(math.radians(angle))
        delta_x = speed * math.sin(math.radians(angle))
        # Add that to the existing position
        new_x = old_x + delta_x
        new_y = old_y + delta_y
        return Position(new_x, new_y)

    def __str__(self):  
        return "(%0.2f, %0.2f)" % (self.x, self.y)


# === Problem 1
class RectangularRoom(object):
    """
    A RectangularRoom represents a rectangular region containing clean or dirty
    tiles.

    A room has a width and a height and contains (width * height) tiles. At any
    particular time, each of these tiles is either clean or dirty.
    """
    def __init__(self, width, height):
        """
        Initializes a rectangular room with the specified width and height.

        Initially, no tiles in the room have been cleaned.

        width: an integer > 0
        height: an integer > 0
        """
        assert isinstance(width, int), 'Width needs to be integer'
        assert isinstance(height, int), 'Height needs to be integer'
        self.width = width
        self.height = height
        self.cleanTiles = [] # a list of listed coordinate pairs
        
        # for x in self.width:
        #     for y in self.height:
        #         self.cleanTiles[(x,y)] = 0
        
    
    def cleanTileAtPosition(self, pos):
        """
        Mark the tile under the position POS as cleaned.

        Assumes that POS represents a valid position inside this room.

        pos: a Position
        """
        x = math.floor(pos.getX())
        y = math.floor(pos.getY())
        if [x,y] not in self.cleanTiles:
            self.cleanTiles.append([x,y])
        #if self.cleanTiles.get((x,y)) == 0:
        #    self.cleanTiles((x,y)) = 1

    def isTileCleaned(self, m, n):
        """
        Return True if the tile (m, n) has been cleaned.

        Assumes that (m, n) represents a valid tile inside the room.

        m: an integer
        n: an integer
        returns: True if (m, n) is cleaned, False otherwise
        """
        return [m, n] in self.cleanTiles
        #return self.cleanTiles.get((m,n)) == 1 #if switching to dictionary
    
    def getNumTiles(self):
        """
        Return the total number of tiles in the room.

        returns: an integer
        """
        return (self.width * self.height)

    def getNumCleanedTiles(self):
        """
        Return the total number of clean tiles in the room.

        returns: an integer
        """
        return len(self.cleanTiles)
        #return sum(cleanTiles.values())  #if you switch to a dictionary

    def getRandomPosition(self):
        """
        Return a random position inside the room.

        returns: a Position object.
        """
        return Position(random.randint(0, self.width-1),random.randint(0,self.height-1))

    def isPositionInRoom(self, pos):
        """
        Return True if pos is inside the room.

        pos: a Position object.
        returns: True if pos is in the room, False otherwise.
        """
        return (pos.getX() >= 0 and \
                pos.getY() >= 0 and \
                pos.getX() < self.width and \
                pos.getY() < self.height)


# =============================================================================
# ############################
# # Testing Problem #1
# ############################
# random.seed(0)
# 
# room = RectangularRoom(random.randint(0,10), random.randint(0,10))
# print(room.getNumTiles())
# print(room.width,room.height)
# 
# # for x in range(room.width):
# #     for y in range(room.height):
# #         print(room.isTileCleaned(x,y))
#         
# # print(room.getNumCleanedTiles())
# # print(room.cleanTiles)
# # print()
# 
# for x in range(room.width):
#     for x in range(room.width):
#         room.cleanTileAtPosition(Position(x,0))
#         
# # print(room.getNumCleanedTiles())
# # print(room.cleanTiles)
#    
# random.seed(0)
# # pos = room.getRandomPosition()
# # print(pos)
# for x in range(room.width+10):
#     for y in range(room.height+10):
#         pos = room.getRandomPosition()
#         print(pos.getX(),',',pos.getY(),',   ', room.isPositionInRoom(pos))
#         # print(room.isPositionInRoom(Position(x,y)))
# 
# ############################
# # End Testing Problem #1
# ############################
# =============================================================================

# === Problem 2
class Robot(object):
    """
    Represents a robot cleaning a particular room.

    At all times the robot has a particular position and direction in the room.
    The robot also has a fixed speed.

    Subclasses of Robot should provide movement strategies by implementing
    updatePositionAndClean(), which simulates a single time-step.
    """
    def __init__(self, room, speed):
        """
        Initializes a Robot with the given speed in the specified room. The
        robot initially has a random direction and a random position in the
        room. The robot cleans the tile it is on.

        room:  a RectangularRoom object.
        speed: a float (speed > 0)
        """
        self.speed = speed
        self.room = room
        self.pos = room.getRandomPosition()
        self.direction = random.randint(0,359)
        self.room.cleanTileAtPosition(self.pos) #the robot cleans the tile it is on

    def getRobotPosition(self):
        """
        Return the position of the robot.

        returns: a Position object giving the robot's position.
        """
        return self.pos
    
    def getRobotDirection(self):
        """
        Return the direction of the robot.

        returns: an integer d giving the direction of the robot as an angle in
        degrees, 0 <= d < 360.
        """
        return self.direction

    def setRobotPosition(self, position):
        """
        Set the position of the robot to POSITION.

        position: a Position object.
        """
        self.pos = position

    def setRobotDirection(self, direction):
        """
        Set the direction of the robot to DIRECTION.

        direction: integer representing an angle in degrees
        """
        self.direction = direction

    def updatePositionAndClean(self):
        """
        Simulate the passage of a single time-step.

        Move the robot to a new position and mark the tile it is on as having
        been cleaned.
        """
        raise NotImplementedError # don't change this!

# =============================================================================
# ############################
# # Testing Problem #2
# ############################
# random.seed(0)
# 
# room = RectangularRoom(random.randint(0,10), random.randint(0,10))
# ivan = Robot(room,1)
# 
# print(room.width, room.height, room.getNumTiles())
# print(ivan.getRobotPosition())
# print(ivan.getRobotDirection())
# position = room.getRandomPosition()
# ivan.setRobotPosition(position)
# ivan.setRobotDirection(14)
# print(ivan.getRobotPosition())
# print(ivan.getRobotDirection())
# 
# ############################
# # End Testing Problem #2
# ############################
# =============================================================================



# === Problem 3
class StandardRobot(Robot):
    """
    A StandardRobot is a Robot with the standard movement strategy.

    At each time-step, a StandardRobot attempts to move in its current
    direction; when it would hit a wall, it *instead* chooses a new direction
    randomly.
    """
    def updatePositionAndClean(self):
        """
        Simulate the passage of a single time-step.

        Move the robot to a new position and mark the tile it is on as having
        been cleaned.
        """
        newPosition = self.pos.getNewPosition(self.direction,self.speed)
        while not self.room.isPositionInRoom(newPosition):
            self.direction = random.randint(0,359)
            newPosition = self.pos.getNewPosition(self.direction,self.speed)
        self.pos = newPosition
        self.room.cleanTileAtPosition(self.pos)
        

# Uncomment this line to see your implementation of StandardRobot in action!
# testRobotMovement(StandardRobot, RectangularRoom)


# === Problem 4
def runSimulation(num_robots, speed, width, height, min_coverage, num_trials,
                  robot_type):
    """
    Runs NUM_TRIALS trials of the simulation and returns the mean number of
    time-steps needed to clean the fraction MIN_COVERAGE of the room.

    The simulation is run with NUM_ROBOTS robots of type ROBOT_TYPE, each with
    speed SPEED, in a room of dimensions WIDTH x HEIGHT.

    num_robots: an int (num_robots > 0)
    speed: a float (speed > 0)
    width: an int (width > 0)
    height: an int (height > 0)
    min_coverage: a float (0 <= min_coverage <= 1.0)
    num_trials: an int (num_trials > 0)
    robot_type: class of robot to be instantiated (e.g. StandardRobot or
                RandomWalkRobot)
    """
    stepsList = [] #keep track of how many steps each trial takes
    
    #Begin Each Trial    
    for t in range(num_trials):
    
        #Begin Free/Optional Visualization Code
        anim = ps2_visualize.RobotVisualization(num_robots, width, height)
    
    
        #Initialize the Room
        room = RectangularRoom(width, height)
    
        #We have an unknown number of robots. 
        robotList = [] # Robot objects will be stored in the list robotList
        
        #Create "num_robots" quantity of Robots
        for r in range(num_robots):
            robotList = robotList + [robot_type(room,speed)]
        
    
        numSteps = 0 #initialize time steps for this Trial
        while (room.getNumCleanedTiles() / room.getNumTiles()) < min_coverage:
            
            anim.update(room, robotList)
            
            for r in range(num_robots):
                robotList[r].updatePositionAndClean()                
            numSteps += 1    
            
        stepsList = stepsList + [numSteps]
        anim.update(room, robotList)
        anim.done()
    
    return (sum(stepsList)/len(stepsList)) #Avg of # time steps

# End of Function -------------------------


# Uncomment this line to see how much your simulation takes on average
print('1 Standard Robot. 10X10, 75% Clean')
print(runSimulation(1, 1.0, 10, 10, 0.50, 1, StandardRobot))
print()
# print('1 Standard Robot. 10X10, 90% Clean')
# print(runSimulation(1, 1.0, 10, 10, 0.90, 60, StandardRobot))
# print()
# print('1 Standard Robot. 5X5, 100% Clean')
# print(runSimulation(1, 1.0, 5, 5, 0.99, 60, StandardRobot))
# print()
# print('10 Standard Robots. 10X10, 100% Clean')
# print(runSimulation(10, 1.0, 10, 10, 1.00, 60, StandardRobot))


# === Problem 5
class RandomWalkRobot(Robot):
    """
    A RandomWalkRobot is a robot with the "random walk" movement strategy: it
    chooses a new direction at random at the end of each time-step.
    """
    def updatePositionAndClean(self):
        """
        Simulate the passage of a single time-step.

        Move the robot to a new position and mark the tile it is on as having
        been cleaned.
        """
        newPosition = self.pos.getNewPosition(self.direction,self.speed)
        while not self.room.isPositionInRoom(newPosition):
            self.direction = random.randint(0,359)
            newPosition = self.pos.getNewPosition(self.direction,self.speed)
        self.pos = newPosition
        self.room.cleanTileAtPosition(self.pos)
        self.direction = random.randint(0,359)
        
# Uncomment this line to see your implementation of StandardRobot in action!
# testRobotMovement(RandomWalkRobot, RectangularRoom)


def showPlot1(title, x_label, y_label):
    """
    What information does the plot produced by this function tell you?
    """
    num_robot_range = range(1, 11)
    times1 = []
    times2 = []
    for num_robots in num_robot_range:
        print("Plotting", num_robots, "robots...")
        times1.append(runSimulation(num_robots, 1.0, 20, 20, 0.8, 20, StandardRobot))
        times2.append(runSimulation(num_robots, 1.0, 20, 20, 0.8, 20, RandomWalkRobot))
    pylab.plot(num_robot_range, times1)
    pylab.plot(num_robot_range, times2)
    pylab.title(title)
    pylab.legend(('StandardRobot', 'RandomWalkRobot'))
    pylab.xlabel(x_label)
    pylab.ylabel(y_label)
    pylab.show()

   
def showPlot2(title, x_label, y_label):
    """
    What information does the plot produced by this function tell you?
    """
    aspect_ratios = []
    times1 = []
    times2 = []
    for width in [10, 20, 25, 50]:
        height = 300//width
        print("Plotting cleaning time for a room of width:", width, "by height:", height)
        aspect_ratios.append(float(width) / height)
        times1.append(runSimulation(2, 1.0, width, height, 0.8, 200, StandardRobot))
        times2.append(runSimulation(2, 1.0, width, height, 0.8, 200, RandomWalkRobot))
    pylab.plot(aspect_ratios, times1)
    pylab.plot(aspect_ratios, times2)
    pylab.title(title)
    pylab.legend(('StandardRobot', 'RandomWalkRobot'))
    pylab.xlabel(x_label)
    pylab.ylabel(y_label)
    pylab.show()


    

# === Problem 6
# NOTE: If you are running the simulation, you will have to close it 
# before the plot will show up.

#
# 1) Write a function call to showPlot1 that generates an appropriately-labeled
#     plot.
#
# showPlot1('Robot Type vs Time','Number of Robots','Time Steps Needed to Clean 80%')
#

#
# 2) Write a function call to showPlot2 that generates an appropriately-labeled
#     plot.
#
# showPlot2('Time to Clean Varying Sized Rooms','Aspect Ratio','Time Steps Needed to Clean 80%')
