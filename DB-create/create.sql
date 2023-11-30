-- SQL for postgresql database table creation
-- Create database 'MultimediaDB' and use the following to create the table

CREATE TABLE
IF NOT EXISTS video_data
(
    id SERIAL PRIMARY KEY,
    video_num INTEGER NOT NULL,
    codec_type VARCHAR
(10) NOT NULL,
    stream_index INTEGER NOT NULL,
    pts INTEGER NOT NULL,
    pts_time INTERVAL,
    dts INTEGER NOT NULL,
    dts_time INTERVAL,
    duration INTEGER NOT NULL,
    duration_time INTERVAL,
    size VARCHAR
(10),
    pos VARCHAR
(10),
    flags VARCHAR
(3),
    data_hash VARCHAR
(50) NOT NULL
);

CREATE INDEX idx_data_hash ON video_data (data_hash);

-- Change data types to VARCHAR
ALTER TABLE video_data
ALTER COLUMN codec_type TYPE
VARCHAR
(50),
ALTER COLUMN stream_index TYPE VARCHAR
(10),
ALTER COLUMN pts TYPE VARCHAR
(20),
ALTER COLUMN pts_time TYPE VARCHAR
(20),
ALTER COLUMN dts TYPE VARCHAR
(20),
ALTER COLUMN dts_time TYPE VARCHAR
(20),
ALTER COLUMN duration TYPE VARCHAR
(20),
ALTER COLUMN duration_time TYPE VARCHAR
(20),
ALTER COLUMN size TYPE VARCHAR
(10),
ALTER COLUMN pos TYPE VARCHAR
(10),
ALTER COLUMN flags TYPE VARCHAR
(10),
ALTER COLUMN data_hash TYPE VARCHAR
(50),
ALTER COLUMN video_num TYPE VARCHAR
(10);



Select *
from video_data;