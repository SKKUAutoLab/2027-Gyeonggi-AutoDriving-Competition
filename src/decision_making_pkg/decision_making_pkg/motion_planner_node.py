import rclpy
from rclpy.node import Node
from rclpy.qos import QoSProfile
from rclpy.qos import QoSHistoryPolicy
from rclpy.qos import QoSDurabilityPolicy
from rclpy.qos import QoSReliabilityPolicy

from interfaces_pkg.msg import PathPlanningResult, MotionCommand
from .lib import decision_making_func_lib as DMFL

#---------------Variable Setting---------------
SUB_PATH_TOPIC_NAME = "path_planning_result"
PUB_TOPIC_NAME = "topic_control_signal"

#----------------------------------------------

# 모션 플랜 발행 주기 (초) - 소수점 필요 (int형은 반영되지 않음)
TIMER = 0.1

class MotionPlanningNode(Node):
    def __init__(self):
        super().__init__('motion_planner_node')

        # 토픽 이름 설정
        self.sub_path_topic = self.declare_parameter('sub_lane_topic', SUB_PATH_TOPIC_NAME).value
        self.pub_topic = self.declare_parameter('pub_topic', PUB_TOPIC_NAME).value
        
        self.timer_period = self.declare_parameter('timer', TIMER).value

        # QoS 설정
        self.qos_profile = QoSProfile(
            reliability=QoSReliabilityPolicy.RELIABLE,
            history=QoSHistoryPolicy.KEEP_LAST,
            durability=QoSDurabilityPolicy.VOLATILE,
            depth=1
        )

        # 변수 초기화
        self.path_data = None

        self.steering_command = 0
        self.left_speed_command = 0
        self.right_speed_command = 0
        

        # 서브스크라이버 설정
        self.path_sub = self.create_subscription(PathPlanningResult, self.sub_path_topic, self.path_callback, self.qos_profile)

        # 퍼블리셔 설정
        self.publisher = self.create_publisher(MotionCommand, self.pub_topic, self.qos_profile)

        # 타이머 설정
        self.timer = self.create_timer(self.timer_period, self.timer_callback)

    def path_callback(self, msg: PathPlanningResult):
        self.path_data = list(zip(msg.x_points, msg.y_points))
        
    def timer_callback(self):

        if self.path_data is None:
            self.steering_command = 0
        else:
            target_slope = DMFL.calculate_slope_between_points(self.path_data[-10], self.path_data[-1])
            
            if target_slope > 0:
                self.steering_command =  7 # 예시 조향 값 (7이 최대 조향) 
            elif target_slope < 0:
                self.steering_command =  -7
            else:
                self.steering_command = 0


        self.left_speed_command = 100  # 예시 속도 값 (255가 최대 속도)
        self.right_speed_command = 100  # 예시 속도 값 (255가 최대 속도)



        self.get_logger().info(f"steering: {self.steering_command}, " 
                               f"left_speed: {self.left_speed_command}, " 
                               f"right_speed: {self.right_speed_command}")

        # 모션 명령 메시지 생성 및 퍼블리시
        motion_command_msg = MotionCommand()
        motion_command_msg.steering = self.steering_command
        motion_command_msg.left_speed = self.left_speed_command
        motion_command_msg.right_speed = self.right_speed_command
        self.publisher.publish(motion_command_msg)

def main(args=None):
    rclpy.init(args=args)
    node = MotionPlanningNode()
    try:
        rclpy.spin(node)
    except KeyboardInterrupt:
        print("\n\nshutdown\n\n")
    finally:
        node.destroy_node()
        rclpy.shutdown()

if __name__ == '__main__':
    main()
