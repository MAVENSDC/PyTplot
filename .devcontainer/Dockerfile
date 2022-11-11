# OS
ARG VARIANT=bullseye
FROM --platform=linux/amd64 mcr.microsoft.com/vscode/devcontainers/base:0-${VARIANT}
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
RUN sudo apt-get install -y python3
RUN sudo apt-get install -y python3-pip
RUN pip install pyspedas