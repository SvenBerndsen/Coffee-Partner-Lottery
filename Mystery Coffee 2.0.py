# Project 2 COTAPP23, Group go1po1.
# Code written by:
# Sven Berndsen 
# Nyasha Grecu 
# Christos Psaropoulos
# Marieke Hooimeijer

# imports
import pandas as pd
import csv
import random
import copy
import os
import smtplib, ssl #used for email sending
import sys, time #used for loading animation


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

# path to CSV file of conversation starters
conversation_starters = pd.read_csv("conversation_starters.csv")

# path to TXT file that stores the messages to the participants of this round
messages_txt = "Coffee Partner Lottery messages to participants.txt"
        
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

# welcome user
print("Welcome to the mystery coffee group maker 2.0!")
print("""This program will make groups based on all participants
that signed up via the online form (https://for ms.gle/sBDoR1QxJJr4EeecA)""")

# ask for group size, max 5
while True:
    try:
        group_size =  int(input('''How many people would you like in each group? (Please enter an number between 2 and 5) '''))
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
    if ngroups.intersection(ogroups):
        ngroups = set()
        nparticipants = copy.deepcopy(participants)
    else:
        new_groups_found = True

# Get a new conversation starter and save it into a file 

# load conversation starters
convo_starters = list(conversation_starters.iloc[:,0])

# read previous starters from file (to avoid redundancies)
# if the is no previous yet, create a empty list
try:
    previous_starters = pd.read_csv("previous_starters.csv")["conversation_starters"].tolist()
except FileNotFoundError:
    previous_starters = []

# function to choose a conversation starter
def choose_convo_starter():
        # choose a conversation starter that hasn't been used before
        convo_starter = random.choice(convo_starters)
        while convo_starter in previous_starters:
            # if the starter is in the already used list of starters try 50 times to find another starter
            attempts = 1 
            while attempts < 51:
                convo_starter = random.choice(convo_starters)
                attempts = attempts + 1
            else:
                print("\nNOTE: The program was unable to find a new conversation starter.")
                print("Therefore, a already used conversation starter was used.\n")
                break
        return convo_starter

# assemble the console output
# assemble output for printout of groups
output_string = ""

output_string += "------------------------------\n"
output_string += "This week's coffee groups are:\n"
output_string += "------------------------------\n"

# assemble output for printout of conversation starter
convo_starter = "-------------------------------------\n"
convo_starter += "This week's conversation starter is:\n"
convo_starter += "------------------------------------\n"


#Create all the groups
group_number = 1
for group in ngroups:
    group = list(group)
    output_string += f"Group {group_number}:\n"
    for i in range(0,len(group)):
        name_email_group = f"{formdata[formdata[header_email] == group[i]].iloc[0][header_name]} ({group[i]})"
        if i < len(group)-1:
            output_string += name_email_group + "\n"
        else:
            output_string += name_email_group + "\n\n"
    group_number = group_number + 1 

    
# write all output to console 
print(output_string)

# choose and print conversation starter
selected_convo = choose_convo_starter()
convo_starter += f"'{selected_convo}'\n"
print(convo_starter)

# write previous conversation starters starters to file
previous_starters.append(selected_convo)
pd.DataFrame({"conversation_starters": previous_starters}).to_csv("previous_starters.csv", index=False)


# Output text file with personalized message to each group member
with open(messages_txt, "w") as file:
    for group in ngroups:
        group = list(group)
        group_names_emails = ''
        for i in range(0,len(group)):
            name_email = f"{formdata[formdata[header_email] == group[i]].iloc[0][header_name]} ({group[i]})"
            if i < len(group)-1:
                group_names_emails += name_email + ", "
            else:
                group_names_emails += name_email
        
        for i in range(0,len(group)):
            message = f'''
Dear {formdata[formdata[header_email] == group[i]].iloc[0][header_name]},

Thank you for signing up for the Mystery Coffee 2.0 this week.

Your group for this week is: 
    {group_names_emails}

The conversation starter for this week is: 
    {convo_starter}

Wishing you lots of fun on your coffee date this week!
The Mystery Coffee 2.0 Team \n \n \n'''
            file.write(message)
    

# function for sending the emails
def send_email(email, name, output):
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
 
            
Dear {name}, 

With this email you receive your group information and conversation starter for this week's coffee meeting!

Your group for this week is:
{output}
    
The conversation starter for this week is:
{selected_convo}

Wishing you lots of fun on your coffee date this week!

With best regards,
The Mystery Coffee 2.0 Team"""
            
        server.sendmail(sender_email, email, message)
    except Exception as e:
        # Print any error messages to stdout
        print(e)
    finally:
        server.quit()
    
# function for loading animation used for sending email which could take some time
def animated_loading():
    chars = "/—\|" 
    for char in chars:
        sys.stdout.write('\r'+'Busy sending all emails...'+char)
        time.sleep(.1)
        sys.stdout.flush() 



# write new groups into CSV file and send an email
print("---------------------------------------------------")
print("Saving new groups into csv file and sending e-mails")
print("---------------------------------------------------")
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
            animated_loading()
                
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

print("\n\nAll done.")