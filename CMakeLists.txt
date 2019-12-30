cmake_minimum_required(VERSION 2.8.3)
project(zenit_printer_agent)

find_package(catkin REQUIRED COMPONENTS
  rospy
  message_generation
  std_msgs
)

catkin_python_setup()

catkin_package()

catkin_install_python(
    PROGRAMS
        scripts/trader_node
		scripts/print_node
    DESTINATION
        ${CATKIN_PACKAGE_BIN_DESTINATION}
)

install(
	FILES
		launch/zenit.launch
	DESTINATION
		${CATKIN_PACKAGE_SHARE_DESTINATION}/launch
)

