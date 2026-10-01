# 2027-Gyeonggi-AutoDriving-Competition
2027 경기도 대학생 자율주행 경진대회 온라인 교육

## 1. 초기 환경설정
```
git clone https://github.com/SKKUAutoLab/2027-Gyeonggi-AutoDriving-Competition.git
cd 2027-Gyeonggi-AutoDriving-Competition/
sh install.sh
source ~/.bashrc
```


## 2. 의존성 설치 (rosdep)
```
cd 2027-Gyeonggi-AutoDriving-Competition/
export AMENT_PREFIX_PATH=''
export CMAKE_PREFIX_PATH=''
source /opt/ros/humble/setup.bash
rosdep install -i --from-path src --rosdistro humble -y
```

## 3. 패키지 빌드
```
cd 2027-Gyeonggi-AutoDriving-Competition/
source /opt/ros/humble/setup.bash
colcon build --packages-select interfaces_pkg --allow-overriding interfaces_pkg 
source install/local_setup.bash

colcon build --symlink-install --packages-select camera_perception_pkg --allow-overriding camera_perception_pkg 
source install/local_setup.bash

colcon build --symlink-install --packages-select decision_making_pkg --allow-overriding decision_making_pkg 
source install/local_setup.bash

colcon build --symlink-install --packages-select debug_pkg --allow-overriding debug_pkg 
source install/local_setup.bash

colcon build --symlink-install --packages-select simulation_pkg --allow-overriding simulation_pkg
source install/local_setup.bash
```

## 4. 시뮬레이터 실행
```
cd 2027-Gyeonggi-AutoDriving-Competition/
sudo killall -9 gazebo gzserver gzclient; ros2 launch simulation_pkg driving_sim.launch.py
```


## 5. 과제 제출
시뮬레이션을 실행해서 차량이 한바퀴 주행하는 영상 촬영해서 eX-campus 과제 및 평가 탭에서 [온라인 과제 제출] 항목에 제출해주세요.
