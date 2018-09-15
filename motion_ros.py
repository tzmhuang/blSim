import bpy
import rospy
from std_msgs.msg import String
from std_msgs.msg import Float32MultiArray

# class moving_mesh(object):
# 	def __init__(self,loc = (0,0,0)):
# 		self.loc = loc
# 		self.mesh = None
	
# 	def spawn(self,spawn_location):
# 		self.loc = spawn_location
# 		bpy.ops.mesh.primitive_cube_add(location = self.loc)
# 		self.mesh = bpy.data.objects.get('Cube')

# 	def coord_mv(self,coord,angle_xyz):
# 		self.mesh.location = coord
# 		self.mesh.rotation_euler = angle_xyz


# 	def callback(self,data):
# 		rospy.loginfo(data.data)
# 		self.coord_mv(data.data,data.data)
# 		return

# 	def listener(self):
# 		rospy.init_node('listener', anonymous = True)
# 		rospy.Subscriber('chatter',Float32MultiArray,self.callback)
# 		rospy.spin()


# origin = (0,0,0)
# cube = moving_mesh()
# cube.spawn(origin)

# x = 0
# while x<5:
# 	x = x+0.1
# 	print(x)
# 	#cube.coord_mv((x,0,0),(0,0,0))

# #cube.listener()
c = bpy.data.objects.get('Cube')
print(c.location)

def callback(data):
	c.location = data.data[0:3]
	c.rotation_euler = data.data[3:6]
   #rospy.loginfo(data.data)
	#self.coord_mv(data.data,data.data)
   #sub_once.unregister()

rospy.init_node('listener', anonymous = True)
rospy.Subscriber('chatter',Float32MultiArray,callback)
rospy.wait_for_message('chatter',Float32MultiArray,5)


# global sub_once


#def listener():

#rospy.Subscriber('talker',Float32MultiArray,callback)
#rospy.spin()

#listener()
#print (msg)
