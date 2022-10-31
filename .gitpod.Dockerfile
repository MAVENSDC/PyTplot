FROM gitpod/workspace-full-vnc
RUN sudo apt-get update && \
    sudo apt-get install -y libgtk-3-dev && \
    sudo rm -rf /var/lib/apt/lists/* \
    sudo apt-get install libxcb-xinerama0
RUN sudo apt-get -y install libsm6 libxrender1 libfontconfig1 libxcomposite-dev libxcursor1 libxi6 libxtst6 libxss1 libxrandr2 libasound2 libegl1
RUN sudo apt-get -y install xvfb
RUN sudo apt-get -y install libgl1-mesa-glx