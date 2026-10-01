
#!/bin/bash

sudo apt-get update
sudo apt-get install -y python3-pip 


pip install opencv-python pyserial 
pip install ultralytics==8.2.69
pip install setuptools==58.2.0 
pip install pynput

sudo apt install gazebo
sudo apt install ros-humble-gazebo-ros-pkgs
sudo apt install ros-humble-xacro
sudo apt install ros-humble-gazebo-ros
sudo apt-get install ros-humble-gazebo-msgs
sudo apt-get install ros-humble-gazebo-plugins


pip install transformers
curl -s https://packagecloud.io/install/repositories/github/git-lfs/script.deb.sh | sudo bash
pip install huggingface_hub



SCRIPT_DIR="$(CDPATH= cd -- "$(dirname -- "$0")" && pwd)"

# cp -r "$SCRIPT_DIR/src/simulation_pkg/models/"* /home/$(whoami)/.gazebo/models
GAZEBO_DIR="/home/$(whoami)/.gazebo"
if [ -d "$GAZEBO_DIR" ]; then
    echo "" # .gazebo 폴더가 존재하는지 확인
else
    echo ".gazebo 폴더가 존재하지 않아 생성합니다."
    mkdir "$GAZEBO_DIR"
fi
MODELS_DIR="$GAZEBO_DIR/models"
if [ -d "$MODELS_DIR" ]; then
    echo "" # .gazebo/models 폴더가 존재하는지 확인
else
    echo "models 폴더가 존재하지 않아 생성합니다."
    mkdir "$MODELS_DIR"
fi


# 패키지 폴더의 모든 내용을 .gazebo/models 폴더로 복사
SOURCE_MODELS_DIR="$SCRIPT_DIR/src/simulation_pkg/models"
if [ -d "$SOURCE_MODELS_DIR" ]; then
    echo "$SOURCE_MODELS_DIR의 내용을 $MODELS_DIR로 복사합니다."
    cp -r "$SOURCE_MODELS_DIR/"* "$MODELS_DIR/"
else
    echo "$SOURCE_MODELS_DIR 폴더가 존재하지 않습니다."
fi



# .gazebo/models 폴더 안의 etc 폴더 삭제
if [ -d "$MODELS_DIR/etc" ]; then
    #echo "$MODELS_DIR/etc 폴더를 삭제합니다."
    rm -rf "$MODELS_DIR/etc"
else
    echo "$MODELS_DIR/etc 폴더가 존재하지 않습니다."
fi



# .bashrc에 기본 설정 추가
BASHRC_FILE="$HOME/.bashrc"

add_alias() {
    local alias_cmd="$1"
    if ! grep -q "$alias_cmd" "$BASHRC_FILE"; then
        echo "$alias_cmd" >> "$BASHRC_FILE"
        echo "'$alias_cmd'가 추가되었습니다."
    else
        echo "'$alias_cmd'가 이미 존재합니다."
    fi
}

if ! grep -q "export ROS_DOMAIN_ID=" "$BASHRC_FILE"; then
    echo "export ROS_DOMAIN_ID=0 # 0~232 사이의 숫자로 변경" >> "$BASHRC_FILE"
    echo "ROS_DOMAIN_ID 설정이 추가되었습니다."
else
    echo "ROS_DOMAIN_ID 설정이 이미 존재합니다."
fi

add_alias "alias MOVE='ros2 service call /go std_srvs/srv/SetBool \"{data: true}\"'"
add_alias "alias STOP='ros2 service call /go std_srvs/srv/SetBool \"{data: false}\"'"

if ! grep -q "qqq()" "$BASHRC_FILE"; then
    cat << 'EOF' >> "$BASHRC_FILE"
qqq() {
    PIDS=$(ps aux | grep '[g]zserver' | awk '{print $2}')

    for pid in $PIDS; do
        kill -9 $pid
    done
}
EOF
    echo "qqq 함수가 추가되었습니다."
else
    echo "qqq 함수가 이미 존재합니다."
fi

add_alias "alias bashrc='gedit ~/.bashrc'"
add_alias "alias ㅠㅁ녹ㅊ='gedit ~/.bashrc'"
add_alias "alias bashup='source ~/.bashrc'"
add_alias "alias ㅠㅁ노ㅕㅔ='source ~/.bashrc'"
add_alias "alias c='clear'"
add_alias "alias ㅊ='clear'"
add_alias "alias rma='rm -rf'"

echo "변경된 .bashrc를 적용합니다."
source "$HOME/.bashrc"
