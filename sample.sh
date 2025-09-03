#!/bin/sh

CAMERA=$1
DURATION=${2:-10}  # default 10 seconds

if [ "$CAMERA" = "cam1" ]; then
    DEVICE="/dev/video0"
elif [ "$CAMERA" = "cam2" ]; then
    DEVICE="/dev/video1"
else
    echo "Usage: $0 cam1|cam2 [duration]"
    exit 1
fi

OUTPUT="/data/local/tmp/${CAMERA}_output_$(date +%s).mp4"

/data/local/tmp/ffmpeg -f v4l2 -i $DEVICE -t $DURATION $OUTPUT
echo "Saved video to $OUTPUT"
