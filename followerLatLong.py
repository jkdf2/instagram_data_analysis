#!/usr/local/bin/python
# Application by Taylor Kline
# Gathers lat / long info on follwers from their most recently posted picture.
# Setting variables in ALL_CAPS is your responsibility.
from instagram.client import InstagramAPI
import os
from time import sleep
from time import localtime

# reads access token from specified line in keyFile
ACCESS_TOKEN_LINE=1
keyFilename = 'keys'
keyFile = open(keyFilename, 'r')
for x in range (0,ACCESS_TOKEN_LINE-1):
    keyFile.readline()
access_token = keyFile.readline().rstrip()

# user specified variables to influence search
USERNAME = 'thelinq'
MAXPAGES = 3 #maximum number of approximately 100-user pages to process
# Note: This number is approximate, as some pages do not have the full 100 users

# output file to be used for html output and opened in web browser
currentTime = str(localtime().tm_year) + '-' + str(localtime().tm_mon) + '-' + str(localtime().tm_mday) + '-' + str(localtime().tm_hour) + '-' + str(localtime().tm_sec)
outputFilename = 'output_' + USERNAME + '_' + currentTime +  '.dat'
outputDirectory = os.path.dirname(os.path.realpath(__file__)) + '/LatLongData/'
try:
        os.makedirs(outputDirectory)
except OSError as exception:
    if exception.errno != errno.EEXIST:
        raise
outputFile = open(os.path.join(outputDirectory, outputFilename), 'w')

# initiate the api
api = InstagramAPI(access_token=access_token)

# track how many users we could get location from
privateUsers = 0
publicUsers = 0

# accepts a userID and gets the last location of the user based on recent photo, if available
"""
Example lat/long search:
print api.media('762502306767443277_398424740').location.point.latitude
print api.media('762502306767443277_398424740').location.point.longitude
"""
def getLastLocation(userID):
    global privateUsers
    global publicUsers
    try:
        userFeed = api.user_recent_media(user_id=userID)[0]
        publicUsers += 1
        print api.media(userFeed[0].id).location.point
        #TODO: try checking lat/long of older pictures if [0] doesn't have location
    except Exception as e:
        #print e
        print "User is set to private."
        privateUsers += 1

# Determines the userID from the username given
userID = api.user_search(USERNAME)[0].id

# Get each follower of the user
followers, nextURL = api.user_followed_by(count = 100, user_id=userID) #count max is 100
totalFollowers = list(followers)
counter = 1

while nextURL and counter < (MAXPAGES): #paginate until there are no more URLs or counter limit is hit
    followers, nextURL = api.user_followed_by(count = 100, user_id=userID, with_next_url=nextURL)
    totalFollowers += list(followers)
    counter += 1
totalFollowers = tuple(totalFollowers) #convert back to immutable tuple
print "Found " + str(len(totalFollowers)) + " followers."
print "Finding most recent Lat/Long of each follower."
sleep(4)

# Now that we've got the followers, find their most recent photo
for eachFollower in totalFollowers:
    getLastLocation(eachFollower.id)
print publicUsers + " have location enabled and " + privateUsers + " followers have no location."

#TODO: Print out stats of how many followers there are vs how much location data is available