cmake_minimum_required(VERSION 3.16)
project(problem_solving LANGUAGES CXX)

set(CMAKE_CXX_STANDARD 17)
set(CMAKE_CXX_STANDARD_REQUIRED ON)
set(CMAKE_CXX_EXTENSIONS OFF)

enable_testing()

if(MSVC)
  add_compile_options(/W4)
else()
  add_compile_options(-Wall -Wextra -Wpedantic)
endif()

# Every problems/<platform>/<slug>/test.cpp becomes one test executable.
# The test includes the sibling solution.cpp (with NO_MAIN defined).
file(GLOB_RECURSE PROBLEM_TESTS CONFIGURE_DEPENDS
     "${CMAKE_SOURCE_DIR}/problems/*/*/test.cpp")

foreach(test_source IN LISTS PROBLEM_TESTS)
  get_filename_component(problem_dir "${test_source}" DIRECTORY)
  get_filename_component(slug "${problem_dir}" NAME)
  get_filename_component(platform_dir "${problem_dir}" DIRECTORY)
  get_filename_component(platform "${platform_dir}" NAME)
  set(target "${platform}_${slug}")
  add_executable(${target} "${test_source}")
  target_include_directories(${target} PRIVATE "${problem_dir}")
  add_test(NAME ${target} COMMAND ${target})
endforeach()
