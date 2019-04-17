# This script pulls relevant info for Ninja's Twitch account, 
# specifically his New Year's Eve event.

###############
# PREREQUISITES
###############
# This section covers things you need to do before this script will work.

# Install Python Twitch API: pip install python-twitch-client

# To get OAuth token, see: https://github.com/tsifrer/python-twitch-client/issues/12
# To see possible scopes, see: https://dev.twitch.tv/docs/authentication/#scopes

# Here's my OAuth code that has (most) Twitch API v5 scopes:
# Scopes: user_subscriptions user_read user_follows_edit user_blocks_read user_blocks_edit openid communities_moderate communities_edit collections_edit chat_login channel_subscriptions channel_stream channel_read channel_feed_read channel_check_subscription channel_commercial channel_editor channel_feed_edit
# Is this even needed?

# Here's my OAuth code that has all new Twitch API scopes:
# Scopes: user:read:email user:read:broadcast user:edit:broadcast user:edit analytics:read:extensions analytics:read:games bits:read clips:edit
# kheftmy6d7dbzecqkmu7e7b2fc92za

##################
# IMPORT LIBRARIES
##################
import urllib
import simplejson as json

import pandas as pd                # allows use of data frame structure
import numpy as np
import datetime                    # allows me to get current timestamp
import time                        # allows me to make the program wait
 
from twitch import TwitchClient    # Twitch API library

#############
# GET USER ID
#############
# Ninja's username is "Ninja".
# This section gets his numeric ID.

# You will need your client ID and OAuth.
# Use the link above to find the OAuth.

# Specify username.
user_name = "Ninja"

# Specify URL.
url = "https://api.twitch.tv/helix/users?login=" + user_name

# Create URL request.
channel_id = urllib.request.Request(url)

# Add client ID and OAuth to request.
channel_id.add_header("Client-ID", 's4tqt4ku0piu2e0yayw6k08l7851qo')
channel_id.add_header("Authorization", "OAuth " + "kheftmy6d7dbzecqkmu7e7b2fc92za")

# Get info from request.
response = urllib.request.urlopen(channel_id)
json_output = json.loads(response.read())

# Get user ID.
user_id = json_output['data'][0]['id']

###########################
# PULL DATA FROM TWITCH API
###########################
# This section pulls relevant data from Ninja's Twitch account.
# It's designed to pull once an hour for ~12-13 hours and 
# generate a CSV results file.

# Create empty data frame.
results = pd.DataFrame(columns = ['time', 'total_views', 'stream_viewers'])

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
    
    # Get livestream viewer data
    
    # Specify URL.
    stream_url = "https://api.twitch.tv/helix/streams?user_login=" + user_name
    
    # Create URL request.
    channel_id = urllib.request.Request(stream_url)
    
    # Add client ID and OAuth to request.
    channel_id.add_header("Client-ID", 's4tqt4ku0piu2e0yayw6k08l7851qo')
    channel_id.add_header("Authorization", "OAuth " + "kheftmy6d7dbzecqkmu7e7b2fc92za")
    
    # Get data.
    response = urllib.request.urlopen(channel_id)
    json_output = json.loads(response.read())
    
    # "json_output" will only have info if a live stream is going on!
    if len(json_output['data']) == 0:
        stream_viewers = np.nan
    else:
        stream_viewers = json_output['data'][0]['viewer_count']
    
    # Generate new row to add to "results"
    to_add = pd.DataFrame({'time': [datetime.datetime.now()], 
                           'total_views': channel.views, 
                           'stream_viewers': stream_viewers})
    
    # Add new row to "results".
    results = results.append(to_add)
    del(to_add)
    
    # Export CSV
    results.to_csv("ninja_twitch_pull.csv")
    
    # Wait before next loop iteration
    #time.sleep(60 * 60)                 # Wait one hour
    time.sleep(3600)
    
