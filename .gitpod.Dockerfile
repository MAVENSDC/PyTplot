FROM gitpod/workspace-full-vnc
RUN sudo apt-get update
RUN sudo apt-get install -y libgtk-3-dev
RUN sudo apt-get install -y libxcb-xinerama0
RUN sudo apt-get install -y libsm6 
RUN sudo apt-get install -y libxcb-util-dev
RUN sudo apt-get install -y libXrender-dev
