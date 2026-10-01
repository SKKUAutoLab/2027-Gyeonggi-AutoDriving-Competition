import rclpy
from rclpy.node import Node
from sensor_msgs.msg import Image
import cv2
from cv_bridge import CvBridge
import os
import time

class ImageSaverNode(Node):
    def __init__(self):
        super().__init__('image_saver_node')
        self.subscription = self.create_subscription(
            Image,
            '/camera/image_raw',
            self.image_callback,
            10)
        self.bridge = CvBridge()
        self.save_dir = os.path.expanduser('~/ros2_saved_images')
        os.makedirs(self.save_dir, exist_ok=True)
        self.get_logger().info(f'이미지 저장 경로: {self.save_dir}')
    
    def image_callback(self, msg):
        try:
            cv_image = self.bridge.imgmsg_to_cv2(msg, desired_encoding='rgb8')
            timestamp = int(time.time() * 1000)  # 밀리초 단위 타임스탬프
            filename = os.path.join(self.save_dir, f'image_{timestamp}.png')
            cv2.imwrite(filename, cv_image)
            self.get_logger().info(f'이미지 저장 완료: {filename}')
        except Exception as e:
            self.get_logger().error(f'이미지 변환 또는 저장 오류: {e}')


def main(args=None):
    rclpy.init(args=args)
    node = ImageSaverNode()
    rclpy.spin(node)
    node.destroy_node()
    rclpy.shutdown()

if __name__ == '__main__':
    main()
