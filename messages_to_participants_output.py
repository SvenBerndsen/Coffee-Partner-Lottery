#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Fri Mar 10 14:54:03 2023

@author: user
"""
# assemble output for printout
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

    
# write output to console
print(output_string)

# print conversation starter too    
print(f'''
-----------------------------
Today's conversation starter:
-----------------------------    
{convo_starter}''')


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