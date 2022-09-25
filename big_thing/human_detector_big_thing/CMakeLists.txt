cmake_minimum_required(VERSION 3.13.0)
project(human_detector)

find_package(OpenCV REQUIRED)

set(project_path "${CMAKE_CURRENT_SOURCE_DIR}/../..")
set(include_dirs
    ${project_path}/include
    ${project_path}/include/capcommon
    ${project_path}/include/utils
    ${CMAKE_CURRENT_SOURCE_DIR}
)
set(utils_path ${project_path}/src/utils)
set(public_lib_path ${project_path}/lib)
set(static_public_lib ${project_path}/src/build/capcommon/libcapcommon.a)

file(GLOB src 
    *.cc 
    *.c 
    ${utils_path}/*.cc
    ${utils_path}/*.c
)

add_executable(${CMAKE_PROJECT_NAME} ${src})
target_include_directories(${CMAKE_PROJECT_NAME} PUBLIC ${include_dirs})
target_link_directories(${CMAKE_PROJECT_NAME} PUBLIC ${public_lib_path})
target_link_libraries(
    ${CMAKE_PROJECT_NAME} 
    ${static_public_lib}
    ${OpenCV_LIBS}
    json-c 
    avahi-client 
    avahi-common 
    paho-mqtt3cs 
    curl
    SoPIoT
)