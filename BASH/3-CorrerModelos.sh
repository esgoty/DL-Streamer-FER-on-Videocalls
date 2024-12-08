#!/bin/bash

# Variables
CONTAINER_NAME="NEWDLSTR"

#TAGS="TOM$(date +"%Y%m%d%H%M%S")"

# Get the current date and time
CURRENT_DATE=$(date +"%Y-%m-%d")
CURRENT_TIME=$(date +"%H-%M-%S")

# Create the TAGS variable in JSON format
TAGS='$(date +"%Y%m%d%H%M%S")'
#TAGS='$(date + "test-full-2")'

#COMMAND= echo 'gst-launch-1.0 \
#v4l2src device=/dev/video0 ! decodebin ! videoconvert n-threads=4 ! capsfilter caps="video/x-raw,format=BGRx" ! \
#gvadetect model=/home/RECURSOS_HOST/produccion/face/face-detection-adas-0001/FP32/face-detection-adas-0001.xml ! \
#gvaclassify model=/home/RECURSOS_HOST/produccion/emot/emotions-recognition-retail-0003/FP32/emotions-recognition-retail-0003.xml model-proc=/home/RECURSOS_HOST/produccion/emot/emotionsproc.json ! \
#	gvametaconvert json-indent=-1 tags='$TAGS' ! \
#	gvametapublish method=kafka file-format=json-lines address=localhost:9092 topic=dlstreamer ! fakesink sync=false '

COMMAND='gst-launch-1.0 \
	v4l2src device=/dev/video0 ! decodebin ! videoconvert n-threads=4 ! capsfilter caps="video/x-raw,format=BGRx" ! \
	gvadetect model=/home/RECURSOS_HOST/produccion/face/face-detection-adas-0001/FP32/face-detection-adas-0001.xml ! \
	gvaclassify model=/home/RECURSOS_HOST/produccion/emot/emotions-recognition-retail-0003/FP32/emotions-recognition-retail-0003.xml \
		model-proc=/home/RECURSOS_HOST/produccion/emot/emotionsproc.json ! \
	tee name=t  \
	t. ! queue ! \
		gvametaconvert json-indent=-1 tags='$TAGS' ! \
		gvametapublish method=kafka file-format=json-lines address=localhost:9092 topic=dlstreamer ! fakesink sync=false \
	t. ! queue ! \
		gvametaconvert json-indent=-1 tags='$TAGS' ! \
		gvametapublish method=file file-format=json-lines \
	      	file-path=/home/RECURSOS_HOST/thepep.json ! fakesink sync=false 
	'
		

# Function to start the Docker container
start_container() {
    echo "Starting the existing container ${CONTAINER_NAME}..."
    docker start "${CONTAINER_NAME}"
}

# Function to run a command inside the Docker container and keep the terminal open
run_command_and_open_shell() {
    echo "Running command in container ${CONTAINER_NAME} after sourcing .bashrc and keeping the terminal open..."
    docker exec -it "${CONTAINER_NAME}" /bin/bash -c "source ~/.bashrc && ${COMMAND}; /bin/bash"
}

# Function to stop the Docker container
stop_container() {
    echo "Stopping container ${CONTAINER_NAME}..."
    docker stop "${CONTAINER_NAME}"
}

# Trap function to stop the container when the script exits
trap stop_container EXIT

# Check if the container exists
if [ "$(docker ps -aq -f name=${CONTAINER_NAME})" ]; then
    # Check if the container is already running
    if [ "$(docker ps -q -f name=${CONTAINER_NAME})" ]; then
        echo "Container ${CONTAINER_NAME} is already running."
    else
        start_container
    fi
    # Run the specified command inside the container and keep the terminal open
    run_command_and_open_shell
else
    echo "Container ${CONTAINER_NAME} does not exist."
fi

