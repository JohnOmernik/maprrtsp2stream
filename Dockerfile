FROM maprpaccstreams

# The mkdir on /tmp is something weird from building maprpaccstreams
RUN  mkdir -p /tmp  && chmod 1777 /tmp &&  apt-get update && apt-get -y install libsm6 libxrender1 libfontconfig1 && rm -rf /var/lib/apt/lists/*

RUN pip3 install opencv-python

CMD ["/bin/bash"]
