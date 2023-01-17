from riotwatcher import TftWatcher
import pandas as pd
import plotly.graph_objects as go
import numpy as np
import matplotlib.pyplot as plt

#Counts placement from 1st place to x place
def count_placement(placement_trend, size):
    placements = np.array(placement_trend, dtype=np.int32)
    i = 1
    placement_data = []
    while i < size: 
        occurrence = np.where(placements == i)[0].size
        placement_data.append(occurrence)
        i+=1
    return placement_data

def changePlacement(placement):
    if placement == 2:
        placement = 1
    elif placement == 3:
        placement = 2
    elif placement == 4:
        placement = 2
    elif placement == 5:
        placement = 3
    elif placement == 6:
        placement = 3
    elif placement == 7:
        placement = 4
    elif placement == 8:
        placement = 4
    else: 
        placement = -1
    return placement 

#Finds placements for when users play together
def duo_placement_list(user1, user2, data): 
    duo_placement = []
    for match in data:
        if friend_id in match["metadata"]["participants"]:     
            my_match_data_1 = match['info']['participants'][match['metadata']['participants'].index(user1['puuid'])]
            my_match_data_2 = match['info']['participants'][match['metadata']['participants'].index(user2['puuid'])]
            duo_placement.append(changePlacement(int(my_match_data_1['placement'])))
            duo_placement.append(changePlacement(int(my_match_data_2['placement'])))
    placement = count_placement(duo_placement, 5)
    return placement

#Finds placement when user plays solo
def placement_list(user, user2, data): 
    placement_trend = []
    for match in data:
        if user2 not in match["metadata"]["participants"]:    
            my_match_data = match['info']['participants'][match['metadata']['participants'].index(user['puuid'])]
            placement_trend.append(int(my_match_data['placement']))
    return count_placement(placement_trend, 9)

if __name__ == "__main__": 
    #Put in your api developer key
    #Summoner ID and region (na1) - count = #number of games  
    #Note rate limits - increasing count increases the amount of requests:
        #20 requests every 1 seconds(s)
        #100 requests every 2 minutes(s)
    api_key = 'your_api_key'
    watcher = TftWatcher(api_key)
    my_region = 'your_region'
    summoner_name = 'your_summoner_name'
    me = watcher.summoner.by_name(my_region, summoner_name)
    matches_ids = watcher.match.by_puuid(my_region, me['puuid'], count=20) #<-count
    matches = [watcher.match.by_id(my_region, item) for item in matches_ids]
    print("*********************")
    print("Gathered user 1 data")
    print("*********************")

    #Friend Summoner ID - count = #number of games 
    summoner_name_friend = 'friend_summoner_name'
    friend = watcher.summoner.by_name(my_region, summoner_name_friend)
    friend_matches_ids = watcher.match.by_puuid(my_region, friend['puuid'], count=20) #<-count
    friend_matches = [watcher.match.by_id(my_region, item) for item in friend_matches_ids]
    print("Gathered user 2 data")
    print("*********************")

    #placement data
    me_id = me["puuid"]
    friend_id = friend['puuid']
    me_solo_placement_data = placement_list(me, friend_id, matches)
    friend_solo_placement_data = placement_list(friend, me_id, friend_matches)
    duo_placement_data = duo_placement_list(me, friend, matches)

    solo_placementTitles = ['first', 'second', 'third', 'fourth', 'fifth', 'sixth', 'seventh', 'eighth']
    duo_placementTitles = ['first', 'second', 'third', 'fourth']
    
    #remove placements with 0 occurrences
    me_solo_dictionary = dict(zip(solo_placementTitles, me_solo_placement_data))
    me_solo_dictionary = {x:y for x,y in me_solo_dictionary.items() if y!=0}

    friend_solo_dictionary = dict(zip(solo_placementTitles, friend_solo_placement_data))
    friend_solo_dictionary = {x:y for x,y in friend_solo_dictionary.items() if y!=0}

    duo_dictionary = dict(zip(duo_placementTitles, duo_placement_data))
    duo_dictionary = {x:y for x,y in duo_dictionary.items() if y!=0}

    print("Creating graphs")
    print("*********************")
    
    #creates donut graph
    title_colors = {'first': '#fc2403','second': '#fc9003','third': '#fcf003','fourth': '#5afc03', 'fifth': '#03fceb', 'sixth': '#0377fc', 'seventh': '#7b03fc', 'eighth': '#fc03df'}
    fig, (ax1, ax2, ax3) = plt.subplots(1, 3, figsize=(8, 8))
    ax1.set_title("Me Solo placement")
    ax2.set_title("Friend Solo Placement")
    ax3.set_title("Double Up Placement")
    inner_radius = 0.6
    chart_radius = 1
    wedge_props = dict(width=chart_radius-inner_radius)
    ax1.pie(me_solo_dictionary.values(), labels = me_solo_dictionary.keys(), colors = [title_colors[key] for key in me_solo_dictionary.keys()], autopct='%1.1f%%', counterclock=False, startangle=-270, radius=chart_radius, wedgeprops=wedge_props)
    ax2.pie(friend_solo_dictionary.values(), labels = friend_solo_dictionary.keys(), colors = [title_colors[key] for key in friend_solo_dictionary.keys()], autopct='%1.1f%%', counterclock=False, startangle=-270, radius=chart_radius, wedgeprops=wedge_props)
    ax3.pie(duo_dictionary.values(), labels = duo_dictionary.keys(), colors = [title_colors[key] for key in duo_dictionary.keys()], autopct='%1.1f%%', counterclock=False, startangle=-270, radius=chart_radius, wedgeprops=wedge_props)
    fig.tight_layout()
    plt.show()