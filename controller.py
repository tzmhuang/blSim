import rospy
from std_msgs.msg import String
from std_msgs.msg import Float32MultiArray 

def talker():
	print('a')
	pub = rospy.Publisher('chatter',Float32MultiArray, queue_size = 10)
	rospy.init_node('talker', anonymous = False)
	rate = rospy.Rate(16) 
	x=0
	y=0
	z=0
	zr = 0
	while not rospy.is_shutdown():
		#hello_str = 'hello world %s' % rospy.get_time()
		x = x+0.0
		zr = zr+0.1
		coord = Float32MultiArray(data = [x,0,0,0,0,zr])
		rospy.loginfo(coord)
		pub.publish(coord)
		rate.sleep()


try:
	talker()
except rospy.ROSInterruptException:
	pass


