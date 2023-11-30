from connections import DbConnect
from dotenv import load_dotenv
import sys
import os
import json
import subprocess

load_dotenv()

dbInfo = {'db_name': os.environ.get('db_name'), 'db_user': os.environ.get('db_user'), 'db_host': os.environ.get(
    'db_host'), 'db_password': os.environ.get('db_password'), 'table_name': os.environ.get('table_name')}

conn = DbConnect(db_info=dbInfo)

# Given an array of json objects, find the first object where dts_time is 00:00.0
def findFirstFrame(data):
    for i in range(len(data)):
        if data[i]['dts_time'] == '0:00:00.000000':
            return i

# Given the hash of the first frame, fetch the record of the first frame in the database
def getFirstFrameRecord(hash):
    query = """
        SELECT video_num,dts_time
        FROM video_data
        WHERE data_hash = %s;
    """
    conn.cur.execute(query, (hash,))
    return conn.cur.fetchone()


try:
    conn.connect_to_db()
except Exception as e:
    raise ValueError(f"Error inserting data {str(e)}") from e

file_name = sys.argv[1]
f= open(file_name,"r")
data = json.load(f)

firstFrame = findFirstFrame(data['packets'])
firstFrameHash = data['packets'][firstFrame]['data_hash']
firstFrameRecord = getFirstFrameRecord(firstFrameHash)
video_path = f"../ffprobe-parse/videos/video{firstFrameRecord[0]}.mp4"

print(firstFrameRecord)

time_str = firstFrameRecord[1]

time_parts = time_str.split(':')
hours = int(time_parts[0])
minutes = int(time_parts[1])
seconds_and_micro = time_parts[2].split('.')
seconds = int(seconds_and_micro[0])
microseconds = int(seconds_and_micro[1]) if len(seconds_and_micro) > 1 else 0

# Calculate the total duration in seconds
total_seconds = hours * 3600 + minutes * 60 + seconds + microseconds / 1e6

# Play the video in VLC
# subprocess.run(["vlc", video_path, "--start-time", str(total_seconds)])

print(video_path, total_seconds, time_str)
