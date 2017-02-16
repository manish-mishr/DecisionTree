from collections import defaultdict
from math import log
from random import shuffle

class_list = []
class_Type = 0
Total_Length = 0
val1_test = {}
global_count = 0

class node(object):
	Root = None
	NodeCount = 0
	TreeCost = 0
	LeafCount = 0
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
	try:
		error_score = float(suml)/(suml+sumr)*ldata + float(sumr)/(sumr+suml)*rdata
	except:
		error_score = 0
	return (error_score,lpart,rpart)

def find_attr_value(train_data,attr,algo):
	data = train_data[attr]
	partition_value = 1
	cond = None
	left_partition = {}
	right_partition = {}
	max_value = max(data) if len(data) > 0 else 0
	min_value = min(data) if len(data) > 0 else 0
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
	length = len(train_data[att])
	if length > 0:
		for ind in range(len(train_data[att])):
			if train_data[att][ind] <= split_cond:
				mydict = left_data
			else:
				mydict = right_data
			for key in train_data:
				mydict[key].append(train_data[key][ind])

		return (left_data,right_data)
	else:
		return (left_data,right_data)

def val_classify(item,root):
	while not root.leaf :
		curr_att = root.attr
		if curr_att == None:
			return majority_class()
		if item[curr_att] <= root.value:
			root = root.left
		else:
			root = root.right
	return root.data_class


def val_accuracy(val_test):
	root = node.Root
	length_test = len(test_data[class_Type])
	wrong = 0
	for test in range(length_test):
		item = {}
		for att in attr_list:
			item[att] = test_data[att][test]
		predicted = val_classify(item,root)
		if item[class_Type] != predicted:
			wrong += 1
	return wrong

def validate_set(train_data,attr_list):
	length = len(train_data)
	step_size = length/4
	random_list = [0 for i in range(length)]
	shuffle(random_list)
	val_test = {}
	val_train = {}
	for att in attr_list:
		val_train[att] = []
		val_test[att] = []

	start = 3*step_size
	end = 4*step_size
	for value in random_list:
		if value < end and value > start:
			mydict = val_train
		else:
			mydict = val_test
		for att in attr_list:
			mydict[att].append(train_data[att][value])
	return(val_train,val_test)

def count(tdata,attr_list):
	for att in attr_list:
		if len(tdata[att]) == 0:
			return 0
	return 1

def Tree(parent,train_data, attr_list,dict_class,algo,classT=None):
	global Total_Length,val1_test,global_count
	if count(train_data,attr_list) == 0:
		parent.leaf = True
		return 
	if parent == None and global_count == 0:
	 	validate_test = {}
		for value in dict_class.values():
	 		Total_Length += value
	 	(cross_data,val1_test) = validate_set(train_data,attr_list)
	 	train_data = {}
	 	train_data = cross_data
	elif parent == None:
	 	return

	(att,split_attr_cond,count_left,count_right) = find_split_attr(train_data,attr_list,algo)
	(left_data, right_data) = classify_train_data(train_data,att,split_attr_cond)
	
	(error,total) = error_count(train_data) 
	try:
		error = float(error)/total
	except:
		error = 0
	if check_leaf(dict_class) or error < 0.10 :
		leaf_node = node(parent=parent)
		leaf_node.leaf = True
		leaf_node.class_count = count_class(train_data)
		if classT == 'L':
			parent.left = leaf_node
		else:
			parent.right = leaf_node
		node.LeafCount += 1
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
		node.NodeCount += 1
		rootnode.set_class()
		Tree(rootnode,left_data,attr_list,count_left,algo,'L')
		Tree(rootnode,right_data,attr_list,count_right,algo,'R')
	prune(attr_list)

def return_leaf(root):
	list_leaf = []
	if check_leaf(root):
		list_leaf.append(root)
	else:
		return_leaf(roo.left)
		return_leaf(root.right)
	return list_leaf
	
def prune(att_list):
	global val1_test
	wrong = val_classify(val1_test,att_list)
	root = node.Root
	list_leaf = return_leaf(root)
	if len(list_leaf) == 0:
		return 
	else:
		for leaf in list_leaf:
			leaf.parent.leaf = True
			new_wrong = val_classify(val1_test)
			if new_wrong < wrong:
				continue
			else:
				leaf.parent.leaf = False


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
					att_value = float(attr_set[i]) if str(i) != class_Type else attr_set[i]
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
	

