# HOW TO RUN

    ## Database setup
        - In this project we use postgres as the database engine.
        - Create a database and name it 'MultimediaDB'.
        - Run the sql script inside '''/DB-create''' directory.
    ## Data population
        - Once the db table has been created, the next step is to process all the videos to be inserted into the database.
        - All videos are present in the '''/DB-populate/videos''' directory.
        - All videos must be named as videoX.mp4 where X is an integer value.
        - Run 
            ''' chmod +x generate-json
                ./generate-json '''
        - This generates json objects and adds them to the '''/DB-populate/videos_json''' directory.
        - Run
            ''' chmod +x insertAllVideos
                ./insertAllVideos '''
        - This inserts all the json objects to the database.
    ## Querying
        - Now the database is populated and ready to be queried.
        - Clear the '''queries/tesing''' directory and insert the video query.
        - Run 
            ''' chmod +x query
                ./query '''
        - This finds the video number and the starting time of the query clip in the video.
        - Uncomment line #61 in query.py to view the video in VLC player.
