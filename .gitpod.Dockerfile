FROM gitpod/workspace-full-vnc
RUN sudo apt-get update
RUN sudo apt-get install -y libgtk-3-dev
RUN sudo apt-get install -y libxcb-xinerama0
RUN sudo apt-get install -y libxcb-render-util0
RUN sudo apt-get install -y libxcb-randr0
RUN sudo apt-get install -y libxcb-shape0
RUN sudo apt-get install -y libxcb-icccm4
RUN sudo apt-get install -y libxcb-image0
RUN sudo apt-get install -y libxcb-keysyms1 
RUN sudo apt-get install -y libxkbcommon-x11-0
# The libraries below are not needed for pytplot to work as is, but are listed as requirements for PyQT5
# If things don't work, maybe try installing these
#RUN sudo apt-get install -y libfontconfig1
#RUN sudo apt-get install -y libfreetype6
#RUN sudo apt-get install -y libxext6
#RUN sudo apt-get install -y libxcb1
#RUN sudo apt-get install -y libx11-6
#RUN sudo apt-get install -y libice6
#RUN sudo apt-get install -y libglib2.0-0
#RUN sudo apt-get install -y libpthread-stubs0-dev
#RUN sudo apt-get install -y libsm6 
#RUN sudo apt-get install -y libxcb-util-dev
#RUN sudo apt-get install -y libxrender-dev
#RUN sudo apt-get install -y libxcb-render0
#RUN sudo apt-get install -y libxkbcommon0
#RUN sudo apt-get install -y libxcb-sync1
#RUN sudo apt-get install -y libxcb-xfixes0
#RUN sudo apt-get install -y libxcb-shm0
RUN sudo rm -rf /var/lib/apt/lists/*