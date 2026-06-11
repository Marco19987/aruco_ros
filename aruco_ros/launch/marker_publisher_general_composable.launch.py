from launch import LaunchDescription
from launch.actions import DeclareLaunchArgument, OpaqueFunction
from launch.substitutions import LaunchConfiguration
from launch.utilities import perform_substitutions
from launch_ros.actions import Node
from launch_ros.actions import ComposableNodeContainer
from launch_ros.descriptions import ComposableNode
from launch_ros.actions import LoadComposableNodes, Node
from launch.conditions import IfCondition



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

    dictionary = DeclareLaunchArgument(
        'dictionary', default_value='0',
        description='Dictionary markers. '
        'ALL_DICTS = 0, ARUCO_MIP_36h12 = 1, ARUCO = 2, ARUCO_MIP_25h7 = 3...CUSTOM = 14'
    )
    
    #  ALL_DICTS = 0,
    # ARUCO_MIP_36h12 = 1,  //*** recommended
    # ARUCO = 2,            // original aruco dictionary. By default
    # ARUCO_MIP_25h7 = 3,
    # ARUCO_MIP_16h3 = 4,
    # ARTAG = 5,  //
    # ARTOOLKITPLUS = 6,
    # ARTOOLKITPLUSBCH = 7,  //
    # TAG16h5 = 8,
    # TAG25h7 = 9,
    # TAG25h9 = 10,
    # TAG36h11 = 11,
    # TAG36h10 = 12,   // april tags
    # CHILITAGS = 13,  // chili tags dictionary . NOT RECOMMENDED. It has distance 0.
    # CUSTOM = 14,  // for used defined dictionaries  (using loadFromfile).

    container_name_to_attach = LaunchConfiguration('container_name_to_attach')
    container_name_to_attach_arg = DeclareLaunchArgument(
        'container_name_to_attach', default_value='aruco_container',
        description='If provided the node will be attached to the container with the given name.'
    )

    # Create the launch description and populate
    ld = LaunchDescription()

    ld.add_action(marker_size_arg)
    ld.add_action(camera_frame_arg)
    ld.add_action(reference_frame)
    ld.add_action(min_marker_size)
    ld.add_action(detection_mode)
    ld.add_action(dictionary)
    ld.add_action(container_name_to_attach_arg)


    aruco_marker_publisher_params = {
            'image_is_rectified': True,
            'marker_size': LaunchConfiguration('marker_size'),
            'reference_frame': LaunchConfiguration('reference_frame'),
            'camera_frame': LaunchConfiguration('camera_frame'),
            'min_marker_size': LaunchConfiguration('min_marker_size'),
            'detection_mode': LaunchConfiguration('detection_mode'),
            'dictionary' : LaunchConfiguration('dictionary')
        }

    # ld.add_action(ComposableNodeContainer(
    #     name='aruco_container',
    #     namespace='robot1',
    #     package='rclcpp_components',
    #     executable='component_container',
    #     composable_node_descriptions=[
    #         ComposableNode(
    #             package='aruco_ros',
    #             plugin='ArucoMarkerPublisher',
    #             name='aruco_marker_publisher',
    #             namespace='robot1',
    #             parameters=[aruco_marker_publisher_params],
    #             remappings=[('/camera_info', 'color/camera_info'),
    #                 ('/image', 'color/image_raw')],
    #             extra_arguments=[{'use_intra_process_comms': True}],
    #             condition=IfCondition(LaunchConfiguration('container_name_to_attach')),
    #         ),
    #     ]
    # ))
    
    ld.add_action(LoadComposableNodes(
        target_container=LaunchConfiguration('container_name_to_attach'),
        composable_node_descriptions=[
            ComposableNode(
                package='aruco_ros',
                plugin='ArucoMarkerPublisher',
                name='aruco_marker_publisher',
                namespace='',
                parameters=[aruco_marker_publisher_params],
                remappings=[('/camera_info', 'color/camera_info'),
                    ('/image', 'color/image_raw')],
                extra_arguments=[{'use_intra_process_comms': True}],
            ),
        ]
    ))


    return ld
