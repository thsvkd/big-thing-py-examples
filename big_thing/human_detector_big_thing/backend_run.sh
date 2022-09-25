if [ ! -d "./jetson-inference/data/networks/SSD-Mobilenet-v2" ]; then
    cd jetson-inference/tools
    ./download-models.sh
fi

./detectnet_cus.py /dev/video0
