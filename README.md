# Real-time emotion recognition on Intel DL Streamer


This repository contains the final project for SPAZ's CEIA final project.

# Preliminaries

    Install Ubuntu 22.05 LTS
    Install OBS studio
    Install Docker
    Download and run the INTEL DLSTREAMER docker image https://hub.docker.com/r/intel/dlstreamer (latest)
    Download and run the APACHE PINOT docker image https://hub.docker.com/r/apachepinot/pinot

# System statup

## Setup

    Database setup: 1-AltaDB.sh (Database creation), 2-AltaTablas.sh (Table creation)

## Per videocall instance

    Activate OBS virtual camera and select full screen
    Run the script 3-CorrerModelos.sh when the video call starts, stop the script when it ends.
    During model execution, run the script real_time_rev.0.py to see real-time metrics.
    After a call, run the script offline_report_rev.0.py to see the balance of a call

Important:
The bash scripts must be modified to reflect the directories where the scripts are saved and the names of the pinot and dlstremaer images.
