FROM pytorch/pytorch:1.8.1-cuda11.1-cudnn8-devel
MAINTAINER dev@synergyai.co

# fix NVIDIA gpg key error
RUN rm /etc/apt/sources.list.d/cuda.list
RUN rm /etc/apt/sources.list.d/nvidia-ml.list
RUN apt-key del 7fa2af80
RUN apt-get update && apt-get install -y --no-install-recommends wget
RUN wget https://developer.download.nvidia.com/compute/cuda/repos/ubuntu1804/x86_64/cuda-keyring_1.0-1_all.deb
RUN dpkg -i cuda-keyring_1.0-1_all.deb

# install dependencies(python3.8)
RUN apt-get update && \
    apt-get install --no-install-recommends -y \
    git python3.8 python3-pip python3.8-dev
RUN pip install -r ./requirements.txt
RUN apt-get -y install build-essential

CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "80"]