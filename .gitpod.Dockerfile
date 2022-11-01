FROM gitpod/workspace-full-vnc
RUN sudo apt-get update && \
    sudo apt-get install -y libgtk-3-dev && \
    sudo rm -rf /var/lib/apt/lists/* \
    sudo apt-get install -y libxcb-xinerama0
RUN sudo apt-get install -y libsm6 
RUN sudo apt-get install -y libxcb-util-dev
RUN sudo apt-get install -y libXrender
RUN sudo apt-get install -y libxcb-render
RUN sudo apt-get install -y libxcb-render-util
RUN sudo apt-get install -y libxcb-randr
RUN sudo apt-get install -y libxcb-shape
RUN sudo apt-get install -y libxcb-sync
RUN sudo apt-get install -y libxcb-xfixes
RUN sudo apt-get install -y libxcb-icccm
RUN sudo apt-get install -y libxcb-shm
RUN sudo apt-get install -y libxcb-image
RUN sudo apt-get install -y libxcb-keysyms
RUN sudo apt-get install -y libxkbcommon
RUN sudo apt-get install -y libxkbcommon-x11
RUN sudo apt-get install -y libfontconfig
RUN sudo apt-get install -y libfreetype
RUN sudo apt-get install -y libXext
RUN sudo apt-get install -y libxcb
RUN sudo apt-get install -y libX11
RUN sudo apt-get install -y libSM
RUN sudo apt-get install -y libICE
RUN sudo apt-get install -y libglib-2.0
RUN sudo apt-get install -y libpthread