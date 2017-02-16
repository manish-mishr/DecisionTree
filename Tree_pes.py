from collections import defaultdict
from math import log

class_list = []
class_Type = 0

class node(object):
	Root = None
	NodeCount = 0
	def __init__(self,att=None,value=None,parent=None):
		self.attr = att
		self.value = value
		self.class_count = defaultdict(int)
		self.left  = None
		self.right = None
		self.leaf = False
		self.data_class = ''
		self. parent = parent

	def set_class(self):
		if self.leaf == False:
			return None
		else:
			(self.data_class,dummy) = majority_class(self.class_count)


def count_class(train_data):
	num_class = {}
	for class_T in class_list:
		num_class[class_T] = 0
	for value in train_data[class_Type]:
		num_class[value] += 1
	return num_class 

def majority_class(class_count):
	class_key = ''
	max_count = 0
	sum_class = 0
	for key in class_count:
		sum_class += class_count[key]
		if class_count[key] > max_count:
			class_key = key
			max_count = class_count[key]
	if class_key == '':
		class_key = key
	return(class_key,sum_class)

def error_count(tdata):
	tclass = count_class(tdata)
	(key,tsum) = majority_class(tclass)
	error = float(tsum - tclass[key])	
	return (error,tsum)
	


def calculate_error(train_data,attr,value,algo):
	lpart ={}
	rpart = {}

	for class_value in class_list:
		lpart[class_value] = 0
		rpart[class_value] = 0

	length = len(train_data[attr])
	for ind in range(length):
		if train_data[attr][ind] <= value:
			lpart[train_data[class_Type][ind]] += 1
		else:
			rpart[train_data[class_Type][ind]] += 1
	
	suml = sum(lpart.values())
	sumr = sum(rpart.values())

	ldata = 1 if algo == 'Gini' else 0
	rdata = 1 if algo == 'Gini' else 0

	for i in range(len(class_list)):
		try:
			if algo == 'Gini':
				ldata -= ((float(lpart[class_list[i]])/suml)**2)
			else:
				try:
					ldata -= ((float(lpart[class_list[i]])/suml)*log(float(lpart[class_list[i]])/suml,2))
				except ValueError:
					ldata -= 0
		except ZeroDivisionError:
			ldata  = 1 if algo == 'Gini' else 0
		try:
			if algo == 'Gini':
				rdata -=  ((float(rpart[class_list[i]])/sumr)**2)
			else:
				try:
					rdata -= ((float(rpart[class_list[i]])/sumr)*log(float(rpart[class_list[i]])/sumr,2))
				except ValueError:
					rdata -= 0
		except:
			rdata = 1 if algo == 'Gini' else 0
	error_score = float(suml)/(suml+sumr)*ldata + float(sumr)/(sumr+suml)*rdata
	return (error_score,lpart,rpart)

def find_attr_value(train_data,attr,algo):
	data = train_data[attr]
	partition_value = 1
	cond = None
	left_partition = {}
	right_partition = {}
	max_value = max(data)
	min_value = min(data)
	step_size = float(max_value - min_value)/10.0
	for i in range(1,10):
		curr_value = min_value + (i*step_size)
		# eval_string = algo + '(train_data,attr,curr_value)'
		(score,lclass,rclass) = calculate_error(train_data,attr,curr_value,algo)
		if score < partition_value:
			partition_value = score
			left_partition = lclass
			right_partition = rclass
			cond = curr_value
	return (partition_value,left_partition,right_partition,cond)

def find_split_attr(train_data,attr_list,algo):
	best_score = 1
	cond = None
	best_attr = None
	left_partition = {}
	right_partition = {}
	for attr in attr_list:
		if attr == class_Type:
			continue
		else:
			(score,lclass,rclass,temp) = find_attr_value(train_data,attr,algo)
			if score < best_score:
				best_score = score
				best_attr = attr
				left_partition = lclass
				right_partition = rclass
				cond = temp
	return (best_attr,cond,left_partition,right_partition)


def check_leaf(class_dict):
	count = 0
	for value in class_dict.values():
		if value > 0:
			count += 1
	if count == 1:
		return True
	else:
		return False


def classify_train_data(train_data,att,split_cond):
	left_data = {}
	right_data = {}
	for key in train_data:
		left_data[key] = []
		right_data[key] = []
	for ind in range(len(train_data[att])):
		if train_data[att][ind] <= split_cond:
			mydict = left_data
		else:
			mydict = right_data
		for key in train_data:
			mydict[key].append(train_data[key][ind])

	return (left_data,right_data)


def Tree(parent,train_data, attr_list,dict_class,algo,classT=None):
	(att,split_attr_cond,count_left,count_right) = find_split_attr(train_data,attr_list,algo)
	(left_data, right_data) = classify_train_data(train_data,att,split_attr_cond)
	(lerror,ltotal) = error_count(left_data)
	(rerror,rtotal) = error_count(right_data)

	
	(perror,total) = error_count(train_data)
	perror = float(perror)/total
	try:
		curr_error = float(lerror+rerror+1)/(ltotal+rtotal)
	except ZeroDivisionError:
		curr_error = 0


	if check_leaf(dict_class) or perror < curr_error :
		leaf_node = node(parent=parent)
		if classT == 'L':
			parent.left = leaf_node
		else:
			parent.right = leaf_node
		node.NodeCount += 1
		leaf_node.class_count = count_class(train_data)
		leaf_node.leaf = True
		leaf_node.set_class()
		return
	else:	
		rootnode = node(att,split_attr_cond,parent)
		if parent == None:
			node.Root = rootnode
		rootnode.class_count = dict_class

		if classT != None:
			if classT == 'L':
				parent.left = rootnode
			else:
				parent.right = rootnode	
		rootnode.set_class()	
		rootnode.error_score = curr_error
		Tree(rootnode,left_data,attr_list,count_left,algo,'L')
		Tree(rootnode,right_data,attr_list,count_right,algo,'R')
	


def readData(filename,att_list,class_att):
	global class_Type
	class_Type = class_att
	data_dict = {}
	class_list = []
	for att in att_list:
		data_dict[att] = []
	try:
		with open(filename,'r') as myfile:
			lines = myfile.readlines()
			length = len(att_list)
			for line in lines:
				line = line.strip()
				attr_set = line.split(',')
				for i in range(length):
					try:
						att_value = float(attr_set[i]) if str(i) != class_Type else attr_set[i]
					except:
						att_value = 0.0
					data_dict[att_list[i]].append(att_value)
				if attr_set[int(class_Type)] not in class_list:
					class_list.append(attr_set[int(class_Type)])
			myfile.close()
		return (data_dict,class_list)
	except IOError:
		print "file do not exist"
		exit()

if __name__=='__main__':
	
	dict_data = defaultdict()
	filename = raw_input("Enter file name: ")
	algo = raw_input("Enter Gini/Entropy: ")

	attr_list = ['pwidth','pheight','swidth','sheight','4']

	(dict_data,temp_list) = readData(filename,attr_list,'4')
	class_list = temp_list[:]
	dict_class = count_class(dict_data)
	Tree(None,dict_data,attr_list,dict_class,algo)
	

