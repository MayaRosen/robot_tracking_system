import math

class MovementController:
    def __init__(self, state_manager):
        self.state_manager = state_manager

    def get_relative_position(self):
        robot_yaw = 0.0
        remote_yaw = self.state_manager.remote_state.yaw_est
        relative_yaw = (remote_yaw - robot_yaw) % (2 * math.pi)
        if relative_yaw > math.pi:
            relative_yaw -= 2 * math.pi
        return "front" if abs(relative_yaw) < math.pi / 2 else "back"

    def compute_movement(self, initial_yaw, target_distance=0.65, max_speed=0.6, max_rotation_speed=0.6, yaw_threshold=0.25):
        state = self.state_manager.remote_state
        current_distance = max(0, state.distance_est - 0.5)
        orientation = state.orientation_est
        current_yaw = state.yaw_est

        yaw_difference = current_yaw - initial_yaw

        if orientation > 2:
            linear_speed = (
                max_speed if current_distance < target_distance - 0.1
                else -max_speed if current_distance > target_distance + 0.1
                else 0.0
            )
        else:
            linear_speed = max_speed

        angular_speed = (
            max_rotation_speed * (1 if yaw_difference > 0 else -1)
            if abs(yaw_difference) > yaw_threshold else 0.0
        )

        return linear_speed, angular_speed, current_yaw
