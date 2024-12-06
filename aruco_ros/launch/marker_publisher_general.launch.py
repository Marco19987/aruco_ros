from launch import LaunchDescription
from launch.actions import DeclareLaunchArgument, OpaqueFunction
from launch.substitutions import LaunchConfiguration
from launch.utilities import perform_substitutions
from launch_ros.actions import Node


def launch_setup(context, *args, **kwargs):

    aruco_marker_publisher_params = {
        'image_is_rectified': True,
        'marker_size': LaunchConfiguration('marker_size'),
        'reference_frame': LaunchConfiguration('reference_frame'),
        'camera_frame': LaunchConfiguration('camera_frame'),
        'min_marker_size': LaunchConfiguration('min_marker_size'),
        'detection_mode': LaunchConfiguration('detection_mode'),
    }

    aruco_marker_publisher = Node(
        package='aruco_ros',
        executable='marker_publisher',
        parameters=[aruco_marker_publisher_params],
        remappings=[('/camera_info', 'realsense_camera/color/camera_info'),
                    ('/image', 'realsense_camera/color/image_raw')],
    )

    return [aruco_marker_publisher]


def generate_launch_description():

    marker_size_arg = DeclareLaunchArgument(
        'marker_size', default_value='0.05',
        description='Marker size in m.'
    )

    camera_frame_arg = DeclareLaunchArgument(
        'camera_frame', default_value='camera_frame',
        description='Name of the camera frame'
    )

    reference_frame = DeclareLaunchArgument(
        'reference_frame', default_value='base',
        description='Reference frame. '
        'Leave it empty and the pose will be published wrt the camera frame. '
    )

    min_marker_size = DeclareLaunchArgument(
        'min_marker_size', default_value='0.02',
        description='Minimum size of the marker in m.'
    )

    detection_mode = DeclareLaunchArgument(
        'detection_mode', default_value='DM_NORMAL',
        description='Detection mode. '
        'DM_NORMAL, DM_VIDEO_FAST, DM_FAST'
    )

    # Create the launch description and populate
    ld = LaunchDescription()

    ld.add_action(marker_size_arg)
    ld.add_action(camera_frame_arg)
    ld.add_action(reference_frame)
    ld.add_action(min_marker_size)
    ld.add_action(detection_mode)


    ld.add_action(OpaqueFunction(function=launch_setup))

    return ld
