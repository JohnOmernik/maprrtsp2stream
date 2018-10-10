#!/usr/bin/python3

import cv2
import json
import os
import sys
import time
import requests
import pprint
from collections import OrderedDict
import datetime
import base64
import confluent_kafka
from confluent_kafka import Producer, KafkaError, version, libversion
import random


try:
    topic_frames =  os.environ["MAPR_STREAMS_STREAM_LOCATION"].replace('"', '') + ":" + os.environ["MAPR_STREAMS_TOPICS"].replace('"', '')
except:
    print("Error getting MAPR_STREAMS_STREAM_LOCATION and MAPR_STREAMS_TOPICS from env")
    sys.exit(1)

try:
    rtsp_url = os.environ["APP_RTSP_URL"].replace('"', '')
except:
    print("You must provide a APP_RTSP_URL to connect to for video")
    sys.exit(1)

try:
    skipframes = int(os.environ["APP_SKIP_FRAMES"].replace('"', ''))
except:
    print("Number of frames to skip between saves not provided in APP_SKIP_FRAMES - defaulting to 30")
    skipframes = 30

try:
    capmax = int(os.environ["APP_CAP_MAX"].replace('"', ''))
except:
    print("Number of max capture frames not provided in APP_CAP_MAX defaulting to -1 (unlimted)")
    capmax = -1 

try:
    cam_name = os.environ["APP_CAM_NAME"].replace('"', '')
except:
    print("You must specify a camera name to go with the written records in ENV Var APP_CAM_NAME")
    sys.exit(1)

def main():
    print("Confluent Kafka Version: %s - Libversion: %s" % (version(), libversion()))
    print("")
    print("Connecting to RTSP: %s" % rtsp_url)
    print("")
    print("Producing video frames to: %s" % topic_frames)
    print("")
    print("Skipping every %s frames and then saving up to %s (-1 is unlimited) frames" % (skipframes, capmax))
    print("")


    p = Producer({'bootstrap.servers': '', 'message.max.bytes':'2978246'})

    output_loc = "./test"
    capcount = 0
    cap = cv2.VideoCapture(rtsp_url)
    while capcount < capmax or capmax == -1:
        ret, frame = cap.read()
        if capcount % skipframes == 0:
            curtime = datetime.datetime.now()
            mystrtime = curtime.strftime("%Y-%m-%d %H:%M:%S")
            epochtime = int(time.time())


            print("Saving to Stream  at %s" % capcount)
            img_str = cv2.imencode('.jpg', frame)[1].tostring()
            encdata = base64.b64encode(img_str)
            encdatastr = encdata.decode('utf-8')

            myrec = OrderedDict()
            myrec['ts'] = mystrtime
            myrec['epoch_ts'] = epochtime
            myrec['cam_name'] = cam_name
            myrec['img'] = encdatastr

            produceMessage(p, topic_frames, json.dumps(myrec))

            # This is more verbose method of writing so we can get raw bytes to save to a stream 
#            w = open(output_loc + "/cap_test_%s.jpg" % capcount, 'wb')
#            w.write(img_str)
#            w.close()

            # This is the prefered method for writing to a file from OpenCV, I am using theimencode so I can get the byte to write directly to MapR Streams
#            cv2.imwrite(output_loc + "/cap_%s.jpg" % (capcount), frame)
        capcount += 1
        if capcount >= 10000000:
            if capcount % skipframe == 0:
                capcount = 0


def produceMessage(p, topic, message_json):
    try:
        p.produce(topic, value=message_json, callback=delivery_callback)
        p.poll(0)
    except BufferError as e:
        print("Buffer full, waiting for free space on the queue")
        p.poll(10)
        p.produce(topic, value=message_json,callback=delivery_callback)
    except KeyboardInterrupt:
        print("\n\nExiting per User Request")
        p.close()
        sys.exit(0)

def delivery_callback(err, msg):
    """ Called once for each message produced to indicate delivery result.
        Triggered by poll() or flush(). """
    if err is not None:
        print('Message delivery failed to %s failed: %s' % (msg.topic(), err))
    else:
        pass





if __name__ == '__main__':
    main()
