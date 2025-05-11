# Real-time Emotion Recognition on Intel DL Streamer

![Python](https://img.shields.io/badge/python-3670A0?style=for-the-badge&logo=python&logoColor=ffdd54)
![Intel DL Streamer](https://img.shields.io/badge/Intel%20DL%20Stremer-%23d9ead3.svg?style=for-the-badge&logo=intel&logoColor=blue)
![Apache Pinot](https://img.shields.io/badge/Apache%20Pinot-green.svg?style=for-the-badge&logo=apache&logoColor=white)
![Apache Kafka](https://img.shields.io/badge/Apache%20kafka-%23FF6F00.svg?style=for-the-badge&logo=apachekafka&logoColor=white)
![Streamlit](https://img.shields.io/badge/Streamlit-017CEE?style=for-the-badge&logo=streamlit&logoColor=#FF4B4B)
![Linux](https://img.shields.io/badge/Linux-grey?style=for-the-badge&logo=ubuntu&logoColor=white)
![Docker](https://img.shields.io/badge/Docker-%23150458.svg?style=for-the-badge&logo=docker&logoColor=white)


This repository contains an implementation of real-time facial emotion recognition on video calls using Intel DL Streamer (for inference and video pipelines), Apache Pinot (for saving inference results), and Streamlit & Tkinter (for metrics and dashboarding).

# Preliminaries

* Install Ubuntu 22.04 LTS
* Install OBS Studio
* Install Docker
* Download and run the Intel DL Streamer Docker image from [https://hub.docker.com/r/intel/dlstreamer](https://hub.docker.com/r/intel/dlstreamer) (latest)
* Download and run the Apache Pinot Docker image from [https://hub.docker.com/r/apachepinot/pinot](https://hub.docker.com/r/apachepinot/pinot) (latest)

# System Startup

## Setup

* Database setup:
    1.  `1-AltaDB.sh` (Database creation)
    2.  `2-AltaTablas.sh` (Table creation)

## Per Video Call Instance

* Activate the OBS virtual camera and select full screen.
* Run the script `3-CorrerModelos.sh` when the video call starts, and stop the script when it ends.
* During model execution, run the script `real_time_rev.0.py` to see real-time metrics.
* After a call, run the script `offline_report_rev.0.py` to see the summary of the call.

**Important:**

The bash scripts must be modified to reflect the directories where the scripts are saved and the names of the Pinot and DL Streamer images.

