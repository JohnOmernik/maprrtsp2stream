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
from confluent_kafka import Consumer, KafkaError, version, libversion
import random

output_loc = "./test"
try:
    topic_frames =  os.environ["MAPR_STREAMS_STREAM_LOCATION"].replace('"', '') + ":" + os.environ["MAPR_STREAMS_TOPICS"].replace('"', '')
except:
    print("Error getting MAPR_STREAMS_STREAM_LOCATION and MAPR_STREAMS_TOPICS from env")
    sys.exit(1)


def main():
    print("Confluent Kafka Version: %s - Libversion: %s" % (version(), libversion()))
    print("")

    conf = {'group.id': 'img2file1', 'default.topic.config': {'auto.offset.reset': 'earliest'}}
    c = Consumer(conf)
    c.subscribe([topic_frames])

    running = True
    while running:
        msg = c.poll(timeout=1.0)
        if msg is None: continue
        if not msg.error():
            mymsg = json.loads(msg.value().decode('utf-8'), object_pairs_hook=OrderedDict)
            outmsg = OrderedDict()
            outmsg['ts'] = mymsg['ts']
            outmsg['epoch_ts'] = mymsg['epoch_ts']
            outmsg['cam_name'] = mymsg['cam_name']
            
            fileout = "%s/stream_%s_%s.jpg" % (output_loc, outmsg['cam_name'], outmsg['ts'].replace(" ", "_").replace(":", "_"))
            mybytes = base64.b64decode(mymsg['img'])
            print("Processing message: %s and saving to %s" % (outmsg, fileout))
            w = open(fileout, 'wb')
            w.write(mybytes)
            w.close()

        elif msg.error().code() != KafkaError._PARTITION_EOF:
            print(msg.error())
            running = False
    c.close()



if __name__ == '__main__':
    main()
