"""
retrieves data from instagram at a particular location, saves it in a pickle
Parameters:
    -latitude
    -longitude
    -outfile prefix (lat, lng, and date will be appended to this string)
Output:
    -a save file of retrieved posts and data about them
"""

from instagram.client import InstagramAPI
import sys
import pandas as pd
import datetime


def table_InstaData(mediaList, query_lat, query_lon):
    """
    returns a list of dictionaries to be converted to a dataframe,
    given a list of media objects from the instagram API
    """

     # initialize a list of dicts that will hold row data from this query
    l_of_d = []
    for media in mediaList:
        if media.type == 'image':
            text = ""
            tags = []

            try:
                text = media.caption.text
            except AttributeError:
                 text = ""

            try:
                 tags = media.tags
            except AttributeError:
                 tags = []

            l_of_d.append({"id":media.id,
                          "created_time":media.created_time,
                          "user":media.user.username,
                          "image_url":media.images['low_resolution'].url,
                          "caption":text,
                          "like_count":media.like_count,
                          "query_lat":query_lat,
                          "query_lon":query_lon,
                          "im_lat":media.location.point.latitude,
                          "im_lon":media.location.point.longitude,
                          "hashtags":tags})

    return l_of_d



def main(argv = None):
    if argv is None:
        argv = sys.argv

      #exit if there aren't enough arguments
    if len(argv) < 4:
        sys.exit("Please provide latitude and longitude")

      # Instagram-specific setup
    client_id = '5fdd1db38a6046d3a3a8447410a04ef0'
    client_secret = 'd6b81556c31b43148081c6ff0707763e'
    api = InstagramAPI(client_id=client_id, client_secret=client_secret)

      #find the latitude and longitude
    lat = argv[1]
    lng = argv[2]

      # get a list of posts at a particular location
    data = api.media_search(count=100, lat=lat, lng=lng)
    recent_Media = table_InstaData(data, lat, lng)

     # put the list and organized data into a dataframe
    df = pd.DataFrame(recent_Media)
    fname = argv[3] + "_" + str(lat) + "_" + str(lng) + "_" + str(datetime.date.today()) + ".pkl"

    df.to_pickle(fname)



if __name__ == '__main__':
    main()