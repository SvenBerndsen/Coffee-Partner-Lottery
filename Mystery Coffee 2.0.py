
# Project 2 COTAPP23, Group go1po1.

# imports
import pandas as pd
import csv
import random
import copy
import os

# link to the online file with all participants linked to google form
SHEET_ID = '1G1Kbl63qxe4FoTaBuBrmKCtodseAqjhbt2UN8pfRsfI'
url = f'https://docs.google.com/spreadsheets/d/{SHEET_ID}/gviz/tq?tqx=out:csv'

# header names in the CSV file (name and e-mail of participants)
header_name = "What is your name?"
header_email = "What is your e-mail?"

# path to TXT file that stores the groups of this round
new_groups_txt = "Coffee Partner Lottery new groups.txt"

# path to CSV file that stores the groups of this round
new_groups_csv = "Coffee Partner Lottery new groups.csv"

# path to CSV file that stores all groups (to avoid repetition)
all_groups_csv = "Coffee Partner Lottery all groups.csv"
        
# init set of old groups
ogroups = set()

DELIMITER=','

# load all previous groups (to avoid redundancies)
if os.path.exists(all_groups_csv):
    with open(all_groups_csv, "r") as file:
        csvreader = csv.reader(file, delimiter=DELIMITER)
        for row in csvreader:
            group = []
            for i in range(0,len(row)):
                group.append(row[i])                        
            ogroups.add(tuple(group))

# load participant's data from the online google sheet
formdata = pd.read_csv(url, sep=DELIMITER)

# create duplicate-free list of participants
participants = list(set(formdata[header_email]))


 # init set of new groups
ngroups = set()


# running set of participants
nparticipants = copy.deepcopy(participants)

# Boolean flag to check if new groups has been found
new_groups_found = False

# ask for group size, max 5
while True:
    try:
        group_size =  int(input('''
How many people would you like in each group? (Please enter an integer number. 
The minimum group size is 2 and the maximum is 5) '''))
        if group_size < 2 :
            print ('The minimum number of group members is 2. Please try again.')
        if group_size > 1 and group_size < 6:
            break
        else: 
            print('The maximum number of group members is 5. Please try again.')  
    except ValueError:
        print("Please enter an integer number.")
        
# define function for making groups
def make_group(size):
    plist = [] # list of group members
    for i in range(0,size):
        p = random.choice(nparticipants) # choose a participant
        nparticipants.remove(p) # remove participant from list of participants
        plist.append(p) # add participant to group list
    plist.sort() # sort list alphabetically
    ngroups.add(tuple(plist)) # add created group to list of groups
    

# try creating new groups until successful
while not new_groups_found:   # to do: add a maximum number of tries
  
    # Calculate remainder when dividing number of participants by chosen group size
    remainder = len(participants)%group_size
    
    # If there is 2 or more people left over, make a group of this size
    if remainder != 0 and remainder != 1:
        make_group(remainder)
        
    # If there is exactly 1 person left over, create a group with an extra member
    elif remainder == 1:
        make_group(group_size+1)
  
    # while still participants left to group, create groups of the chosen group size
    while len(nparticipants) > 0:
        make_group(group_size) 
        

    # check if all new groups are indeed new, else reset
    if ngroups != ogroups:
        new_groups_found = True
    else:
        ngroups = set()
        nparticipants = copy.deepcopy(participants)


# assemble output for printout and for email output
output_string = ""

output_string += "------------------------\n"
output_string += "Today's coffee partners:\n"
output_string += "------------------------\n"

for group in ngroups:
    group = list(group)
    output_string += "* "
    for i in range(0,len(group)):
        name_email_group = f"{formdata[formdata[header_email] == group[i]].iloc[0][header_name]} ({group[i]})"
        if i < len(group)-1:
            output_string += name_email_group + ", "
        else:
            output_string += name_email_group + "\n"

def send_email(email, name, output):
    import smtplib, ssl

    smtp_server = "smtp.gmail.com"
    port = 587
    sender_email = "coffeepartneruu@gmail.com"
    password = "egwnmceqwlrawygf"
    
    
    context = ssl.create_default_context()
    
    try:
        server = smtplib.SMTP(smtp_server,port)
        server.ehlo() # Can be omitted
        server.starttls(context=context) # Secure the connection
        server.ehlo() # Can be omitted
        server.login(sender_email, password)
        sender_email = "coffeepartneruu@gmail.com"
        message = f"""Subject: Your coffee group for this week
 
            
Hi {name}, 
This message is sent from Python.
Your group for this week is:
{output}
    
Conversation_starter"""
            
        server.sendmail(sender_email, email, message)
    except Exception as e:
        # Print any error messages to stdout
        print(e)
    finally:
        server.quit()

    
# write output to console
print(output_string)

# write output into text file for later use
with open(new_groups_txt, "wb") as file:
    file.write(output_string.encode("utf8"))

# write new groups into CSV file and send an email
with open(new_groups_csv, "w") as file:
    #make headers up to maximum group size of 6
    header = ["name1", "email1", "name2", "email2", "name3", "email3" , "name4", "email4" , "name5", "email5" , "name6", "email6"]
    file.write(DELIMITER.join(header) + "\n")
    for group in ngroups:
        group = list(group)
        for i in range(0,len(group)):
            receiver_email = f"{group[i]}"
            receiver_name = f"{formdata[formdata[header_email] == group[i]].iloc[0][header_name]}"
            name_email_group = f"{formdata[formdata[header_email] == group[i]].iloc[0][header_name]}{DELIMITER} {group[i]}"
            output_email = ""
            for i in range(0,len(group)):
                name_email_group = f"{formdata[formdata[header_email] == group[i]].iloc[0][header_name]} ({group[i]})"
                if i < len(group):
                    output_email += name_email_group + "\n"
            
            #send e-mail
            send_email(receiver_email, receiver_name, output_email)
            
            #write to the file
            if i < len(group)-1:
                file.write(name_email_group + DELIMITER + " ")
            else:
                file.write(name_email_group + "\n")
                
# append groups to history file
if os.path.exists(all_groups_csv):
    mode = "a"
else:
    mode = "w"

with open(all_groups_csv, mode) as file:
    for group in ngroups:
        group = list(group)
        for i in range(0,len(group)):
            if i < len(group)-1:
                file.write(group[i] + DELIMITER)
            else:
                file.write(group[i] + "\n")
                







# # import email
# import smtplib, ssl

# smtp_server = "smtp.gmail.com"
# port = 587
# sender_email = "coffeepartneruu@gmail.com"
# password = "egwnmceqwlrawygf"

# #send email with group based on 
# # Create a secure SSL context
# context = ssl.create_default_context()

# with open('Coffee Partner Lottery new groups.csv', mode='r') as csv_file:
#     groups_reader = csv.DictReader(csv_file)
#     output_string = ""
#     receiver_email = []
#     for row in groups_reader:
#         for i in range(0,len(group)):
#             print(group)
#             receiver_email = [f'{group[i]}']
#             print(receiver_email)
#             try:
#                 server = smtplib.SMTP(smtp_server,port)
#                 server.ehlo() # Can be omitted
#                 server.starttls(context=context) # Secure the connection
#                 server.ehlo() # Can be omitted
#                 server.login(sender_email, password)
#                 # TODO: add name to email and change for group since 
#                 sender_email = "coffeepartneruu@gmail.com"
#                 message = f"""Subject: Your coffee group for this week
 
            
# Hi, 
# This message is sent from Python.
# Your group for this week is:
# {output_string}"""
            
#                 server.sendmail(sender_email, receiver_email, message)
#             except Exception as e:
#                 # Print any error messages to stdout
#                 print(e)
#             finally:
#                 server.quit()
#             receiver_email = []
             
# print finishing message
print()
print("Job done.")

