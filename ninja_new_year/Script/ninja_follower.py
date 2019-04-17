import urllib
import simplejson as json

import pandas as pd                # allows use of data frame structure
import numpy as np
import datetime                    # allows me to get current timestamp
import time                        # allows me to make the program wait
 
from twitch import TwitchClient    # Twitch API library


# Specify username.19571641 is the user_id for Ninja
user_id = "19571641"

# Specify URL.
url = "https://api.twitch.tv/helix/users/follows?to_id=" + user_id

# Create URL request.
channel_id = urllib.request.Request(url)

# Add client ID and OAuth to request.
channel_id.add_header("Client-ID", 's4tqt4ku0piu2e0yayw6k08l7851qo')
channel_id.add_header("Authorization", "OAuth " + "kheftmy6d7dbzecqkmu7e7b2fc92za")

# Get info from request.
response = urllib.request.urlopen(channel_id)
json_output = json.loads(response.read())


# Create empty data frame.
results = pd.DataFrame(columns = ['time', 'follower_count'])

# Start loop
for i in range(24):
    
    # Print progress
    print('')
    print('Iteration:', i + 1)
    print('')
    
    # Get total views data
    
    # Create client.
    client = TwitchClient(client_id = 's4tqt4ku0piu2e0yayw6k08l7851qo')

    # Get channel.
    channel = client.channels.get_by_id(user_id)
    
    # Get follower count data
    
    # Specify URL.
    follower_url = "https://api.twitch.tv/helix/users/follows?to_id=" + user_id
    
    # Create URL request.
    channel_id = urllib.request.Request(follower_url)
    
    # Add client ID and OAuth to request.
    channel_id.add_header("Client-ID", 's4tqt4ku0piu2e0yayw6k08l7851qo')
    channel_id.add_header("Authorization", "OAuth " + "kheftmy6d7dbzecqkmu7e7b2fc92za")
    
    # Get data.
    response = urllib.request.urlopen(channel_id)
    json_output = json.loads(response.read())
    
    
    # telling where follower count is 
    follower_count = json_output['total']
    
    
    # Generate new row to add to "results"
    to_add = pd.DataFrame({'time': [datetime.datetime.now()], 
                           'follower_count': follower_count})
    
    # Add new row to "results".
    results = results.append(to_add)
    del(to_add)
    
    # Export CSV
    results.to_csv("ninja_follower_count.csv")
    
    # Wait before next loop iteration
    #time.sleep(60 * 60)                 # Wait one hour
    time.sleep(3600) #3600 for an hour
    
