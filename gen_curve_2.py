'''logic error: curve drawing, centre calc''' 

import bpy
import numpy as np
#import pandas as pd
import csv
from math import floor, pi, cos, sin

def seg_gen(data):
    n = len(data)
    c = bpy.data.curves.new(name = 'gen_segment',type = 'CURVE')
    c.dimensions = '3D'
    spl = c.splines.new('NURBS')
    spl.points.add(n-1)
    pts = spl.points
    for i, e in enumerate(data):
    	x,y,z = e
    	pts[i].co = (x,y,z,1)
    return c

def seg_link(seg_obj):
	scn = bpy.context.scene
	scn.objects.link(seg_obj)
	return True

def h_bound(crnt,add):
	h = crnt + add
	sign = int(h<0)
	h = h - floor(h/360)*360
	return h

def r_mat(ang,anti_clockwise):
	rad = ang*pi/180
	sign = 2*int(anti_clockwise)-1
	return np.array([[cos(rad),sin(rad)*sign],[-sin(rad)*sign,cos(rad)]]) #counter_clockwise

def centre(pt,d,crv,deg):
	pt = np.array(pt).reshape(1,2)
	d = d*pi/180
	d_pt = np.array((cos(d),sin(d))).reshape(1,2)
	direction = int(deg<0) #right is clockwise
	r_pt = np.matmul(d_pt,r_mat(90,direction))
	t_r_pt = r_pt/np.sqrt((np.dot(r_pt,r_pt.transpose())))/crv
	c = t_r_pt + pt
	print(pt,c,crv,d,d_pt)
	return c

def data_cvrt(array):
	#['line',length,r_direction(deg),*start_x, *start_y]
	#['curve', curvature, deg, *start_-x, *start_y]
	data = np.empty((0,4)) #[station, x,y,z]
	nrow, ncol = array.shape
	g_h = 0
	res = 1	#per meter/deg
	station = 0
	startPt = (0,0)
	for i, seg in enumerate(array):
		if seg[0] == 'line':
			l,direction = seg[1:3]
			x,y = startPt
			direction = -direction #right is positive
			g_h = h_bound(g_h,direction)
			n_pt = int(l*res)
			rad = direction*pi/180
			data = np.concatenate((data,np.array([[station,x,y,0]])),0)
			for n in range(1,int(n_pt)):
				temp = [station+n*l/(n_pt),x+n*l/n_pt*cos(rad),y+n*l/n_pt*sin(rad),0]
				temp = np.array(temp).reshape(1,4)
				data = np.concatenate((data,temp),0)
			station = station+l
			startPt = data[-1][1:3]
		elif seg[0] == 'curve': 
			c,deg = seg[1:3]
			x,y = startPt
			n_pt = int(abs(deg)*res)
			c_l = deg/360*2*pi/c
			ctr = centre((x,y),g_h,c,deg)
			data = np.concatenate((data,np.array([[station,x,y,0]])),0)
			ori_pt = np.array((cos(g_h*pi/180),sin(g_h*pi/180))).reshape(1,2)
			print('g_h: ',g_h)
			print('ori_pt', ori_pt)
			dr_pts = np.empty((0,2))
			s = np.empty((0,1))
			if int(deg) > 0:	#turning right
				s_pt = np.matmul(ori_pt,r_mat(90,True))/np.sqrt(np.dot(ori_pt,ori_pt.transpose()))/c
				for n in range(1,int(n_pt)):
					nxt_pt = np.matmul(s_pt,r_mat(n*abs(deg)/n_pt,False))
					dr_pts = np.concatenate((dr_pts,nxt_pt),0)
					tmp_s = station + n*2*pi/c*abs(deg)/n_pt/360
					tmp_s = np.array(tmp_s).reshape(1,1)
					s = np.concatenate((s,tmp_s),0)
			else:
				s_pt = np.matmul(ori_pt,r_mat(90,False))/np.sqrt(np.dot(ori_pt,ori_pt.transpose()))/c
				for n in range(1,int(n_pt)):
					nxt_pt = np.matmul(s_pt,r_mat(n*abs(deg)/n_pt,True))
					dr_pts = np.concatenate((dr_pts,nxt_pt),0)
					tmp_s = station + n*2*pi/c*abs(deg)/n_pt/360
					tmp_s = np.array(tmp_s).reshape(1,1)
					s = np.concatenate((s,tmp_s),0)
			t_dr_pts = dr_pts+ctr
			z = np.zeros((n_pt-1,1))
			print(s.shape,t_dr_pts.shape,z.shape )
			crv_data= np.concatenate((s,t_dr_pts,z),1)
			data = np.concatenate((data,crv_data),0)
			station = station + c_l
			g_h = h_bound(g_h,-deg)
			startPt = data[-1][1:3]
		else:
			raise Exception('error: cannot recognise seg type')
	return data

def draw():
	# csv_path = '/home/tom/Desktop/path.csv'
	# txt_path = '/home/tom/Desktop/tmp.csv'
	# texture_path = '/home/tom/Desktop/r_tex.jpg'
	csv_path = 'C:\\Users\\tom\\Desktop\\blSim\\path.csv'
	save_path = 'C:\\Users\\tom\\Desktop\\blSim\\tmp.csv'
	texture_path = 'C:\\Users\\tom\\Desktop\\blSim\\r_tex.jpg'
	#csv_file = pd.read_csv(csv_path, header = None)
	csv_file = open(csv_path,newline = '')
	rows = csv.reader(csv_file)
	csv_data = np.array(list(rows), dtype = 'object')
	csv_data[:,1:4] = csv_data[:,1:3].astype('double').astype('object')
	output = data_cvrt(csv_data)
	np.savetxt(save_path,output,delimiter = ',')

	cv = seg_gen(output[:,1:4])
	seg_obj = bpy.data.objects.new('gen_segment', cv)
	seg_link(seg_obj)

	'''applying road texture'''

	bpy.ops.mesh.primitive_plane_add(radius = 2,location = (0,0,0))

	plane = bpy.data.objects.get('Plane')
	plane.select = True


	img = bpy.data.images.load(texture_path)
	tex = bpy.data.textures.new('road_tex',type = 'IMAGE')
	tex.image = img
	mat = bpy.data.materials.new('road_mat')
	t_slot = mat.texture_slots.add()
	t_slot.texture = tex
	plane.material_slots.data.active_material = mat

	bpy.context.scene.objects.active = plane
	bpy.ops.object.editmode_toggle()
	plane.data.uv_textures.new(name = 'UV')
	plane.active_material.emit = 2
	bpy.ops.object.editmode_toggle()


	for area in bpy.context.screen.areas:
		if area.type == 'VIEW_3D':
			for space in area.spaces:
				if space.type == 'VIEW_3D':
					space.viewport_shade = 'MATERIAL'


	m_array = plane.modifiers.new(name = 'road_surface', type = 'ARRAY')
	m_array.count = output[-1][0]*0.8
	m_curve = plane.modifiers.new(name = 'path', type = 'CURVE')
	m_curve.object = bpy.data.objects['gen_segment']
	return True
