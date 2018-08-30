#!/usr/bin/python3
import argparse
import csv
import re
import os

parser = argparse.ArgumentParser(description="Some Description...")
parser.add_argument("-scan", "--csv_file_name", nargs="+", help="Some text...")
parser.add_argument("-add", "--new_mac_address", nargs="+", help="Some text...")
parser.add_argument("-remove", "--mac_address", nargs="+", help="Some text...")
parser.add_argument("-replace","--old_mac_address", nargs="+", help="Some text...")
args = parser.parse_args()

# print(len(argparse))
# print (vars(args))
# print (args)
# exit()
# print ("aaaaaaaaa")

# regex_mac = re.compile(r'(?:[0-9a-f]:?){12}')
regex_mac = re.compile(r'(?:(([0-9a-fA-F]{2}\:{1}){5}[0-9a-fA-F]{2}))')
regexp_mac = re.compile(r'(^(([0-9a-fA-F]{2}\:{1}){5}[0-9a-fA-F]{2})$)')
regex_ip = re.compile(r'(\d{1,3}\.\d{1,3}\.\d{1,3}\.\d{1,3})')
regex_hname = re.compile(r'(?:([a-z]{3,8}\_[0-9]{1,2}):?)')
regex_room_name = re.compile(r'([a-z]{3,8})')

ip_basis = "10.116.99."
classrooms = ['galilei', 'faraday', 'ohm', 'newton', 'einstein', 'maxwell', 'library']

crnt_room = ""
crnt_row_nmber = ""
crnt_row_content = ""

####### Tot's functions	  ***************************

##### 	Assistant functions   ********** OK
def mac_exist(classroom_name, mac_address):

	csv_file = open(classroom_name+".csv", "r")
	readCSV = csv_file.readlines()
	csv_file.close()

	for i in range(len(readCSV)):
		mac_address_check = re.match(regex_mac, readCSV[i].strip())
		if mac_address == mac_address_check.group():
			# print("\n" + mac_address + " mac address already exists in " + classroom_name+".csv file.\nRow number:\t" + str(i+1) + "\nRow content:\t" + readCSV[i].strip() + "\n")
			return True
	return False
def new_mac_exist(mac_address):

	csv_file = open("general.csv", "r")
	readCSV = csv_file.readlines()
	csv_file.close()

	for i in range(len(readCSV)):
		mac_address_check = re.match(regex_mac, readCSV[i].strip())
		if mac_address == mac_address_check.group():
			# print("\n" + mac_address + " mac address already exists in " + classroom_name+".csv file.\nRow number:\t" + str(i+1) + "\nRow content:\t" + readCSV[i].strip() + "\n")
			crnt_room = re.search(regex_room_name, readCSV[i].strip()).group()
			crnt_row_nmber = readCSV.index(readCSV[i])+1
			crnt_row_content = readCSV[i].strip()
			print("crnt_row_nmber:")
			print(crnt_row_nmber)
			return True
	return False

def init_csv(csv_file):
	if os.path.isfile("./" + csv_file + ".csv"):
		mac = []
		csvfile = open (csv_file + ".csv", 'r')
		readCSV = csvfile.readlines()
		csvfile.close()

		for x in readCSV:
			value = x.strip()
			c = re.search(regex_mac, value)
			if c:
				mac.append(c.group())

		with open(csv_file+".csv", 'w+') as crnt_csv:
			if (csv_file == "galilei"):
				crnt_ip = 10
			elif (csv_file == "faraday"):
				crnt_ip = 42
			elif (csv_file == "ohm"):
				crnt_ip = 73
			elif (csv_file == "newton"):
				crnt_ip = 86
			elif (csv_file == "einstein"):
				crnt_ip = 117
			elif (csv_file == "maxwell"):
				crnt_ip = 148
			elif (csv_file == "library"):
				crnt_ip = 180

			crnt_hname = 0
			init_ip = []
			init_hname = []

			for y in range(len(mac)):
				crnt_csv.write(str(mac[y]) + ", 10.116.99." + str(crnt_ip) + ", " + csv_file + "_" + str(crnt_hname) + "\n")

				init_ip.append(str(ip_basis) + str(crnt_ip))
				init_hname.append(csv_file + "_" + str(crnt_hname))

				crnt_ip = crnt_ip + 1
				crnt_hname = crnt_hname + 1
		print(csv_file + ".csv \tfile is initialized")
		# create_general_csv()
		# create_conf_files()
	else:
		print(csv_file + ".csv \tfile not found.")
		print(csv_file.capitalize() + " class data has not been updated in the general.csv, dhcpd.conf.csv and hosts.csv files.")

def create_general_csv():
	with open("general.csv", 'w+') as general:

		for j in classrooms:
			if os.path.isfile("./" + j + ".csv"):
				with open(j+".csv", 'r+') as crnt_csv:
					read_crnt_csv_line = crnt_csv.readlines()
					crnt_csv.close()
					for k in range(len(read_crnt_csv_line)):
						general.write(read_crnt_csv_line[k])
		print("general.csv \tfile succesfuly updated")
		general.close()

def get_data_from_general_csv():
	# Checks if the general.csv file exists
	if os.path.isfile("./general.csv"):
		# If exists then open
		with open("general.csv", 'r') as general:
			readCSV = general.readlines()
			general.close()

			mac=[]
			ip=[]
			hname=[]
			
			for i in range(len(readCSV)):
				# print(len(readCSV))
				# exit()
				value = readCSV[i].strip()
				crnt_mac = re.search(regex_mac, value)
				crnt_ip = re.search(regex_ip, value)
				crnt_hname = re.search(regex_hname, value)

				if crnt_mac and crnt_ip and crnt_hname:
					mac.append(crnt_mac.group())
					ip.append(crnt_ip.group())
					hname.append(crnt_hname.group())

				else:
					print("It seems that there is some error in the file. Please, check the general.csv file.")
					exit()
			return mac, ip, hname
	else:
		print("general.csv \tfile not found!\n")

def create_conf_files():
	mac, ip, hname = get_data_from_general_csv()
	# Create DHCPD.conf file
	with open("dhcpd.conf.txt", 'w+') as dhcpd:
		for i in range(len(mac)):
			dhcpd.write("host " + str(hname[i]) + " {\n\thardware ethernet " + str(mac[i]) + ";\n\tfixed-address " + str(ip[i] )+ ";\n\toption host-name \"" + str(hname[i]) + "\";\n}\n")
		dhcpd.close()
		print("dhcpd.conf \tfile succesfuly updated.")

	with open("hosts.txt", 'w+') as hosts:
		hosts.write("127.0.0.1\t\tlocalhost\n10.116.99.210\tsaed-kickstart\n10.116.99.240\tam04-saed-srv\n10.116.99.241\tam04-saed-sgm\n10.116.99.242\tam04-saed-fs01\n10.116.99.244\tam04-saed-emt2x4\n10.116.99.245\tam04-saed-sym1\n\n")
		for j in range(len(mac)):
			hosts.write(str(ip[j]) + "\t" + str(hname[j]) + "\n")
		hosts.close()
		print("hosts \t\tfile succesfuly updated.\n\n")

#####	Basic functions   **************

#	Scan all csv --- OK
def scan_all_csv():
	print("****************************************************\nSCANNING AND INITIALIZING ALL CSV FILES...\n")
	for i in classrooms:
		scan_csv(i)

	# create_general_csv()
	# create_conf_files()

#	Scan csv --- OK
def scan_csv(csv_file):
	init_csv(csv_file)

	# create_general_csv()
	# create_conf_files()

#	ADD MACHINE --- OK
def add_machine(new_data):
	file_changed = False
	new_mac = []

	csv_file = open("general.csv", "r")
	readCSV = csv_file.readlines()
	csv_file.close()

	for k in range(1, len(new_data)):
		is_exist = False
		check_mac_address = re.match(regexp_mac, new_data[k])
		
		if check_mac_address:
			for i in range(len(readCSV)):
				# crnt_mac = re.match(regexp_mac, readCSV[i])
				# print(crnt_mac)
				# exit()
				if new_data[k] == re.match(regex_mac, readCSV[i]).group():
					crnt_room = re.search(regex_room_name, readCSV[i].strip())
					is_exist = True
					print("\n" + new_data[k] + " mac address already exists in " + str(crnt_room.group()) + ".csv file.")
					print("File name:\tgeneral.csv")
					print("Row number:\t" + str(readCSV.index(readCSV[i])+1))
					print("Row content:\t" + readCSV[i].strip() + "\n\n\n")
				else:
					continue
			if not is_exist:
				file_changed = True
				new_mac.append(new_data[k])
				print("The new machine with " + new_data[k] + " mac address successfully added in " + new_data[0] + ".csv file.\n")
		else:
			print(new_data[k] + " mac address is incorrect.\n")

	if file_changed:
		crnt_csv = open(new_data[0]+".csv", "a")
		for n in range(len(new_mac)):
			crnt_csv.write(new_mac[n])
		crnt_csv.close()

		del new_mac

		scan_csv(new_data[0])
		create_general_csv()
		create_conf_files()

#	REMOVE MACHINE --- OK
def remove_machine(remove_data):
	file_changed = False
	csv_file = open(remove_data[0]+".csv", "r")
	readCSV = csv_file.readlines()
	csv_file.close()

	for k in range(1, len(remove_data)):
		is_exist = False
		check_mac_address = re.match(regexp_mac, remove_data[k])

		if check_mac_address:
			for i in readCSV:
				exists = "NO"
				crnt_mac = re.match(regex_mac, i.strip())
				if remove_data[k] == crnt_mac.group():
					# confirm = input("Do you really want do delete " + remove_data[k] + " mac address from " + remove_data[0] + ".csv file\nRow content is:\t" + readCSV[readCSV.index(i)] + "\nType yes or no (y/n):\t")
					# if confirm == "y" or confirm == "Y":
					file_changed = True
					is_exist = True
					print(remove_data[k] + " mac address has successfully removed from " + remove_data[0]+".csv file.")
					print("Row with this content was deleted:\t" + readCSV[readCSV.index(i)] + "\n\n")
					del readCSV[readCSV.index(i)]
				else:
					continue
			if not is_exist:
				print(remove_data[k] + " mac address does not exist in " + remove_data[0] + ".csv file.\n")
		else:
			print(remove_data[k] + " mac address is not correct.\n")
			continue
	csv_file = open(remove_data[0]+".csv", "w")
	
	for j in range(len(readCSV)):
		csv_file.write(readCSV[j])
	csv_file.close()

	if file_changed:
		scan_csv(remove_data[0])
		create_general_csv()
		create_conf_files()

#	REPLACE MACHINE --- OK
def replace_machine(replace_data):
	file_changed = False
	old=[]
	new=[]
	new_mac =[]

	crnt_csv = open(replace_data[0]+".csv", "r")
	readCSV = crnt_csv.readlines()
	crnt_csv.close()

	for y in range(len(readCSV)):
		value = re.match(regex_mac, readCSV[y]).group()
		new_mac.append(value)
		# print(new_mac)

	crnt_csv = open("general.csv", "r")
	read_general = crnt_csv.readlines()
	crnt_csv.close()

	for i in range(1, len(replace_data)):
		old_mac_is_exist=False
		if re.match(regex_mac, replace_data[i]):
			print(i)
			if mac_exist(replace_data[0], replace_data[i]) and (i+1)%2==0:
				# if (i+1)%2==0:
				print("ssssss")
				old_mac_is_exist = True
					# old.append(replace_data[i])
				# i+=1
			else:
				print(replace_data[i] + " mac address does not exist in " + replace_data[0] + ".csv file")
				continue

			if new_mac_exist(replace_data[0]):
				print("crnt_row_nmber:")
				print(crnt_row_nmber)
				print(replace_data[0] + " mac address already exist in " + crnt_room + ".csv file")
				print("File name:\tgeneral.csv")
				print("Row number:\t" + str(crnt_row_nmber))
				print("Row content:\t" + crnt_row_content + "\n\n\n")
				i+=1
				continue
			elif new_mac_exist(replace_data[i]) and old_mac_is_exist and (i+1)%2==1:
				# if (i+1)%2==1:
				old.append(replace_data[i-1])
				new.append(replace_data[i])
				i+=1
		else:
			print(replace_data[i] + "\tis incorrect\n")
	
	print(old)
	print(new)
	for unique in range(len(new)):
		for x in range(len(new)):
			if x==unique:
				continue
			if new[unique] == new[x]:
				print("***************************************************************")
				print("You want to attach same mac address to different mac addresses.")
				print("It is unacceptable")
				print("***************************************************************")
				exit()

								# for i in range(len(old)):
								# 	old_mac_is_exist = False
									
								# 	for j in range(len(readCSV)):
								# 		if old[i] == re.match(regex_mac, readCSV[j]).group():
								# 			old_mac_is_exist = True
								# 			break
								# 	if not old_mac_is_exist:
								# 		print(old[i] + " mac address does not exist in " + replace_data[0]+".csv file.\n\n")
								# 		continue

								# 	# for k in range(len(new)):
								# for m in range(len(new)):
								# 	new_mac_is_exist = True
								# 	for h in range(len(read_general)):
								# 		if new[m] == re.match(regex_mac, read_general[h]).group():
								# 			new_mac_is_exist = False
								# 			crnt_room = re.search(regex_room_name, read_general[h]).group()
								# 			crnt_row_nmber = read_general.index(read_general[h])+1
								# 			crnt_row_content = read_general[h].strip()
								# 			print(new[m] + " mac address already exist in " + crnt_room+".csv file")
								# 			print("File name:\tgeneral.csv")
								# 			print("Row number:\t" + str(crnt_row_nmber))
								# 			print("Row content:\t" + crnt_row_content + "\n\n\n")
								# 			break


#*\
	# file_changed = False
	# old=[]
	# new=[]
	# new_mac =[]

	# crnt_csv = open(replace_data[0]+".csv", "r")
	# readCSV = crnt_csv.readlines()
	# crnt_csv.close()

	# for y in range(len(readCSV)):
	# 	value = re.match(regex_mac, readCSV[y]).group()
	# 	new_mac.append(value)

	# crnt_csv = open("general.csv", "r")
	# read_general = crnt_csv.readlines()
	# crnt_csv.close()

	# for i in range(1, len(replace_data)):
	# 	if re.match(regex_mac, replace_data[i]):
	# 		if (i+1)%2==0:
	# 			old.append(replace_data[i])
	# 		if (i+1)%2==1:
	# 			new.append(replace_data[i])
	# 	else:
	# 		print(replace_data[i] + "\tis incorrect\n")
	
	# for unique in range(len(new)):
	# 	for x in range(len(new)):
	# 		if x==unique:
	# 			continue
	# 		if new[unique] == new[x]:
	# 			print("***************************************************************")
	# 			print("You want to attach same mac address to different mac addresses.")
	# 			print("It is unacceptable")
	# 			print("***************************************************************")
	# 			exit()

	# for i in range(len(old)):
	# 	old_mac_is_exist = False
		
	# 	for j in range(len(readCSV)):
	# 		if old[i] == re.match(regex_mac, readCSV[j]).group():
	# 			old_mac_is_exist = True
	# 	if not old_mac_is_exist:
	# 		print(old[i] + " mac address does not exist in " + replace_data[0]+".csv file.\n\n")
	# 		continue

	# 	# for k in range(len(new)):
	# 	new_mac_is_exist = True

	# 	for h in range(len(read_general)):
	# 		if new[i] == re.match(regex_mac, read_general[h]).group():
	# 			new_mac_is_exist = False
	# 			crnt_room = re.search(regex_room_name, read_general[h]).group()
	# 			crnt_row_nmber = read_general.index(read_general[h])+1
	# 			crnt_row_content = read_general[h].strip()
	# 			print(new[i] + " mac address already exist in " + crnt_room+".csv file")
	# 			print("File name:\tgeneral.csv")
	# 			print("Row number:\t" + str(crnt_row_nmber))
	# 			print("Row content:\t" + crnt_row_content + "\n\n\n")
	# 			exit()


		# for h in range(len(read_general)):
		# 	if new[i] == re.match(regex_mac, read_general[h]).group():
		# 		new_mac_is_exist = False
		# 		crnt_room = re.search(regex_room_name, read_general[h]).group()
		# 		crnt_row_nmber = read_general.index(read_general[h])+1
		# 		crnt_row_content = read_general[h].strip()
		# if not new_mac_is_exist:
		# 	print(new[i] + " mac address already exist in " + crnt_room+".csv file")
		# 	print("File name:\tgeneral.csv")
		# 	print("Row number:\t" + str(crnt_row_nmber))
		# 	print("Row content:\t" + crnt_row_content + "\n\n\n")
		# 	continue



		# if old_mac_is_exist and new_mac_is_exist:
			for replacing in range(len(old)):
				for change in range(len(new_mac)):
					if old[replacing] == re.match(regex_mac, new_mac[change]).group():
						new_mac[change] = new[replacing]
						file_changed = True
			
			crnt_csv = open(replace_data[0]+".csv", "w")
			for c in range(len(new_mac)):
				crnt_csv.write(new_mac[c]+"\n")
			crnt_csv.close()	

			print("Mac address " + old[i] + " has been changed to " + new[i] + " successfully.\n")


	if file_changed:
		scan_csv(replace_data[0])
		create_general_csv()
		create_conf_files()

####### ******************************************

classroom = {
           "galilei" : scan_csv,
           "faraday" : scan_csv,
           "ohm"     : scan_csv,
           "newton"  : scan_csv,
           "einstein": scan_csv,
           "maxwell" : scan_csv,
           "library" : scan_csv,}

# Scan csv files
if args.csv_file_name:
	print("\n\n")

	dbr = False

	for n in range(len(args.csv_file_name)):
		args.csv_file_name[n] = args.csv_file_name[n].lower()

	if (args.csv_file_name[0]=="all"):
		scan_all_csv()
		print("")
		create_general_csv()
		create_conf_files()

		exit()
	else:
		for a in args.csv_file_name:
			if a in classrooms:
				if os.path.isfile("./" + a + ".csv"):
					print("\nScaning " + a + ".csv file...")
					classroom[a](a)
					dbr = True
				else:
					print(a + ".csv file not found.\n" + a.capitalize() + " class data has not been updated in the general.csv, dhcpd.conf.csv and hosts.csv files.")
			else:
				print(a + " classroom does not exist.\n\nValid classrooms names are:\n")
				for i in classrooms:
					print(i)
				exit()
		if dbr:
			print("")
			create_general_csv()
			create_conf_files()
		
		exit()

# Add machine - OK
if args.new_mac_address:
	print("\n\n")

	for n in range(len(args.new_mac_address)):
		args.new_mac_address[n] = args.new_mac_address[n].lower()

	if (len(args.new_mac_address) < 2):
		print("\nFor '-add' command You should enter min two arguments:   classroom_name   new_mac_address\n\nYou can add more than one new machine and you should maintain the input data order\nOrder is: -add   classroom_name   new_mac_address 1   new_mac_address 2   ...")
		exit()

	if args.new_mac_address[0] in classrooms:
		if os.path.isfile("./" + args.new_mac_address[0]+".csv"):
			add_machine(args.new_mac_address)

			exit()
		else:
			print(args.new_mac_address[0]+".csv file not found.")
			exit()
	else:
		print(args.new_mac_address[0] + " classroom does not exist.\n\nValid classrooms names are:\n")
		for i in classrooms:
			print(i)
		exit()

# Remove machine - OK
if args.mac_address:
	print("\n\n")

	for n in range(len(args.mac_address)):
		args.mac_address[n] = args.mac_address[n].lower()

	if (len(args.mac_address) < 2):
		print("\nFor '-remove' command You should enter min two arguments:   classroom_name   mac_address\n\nYou can remove more than one machine and you should maintain the input data order\nOrder is: -remove   classroom_name   mac_address 1   mac_address 2   ...")
		exit()

	if args.mac_address[0] in classrooms:
		if os.path.isfile("./" + args.mac_address[0]+".csv"):
			remove_machine(args.mac_address)
		else:
			print(args.mac_address[0]+".csv file not found.")
			exit()
	else:
		print(args.mac_address[0] + " classroom does not exist.\n\nValid classrooms names are:\n")
		for i in classrooms:
			print(i)
		exit()

# Replace machine - OK
if args.old_mac_address:
	print("\n\n")

	for n in range(len(args.old_mac_address)):
		args.old_mac_address[n] = args.old_mac_address[n].lower()

	if (len(args.old_mac_address)<3):
		print("\nFor '-replace' command You should enter min three arguments:   classroom_name   old_mac_address new_mac_address\n\nYou can replace more than one machine and you should maintain the input data order\nOrder is: -remove   classroom_name   old_mac_address   new_mac_address   old_mac_address   new_mac_address ...\n")
		exit()
	else:
		if (len(args.old_mac_address)%2 == 0):
			print("\nThe information you entered is incomplete\n")
			print("\nFor '-replace' command You should enter min three arguments:   classroom_name   old_mac_address   new_mac_address\n\nYou can replace more than one machine and you should maintain the input data order\nOrder is: -remove   classroom_name   old_mac_address   new_mac_address   old_mac_address new_mac_address ...\n")
			exit()
		else:
			if args.old_mac_address[0] in classrooms:
				# print("Tamama")
				if os.path.isfile("./" + args.old_mac_address[0]+".csv"):
					replace_machine(args.old_mac_address)

					exit()
				else:
					print(args.old_mac_address[0]+".csv file not found.")
					exit()
			else:
				print(args.old_mac_address[0] + " classroom does not exist.\n\nValid classrooms names are:\n")
				for i in classrooms:
					print(i)
				exit()
