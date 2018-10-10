# maprrtsp2stream
Take a Real Time Streaming Protocol (RTSP) feed and put frames onto a MapR Stream Topic
----------
## Design
---------
This is designed to be somewhat simple in approach. Set some variables, build a container, create streams, run container/app, and then you have frames of a RTSP (IP Cameras etc) in MapR Streams for analysis.  


### Setup
---------
- Clone this Repository. 
- Copy env.list.template to env.list
- Now update env.list to reflect your MapR cluster, environment, and RTSP URL. Comments in the file should assist this process. If there are quests, please raise an issue and I will clarify. 
- Ensure that a ticket for your user is generated based on the location in env.list.   
- Now that things are set, build by running ./build.sh
- If things build correctly, now run ./mkstream.sh to create the stream volume, stream, and topic.  You will need access to maprcli. If you can't run that where you are, copy mkstream.sh and env.list to the system with maprcli to create the streams
- At this point you should be able to run the container via ./run.sh.  Essentially CD to $APP_HOME_POSIX and then cd ./code and run rtsp2stream.sh to run the app! 


### Output
--------
A basic consumer script that reads off the stream and saves to files is included for demo purposes at stream2file.py (run with stream2file.sh)

### Help/Troublshooting
---------
This should be fairly straight forward. If there are issues, or just unclear documenation, please raise issues and I will address!


