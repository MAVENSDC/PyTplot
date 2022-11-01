FROM gitpod/workspace-full-vnc
RUN sudo apt-get update && \
    sudo apt-get install -y libgtk-3-dev && \
    sudo rm -rf /var/lib/apt/lists/* \
    sudo apt-get install libxcb-xinerama0
RUN sudo apt-get -y install libsm6 
RUN sudo apt-get install libxcb-util-dev
RUN sudo apt-get install libXrender
RUN sudo apt-get install libxcb-render
RUN sudo apt-get install libxcb-render-util
RUN sudo apt-get install libxcb-randr
RUN sudo apt-get install libxcb-shape
RUN sudo apt-get install libxcb-sync
RUN sudo apt-get install libxcb-xfixes
RUN sudo apt-get install libxcb-icccm
RUN sudo apt-get install libxcb-shm
RUN sudo apt-get install libxcb-image
RUN sudo apt-get install libxcb-keysyms
RUN sudo apt-get install libxkbcommon
RUN sudo apt-get install libxkbcommon-x11
RUN sudo apt-get install libfontconfig
RUN sudo apt-get install libfreetype
RUN sudo apt-get install libXext
RUN sudo apt-get install libxcb
RUN sudo apt-get install libX11
RUN sudo apt-get install libSM
RUN sudo apt-get install libICE
RUN sudo apt-get install libglib-2.0
RUN sudo apt-get install libpthread