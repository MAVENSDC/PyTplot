FROM gitpod/workspace-full-vnc
RUN sudo apt-get update && \
    sudo apt-get install -y libgtk-3-dev && \
    sudo rm -rf /var/lib/apt/lists/* \
    sudo apt-get install libxcb-xinerama0
RUN sudo apt-get -y install libsm6 
RUN sudo apt-get -y libxrender1 
RUN sudo apt-get -y libfontconfig1 
RUN sudo apt-get -y libxcomposite-dev 
RUN sudo apt-get -y libxcursor1 
RUN sudo apt-get -y libxi6 
RUN sudo apt-get -y libxtst6 
RUN sudo apt-get -y libxrandr2 
RUN sudo apt-get -y libasound2 
RUN sudo apt-get -y libegl1
RUN sudo apt-get -y install xvfb
RUN sudo apt-get -y install libgl1-mesa-glx