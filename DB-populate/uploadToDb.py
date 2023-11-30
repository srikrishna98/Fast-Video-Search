from connections import DbConnect
from dotenv import load_dotenv
import sys
import os
import json
import re

load_dotenv()

dbInfo = {'db_name': os.environ.get('db_name'), 'db_user': os.environ.get('db_user'), 'db_host': os.environ.get(
    'db_host'), 'db_password': os.environ.get('db_password'), 'table_name': os.environ.get('table_name')}

conn = DbConnect(db_info=dbInfo)


def doInsert(insert_data):
    print(f"Inserting data: {insert_data['pos']}")
    insert_query = """
        INSERT INTO video_data (
            codec_type, stream_index, pts, pts_time, dts, dts_time,
            duration, duration_time, size, pos, flags, data_hash, video_num
        ) VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s);
    """
    conn.cur.execute(insert_query, (
        insert_data['codec_type'],
        insert_data['stream_index'],
        insert_data['pts'],
        insert_data['pts_time'],
        insert_data['dts'],
        insert_data['dts_time'],
        insert_data['duration'],
        insert_data['duration_time'],
        insert_data['size'],
        insert_data['pos'],
        insert_data['flags'],
        insert_data['data_hash'],
        insert_data['video_num']
    ))

try:
    conn.connect_to_db()
except Exception as e:
    raise ValueError(f"Error inserting data {str(e)}") from e

file_name = sys.argv[1]
f= open(file_name,"r")
data = json.load(f)

if match := re.search(r'video(\d+)', file_name):
    video_num = match[1]
for insert_data in data['packets']:
    insert_data['video_num'] = video_num
    doInsert(insert_data)

conn.conn.commit()
conn.conn.close()


