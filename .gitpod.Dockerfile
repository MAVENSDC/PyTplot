FROM gitpod/workspace-full-vnc
RUN sudo apt-get update && \
    sudo apt-get install -y libgtk-3-dev && \
    sudo rm -rf /var/lib/apt/lists/* \
    sudo apt-get -y install libxcb-xinerama0
RUN sudo apt-get -y install libsm6 
RUN sudo apt-get -y install libxcb-util-dev
RUN sudo apt-get -y install libXrender
RUN sudo apt-get -y install libxcb-render
RUN sudo apt-get -y install libxcb-render-util
RUN sudo apt-get -y install libxcb-randr
RUN sudo apt-get -y install libxcb-shape
RUN sudo apt-get -y install libxcb-sync
RUN sudo apt-get -y install libxcb-xfixes
RUN sudo apt-get -y install libxcb-icccm
RUN sudo apt-get -y install libxcb-shm
RUN sudo apt-get -y install libxcb-image
RUN sudo apt-get -y install libxcb-keysyms
RUN sudo apt-get -y install libxkbcommon
RUN sudo apt-get -y install libxkbcommon-x11
RUN sudo apt-get -y install libfontconfig
RUN sudo apt-get -y install libfreetype
RUN sudo apt-get -y install libXext
RUN sudo apt-get -y install libxcb
RUN sudo apt-get -y install libX11
RUN sudo apt-get -y install libSM
RUN sudo apt-get -y install libICE
RUN sudo apt-get -y install libglib-2.0
RUN sudo apt-get -y install libpthread