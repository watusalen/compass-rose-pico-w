# Generated CMake Pico project file

cmake_minimum_required(VERSION 3.13)

set(CMAKE_C_STANDARD 11)
set(CMAKE_CXX_STANDARD 17)
set(CMAKE_EXPORT_COMPILE_COMMANDS ON)

# == DO NOT EDIT THE FOLLOWING LINES for the Raspberry Pi Pico VS Code Extension to work ==
if(WIN32)
    set(USERHOME $ENV{USERPROFILE})
else()
    set(USERHOME $ENV{HOME})
endif()
set(sdkVersion 1.5.1)
set(toolchainVersion 13_2_Rel1)
set(picotoolVersion 2.0.0)
set(picoVscode ${USERHOME}/.pico-sdk/cmake/pico-vscode.cmake)
if (EXISTS ${picoVscode})
    include(${picoVscode})
endif()
# ====================================================================================

set(PICO_BOARD pico_w CACHE STRING "Board type")

# Pull in Raspberry Pi Pico SDK (must be before project)
include(pico_sdk_import.cmake)

project(picow_joystick_client C CXX ASM)

# Initialise the Raspberry Pi Pico SDK
pico_sdk_init()

# Biblioteca utilitária LWIP/HTTP
pico_add_library(example_lwip_http_util NOFLAG)
target_sources(example_lwip_http_util INTERFACE
    ${CMAKE_CURRENT_LIST_DIR}/src/example_http_client_util.c
)
pico_mirrored_target_link_libraries(example_lwip_http_util INTERFACE
    pico_lwip_http
    pico_lwip_mbedtls
    pico_mbedtls
)
target_include_directories(example_lwip_http_util INTERFACE
    ${CMAKE_CURRENT_LIST_DIR}/include
)

# Definições de Wi-Fi
set(WIFI_SSID "Lapec_Professores")
set(WIFI_PASSWORD "w1q2e3r4")

# ================= Executable: picow_joystick_client =================
add_executable(picow_joystick_client
    src/picow_joystick_client.c
)

# passa SSID/SENHA via define
target_compile_definitions(picow_joystick_client PRIVATE
    WIFI_SSID=\"${WIFI_SSID}\"
    WIFI_PASSWORD=\"${WIFI_PASSWORD}\"
)

# Nome e versão
pico_set_program_name(picow_joystick_client "picow_joystick_client")
pico_set_program_version(picow_joystick_client "0.1")

# saída de stdio
pico_enable_stdio_uart(picow_joystick_client 0)
pico_enable_stdio_usb(picow_joystick_client 1)

# inclui headers e libs
target_include_directories(picow_joystick_client PRIVATE
    ${CMAKE_CURRENT_LIST_DIR}/include
)
target_link_libraries(picow_joystick_client
    pico_stdlib
    pico_cyw43_arch_lwip_threadsafe_background
    example_lwip_http_util
    hardware_adc
)

pico_add_extra_outputs(picow_joystick_client)

# ================ Executable: picow_joystick_client_verify ================
add_executable(picow_joystick_client_verify
    src/picow_joystick_verify.c
)

target_compile_definitions(picow_joystick_client_verify PRIVATE
    WIFI_SSID=\"${WIFI_SSID}\"
    WIFI_PASSWORD=\"${WIFI_PASSWORD}\"
    # forçar verificação de certificado
    ALTCP_MBEDTLS_AUTHMODE=MBEDTLS_SSL_VERIFY_REQUIRED
)

target_include_directories(picow_joystick_client_verify PRIVATE
    ${CMAKE_CURRENT_LIST_DIR}/include
)
target_link_libraries(picow_joystick_client_verify
    pico_stdlib
    pico_cyw43_arch_lwip_threadsafe_background
    example_lwip_http_util
)

pico_add_extra_outputs(picow_joystick_client_verify)

# Ignore warnings from lwip code
set_source_files_properties(
    ${PICO_LWIP_PATH}/src/apps/altcp_tls/altcp_tls_mbedtls.c
    PROPERTIES
    COMPILE_OPTIONS "-Wno-unused-result"
)
