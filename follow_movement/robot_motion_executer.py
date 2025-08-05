import time
import threading
from unitree_sdk2py.go2.sport.sport_client import SportClient
from unitree_sdk2py.go2.obstacles_avoid.obstacles_avoid_client import ObstaclesAvoidClient
from movement_controller import MovementController
from capture_image import take_picture
from object_detection import detect_objects


class RobotMotionExecutor:
    def __init__(self, state_manager):
        self.state_manager = state_manager
        self.movement = MovementController(state_manager)
        self.client = SportClient()
        self.obstacle_client = ObstaclesAvoidClient()
        self.client.SetTimeout(10.0)
        self.client.Init()
        self.obstacle_client.Init()
        self.obstacle_client.UseRemoteCommandFromApi(True)


    def move_based_on_remote(self, duration):
        print(f"Starting movement for {duration:.2f} seconds...")
        self.obstacle_client.SwitchSet(True)

        initial_yaw = self.state_manager.remote_state.yaw_est
        last_position = self.movement.get_relative_position()
        print(f"Initial Yaw: {initial_yaw:.2f}, Initial Position: {last_position}")

        start_time = time.time()
        stop_detection = threading.Event()

        # ✅ Detection thread function
        def detect_loop():
            while not stop_detection.is_set():
                try:
                    if take_picture("frame.jpg"):
                        found = detect_objects("frame.jpg")
                        if "person" in found:
                            print("🐶 person detected!")
                            self.client.stretch()
                except Exception as e:
                    print(f"[Detection error] {e}")
                time.sleep(2.0)  # Run every 2 seconds

        # ✅ Start detection thread
        detection_thread = threading.Thread(target=detect_loop)
        detection_thread.start()

        try:
            while time.time() - start_time < duration:
                current_position = self.movement.get_relative_position()
                if current_position != last_position:
                    print(f"Remote switched from {last_position} to {current_position}!")
                    last_position = current_position

                linear_speed, angular_speed, current_yaw = self.movement.compute_movement(initial_yaw)

                print(f"Current Yaw: {current_yaw:.2f}, Target Yaw: {initial_yaw:.2f}, "
                    f"Yaw Difference: {current_yaw - initial_yaw:.2f}")

                self.obstacle_client.Move(linear_speed, 0.0, angular_speed)
                time.sleep(0.05)

        finally:
            stop_detection.set()
            detection_thread.join()
            self.cleanup()


    def cleanup(self):
        print("Cleaning up...")
        self.client.StopMove()
        self.obstacle_client.SwitchSet(False)
        self.obstacle_client.UseRemoteCommandFromApi(False)
        print("Robot stopped and obstacle avoidance disabled.")
