# -*- coding: utf-8 -*-
"""
Created on Wed Mar  8 17:01:18 2023

@author: marie
"""
DELIMITER=','

import pandas as pd
import random

# path to CSV file of conversation starters
conversation_starters = "conversation_starters.csv"

# load conversation starters
all_convo_starters = pd.read_csv(conversation_starters)
convo_starters = list(all_convo_starters.iloc[:,0])
convo_starter = random.choice(convo_starters)


# write conversation starter
print(convo_starter)

