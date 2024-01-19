#!/bin/bash
# touch setup.sh
# chmod +x ./setup.sh
# vim ./setup.sh
# v
# ctrl shift v ( paste this text in vim )
# esc
# :wq
# ./setup.sh

echo -e "\033[0;36m 🐢 🐢 🐢 🐢 🐢 🐢 🐢 🐢 🐢 \033[0m"

if [ -f .setup.env ]; then
    export $(cat .setup.env | xargs)
    echo -e "\033[0;36m LOADED ENV \033[0m"
else
    echo -e "\e[31m ESSENTIAL ENV VARIABLES NOT FOUND \e[31m"
fi

FILE="/etc/needrestart/needrestart.conf"

echo "\$nrconf{restart} = 'a';" | sudo tee -a "$FILE" > /dev/null

echo -e "\033[0;36m ${FILE} MODIFIED TO MAKE TERMINAL NO INTERACTIVE \033[0m"

echo -e "\033[0;36m INSTALLING THINGS \033[0m"

export DEBIAN_FRONTEND=noninteractive

sudo apt update

sudo apt install git python3 python3-pip python3.10-venv libgl1-mesa-glx tree -y -qq

unset DEBIAN_FRONTEND

git_version=$(git --version)
python_version=$(python3 --version)

echo -e "\033[0;36m GIT INSTALLED, VERSION IS ${git_version} 👍\033[0m"
echo -e "\033[0;36m PYTHON INSTALLED, VERSION IS ${python_version} 👍\033[0m"
echo -e "\033[0;36m INSTALLED libgl1-mesa-glx 👍  \033[0m"

git config --global credential.helper "store --file ~/.git-credentials"
git config --global user.name "${GIT_USERNAME}"
git config --global user.email "${GIT_EMAIL}"

echo "https://${GIT_USERNAME}:${GIT_TOKEN}@github.com" > ~/.git-credentials

echo -e "\033[0;36m GIT CREDENTIALS SETUP 👍\033[0m"

mkdir ipd

cd ipd

git clone https://github.com/catosaurusrex2003/IPD-backend.git

echo -e "\033[0;36m CLONED REPO 👍\033[0m"

cd IPD-backend

python3 -m venv env

source env/bin/activate

pip install torch torchvision torchaudio --index-url https://download.pytorch.org/whl/cpu

echo -e "\033[0;36m INSTALLED torch torchvision torchaudio for linux 🐢 \033[0m"

echo -e "\033[0;36m INSTALLING requirements.txt  \033[0m"

pip install -r requirements.txt

echo -e "\033[0;36m INSTALLED requirements.txt 👍  \033[0m"

cd sqs-poller

pip install gdown==4.7.3 loguru

echo -e "\033[0;36m INSTALLED gdown 👍  \033[0m"

gdown https://drive.google.com/drive/u/0/folders/1xkfY0NPG_JsD1t8oAVqW7eIZNYt7Yac2 -O models --folder

echo -e "\033[0;36m MODEL FOLDER DOWNLOADED 👍  \033[0m"

echo -e "\033[0;36m 🥳🥳🥳🥳🥳 EVERYTHING SETUP 🥳🥳🥳🥳🥳🥳🥳   \033[0m"

echo -e "\033[0;36m NOW RUNNING 🏃🏻 \033[0m"

python poller.py