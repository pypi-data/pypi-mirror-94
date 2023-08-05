The idea of repository based on https://github.com/chaserhkj/PyMajSoul/

Python wrappers for Majsoul allow you to interact with their servers from Python scripts.

## For User

1. Install python packages from `requerements.txt`
2. `python example.py -u username -p password`

This example is working only with **Python3.7+**.

Also, you need to have a Chinese account to run this example, because only accounts from these servers has the ability to login with login and password.

If you want to login to EN or JP servers you need to write your code to authenticate via email code or social network. Protobuf wrapper from this repository contains all needed API objects.

## For Developer

### Requirements

1. Install python packages from `requerements.txt`
1. Install protobuf compiler `sudo apt install protobuf-compiler`

### How to update protocol files to the new version

It was tested on Ubuntu.

1. Download the new `liqi.json` file (find it in the network tab of your browser) and put it to `ms/liqi.json`
1. `python generate_proto_file.py`
1. `protoc --python_out=plugins=grpc:. protocol.proto`
1. `chmod +x ms-plugin.py`
1. `sudo cp ms-plugin.py /usr/bin/ms-plugin.py`
1. `protoc --custom_out=. --plugin=protoc-gen-custom=ms-plugin.py ./protocol.proto`