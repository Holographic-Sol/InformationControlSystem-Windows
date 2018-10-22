import os
import sys
import time
import codecs
import psutil
import socket
import os.path
import subprocess
import win32com.client
import distutils.dir_util
import speech_recognition as sr

from PyQt5.QtWidgets import QMainWindow, QApplication, QPushButton, QLineEdit, QLabel
from PyQt5.QtCore import Qt
from PyQt5.QtCore import QThread
from PyQt5.QtCore import QCoreApplication
from PyQt5.QtGui import QIcon, QPixmap
from PyQt5 import QtGui
from PyQt5 import QtCore


# Files
secondary_key_store = 'secondary-key.tmp'
plugin_index = 'Indexes/CSV-Indexes/csv-plugin-index.py'
config_file = 'config.conf'

audio_index_file = 'Indexes/CSV-Indexes/csv-user-audio-index.py'
image_index_file = 'Indexes/CSV-Indexes/csv-user-image-index.py'
program_index_file = 'Indexes/CSV-Indexes/csv-user-program-index.py'
text_index_file = 'Indexes/CSV-Indexes/csv-user-text-index.py'
video_index_file = 'Indexes/CSV-Indexes/csv-user-video-index.py'

directory_index_file = ['Indexes/CSV-Indexes/csv-user-directory-index.py',
                        'Indexes/CSV-Indexes/csv-d1-directory-index.py',
                        'Indexes/CSV-Indexes/csv-d2-directory-index.py',
                        'Indexes/CSV-Indexes/csv-d3-directory-index.py',
                        'Indexes/CSV-Indexes/csv-d4-directory-index.py',
                        'Indexes/CSV-Indexes/csv-d4-directory-index.py',
                        'Indexes/CSV-Indexes/csv-d5-directory-index.py',
                        'Indexes/CSV-Indexes/csv-d6-directory-index.py',
                        'Indexes/CSV-Indexes/csv-d7-directory-index.py',
                        'Indexes/CSV-Indexes/csv-d8-directory-index.py',
                        ]

# Directories
indexes_dir = 'Indexes'
plugin_dir = 'Plugins'
transcripts_dir = 'Transcriptions'
resources_dir = 'Resources'
user_programs_dir = 'UserPrograms'

# Data
showHideValue = 0
show_hide_settings = ()
sr_active = False

# Threads
speechRecognitionThread = ()
guiControllerThread = ()
drawMenuThread = ()
openDirectoryThread = ()
findOpenAudioThread = ()
findOpenImageThread = ()
findOpenTextThread = ()
findOpenVideoThread = ()
findOpenProgramThread = ()
configInteractionPermissionThread = ()
symbiotServerThread = ()
guiMode1Thread = ()

# Heal a missing configuration file
if not os.path.exists('config.conf'):
    open('config.conf', 'w').close()

# Make Paths If Paths Not Exist
distutils.dir_util.mkpath(indexes_dir)
distutils.dir_util.mkpath(plugin_dir)
distutils.dir_util.mkpath(resources_dir)
distutils.dir_util.mkpath(transcripts_dir)
distutils.dir_util.mkpath(user_programs_dir)

# Speech Recognition
value = ''
primary_key = ''
secondary_key = ''

# Encoding
encode = u'\u5E73\u621015\u200e'

# Windows Text To Speech API
speaker = win32com.client.Dispatch("SAPI.SpVoice")

# Subprocess Info
info = subprocess.STARTUPINFO()
info.dwFlags = 1
info.wShowWindow = 0

# Psutil.Processes
sppsutil = []
stop_transcription_psutil = []
list_transcriptions_psutil = []
get_latest_transcriptions_psutil = []
remove_bookmark_psutil = []
index_engine_psutil = []
plugin_index_psutil = ()
audio_index_psutil = ()
video_index_psutil = ()
image_index_psutil = ()
text_index_psutil = ()
drive1_index_psutil = ()
drive2_index_psutil = ()
drive3_index_psutil = ()
drive4_index_psutil = ()
drive5_index_psutil = ()
drive6_index_psutil = ()
drive7_index_psutil = ()
drive8_index_psutil = ()
user_directory_index_psutil = ()
user_prog_index_engine_psutil = ()
ask_google_psutil = []
wiktionary_define_psutil = []

# PIDs
sppid = []
main_thread_pid = os.getpid()
index_engine_pid = []
list_transcriptions_pid = []
get_latest_transcription_pid = []
remove_bookmark_pid = []
ask_google_pid = []
wiktionary_define_pid = []

# Media Player Global Data
target_index = ''
multiple_matches = []
target_match = ''
currentAudioMedia = ''
media_playing_check = ()

# Ascertain Configuration Settings
check_allow_symbiot_config = False
check_symbiot_server_port_config = False
check_symbiot_server_ip_config = False
check_symbiot_ip_config = False
check_symbiot_mac_config = False

check_wiki_local_server_ip = False
check_wiki_local_server_port = False

check_index_audio_config = False
check_index_video_config = False
check_index_image_config = False
check_index_text_config = False
check_index_drive1_config = False
check_index_drive2_config = False
check_index_drive3_config = False
check_index_drive4_config = False
check_index_drive5_config = False
check_index_drive6_config = False
check_index_drive7_config = False
check_index_drive8_config = False

symbiot_configuration = ''
symbiot_server_ip_configuration = ''
symbiot_server_port_configuration = ''
symbiot_ip_configuration = ''
symbiot_mac_configuration = ''
symbiot_configuration_Bool = False
symbiot_server_ip_configuration_Bool = False
symbiot_server_port_configuration_Bool = False
symbiot_ip_configuration_Bool = False
symbiot_mac_configuration_Bool = False

wiki_show_browser_Bool = False
wiki_show_browser_configuration = ''
wiki_dictate_Bool = False
wiki_dictate_configuration = ''
allow_wiki_local_server_Bool = False
allow_wiki_local_server_configuration = ''
wiki_local_server_ip_configuration = ''
wiki_local_server_port_configuration = ''
wiki_local_server_ip_configuration_Bool = False
wiki_local_server_port_configuration_Bool = False

audio_configuration = ''
video_configuration = ''
image_configuration = ''
text_configuration = ''

drive1_configuration = ''
drive2_configuration = ''
drive3_configuration = ''
drive4_configuration = ''
drive5_configuration = ''
drive6_configuration = ''
drive7_configuration = ''
drive8_configuration = ''

plugin_active_config_Bool = True

audio_active_config = ''
audio_active_config_Bool = ()

video_active_config = ''
video_active_config_Bool = ()

image_active_config = ''
image_active_config_Bool = ()

text_active_config = ''
text_active_config_Bool = ()

drive_1_active_config = ''
drive_1_active_config_Bool = ()

drive_2_active_config = ''
drive_2_active_config_Bool = ()

drive_3_active_config = ''
drive_3_active_config_Bool = ()

drive_4_active_config = ''
drive_4_active_config_Bool = ()

drive_5_active_config = ''
drive_5_active_config_Bool = ()

drive_6_active_config = ''
drive_6_active_config_Bool = ()

drive_7_active_config = ''
drive_7_active_config_Bool = ()

drive_8_active_config = ''
drive_8_active_config_Bool = ()


# Perform Configuration Checks
def configurationChecksFunction():
    global check_allow_symbiot_config
    global symbiot_configuration
    global symbiot_configuration_Bool
    global symbiot_server_ip_configuration
    global symbiot_server_port_configuration
    global symbiot_ip_configuration
    global symbiot_mac_configuration
    global symbiot_server_ip_configuration_Bool
    global symbiot_server_port_configuration_Bool
    global symbiot_ip_configuration_Bool
    global symbiot_mac_configuration_Bool

    global wiki_local_server_ip_configuration_Bool
    global wiki_local_server_port_configuration_Bool
    global wiki_local_server_ip_configuration
    global wiki_local_server_port_configuration
    global wiki_dictate_Bool
    global wiki_show_browser_Bool
    global allow_wiki_local_server_Bool
    global wiki_show_browser_configuration
    global wiki_dictate_configuration
    global allow_wiki_local_server_configuration

    global check_index_audio_config
    global audio_configuration
    global audio_active_config
    global audio_active_config_Bool

    global check_index_video_config
    global video_configuration
    global video_active_config
    global video_active_config_Bool

    global check_index_image_config
    global image_configuration
    global image_active_config
    global image_active_config_Bool

    global check_index_text_config
    global text_configuration
    global text_active_config
    global text_active_config_Bool

    global check_index_drive1_config
    global drive1_configuration
    global drive_1_active_config
    global drive_1_active_config_Bool

    global check_index_drive2_config
    global drive2_configuration
    global drive_2_active_config
    global drive_2_active_config_Bool

    global check_index_drive3_config
    global drive3_configuration
    global drive_3_active_config
    global drive_3_active_config_Bool

    global check_index_drive4_config
    global drive4_configuration
    global drive_4_active_config
    global drive_4_active_config_Bool

    global check_index_drive5_config
    global drive5_configuration
    global drive_5_active_config
    global drive_5_active_config_Bool

    global check_index_drive6_config
    global drive6_configuration
    global drive_6_active_config
    global drive_6_active_config_Bool

    global check_index_drive7_config
    global drive7_configuration
    global drive_7_active_config
    global drive_7_active_config_Bool

    global check_index_drive8_config
    global drive8_configuration
    global drive_8_active_config
    global drive_8_active_config_Bool

    # Wiki Configuration
    with open('config.conf', 'r') as fo:
        for line in fo:
            line = line.strip()
            if line == 'WIKI_TRANSCRIPT_SHOW_BROWSER: disabled':
                wiki_show_browser_Bool = False
                wiki_show_browser_configuration = line.replace('WIKI_TRANSCRIPT_SHOW_BROWSER: ', '')
                print('show wiki pages: false')
            if line == 'WIKI_TRANSCRIPT_SHOW_BROWSER: enabled':
                wiki_show_browser_Bool = True
                wiki_show_browser_configuration = line.replace('WIKI_TRANSCRIPT_SHOW_BROWSER: ', '')
                print('show wiki pages: true')

            if line == 'WIKI_TRANSCRIPT_DICTATE: enabled':
                wiki_dictate_Bool = True
                wiki_dictate_configuration = line.replace('WIKI_TRANSCRIPT_DICTATE: ', '')
                print('dictate wiki pages: true')
            if line == 'WIKI_TRANSCRIPT_DICTATE: disabled':
                wiki_dictate_Bool = False
                wiki_dictate_configuration = line.replace('WIKI_TRANSCRIPT_DICTATE: ', '')
                print('dictate wiki pages: false')

            if line == 'ALLOW_WIKI_LOCAL_SERVER: disabled':
                allow_wiki_local_server_Bool = False
                allow_wiki_local_server_configuration = line.replace('ALLOW_WIKI_LOCAL_SERVER: ', '')
                print('using local wiki server: false')
            if line == 'ALLOW_WIKI_LOCAL_SERVER: enabled':
                allow_wiki_local_server_Bool = True
                allow_wiki_local_server_configuration = line.replace('ALLOW_WIKI_LOCAL_SERVER: ', '')
                print('using local wiki server: true')

            if line.startswith('WIKI_LOCAL_SERVER: '):
                wiki_local_server_ip_configuration = line.replace('WIKI_LOCAL_SERVER: ', '')
                print('local wiki server:', wiki_local_server_ip_configuration)
            if line.startswith('WIKI_LOCAL_SERVER_PORT: '):
                wiki_local_server_port_configuration = line.replace('WIKI_LOCAL_SERVER_PORT: ', '')
                print('local wiki server port:', wiki_local_server_port_configuration)

    # Symbiot Configuration
    with open('config.conf', 'r') as fo:
        for line in fo:
            line = line.strip()
            if line == 'ALLOW_SYMBIOT: TRUE':
                symbiot_configuration_Bool = True
                symbiot_configuration = 'Enabled'
                print('symbiot: enabled')
            elif line == 'ALLOW_SYMBIOT: FALSE':
                symbiot_configuration_Bool = False
                symbiot_configuration = 'Disabled'
                print('symbiot: disabled')
            else:
                pass
    with open('config.conf', 'r') as fo:
        for line in fo:
            line = line.strip()
            if line.startswith('SYMBIOT_SERVER: '):
                if line != 'SYMBIOT_SERVER: ':
                    line = line.replace('SYMBIOT_SERVER: ', '')
                    symbiot_server_ip_configuration = line
                    print('symbiot server ip config:', symbiot_server_ip_configuration)
            if line.startswith('SYMBIOT_SERVER_PORT: '):
                if line != 'SYMBIOT_SERVER_PORT: ':
                    line = line.replace('SYMBIOT_SERVER_PORT: ', '')
                    symbiot_server_port_configuration = line
                    print('symbiot server port config:', symbiot_server_port_configuration)
            if line.startswith('SYMBIOT_IP: '):
                if line != 'SYMBIOT_IP: ':
                    line = line.replace('SYMBIOT_IP: ', '')
                    symbiot_ip_configuration = line
                    print('symbiot ip config:', symbiot_ip_configuration)
            if line.startswith('SYMBIOT_MAC: '):
                if line != 'SYMBIOT_MAC: ':
                    line = line.replace('SYMBIOT_MAC: ', '')
                    symbiot_mac_configuration = line
                    print('symbiot mac config:', symbiot_mac_configuration)

    # Audio Configuration
    with open('config.conf', 'r') as fo:
        for line in fo:
            line = line.strip()
            if line.startswith('DIRAUD: '):
                line2 = line.replace('DIRAUD: ', '')
                line2 = line2.strip()
                if os.path.exists(line2):
                    check_index_audio_config = True
                    print('check index audio config: path exists')
                    audio_configuration = line
                elif not os.path.exists(line2):
                    print('audio path in configuration: invalid')
            if line.startswith('INDEXENGINE_AUDIO: '):
                if line.endswith('disabled'):
                    audio_active_config = 'Disabled'
                    audio_active_config_Bool = False
                    print('index audio active: disabled')
                elif line.endswith('enabled'):
                    audio_active_config = 'Enabled'
                    audio_active_config_Bool = True
                    print('index audio active: enabled')
        fo.close()
    if check_index_audio_config == False:
        print('check index audio config: missing/malformed data... creating default configuration')
        defaultAudioPath = os.path.join(os.path.expanduser('~'), 'Music')
        with open('config.conf', 'a') as fo:
            fo.writelines('DIRAUD: ' + defaultAudioPath + '\n')
            check_index_audio_config = True
            audio_configuration = defaultAudioPath
        fo.close()

    # Video Configuration
    with open('config.conf', 'r') as fo:
        for line in fo:
            line = line.strip()
            if line.startswith('DIRVID: '):
                line2 = line.replace('DIRVID: ', '')
                line2 = line2.strip()
                if os.path.exists(line2):
                    check_index_video_config = True
                    print('check index video config: path exists')
                    video_configuration = line
                elif not os.path.exists(line2):
                    print('video path in configuration: invalid')
            if line.startswith('INDEXENGINE_VIDEO: '):
                if line.endswith('disabled'):
                    video_active_config = 'Disabled'
                    video_active_config_Bool = False
                    print('index video active: disabled')
                elif line.endswith('enabled'):
                    video_active_config = 'Enabled'
                    video_active_config_Bool = True
                    print('index video active: enabled')
        fo.close()
    if check_index_video_config == False:
        print('check index video config: missing/malformed data... creating default configuration')
        defaultVideoPath = os.path.join(os.path.expanduser('~'), 'Videos')
        with open('config.conf', 'a') as fo:
            fo.writelines('DIRVID: ' + defaultVideoPath + '\n')
            check_index_video_config = True
            video_configuration = defaultVideoPath
        fo.close()

    # Image Configuration
    with open('config.conf', 'r') as fo:
        for line in fo:
            line = line.strip()
            if line.startswith('DIRIMG: '):
                line2 = line.replace('DIRIMG: ', '')
                line2 = line2.strip()
                if os.path.exists(line2):
                    check_index_image_config = True
                    print('check index image config: path exists')
                    image_configuration = line
                elif not os.path.exists(line2):
                    print('video path in configuration: invalid')
            if line.startswith('INDEXENGINE_IMAGE: '):
                if line.endswith('disabled'):
                    image_active_config = 'Disabled'
                    image_active_config_Bool = False
                    print('index image active: disabled')
                elif line.endswith('enabled'):
                    image_active_config = 'Enabled'
                    image_active_config_Bool = True
                    print('index image active: enabled')
        fo.close()
    if check_index_image_config == False:
        print('check index image config: missing/malformed data... creating default configuration')
        defaultImagePath = os.path.join(os.path.expanduser('~'), 'Pictures')
        with open('config.conf', 'a') as fo:
            fo.writelines('DIRIMG: ' + defaultImagePath + '\n')
            check_index_image_config = True
            image_configuration = defaultImagePath
        fo.close()

    # Text Configuration
    with open('config.conf', 'r') as fo:
        for line in fo:
            line = line.strip()
            if line.startswith('DIRTXT: '):
                line2 = line.replace('DIRTXT: ', '')
                line2 = line2.strip()
                if os.path.exists(line2):
                    check_index_text_config = True
                    print('check index text config: path exists')
                    text_configuration = line
                elif not os.path.exists(line2):
                    print('text path in configuration: invalid')
            if line.startswith('INDEXENGINE_TEXT: '):
                if line.endswith('disabled'):
                    text_active_config = 'Disabled'
                    text_active_config_Bool = False
                    print('index text active: disabled')
                elif line.endswith('enabled'):
                    text_active_config = 'Enabled'
                    text_active_config_Bool = True
                    print('index text active: enabled')
        fo.close()
    if check_index_text_config == False:
        print('check index text config: missing/malformed data... creating default configuration')
        defaultTextPath = os.path.join(os.path.expanduser('~'), 'Documents')
        with open('config.conf', 'a') as fo:
            fo.writelines('DIRTXT: ' + defaultTextPath + '\n')
            check_index_text_config = True
            text_configuration = defaultTextPath
        fo.close()

    # Drive1 Configuration
    with open('config.conf', 'r') as fo:
        for line in fo:
            line = line.strip()
            if line.startswith('DRIVE1: '):
                line2 = line.replace('DRIVE1: ', '')
                line2 = line2.strip()
                if os.path.exists(line2):
                    check_index_drive1_config = True
                    print('check index drive1 config: path exists')
                    drive1_configuration = line
                elif not os.path.exists(line2):
                    print('drive1 path in configuration: invalid')
            if line.startswith('INDEXENGINE_DRIVE1: '):
                if line.endswith('disabled'):
                    drive_1_active_config = 'Disabled'
                    drive_1_active_config_Bool = False
                    print('index drive1 active: disabled')
                elif line.endswith('enabled'):
                    drive_1_active_config = 'Enabled'
                    drive_1_active_config_Bool = True
                    print('index drive1 active: enabled')
        fo.close()
    if check_index_drive1_config == False:
        defaultDrive1Config = 'null'
        drive1_configuration = defaultDrive1Config

    # Drive2 Configuration
    with open('config.conf', 'r') as fo:
        for line in fo:
            line = line.strip()
            if line.startswith('DRIVE2: '):
                line2 = line.replace('DRIVE2: ', '')
                line2 = line2.strip()
                if os.path.exists(line2):
                    check_index_drive2_config = True
                    print('check index drive2 config: path exists')
                    drive2_configuration = line
                elif not os.path.exists(line2):
                    print('drive2 path in configuration: invalid')
            if line.startswith('INDEXENGINE_DRIVE2: '):
                if line.endswith('disabled'):
                    drive_2_active_config = 'Disabled'
                    drive_2_active_config_Bool = False
                    print('index drive2 active: disabled')
                elif line.endswith('enabled'):
                    drive_2_active_config = 'Enabled'
                    drive_2_active_config_Bool = True
                    print('index drive2 active: enabled')
        fo.close()
    if check_index_drive2_config == False:
        defaultDrive2Config = 'null'
        drive2_configuration = defaultDrive2Config

    # Drive3 Configuration
    with open('config.conf', 'r') as fo:
        for line in fo:
            line = line.strip()
            if line.startswith('DRIVE3: '):
                line2 = line.replace('DRIVE3: ', '')
                line2 = line2.strip()
                if os.path.exists(line2):
                    check_index_drive3_config = True
                    print('check index drive3 config: path exists')
                    drive3_configuration = line
                elif not os.path.exists(line2):
                    print('drive3 path in configuration: invalid')
            if line.startswith('INDEXENGINE_DRIVE3: '):
                if line.endswith('disabled'):
                    drive_3_active_config = 'Disabled'
                    drive_3_active_config_Bool = False
                    print('index drive3 active: disabled')
                elif line.endswith('enabled'):
                    drive_3_active_config = 'Enabled'
                    drive_3_active_config_Bool = True
                    print('index drive3 active: enabled')
        fo.close()
    if check_index_drive3_config == False:
        defaultDrive3Config = 'null'
        drive3_configuration = defaultDrive3Config

    # Drive4 Configuration
    with open('config.conf', 'r') as fo:
        for line in fo:
            line = line.strip()
            if line.startswith('DRIVE4: '):
                line2 = line.replace('DRIVE4: ', '')
                line2 = line2.strip()
                if os.path.exists(line2):
                    check_index_drive4_config = True
                    print('check index drive4 config: path exists')
                    drive4_configuration = line
                elif not os.path.exists(line2):
                    print('drive4 path in configuration: invalid')
            if line.startswith('INDEXENGINE_DRIVE4: '):
                if line.endswith('disabled'):
                    drive_4_active_config = 'Disabled'
                    drive_4_active_config_Bool = False
                    print('index drive4 active: disabled')
                elif line.endswith('enabled'):
                    drive_4_active_config = 'Enabled'
                    drive_4_active_config_Bool = True
                    print('index drive4 active: enabled')
        fo.close()
    if check_index_drive4_config == False:
        defaultDrive4Config = 'null'
        drive4_configuration = defaultDrive4Config

    # Drive5 Configuration
    with open('config.conf', 'r') as fo:
        for line in fo:
            line = line.strip()
            if line.startswith('DRIVE5: '):
                line2 = line.replace('DRIVE5: ', '')
                line2 = line2.strip()
                if os.path.exists(line2):
                    check_index_drive5_config = True
                    print('check index drive5 config: path exists')
                    drive5_configuration = line
                elif not os.path.exists(line2):
                    print('drive5 path in configuration: invalid')
            if line.startswith('INDEXENGINE_DRIVE5: '):
                if line.endswith('disabled'):
                    drive_5_active_config = 'Disabled'
                    drive_5_active_config_Bool = False
                    print('index drive5 active: disabled')
                elif line.endswith('enabled'):
                    drive_5_active_config = 'Enabled'
                    drive_5_active_config_Bool = True
                    print('index drive5 active: enabled')
        fo.close()
    if check_index_drive5_config == False:
        defaultDrive5Config = 'null'
        drive5_configuration = defaultDrive5Config

    # Drive6 Configuration
    with open('config.conf', 'r') as fo:
        for line in fo:
            line = line.strip()
            if line.startswith('DRIVE6: '):
                line2 = line.replace('DRIVE6: ', '')
                line2 = line2.strip()
                if os.path.exists(line2):
                    check_index_drive6_config = True
                    print('check index drive6 config: path exists')
                    drive6_configuration = line
                elif not os.path.exists(line2):
                    print('drive6 path in configuration: invalid')
            if line.startswith('INDEXENGINE_DRIVE6: '):
                if line.endswith('disabled'):
                    drive_6_active_config = 'Disabled'
                    drive_6_active_config_Bool = False
                    print('index drive6 active: disabled')
                elif line.endswith('enabled'):
                    drive_6_active_config = 'Enabled'
                    drive_6_active_config_Bool = True
                    print('index drive6 active: enabled')
        fo.close()
    if check_index_drive6_config == False:
        defaultDrive6Config = 'null'
        drive6_configuration = defaultDrive6Config

    # Drive7 Configuration
    with open('config.conf', 'r') as fo:
        for line in fo:
            line = line.strip()
            if line.startswith('DRIVE7: '):
                line2 = line.replace('DRIVE7: ', '')
                line2 = line2.strip()
                if os.path.exists(line2):
                    check_index_drive7_config = True
                    print('check index drive7 config: path exists')
                    drive7_configuration = line
                elif not os.path.exists(line2):
                    print('drive7 path in configuration: invalid')
            if line.startswith('INDEXENGINE_DRIVE7: '):
                if line.endswith('disabled'):
                    drive_7_active_config = 'Disabled'
                    drive_7_active_config_Bool = False
                    print('index drive7 active: disabled')
                elif line.endswith('enabled'):
                    drive_7_active_config = 'Enabled'
                    drive_7_active_config_Bool = True
                    print('index drive7 active: enabled')
        fo.close()
    if check_index_drive7_config == False:
        defaultDrive7Config = 'null'
        drive7_configuration = defaultDrive7Config

    # Drive8 Configuration
    with open('config.conf', 'r') as fo:
        for line in fo:
            line = line.strip()
            if line.startswith('DRIVE8: '):
                line2 = line.replace('DRIVE8: ', '')
                line2 = line2.strip()
                if os.path.exists(line2):
                    check_index_drive8_config = True
                    print('check index drive8 config: path exists')
                    drive8_configuration = line
                elif not os.path.exists(line2):
                    print('drive8 path in configuration: invalid')
            if line.startswith('INDEXENGINE_DRIVE8: '):
                if line.endswith('disabled'):
                    drive_8_active_config = 'Disabled'
                    drive_8_active_config_Bool = False
                    print('index drive8 active: disabled')
                elif line.endswith('enabled'):
                    drive_8_active_config = 'Enabled'
                    drive_8_active_config_Bool = True
                    print('index drive8 active: enabled')
        fo.close()
    if check_index_drive8_config == False:
        defaultDrive8Config = 'null'
        drive8_configuration = defaultDrive8Config


def pluginIndexEngineFunction():
    global plugin_active_config_Bool
    global plugin_index_psutil
    if plugin_active_config_Bool == True:
        cmd = ('python ' + 'index-engine-plugins.py')
        plugin_index_engine_proc = subprocess.Popen(cmd, shell=False, startupinfo=info)
        plugin_index_engine_pid = plugin_index_engine_proc.pid
        plugin_index_psutil = psutil.Process(plugin_index_engine_pid)
        print('command:', cmd)
        print('subprocess PID :', plugin_index_engine_pid)
        if psutil.pid_exists(plugin_index_engine_pid) == True:
            print('plugin index engine running  :', 'yes')
        else:
            print('plugin index engine running  :', 'failed')


def audioIndexEngineFunction():
    global audio_active_config_Bool
    global audio_index_psutil
    if audio_active_config_Bool == True:
        if check_index_audio_config == True:
            cmd = ('python ' + 'index-engine-user-audio.py')
            audio_index_engine_proc = subprocess.Popen(cmd, shell=False, startupinfo=info)
            audio_index_engine_pid = audio_index_engine_proc.pid
            audio_index_psutil = psutil.Process(audio_index_engine_pid)
            print('command:', cmd)
            print('subprocess PID :', audio_index_engine_pid)
            if psutil.pid_exists(audio_index_engine_pid) == True:
                print('audio index engine running  :', 'yes')
            else:
                print('audio index engine running  :', 'failed')


def imageIndexEngineFunction():
    global image_active_config_Bool
    global image_index_psutil
    if image_active_config_Bool == True:
        if check_index_image_config == True:
            cmd = ('python ' + 'index-engine-user-image.py')
            image_index_engine_proc = subprocess.Popen(cmd, shell=False, startupinfo=info)
            image_index_engine_pid = image_index_engine_proc.pid
            image_index_psutil = psutil.Process(image_index_engine_pid)
            print('command:', cmd)
            print('subprocess PID :', image_index_engine_pid)
            if psutil.pid_exists(image_index_engine_pid) == True:
                print('image index engine running  :', 'yes')
            else:
                print('image index engine running  :', 'failed')


def textIndexEngineFunction():
    global text_active_config_Bool
    global text_index_psutil
    if text_active_config_Bool == True:
        if check_index_text_config == True:
            cmd = ('python ' + 'index-engine-user-text.py')
            text_index_engine_proc = subprocess.Popen(cmd, shell=False, startupinfo=info)
            text_index_engine_pid = text_index_engine_proc.pid
            text_index_psutil = psutil.Process(text_index_engine_pid)
            print('command:', cmd)
            print('subprocess PID :', text_index_engine_pid)
            if psutil.pid_exists(text_index_engine_pid) == True:
                print('text index engine running  :', 'yes')
            else:
                print('text index engine running  :', 'failed')


def videoIndexEngineFunction():
    global video_active_config_Bool
    global video_index_psutil
    if video_active_config_Bool == True:
        if check_index_video_config == True:
            cmd = ('python ' + 'index-engine-user-video.py')
            video_index_engine_proc = subprocess.Popen(cmd, shell=False, startupinfo=info)
            video_index_engine_pid = video_index_engine_proc.pid
            video_index_psutil = psutil.Process(video_index_engine_pid)
            print('command:', cmd)
            print('subprocess PID :', video_index_engine_pid)
            if psutil.pid_exists(video_index_engine_pid) == True:
                print('video index engine running  :', 'yes')
            else:
                print('video index engine running  :', 'failed')


def userProgramsIndexEngineFunction():
    global user_prog_index_engine_psutil
    cmd = ('python ' + 'index-engine-user-programs.py')
    user_prog_index_engine_proc = subprocess.Popen(cmd, shell=False, startupinfo=info)
    user_prog_index_engine_pid = user_prog_index_engine_proc.pid
    user_prog_index_engine_psutil = psutil.Process(user_prog_index_engine_pid)
    print('command:', cmd)
    print('subprocess PID :', user_prog_index_engine_pid)
    if psutil.pid_exists(user_prog_index_engine_pid) == True:
        print('user programs index engine running  :', 'yes')
    else:
        print('user programs index engine running  :', 'failed')


def userDirectoriesIndexEngineFunction():
    global user_directory_index_psutil
    cmd = ('python ' + 'index-engine-user-directory.py')
    user_directories_index_engine_proc = subprocess.Popen(cmd, shell=False, startupinfo=info)
    user_directories_index_engine_pid = user_directories_index_engine_proc.pid
    user_directory_index_psutil = psutil.Process(user_directories_index_engine_pid)
    print('command:', cmd)
    print('subprocess PID :', user_directories_index_engine_pid)
    if psutil.pid_exists(user_directories_index_engine_pid) == True:
        print('user directories index engine running  :', 'yes')
    else:
        print('user directories index engine running  :', 'failed')


def drive1IndexEngineFunction():
    global drive_1_active_config_Bool
    global drive1_index_psutil
    if drive_1_active_config_Bool == True:
        if check_index_drive1_config == True:
            cmd = ('python ' + 'index-engine-directory-d1.py')
            drive_1_index_engine_proc = subprocess.Popen(cmd, shell=False, startupinfo=info)
            drive_1_index_engine_pid = drive_1_index_engine_proc.pid
            drive1_index_psutil = psutil.Process(drive_1_index_engine_pid)
            print('command:', cmd)
            print('subprocess PID :', drive_1_index_engine_pid)
            if psutil.pid_exists(drive_1_index_engine_pid) == True:
                print('drive1 index engine running  :', 'yes')
            else:
                print('drive1 index engine running  :', 'failed')


def drive2IndexEngineFunction():
    global drive_2_active_config_Bool
    global drive2_index_psutil
    if drive_2_active_config_Bool == True:
        if check_index_drive2_config == True:
            cmd = ('python ' + 'index-engine-directory-d2.py')
            drive_2_index_engine_proc = subprocess.Popen(cmd, shell=False, startupinfo=info)
            drive_2_index_engine_pid = drive_2_index_engine_proc.pid
            drive2_index_psutil = psutil.Process(drive_2_index_engine_pid)
            print('command:', cmd)
            print('subprocess PID :', drive_2_index_engine_pid)
            if psutil.pid_exists(drive_2_index_engine_pid) == True:
                print('drive2 index engine running  :', 'yes')
            else:
                print('drive2 index engine running  :', 'failed')


def drive3IndexEngineFunction():
    global drive_3_active_config_Bool
    global drive3_index_psutil
    if drive_3_active_config_Bool == True:
        if check_index_drive3_config == True:
            cmd = ('python ' + 'index-engine-directory-d3.py')
            drive_3_index_engine_proc = subprocess.Popen(cmd, shell=False, startupinfo=info)
            drive_3_index_engine_pid = drive_3_index_engine_proc.pid
            drive3_index_psutil = psutil.Process(drive_3_index_engine_pid)
            print('command:', cmd)
            print('subprocess PID :', drive_3_index_engine_pid)
            if psutil.pid_exists(drive_3_index_engine_pid) == True:
                print('drive3 index engine running  :', 'yes')
            else:
                print('drive3 index engine running  :', 'failed')


def drive4IndexEngineFunction():
    global drive_4_active_config_Bool
    global drive4_index_psutil

    if drive_4_active_config_Bool == True:
        if check_index_drive4_config == True:
            cmd = ('python ' + 'index-engine-directory-d4.py')
            drive_4_index_engine_proc = subprocess.Popen(cmd, shell=False, startupinfo=info)
            drive_4_index_engine_pid = drive_4_index_engine_proc.pid
            drive4_index_psutil = psutil.Process(drive_4_index_engine_pid)
            print('command:', cmd)
            print('subprocess PID :', drive_4_index_engine_pid)
            if psutil.pid_exists(drive_4_index_engine_pid) == True:
                print('drive4 index engine running  :', 'yes')
            else:
                print('drive4 index engine running  :', 'failed')


def drive5IndexEngineFunction():
    global drive_5_active_config_Bool
    global drive5_index_psutil

    if drive_5_active_config_Bool == True:
        if check_index_drive5_config == True:
            cmd = ('python ' + 'index-engine-directory-d5.py')
            drive_5_index_engine_proc = subprocess.Popen(cmd, shell=False, startupinfo=info)
            drive_5_index_engine_pid = drive_5_index_engine_proc.pid
            drive5_index_psutil = psutil.Process(drive_5_index_engine_pid)
            print('command:', cmd)
            print('subprocess PID :', drive_5_index_engine_pid)
            if psutil.pid_exists(drive_5_index_engine_pid) == True:
                print('drive5 index engine running  :', 'yes')
            else:
                print('drive5 index engine running  :', 'failed')


def drive6IndexEngineFunction():
    global drive_6_active_config_Bool
    global drive6_index_psutil

    if drive_6_active_config_Bool == True:
        if check_index_drive6_config == True:
            cmd = ('python ' + 'index-engine-directory-d6.py')
            drive_6_index_engine_proc = subprocess.Popen(cmd, shell=False, startupinfo=info)
            drive_6_index_engine_pid = drive_6_index_engine_proc.pid
            drive6_index_psutil = psutil.Process(drive_6_index_engine_pid)
            print('command:', cmd)
            print('subprocess PID :', drive_6_index_engine_pid)
            if psutil.pid_exists(drive_6_index_engine_pid) == True:
                print('drive6 index engine running  :', 'yes')
            else:
                print('drive6 index engine running  :', 'failed')


def drive7IndexEngineFunction():
    global drive_7_active_config_Bool
    global drive7_index_psutil

    if drive_7_active_config_Bool == True:
        if check_index_drive7_config == True:
            cmd = ('python ' + 'index-engine-directory-d7.py')
            drive_7_index_engine_proc = subprocess.Popen(cmd, shell=False, startupinfo=info)
            drive_7_index_engine_pid = drive_7_index_engine_proc.pid
            drive7_index_psutil = psutil.Process(drive_7_index_engine_pid)
            print('command:', cmd)
            print('subprocess PID :', drive_7_index_engine_pid)
            if psutil.pid_exists(drive_7_index_engine_pid) == True:
                print('drive7 index engine running  :', 'yes')
            else:
                print('drive7 index engine running  :', 'failed')


def drive8IndexEngineFunction():
    global drive_8_active_config_Bool
    global drive8_index_psutil

    if drive_8_active_config_Bool == True:
        if check_index_drive8_config == True:
            cmd = ('python ' + 'index-engine-directory-d1.py')
            drive_8_index_engine_proc = subprocess.Popen(cmd, shell=False, startupinfo=info)
            drive_8_index_engine_pid = drive_8_index_engine_proc.pid
            drive8_index_psutil = psutil.Process(drive_8_index_engine_pid)
            print('command:', cmd)
            print('subprocess PID :', drive_8_index_engine_pid)
            if psutil.pid_exists(drive_8_index_engine_pid) == True:
                print('drive8 index engine running  :', 'yes')
            else:
                print('drive8 index engine running  :', 'failed')


def runIndexEnginesFunction():
    configurationChecksFunction()
    pluginIndexEngineFunction()
    audioIndexEngineFunction()
    imageIndexEngineFunction()
    textIndexEngineFunction()
    videoIndexEngineFunction()
    userProgramsIndexEngineFunction()
    drive1IndexEngineFunction()
    drive2IndexEngineFunction()
    drive3IndexEngineFunction()
    drive4IndexEngineFunction()
    drive5IndexEngineFunction()
    drive6IndexEngineFunction()
    drive7IndexEngineFunction()
    drive8IndexEngineFunction()
    userDirectoriesIndexEngineFunction()


def findDictateWikipediaTranscriptFunction():
    stopTranscriptionFunction()
    if len(stop_transcription_psutil) >= 0:
        stop_transcription_psutil.clear()
    cmd = 'python wikipedia-transcript-dictation.py'
    print('running command:', cmd)
    stprocess = subprocess.Popen(cmd, shell=False, startupinfo=info)
    stpid = stprocess.pid
    stop_transcription_psutil.append(psutil.Process(stpid))
    print('subprocess PID:', stpid)


def findDictateAnyTranscriptFunction():
    stopTranscriptionFunction()
    if len(stop_transcription_psutil) >= 0:
        stop_transcription_psutil.clear()
    cmd = 'python transcript-dictate.py'
    print('running command:', cmd)
    atprocess = subprocess.Popen(cmd, shell=False, startupinfo=info)
    atpid = atprocess.pid
    stop_transcription_psutil.append(psutil.Process(atpid))
    print('subprocess PID:', atpid)


def listTranscriptionsFunction():
    stopTranscriptionFunction()
    if len(list_transcriptions_psutil) >= 0:
        list_transcriptions_psutil.clear()
    cmd = 'python transcript-list.py'
    print('running command:', cmd)
    ltprocess = subprocess.Popen(cmd, shell=False, startupinfo=info)
    list_transcriptions_pid = ltprocess.pid
    list_transcriptions_psutil.append(psutil.Process(list_transcriptions_pid))
    print('subprocess PID:', list_transcriptions_pid)


def getLatestTranscriptionFunction():
    stopTranscriptionFunction()
    if len(get_latest_transcriptions_psutil) >= 0:
        get_latest_transcriptions_psutil.clear()
    cmd = 'python transcript-most-recent.py'
    print('running command:', cmd)
    gltprocess = subprocess.Popen(cmd, shell=False, startupinfo=info)
    get_latest_transcription_pid = gltprocess.pid
    get_latest_transcriptions_psutil.append(psutil.Process(get_latest_transcription_pid))
    print('subprocess PID:', get_latest_transcription_pid)


def removeBookmarkFunction():
    stopTranscriptionFunction()
    if len(remove_bookmark_psutil) >= 0:
        remove_bookmark_psutil.clear()
    cmd = 'python transcript-bookmark-remove.py'
    print('running command:', cmd)
    rbprocess = subprocess.Popen(cmd, shell=False, startupinfo=info)
    remove_bookmark_pid = rbprocess.pid
    remove_bookmark_psutil.append(psutil.Process(remove_bookmark_pid))
    print('subprocess PID:', remove_bookmark_pid)


def askGoogleTranscriptionFunction():
    stopTranscriptionFunction()
    if len(ask_google_psutil) >= 0:
        ask_google_psutil.clear()
    cmd = 'python transcript-ask-google.py'
    print('running command:', cmd)
    googleprocess = subprocess.Popen(cmd, shell=False, startupinfo=info)
    ask_google_pid = googleprocess.pid
    ask_google_psutil.append(psutil.Process(ask_google_pid))
    print('subprocess PID:', ask_google_pid)


def wiktionaryDefineFunction():
    stopTranscriptionFunction()
    if len(wiktionary_define_psutil) >= 0:
        wiktionary_define_psutil.clear()
    cmd = 'python transcript-wiktionary-define.py'
    print('running command:', cmd)
    defineprocess = subprocess.Popen(cmd, shell=False, startupinfo=info)
    wiktionary_define_pid = defineprocess.pid
    wiktionary_define_psutil.append(psutil.Process(wiktionary_define_pid))
    print('subprocess PID:', wiktionary_define_pid)


def findOpenAudioFunction():
    findOpenAudioThread.start()


def openDirectoryFunction():
    openDirectoryThread.start()


def findOpenImageFunction():
    findOpenImageThread.start()


def findOpenTextFunction():
    findOpenTextThread.start()


def findOpenVideoFunction():
    findOpenVideoThread.start()


def findOpenProgramFunction():
    findOpenProgramThread.start()


def stopTranscriptionFunction():
    try:
        print('killing transcription process:', stop_transcription_psutil)
        stop_transcription_psutil[0].kill()
    except:
        pass
    try:
        print('killing transcription process:', ask_google_psutil[0])
        ask_google_psutil[0].kill()
    except:
        pass
    try:
        print('killing transcription process:', wiktionary_define_psutil[0])
        wiktionary_define_psutil[0].kill()
    except:
        pass
    try:
        print('killing transcription process:', list_transcriptions_psutil[0])
        list_transcriptions_psutil[0].kill()
    except:
        pass
    try:
        print('killing transcription process:', get_latest_transcriptions_psutil[0])
        get_latest_transcriptions_psutil[0].kill()
    except:
        pass
    try:
        print('killing transcription process:', remove_bookmark_psutil[0])
        remove_bookmark_psutil[0].kill()
    except:
        pass


def stopIndexingPluginsFunction():
    try:
        print('killing index engine process:', plugin_index_psutil)
        plugin_index_psutil.kill()
    except:
        pass


def stopIndexingAudioFunction():
    try:
        print('killing index engine process:', audio_index_psutil)
        audio_index_psutil.kill()
    except:
        pass


def stopIndexingImageFunction():
    try:
        print('killing index engine process:', image_index_psutil)
        image_index_psutil.kill()
    except:
        pass


def stopIndexinTextFunction():
    try:
        print('killing index engine process:', text_index_psutil)
        text_index_psutil.kill()
    except:
        pass


def stopIndexingVideoFunction():
    try:
        print('killing index engine process:', video_index_psutil)
        video_index_psutil.kill()
    except:
        pass


def stopIndexingUserProgramsFunction():
    try:
        print('killing index engine process:', user_prog_index_engine_psutil)
        user_prog_index_engine_psutil.kill()
    except:
        pass


def stopIndexingUserDirectoryFunction():
    try:
        print('killing index engine process:', user_directory_index_psutil)
        user_directory_index_psutil.kill()
    except:
        pass


def stopIndexingDrive1Function():
    try:
        print('killing index engine process:', drive1_index_psutil)
        drive1_index_psutil.kill()
    except:
        pass


def stopIndexingDrive2Function():
    try:
        print('killing index engine process:', drive2_index_psutil)
        drive2_index_psutil.kill()
    except:
        pass


def stopIndexingDrive3Function():
    try:
        print('killing index engine process:', drive3_index_psutil)
        drive3_index_psutil.kill()
    except:
        pass


def stopIndexingDrive4Function():
    try:
        print('killing index engine process:', drive4_index_psutil)
        drive4_index_psutil.kill()
    except:
        pass


def stopIndexingDrive5Function():
    try:
        print('killing index engine process:', drive5_index_psutil)
        drive5_index_psutil.kill()
    except:
        pass


def stopIndexingDrive6Function():
    try:
        print('killing index engine process:', drive6_index_psutil)
        drive6_index_psutil.kill()
    except:
        pass


def stopIndexingDrive7Function():
    try:
        print('killing index engine process:', drive7_index_psutil)
        drive7_index_psutil.kill()
    except:
        pass


def stopIndexingDrive8Function():
    try:
        print('killing index engine process:', drive8_index_psutil)
        drive8_index_psutil.kill()
    except:
        pass


def stopIndexingFunction():
    stopIndexingPluginsFunction()
    stopIndexingAudioFunction()
    stopIndexingImageFunction()
    stopIndexinTextFunction()
    stopIndexingVideoFunction()
    stopIndexingUserProgramsFunction()
    stopIndexingUserDirectoryFunction()
    stopIndexingDrive1Function()
    stopIndexingDrive2Function()
    stopIndexingDrive3Function()
    stopIndexingDrive4Function()
    stopIndexingDrive5Function()
    stopIndexingDrive6Function()
    stopIndexingDrive7Function()
    stopIndexingDrive8Function()


internal_commands_list = {'stop transcription': stopTranscriptionFunction,
                          'search wikipedia': findDictateWikipediaTranscriptFunction,
                          'transcriptions available for': listTranscriptionsFunction,
                          'latest transcription for': getLatestTranscriptionFunction,
                          'remove bookmark': removeBookmarkFunction,
                          'define': wiktionaryDefineFunction,
                          'ask google': askGoogleTranscriptionFunction,
                          'play audio': findOpenAudioFunction,
                          'directory': openDirectoryFunction,
                          'open image': findOpenImageFunction,
                          'open text': findOpenTextFunction,
                          'open video': findOpenVideoFunction,
                          'run program': findOpenProgramFunction,
                          'transcription': findDictateAnyTranscriptFunction,
                          }

key_word = ['stop transcription',
            'search wikipedia',
            'transcriptions available for',
            'latest transcription for',
            'remove bookmark',
            'define',
            'ask google',
            'play audio',
            'directory',
            'open image',
            'open text',
            'open video',
            'run program',
            'transcription',
            ]


class App(QMainWindow):
    def __init__(self):
        super(App, self).__init__()
        self.indexTextEditable = False
        self.indexImageEditable = False
        self.indexVideoEditable = False
        self.indexAudioEditable = False
        self.indexDrive1Editable = False
        self.indexDrive2Editable = False
        self.indexDrive3Editable = False
        self.indexDrive4Editable = False
        self.indexDrive5Editable = False
        self.indexDrive6Editable = False
        self.indexDrive7Editable = False
        self.indexDrive8Editable = False
        self.symbiotServerIPEditable = False
        self.symbiotServerPortEditable = False
        self.symbiotIPEditable = False
        self.symbiotMACEditable = False
        self.wikiServerIPEditable = False
        self.wikiServerPortEditable = False
        self.title = "Information & Control System'"

        # minimal Geometry
        self.minimal_left = 547
        self.minimal_top = 0
        self.minimal_width = 826
        self.minimal_height = 144

        # minimal Geometry + settings
        self.minimal_extra_left = 547
        self.minimal_extra_top = 0
        self.minimal_extra_width = 826
        self.minimal_extra_height = 400

        # Full Screen Geometry
        self.left_max = 0
        self.top_max = 0
        self.width_max = 1920
        self.height_max = 1080



        p = self.palette()
        p.setColor(self.backgroundRole(), Qt.black)
        self.setPalette(p)
        # self.setWindowOpacity(0.75)

        self.initUI()

    def initUI(self):

        global value
        global secondary_key
        global sppid
        global target_index
        global target_match
        global multiple_matches
        global findOpenAudioThread
        global currentAudioMedia
        global speechRecognitionThread
        global guiControllerThread
        global drawMenuThread
        global menuVisible
        global openDirectoryThread
        global findOpenImageThread
        global findOpenTextThread
        global findOpenVideoThread
        global findOpenProgramThread
        global configInteractionPermissionThread
        global symbiotServerthread
        global symbiot_configuration_Bool
        global wiki_local_server_ip_configuration_Bool
        global wiki_local_server_port_configuration_Bool
        global guiMode1Thread
        global show_hide_settings
        global sr_active

        # UI Geometry
        self.setWindowTitle('Information & Control System')
        # self.setWindowFlags(Qt.Window | Qt.FramelessWindowHint)
        self.setWindowFlags(QtCore.Qt.CustomizeWindowHint)

        # # max
        # self.setGeometry(self.left_max, self.top_max, self.width_max, self.height_max)
        # self.setFixedSize(self.width_max, self.height_max)

        # min
        self.setGeometry(self.minimal_left, self.minimal_top, self.minimal_width, self.minimal_height)
        self.setFixedSize(self.minimal_width, self.minimal_height)

        self.setWindowIcon(QtGui.QIcon("./Resources/logo_icon.ico"))

        # oImage = QImage("./Resources/main_dash_background_image4.png")
        # sImage = oImage.scaled(QSize(1920, 1080))  # resize Image to widgets size
        # palette = QPalette()
        # palette.setBrush(10, QBrush(sImage))  # 10 = Windowrole
        # self.setPalette(palette)

        # Close
        self.exitClose = QPushButton(self)
        self.exitClose.move(778, 0)
        self.exitClose.resize(48, 24)
        self.exitClose.clicked.connect(stopIndexingFunction)
        self.exitClose.clicked.connect(stopTranscriptionFunction)
        self.exitClose.clicked.connect(QCoreApplication.instance().quit)
        self.exitClose.setStyleSheet(
            """QPushButton {background-color: rgb(255, 0,0);
           border:1px solid rgb(0, 0, 0);}"""
        )
        # Hide
        self.hiddenButton = QPushButton(self)
        self.hiddenButton.move(730, 0)
        self.hiddenButton.resize(48, 24)
        self.hiddenButton.clicked.connect(self.showMinimized)
        self.hiddenButton.setStyleSheet(
            """QPushButton {background-color: rgb(0, 0,255);
           border:1px solid rgb(0, 0, 0);}"""
        )

        # Settings Title
        self.settings_menu_title = QLabel(self)
        self.settings_menu_title.move(100, 24)
        self.settings_menu_title.resize(300, 96)
        newfont = QtGui.QFont("Times", 48, QtGui.QFont.Bold)
        self.settings_menu_title.setFont(newfont)
        self.settings_menu_title.setText("Settings")
        self.settings_menu_title.setStyleSheet(
            """QLabel {background-color: rgb(0, 0, 0);
           color: yellow;
           border: false;}"""
        )
        self.settings_menu_title.hide()

        # Settings Menu
        show_hide_settings = QPushButton(self)
        show_hide_settings.move(3, 30)
        show_hide_settings.resize(48, 48)
        show_hide_settings.clicked.connect(self.showHideSettingsFunction)
        show_hide_settings.setIcon(QIcon("./Resources/image/setting_menu_icon.png"))
        show_hide_settings.setStyleSheet(
            """QPushButton{background-color: rgb(0, 0, 0);
           border:1px solid rgb(0, 0, 255);}"""
        )

        def srActiveFunction():
            if sr_active == False:
                speechRecognitionOnFunction()
            elif sr_active == True:
                speechRecognitionOffFunction()

        def speechRecognitionOnFunction():
            global sr_active
            sr_active = True
            self.srOnButton.setIcon(QIcon("./Resources/image/voice_image_icon.png"))
            self.srOnButton.setStyleSheet(
                """QPushButton {background-color: rgb(0, 0, 0);
                border:1px solid rgb(0, 255, 0);}"""
            )
            speechRecognitionThread.start()
            print('speech recognition: on')

        def speechRecognitionOffFunction():
            global sr_active
            sr_active = False
            self.srOnButton.setIcon(QIcon("./Resources/image/voice_image_icon.png"))
            self.srOnButton.setStyleSheet(
                """QPushButton {background-color: rgb(0, 0, 0);
                border:1px solid rgb(0, 0, 255);}"""
            )
            speechRecognitionThread.stop_sr()
            guiControllerOffFunction()
            print('speech recognition: off')

        def guiControllerOffFunction():
            guiControllerThread.stop_guiController()
            print('guiController: off')

        def symbiotEnableDisableFunction():
            global symbiot_configuration_Bool
            # global symbiotServerThread

            if symbiot_configuration_Bool == False:
                print('enabling symbiot server')
                symbiotServerThread.start()
                symbiot_configuration_Bool = True
                symbiotButton.setStyleSheet(
                    """QPushButton {background-color: rgb(0, 0, 0);
                    border:1px solid rgb(0, 255, 0);}"""
                )

            elif symbiot_configuration_Bool == True:
                print('disabling symbiot server')
                symbiotServerThread.symbiot_server_off()
                symbiot_configuration_Bool = False
                symbiotButton.setStyleSheet(
                    """QPushButton {background-color: rgb(0, 0, 0);
                    border:1px solid rgb(0, 0, 255);}"""
                )

        # Symbiot On/Off
        symbiotButton = QPushButton(self)
        symbiotButton.move(3, 78)
        symbiotButton.resize(48, 48)
        symbiotButton.clicked.connect(symbiotEnableDisableFunction)
        if symbiot_configuration_Bool == True:
            symbiotButton.setIcon(QIcon("./Resources/image/symbiot_button_icon.png"))
            symbiotButton.setStyleSheet(
                """QPushButton{background-color: rgb(0, 0, 0);
               border:1px solid rgb(0, 0, 0);}"""
            )

            symbiot_configuration_Bool = False
        elif symbiot_configuration_Bool == False:
            symbiotButton.setIcon(QIcon("./Resources/image/symbiot_button_icon.png"))
            symbiotButton.setStyleSheet(
                """QPushButton{background-color: rgb(0, 0, 0);
               border:1px solid rgb(0, 0, 255);}"""
            )

        # Sr on
        self.srOnButton = QPushButton(self)
        self.srOnButton.move(774, 30)
        self.srOnButton.resize(48, 48)
        self.srOnButton.setIcon(QIcon("./Resources/image/voice_image_icon.png"))
        self.srOnButton.clicked.connect(srActiveFunction)
        self.srOnButton.setStyleSheet(
            """QPushButton{background-color: rgb(0, 0, 0);
           border:1px solid rgb(0, 0, 255);}"""
        )

        # Sr Indicator
        self.srIndicator = QLabel(self)
        self.srIndicator.move(810, 390)
        self.srIndicator.resize(300, 300)
        pixmap = QPixmap('./Resources/image/sr_indicator_off_icon.png')
        self.srIndicator.setPixmap(pixmap)
        self.srIndicator.hide()

        # Create Speech Interpretation Info
        self.srInfo = QLineEdit(self)
        self.srInfo.move(70, 30)
        self.srInfo.resize(700, 20)
        self.srInfo.setReadOnly(True)
        self.srInfo.setStyleSheet(
            """QLineEdit {background-color: black;
            border:1px solid rgb(0, 0, 255);
            border-bottom:1px solid rgb(0, 0, 0);
            selection-color: black;
            selection-background-color: black;
            color: rgb(115, 255, 0);}"""
        )
        # Create Speech Interpretation TextBox
        self.textBoxValue = QLineEdit(self)
        self.textBoxValue.move(70, 50)
        self.textBoxValue.resize(700, 20)
        self.textBoxValue.setReadOnly(True)
        self.textBoxValue.setStyleSheet(
            """QLineEdit {background-color: black;
            border-top:1px solid rgb(0, 0, 0);
            border-left:1px solid rgb(0, 0, 255);
            border-right:1px solid rgb(0, 0, 255);
            border-bottom:1px solid rgb(0, 0, 0);
            selection-color: black;
            selection-background-color: black;
            color: #00FF00;}"""
        )

        # Create verbose textbox
        self.textBoxVerbose1 = QLineEdit(self)
        self.textBoxVerbose1.move(70, 70)
        self.textBoxVerbose1.resize(700, 20)
        self.textBoxVerbose1.setReadOnly(True)
        self.textBoxVerbose1.setStyleSheet(
            """QLineEdit {background-color: black;
            border:1px solid rgb(0, 0, 255);
            border-top:1px solid rgb(0, 0, 0);
            border-bottom:1px solid rgb(0, 0, 0);
            selection-color: black;
            selection-background-color: black;
            color: #00FF00;}"""
        )
        # Create verbose textbox2
        self.textBoxVerbose2 = QLineEdit(self)
        self.textBoxVerbose2.move(70, 90)
        self.textBoxVerbose2.resize(700, 20)
        self.textBoxVerbose2.setReadOnly(True)
        self.textBoxVerbose2.setStyleSheet(
            """QLineEdit {background-color: black;
            border:1px solid rgb(0, 0, 255);
            border-top:1px solid rgb(0, 0, 0);
            selection-color: black;
            selection-background-color: black;
            color: #00FF00;}"""
        )

        # SETTINGS
        def configInteractionPermissionFunction():
            configInteractionPermissionThread.start()

        self.indexTitle = QLabel(self)
        self.indexTitle.move(70, 148)
        self.indexTitle.resize(100, 20)
        self.indexTitle.setText('User Index Settings')
        self.indexTitle.setStyleSheet(
            """QLabel {
           color: yellow;
           border: false;}"""
        )
        self.indexTitle2 = QLabel(self)
        self.indexTitle2.move(390, 148)
        self.indexTitle2.resize(120, 20)
        self.indexTitle2.setText('Advanced Index Settings')
        self.indexTitle2.setStyleSheet(
            """QLabel {
           color: yellow;
           border: false;}"""
        )

        # Wiki Settings
        self.wikiSettingsLabel = QLabel(self)
        self.wikiSettingsLabel.move(390, 263)
        self.wikiSettingsLabel.resize(100, 20)
        self.wikiSettingsLabel.setText('Information Settings')
        self. wikiSettingsLabel.setStyleSheet(
            """QLabel {
           color: yellow;
           border: false;}"""
        )
        # Wiki show in browser
        self.wikiShowBrowserLabel = QLabel(self)
        self.wikiShowBrowserLabel.move(390, 283)
        self.wikiShowBrowserLabel.resize(135, 20)
        self.wikiShowBrowserLabel.setText('Show Wikipedia in Browser?')
        self.wikiShowBrowserLabel.setStyleSheet(
            """QLabel {
           color: green;
           border: false;}"""
        )

        self.wikiShowBrowserButton = QPushButton(self)
        self.wikiShowBrowserButton.move(525, 283)
        self.wikiShowBrowserButton.resize(50, 20)
        if wiki_show_browser_Bool == False:
            self.wikiShowBrowserButton.setText('Disabled')
            self.wikiShowBrowserButton.setStyleSheet(
                """QPushButton {background-color: rgb(0, 0, 0);
               color: red;
               border: false;}"""
            )
        elif wiki_show_browser_Bool == True:
            self.wikiShowBrowserButton.setText('Enabled')
            self.wikiShowBrowserButton.setStyleSheet(
                """QPushButton {background-color: rgb(0, 0, 0);
               color: green;
               border: false;}"""
            )
        self.wikiShowBrowserButton.clicked.connect(self.wikiShowBrowserFunction)
        self.wikiShowBrowserButton.hide()

        # Dictate Wiki transcripts
        self.dictateWikiLabel = QLabel(self)
        self.dictateWikiLabel.move(390, 298)
        self.dictateWikiLabel.resize(135, 20)
        self.dictateWikiLabel.setText('Dictate Wiki Transcripts?')
        self.dictateWikiLabel.setStyleSheet(
            """QLabel {
           color: green;
           border: false;}"""
        )
        self.dictateWikiButton = QPushButton(self)
        self.dictateWikiButton.move(525, 298)
        self.dictateWikiButton.resize(50, 20)
        if wiki_dictate_Bool == False:
            self.dictateWikiButton.setText('Disabled')
            self.dictateWikiButton.setStyleSheet(
                """QPushButton {background-color: rgb(0, 0, 0);
               color: red;
               border: false;}"""
            )
        elif wiki_dictate_Bool == True:
            self.dictateWikiButton.setText('Enabled')
            self.dictateWikiButton.setStyleSheet(
                """QPushButton {background-color: rgb(0, 0, 0);
               color: green;
               border: false;}"""
            )
        self.dictateWikiButton.clicked.connect(self.dictateWikiFunction)
        self.dictateWikiButton.hide()

        # Enable/Disable USE of Local Wiki Server
        self.useLocalWikiLabel = QLabel(self)
        self.useLocalWikiLabel.move(390, 313)
        self.useLocalWikiLabel.resize(135, 20)
        self.useLocalWikiLabel.setText('Use Local Wiki Server?')
        self.useLocalWikiLabel.setStyleSheet(
            """QLabel {
           color: green;
           border: false;}"""
        )
        self.useLocalWikiButton = QPushButton(self)
        self.useLocalWikiButton.move(525, 313)
        self.useLocalWikiButton.resize(50, 20)
        if allow_wiki_local_server_Bool == False:
            self.useLocalWikiButton.setText('Disabled')
            self.useLocalWikiButton.setStyleSheet(
                """QPushButton {background-color: rgb(0, 0, 0);
               color: red;
               border: false;}"""
            )
        elif allow_wiki_local_server_Bool == True:
            self.useLocalWikiButton.setText('Enabled')
            self.useLocalWikiButton.setStyleSheet(
                """QPushButton {background-color: rgb(0, 0, 0);
               color: green;
               border: false;}"""
            )
        self.useLocalWikiButton.clicked.connect(self.useLocalWikiFunction)

        # Wiki Server IP Button
        self.wikiServerIPButton = QPushButton(self)
        self.wikiServerIPButton.move(570, 283)
        self.wikiServerIPButton.resize(75, 20)
        self.wikiServerIPButton.setText('Wiki Server')
        self.wikiServerIPButton.clicked.connect(self.wikiServerIPFunction)
        self.wikiServerIPButton.setStyleSheet(
            """QPushButton {background-color: rgb(0, 0, 0);
           color: green;
           border: false;}"""
        )
        # Wiki Server IP Edit
        self.wikiServerIPEdit = QLineEdit(self)
        self.wikiServerIPEdit.move(640, 283)
        self.wikiServerIPEdit.resize(110, 20)
        self.wikiServerIPEdit.setReadOnly(True)
        self.wikiServerIPEdit.setText(wiki_local_server_ip_configuration)  # .replace('SYMBIOT_SERVER: ', ''))
        self.wikiServerIPEdit.returnPressed.connect(self.writeWikiServerFunction)
        self.wikiServerIPEdit.setStyleSheet(
            """QLineEdit {background-color: rgb(15, 14, 15);
            border:5px solid rgb(0, 0, 0);
            selection-color: black;
            selection-background-color: black;
            color: grey;}"""
        )
        # Wiki Server Port Button
        self.wikiServerPortButton = QPushButton(self)
        self.wikiServerPortButton.move(570, 298)
        self.wikiServerPortButton.resize(125, 20)
        self.wikiServerPortButton.setText('Wiki Server Port')
        self.wikiServerPortButton.clicked.connect(self.wikiServerPortFunction)
        self.wikiServerPortButton.setStyleSheet(
            """QPushButton {background-color: rgb(0, 0, 0);
           color: green;
           border: false;}"""
        )
        # Wiki Server Port Edit
        self.wikiServerPortEdit = QLineEdit(self)
        self.wikiServerPortEdit.move(695, 298)
        self.wikiServerPortEdit.resize(55, 20)
        self.wikiServerPortEdit.setReadOnly(True)
        self.wikiServerPortEdit.setText(wiki_local_server_port_configuration)  # .replace('SYMBIOT_SERVER: ', ''))
        self.wikiServerPortEdit.returnPressed.connect(self.writeWikiServerPortFunction)
        self.wikiServerPortEdit.setStyleSheet(
            """QLineEdit {background-color: rgb(15, 14, 15);
            border:5px solid rgb(0, 0, 0);
            selection-color: black;
            selection-background-color: black;
            color: grey;}"""
        )

        # Symbiot Settings
        self.symbiotTitle = QLabel(self)
        self.symbiotTitle.move(74, 263)
        self.symbiotTitle.resize(100, 20)
        self.symbiotTitle.setText('Symbiot Settings')
        self.symbiotTitle.setStyleSheet(
            """QLabel {
           color: yellow;
           border: false;}"""
        )
        # Symbiot Server IP Button
        self.symbiotServerIPButton = QPushButton(self)
        self.symbiotServerIPButton.move(74, 283)
        self.symbiotServerIPButton.resize(80, 20)
        self.symbiotServerIPButton.setText('Server IP')
        self.symbiotServerIPButton.clicked.connect(self.symbiotServerIPFunction)
        self.symbiotServerIPButton.setStyleSheet(
            """QPushButton {background-color: rgb(0, 0, 0);
           color: green;
           border: false;}"""
        )
        # Symbiot Server IP Edit
        self.symbiotServerIPEdit = QLineEdit(self)
        self.symbiotServerIPEdit.move(144, 283)
        self.symbiotServerIPEdit.resize(120, 20)
        self.symbiotServerIPEdit.setReadOnly(True)
        self.symbiotServerIPEdit.setText(symbiot_server_ip_configuration)  # .replace('SYMBIOT_SERVER: ', ''))
        self.symbiotServerIPEdit.returnPressed.connect(self.writeSymbiotServerIPFunction)
        self.symbiotServerIPEdit.setStyleSheet(
            """QLineEdit {background-color: rgb(15, 14, 15);
            border:5px solid rgb(0, 0, 0);
            selection-color: black;
            selection-background-color: black;
            color: grey;}"""
        )
        # Symbiot Server Port Button
        self.symbiotServerPortButton = QPushButton(self)
        self.symbiotServerPortButton.move(74, 298)
        self.symbiotServerPortButton.resize(80, 20)
        self.symbiotServerPortButton.setText('Server Port')
        self.symbiotServerPortButton.clicked.connect(self.symbiotServerPortFunction)
        self.symbiotServerPortButton.setStyleSheet(
            """QPushButton {background-color: rgb(0, 0, 0);
           color: green;
           border: false;}"""
        )
        # Symbiot Server Port Edit
        self.symbiotServerPortEdit = QLineEdit(self)
        self.symbiotServerPortEdit.move(144, 298)
        self.symbiotServerPortEdit.resize(120, 20)
        self.symbiotServerPortEdit.setReadOnly(True)
        self.symbiotServerPortEdit.setText(symbiot_server_port_configuration)  # .replace('SYMBIOT_SERVER_PORT: ', ''))
        self.symbiotServerPortEdit.returnPressed.connect(self.writeSymbiotServerPortFunction)
        self.symbiotServerPortEdit.setStyleSheet(
            """QLineEdit {background-color: rgb(15, 14, 15);
            border:5px solid rgb(0, 0, 0);
            selection-color: black;
            selection-background-color: black;
            color: grey;}"""
        )
        # Symbiot IP Button
        self.symbiotIPButton = QPushButton(self)
        self.symbiotIPButton.move(74, 313)
        self.symbiotIPButton.resize(80, 20)
        self.symbiotIPButton.setText('Symbiot IP')
        self.symbiotIPButton.clicked.connect(self.symbiotIPFunction)
        self.symbiotIPButton.setStyleSheet(
            """QPushButton {background-color: rgb(0, 0, 0);
           color: green;
           border: false;}"""
        )
        # Symbiot IP Edit
        self.symbiotIPEdit = QLineEdit(self)
        self.symbiotIPEdit.move(144, 313)
        self.symbiotIPEdit.resize(120, 20)
        self.symbiotIPEdit.setReadOnly(True)
        self.symbiotIPEdit.setText(symbiot_ip_configuration)  # .replace('SYMBIOT_IP: ', ''))
        self.symbiotIPEdit.returnPressed.connect(self.writeSymbiotIPFunction)
        self.symbiotIPEdit.setStyleSheet(
            """QLineEdit {background-color: rgb(15, 14, 15);
            border:5px solid rgb(0, 0, 0);
            selection-color: black;
            selection-background-color: black;
            color: grey;}"""
        )
        # Symbiot MAC Button
        self.symbiotMACButton = QPushButton(self)
        self.symbiotMACButton.move(74, 328)
        self.symbiotMACButton.resize(80, 20)
        self.symbiotMACButton.setText('Symbiot MAC')
        self.symbiotMACButton.clicked.connect(self.symbiotMACFunction)
        self.symbiotMACButton.setStyleSheet(
            """QPushButton {background-color: rgb(0, 0, 0);
           color: green;
           border: false;}"""
        )
        # Symbiot MAC Edit
        self.symbiotMACEdit = QLineEdit(self)
        self.symbiotMACEdit.move(144, 328)
        self.symbiotMACEdit.resize(120, 20)
        self.symbiotMACEdit.setReadOnly(True)
        self.symbiotMACEdit.setText(symbiot_mac_configuration)  # .replace('SYMBIOT_MAC: ', ''))
        self.symbiotMACEdit.returnPressed.connect(self.writeSymbiotMACFunction)
        self.symbiotMACEdit.setStyleSheet(
            """QLineEdit {background-color: rgb(15, 14, 15);
            border:5px solid rgb(0, 0, 0);
            selection-color: black;
            selection-background-color: black;
            color: grey;}"""
        )

        # Index Audio Settings
        self.indexAudioButton = QPushButton(self)
        self.indexAudioButton.move(74, 168)
        self.indexAudioButton.resize(45, 20)
        self.indexAudioButton.setText('Audio')
        self.indexAudioButton.clicked.connect(self.indexAudioConfigurationFunction)
        self.indexAudioButton.setStyleSheet(
            """QPushButton {background-color: rgb(0, 0, 0);
           color: green;
           border: false;}"""
        )
        self.indexAudioEdit = QLineEdit(self)
        self.indexAudioEdit.move(119, 168)
        self.indexAudioEdit.resize(170, 20)
        self.indexAudioEdit.setReadOnly(True)
        self.indexAudioEdit.setText(audio_configuration.replace('DIRAUD: ', ''))
        self.indexAudioEdit.returnPressed.connect(self.writeAudioPathFunction)
        self.indexAudioEdit.setStyleSheet(
            """QLineEdit {background-color: rgb(15, 14, 15);
            border:5px solid rgb(0, 0, 0);
            selection-color: black;
            selection-background-color: black;
            color: grey;}"""
        )
        self.indexAudioEnableDisableButton = QPushButton(self)
        self.indexAudioEnableDisableButton.move(289, 168)
        self.indexAudioEnableDisableButton.resize(45, 20)
        self.indexAudioEnableDisableButton.setText(audio_active_config)
        self.indexAudioEnableDisableButton.clicked.connect(configInteractionPermissionFunction)
        self.indexAudioEnableDisableButton.clicked.connect(self.audioIndexEnableDisableFunction)
        if audio_active_config_Bool == False:
            self.indexAudioEnableDisableButton.setStyleSheet(
                """QPushButton {background-color: rgb(0, 0, 0);
               color: red;
               border: false;}"""
            )
        elif audio_active_config_Bool == True:
            self.indexAudioEnableDisableButton.setStyleSheet(
                """QPushButton {background-color: rgb(0, 0, 0);
               color: green;
               border: false;}"""
            )

        # Video Index Settings
        self.indexVideoButton = QPushButton(self)
        self.indexVideoButton.move(74, 183)
        self.indexVideoButton.resize(45, 20)
        self.indexVideoButton.setText('Video')
        self.indexVideoButton.clicked.connect(self.indexVideoConfigurationFunction)
        self.indexVideoButton.setStyleSheet(
            """QPushButton {background-color: rgb(0, 0, 0);
           color: green;
           border: false;}"""
        )
        self.indexVideoEdit = QLineEdit(self)
        self.indexVideoEdit.move(119, 183)
        self.indexVideoEdit.resize(170, 20)
        self.indexVideoEdit.setReadOnly(True)
        self.indexVideoEdit.setText(video_configuration.replace('DIRVID: ', ''))
        self.indexVideoEdit.returnPressed.connect(self.writeVideoPathFunction)
        self.indexVideoEdit.setStyleSheet(
            """QLineEdit {background-color: rgb(15, 14, 15);
            border:5px solid rgb(0, 0, 0);
            selection-color: black;
            selection-background-color: black;
            color: grey;}"""
        )
        self.indexVideoEnableDisableButton = QPushButton(self)
        self.indexVideoEnableDisableButton.move(289, 183)
        self.indexVideoEnableDisableButton.resize(45, 20)
        self.indexVideoEnableDisableButton.setText(video_active_config)
        self.indexVideoEnableDisableButton.clicked.connect(configInteractionPermissionFunction)
        self.indexVideoEnableDisableButton.clicked.connect(self.videoIndexEnableDisableFunction)
        if video_active_config_Bool == False:
            self.indexVideoEnableDisableButton.setStyleSheet(
                """QPushButton {background-color: rgb(0, 0, 0);
               color: red;
               border: false;}"""
            )
        elif video_active_config_Bool == True:
            self.indexVideoEnableDisableButton.setStyleSheet(
                """QPushButton {background-color: rgb(0, 0, 0);
               color: green;
               border: false;}"""
            )

        # Images Index Settings
        self.indexImagesButton = QPushButton(self)
        self.indexImagesButton.move(74, 198)
        self.indexImagesButton.resize(45, 20)
        self.indexImagesButton.setText('  Images')
        self.indexImagesButton.clicked.connect(self.indexImagesConfigurationFunction)
        self.indexImagesButton.setStyleSheet(
            """QPushButton {background-color: rgb(0, 0, 0);
           color: green;
           border: false;}"""
        )
        self.indexImagesEdit = QLineEdit(self)
        self.indexImagesEdit.move(119, 198)
        self.indexImagesEdit.resize(170, 20)
        self.indexImagesEdit.setReadOnly(True)
        self.indexImagesEdit.setText(image_configuration.replace('DIRIMG: ', ''))
        self.indexImagesEdit.returnPressed.connect(self.writeImagesPathFunction)
        self.indexImagesEdit.setStyleSheet(
            """QLineEdit {background-color: rgb(15, 14, 15);
            border:5px solid rgb(0, 0, 0);
            selection-color: black;
            selection-background-color: black;
            color: grey;}"""
        )
        self.indexImageEnableDisableButton = QPushButton(self)
        self.indexImageEnableDisableButton.move(289, 198)
        self.indexImageEnableDisableButton.resize(45, 20)
        self.indexImageEnableDisableButton.setText(image_active_config)
        self.indexImageEnableDisableButton.clicked.connect(configInteractionPermissionFunction)
        self.indexImageEnableDisableButton.clicked.connect(self.imageIndexEnableDisableFunction)
        if image_active_config_Bool == False:
            self.indexImageEnableDisableButton.setStyleSheet(
                """QPushButton {background-color: rgb(0, 0, 0);
               color: red;
               border: false;}"""
            )
        elif image_active_config_Bool == True:
            self.indexImageEnableDisableButton.setStyleSheet(
                """QPushButton {background-color: rgb(0, 0, 0);
               color: green;
               border: false;}"""
            )

        # Text Index Settings
        self.indexTextButton = QPushButton(self)
        self.indexTextButton.move(74, 213)
        self.indexTextButton.resize(45, 20)
        self.indexTextButton.setText('Text')
        self.indexTextButton.clicked.connect(self.indexTextConfigurationFunction)
        self.indexTextButton.setStyleSheet(
            """QPushButton {background-color: rgb(0, 0, 0);
           color: green;
           border: false;}"""
        )
        self.indexTextEdit = QLineEdit(self)
        self.indexTextEdit.move(119, 213)
        self.indexTextEdit.resize(170, 20)
        self.indexTextEdit.setReadOnly(True)
        self.indexTextEdit.setText(text_configuration.replace('DIRTXT: ', ''))
        self.indexTextEdit.returnPressed.connect(self.writeTextPathFunction)
        self.indexTextEdit.setStyleSheet(
            """QLineEdit {background-color: rgb(15, 14, 15);
            border:5px solid rgb(0, 0, 0);
            selection-color: black;
            selection-background-color: black;
            color: grey;}"""
        )
        self.indexTextEnableDisableButton = QPushButton(self)
        self.indexTextEnableDisableButton.move(289, 213)
        self.indexTextEnableDisableButton.resize(45, 20)
        self.indexTextEnableDisableButton.setText(text_active_config)
        self.indexTextEnableDisableButton.clicked.connect(configInteractionPermissionFunction)
        self.indexTextEnableDisableButton.clicked.connect(self.textIndexEnableDisableFunction)
        if text_active_config_Bool == False:
            self.indexTextEnableDisableButton.setStyleSheet(
                """QPushButton {background-color: rgb(0, 0, 0);
               color: red;
               border: false;}"""
            )
        elif text_active_config_Bool == True:
            self.indexTextEnableDisableButton.setStyleSheet(
                """QPushButton {background-color: rgb(0, 0, 0);
               color: green;
               border: false;}"""
            )

        # Drive1 Index Settings
        self.drive1Button = QPushButton(self)
        self.drive1Button.move(370, 168)
        self.drive1Button.resize(45, 20)
        self.drive1Button.setText(' 1')
        self.drive1Button.clicked.connect(self.indexDrive1ConfigurationFunction)
        self.drive1Button.setStyleSheet(
            """QPushButton {background-color: rgb(0, 0, 0);
           color: green;
           border: false;}"""
        )
        self.drive1TextEdit = QLineEdit(self)
        self.drive1TextEdit.move(415, 168)
        self.drive1TextEdit.resize(100, 20)
        self.drive1TextEdit.setReadOnly(True)
        self.drive1TextEdit.setText(drive1_configuration.replace('DRIVE1: ', ''))
        self.drive1TextEdit.returnPressed.connect(self.writeDrive1PathFunction)
        self.drive1TextEdit.setStyleSheet(
            """QLineEdit {background-color: rgb(15, 14, 15);
            border:5px solid rgb(0, 0, 0);
            selection-color: black;
            selection-background-color: black;
            color: grey;}"""
        )
        self.drive1EnableDisableButton = QPushButton(self)
        self.drive1EnableDisableButton.move(515, 168)
        self.drive1EnableDisableButton.resize(45, 20)
        self.drive1EnableDisableButton.setText(drive_1_active_config)
        self.drive1EnableDisableButton.clicked.connect(configInteractionPermissionFunction)
        self.drive1EnableDisableButton.clicked.connect(self.drive1EnableDisableFunction)
        if drive_1_active_config_Bool == False:
            self.drive1EnableDisableButton.setStyleSheet(
                """QPushButton {background-color: rgb(0, 0, 0);
               color: red;
               border: false;}"""
            )
        elif drive_1_active_config_Bool == True:
            self.drive1EnableDisableButton.setStyleSheet(
                """QPushButton {background-color: rgb(0, 0, 0);
               color: green;
               border: false;}"""
            )

        # Drive2 Index Settings
        self.drive2Button = QPushButton(self)
        self.drive2Button.move(370, 183)
        self.drive2Button.resize(45, 20)
        self.drive2Button.setText(' 2')
        self. drive2Button.clicked.connect(self.indexDrive2ConfigurationFunction)
        self.drive2Button.setStyleSheet(
            """QPushButton {background-color: rgb(0, 0, 0);
           color: green;
           border: false;}"""
        )
        self.drive2TextEdit = QLineEdit(self)
        self.drive2TextEdit.move(415, 183)
        self.drive2TextEdit.resize(100, 20)
        self.drive2TextEdit.setReadOnly(True)
        self.drive2TextEdit.setText(drive2_configuration.replace('DRIVE2: ', ''))
        self.drive2TextEdit.returnPressed.connect(self.writeDrive2PathFunction)
        self.drive2TextEdit.setStyleSheet(
            """QLineEdit {background-color: rgb(15, 14, 15);
            border:5px solid rgb(0, 0, 0);
            selection-color: black;
            selection-background-color: black;
            color: grey;}"""
        )
        self.drive2EnableDisableButton = QPushButton(self)
        self.drive2EnableDisableButton.move(515, 183)
        self.drive2EnableDisableButton.resize(45, 20)
        self.drive2EnableDisableButton.setText(drive_2_active_config)
        self.drive2EnableDisableButton.clicked.connect(configInteractionPermissionFunction)
        self.drive2EnableDisableButton.clicked.connect(self.drive2EnableDisableFunction)
        if drive_2_active_config_Bool == False:
            self.drive2EnableDisableButton.setStyleSheet(
                """QPushButton {background-color: rgb(0, 0, 0);
               color: red;
               border: false;}"""
            )
        elif drive_2_active_config_Bool == True:
            self.drive2EnableDisableButton.setStyleSheet(
                """QPushButton {background-color: rgb(0, 0, 0);
               color: green;
               border: false;}"""
            )

        # Drive3 Index Settings
        self.drive3Button = QPushButton(self)
        self.drive3Button.move(370, 198)
        self.drive3Button.resize(45, 20)
        self.drive3Button.setText(' 3')
        self.drive3Button.clicked.connect(self.indexDrive3ConfigurationFunction)
        self.drive3Button.setStyleSheet(
            """QPushButton {background-color: rgb(0, 0, 0);
           color: green;
           border: false;}"""
        )
        self.drive3TextEdit = QLineEdit(self)
        self.drive3TextEdit.move(415, 198)
        self.drive3TextEdit.resize(100, 20)
        self.drive3TextEdit.setReadOnly(True)
        self.drive3TextEdit.setText(drive3_configuration.replace('DRIVE3: ', ''))
        self.drive3TextEdit.returnPressed.connect(self.writeDrive3PathFunction)
        self.drive3TextEdit.setStyleSheet(
            """QLineEdit {background-color: rgb(15, 14, 15);
            border:5px solid rgb(0, 0, 0);
            selection-color: black;
            selection-background-color: black;
            color: grey;}"""
        )
        self.drive3EnableDisableButton = QPushButton(self)
        self.drive3EnableDisableButton.move(515, 198)
        self.drive3EnableDisableButton.resize(45, 20)
        self.drive3EnableDisableButton.setText(drive_3_active_config)
        self.drive3EnableDisableButton.clicked.connect(configInteractionPermissionFunction)
        self.drive3EnableDisableButton.clicked.connect(self.drive3EnableDisableFunction)
        if drive_3_active_config_Bool == False:
            self.drive3EnableDisableButton.setStyleSheet(
                """QPushButton {background-color: rgb(0, 0, 0);
               color: red;
               border: false;}"""
            )
        elif drive_3_active_config_Bool == True:
            self.drive3EnableDisableButton.setStyleSheet(
                """QPushButton {background-color: rgb(0, 0, 0);
               color: green;
               border: false;}"""
            )

        # Drive4 Indexing Settings
        self.drive4Button = QPushButton(self)
        self.drive4Button.move(370, 213)
        self.drive4Button.resize(45, 20)
        self.drive4Button.setText(' 4')
        self.drive4Button.clicked.connect(self.indexDrive4ConfigurationFunction)
        self.drive4Button.setStyleSheet(
            """QPushButton {background-color: rgb(0, 0, 0);
           color: green;
           border: false;}"""
        )
        self.drive4TextEdit = QLineEdit(self)
        self.drive4TextEdit.move(415, 213)
        self.drive4TextEdit.resize(100, 20)
        self.drive4TextEdit.setReadOnly(True)
        self.drive4TextEdit.setText(drive4_configuration.replace('DRIVE4: ', ''))
        self.drive4TextEdit.returnPressed.connect(self.writeDrive4PathFunction)
        self.drive4TextEdit.setStyleSheet(
            """QLineEdit {background-color: rgb(15, 14, 15);
            border:5px solid rgb(0, 0, 0);
            selection-color: black;
            selection-background-color: black;
            color: grey;}"""
        )
        self.drive4EnableDisableButton = QPushButton(self)
        self.drive4EnableDisableButton.move(515, 213)
        self.drive4EnableDisableButton.resize(45, 20)
        self.drive4EnableDisableButton.setText(drive_4_active_config)
        self.drive4EnableDisableButton.clicked.connect(configInteractionPermissionFunction)
        self.drive4EnableDisableButton.clicked.connect(self.drive4EnableDisableFunction)
        if drive_4_active_config_Bool == False:
            self.drive4EnableDisableButton.setStyleSheet(
                """QPushButton {background-color: rgb(0, 0, 0);
               color: red;
               border: false;}"""
            )
        elif drive_4_active_config_Bool == True:
            self.drive4EnableDisableButton.setStyleSheet(
                """QPushButton {background-color: rgb(0, 0, 0);
               color: green;
               border: false;}"""
            )
        # Drive5 Index Settings
        self.drive5Button = QPushButton(self)
        self.drive5Button.move(565, 168)
        self.drive5Button.resize(45, 20)
        self.drive5Button.setText(' 5')
        self.drive5Button.clicked.connect(self.indexDrive5ConfigurationFunction)
        self.drive5Button.setStyleSheet(
            """QPushButton {background-color: rgb(0, 0, 0);
           color: green;
           border: false;}"""
        )
        self.drive5TextEdit = QLineEdit(self)
        self.drive5TextEdit.move(610, 168)
        self.drive5TextEdit.resize(100, 20)
        self.drive5TextEdit.setReadOnly(True)
        self.drive5TextEdit.setText(drive5_configuration.replace('DRIVE5: ', ''))
        self.drive5TextEdit.returnPressed.connect(self.writeDrive5PathFunction)
        self.drive5TextEdit.setStyleSheet(
            """QLineEdit {background-color: rgb(15, 14, 15);
            border:5px solid rgb(0, 0, 0);
            selection-color: black;
            selection-background-color: black;
            color: grey;}"""
        )
        self.drive5EnableDisableButton = QPushButton(self)
        self.drive5EnableDisableButton.move(710, 168)
        self.drive5EnableDisableButton.resize(45, 20)
        self.drive5EnableDisableButton.setText(drive_5_active_config)
        self.drive5EnableDisableButton.clicked.connect(configInteractionPermissionFunction)
        self.drive5EnableDisableButton.clicked.connect(self.drive5EnableDisableFunction)
        if drive_5_active_config_Bool == False:
            self.drive5EnableDisableButton.setStyleSheet(
                """QPushButton {background-color: rgb(0, 0, 0);
               color: red;
               border: false;}"""
            )
        elif drive_5_active_config_Bool == True:
            self.drive5EnableDisableButton.setStyleSheet(
                """QPushButton {background-color: rgb(0, 0, 0);
               color: green;
               border: false;}"""
            )

        # Drive6 Index Settings
        self.drive6Button = QPushButton(self)
        self.drive6Button.move(565, 183)
        self.drive6Button.resize(45, 20)
        self.drive6Button.setText(' 6')
        self.drive6Button.clicked.connect(self.indexDrive6ConfigurationFunction)
        self.drive6Button.setStyleSheet(
            """QPushButton {background-color: rgb(0, 0, 0);
           color: green;
           border: false;}"""
        )
        self.drive6TextEdit = QLineEdit(self)
        self.drive6TextEdit.move(610, 183)
        self.drive6TextEdit.resize(100, 20)
        self.drive6TextEdit.setReadOnly(True)
        self.drive6TextEdit.setText(drive6_configuration.replace('DRIVE6: ', ''))
        self.drive6TextEdit.returnPressed.connect(self.writeDrive6PathFunction)
        self.drive6TextEdit.setStyleSheet(
            """QLineEdit {background-color: rgb(15, 14, 15);
            border:5px solid rgb(0, 0, 0);
            selection-color: black;
            selection-background-color: black;
            color: grey;}"""
        )
        self.drive6EnableDisableButton = QPushButton(self)
        self.drive6EnableDisableButton.move(710, 183)
        self.drive6EnableDisableButton.resize(45, 20)
        self.drive6EnableDisableButton.setText(drive_6_active_config)
        self.drive6EnableDisableButton.clicked.connect(configInteractionPermissionFunction)
        self.drive6EnableDisableButton.clicked.connect(self.drive6EnableDisableFunction)
        if drive_6_active_config_Bool == False:
            self.drive6EnableDisableButton.setStyleSheet(
                """QPushButton {background-color: rgb(0, 0, 0);
               color: red;
               border: false;}"""
            )
        elif drive_6_active_config_Bool == True:
            self.drive6EnableDisableButton.setStyleSheet(
                """QPushButton {background-color: rgb(0, 0, 0);
               color: green;
               border: false;}"""
            )

        # Drive7 Index Settings
        self.drive7Button = QPushButton(self)
        self.drive7Button.move(565, 198)
        self.drive7Button.resize(45, 20)
        self.drive7Button.setText(' 7')
        self.drive7Button.clicked.connect(self.indexDrive7ConfigurationFunction)
        self.drive7Button.setStyleSheet(
            """QPushButton {background-color: rgb(0, 0, 0);
           color: green;
           border: false;}"""
        )
        self.drive7TextEdit = QLineEdit(self)
        self.drive7TextEdit.move(610, 198)
        self.drive7TextEdit.resize(100, 20)
        self.drive7TextEdit.setReadOnly(True)
        self.drive7TextEdit.setText(drive7_configuration.replace('DRIVE7: ', ''))
        self.drive7TextEdit.returnPressed.connect(self.writeDrive7PathFunction)
        self.drive7TextEdit.setStyleSheet(
            """QLineEdit {background-color: rgb(15, 14, 15);
            border:5px solid rgb(0, 0, 0);
            selection-color: black;
            selection-background-color: black;
            color: grey;}"""
        )
        self.drive7EnableDisableButton = QPushButton(self)
        self.drive7EnableDisableButton.move(710, 198)
        self.drive7EnableDisableButton.resize(45, 20)
        self.drive7EnableDisableButton.setText(drive_7_active_config)
        self.drive7EnableDisableButton.clicked.connect(configInteractionPermissionFunction)
        self.drive7EnableDisableButton.clicked.connect(self.drive7EnableDisableFunction)
        if drive_7_active_config_Bool == False:
            self.drive7EnableDisableButton.setStyleSheet(
                """QPushButton {background-color: rgb(0, 0, 0);
               color: red;
               border: false;}"""
            )
        elif drive_7_active_config_Bool == True:
            self.drive7EnableDisableButton.setStyleSheet(
                """QPushButton {background-color: rgb(0, 0, 0);
               color: green;
               border: false;}"""
            )

        # Drive8 Indexing Settings
        self.drive8Button = QPushButton(self)
        self.drive8Button.move(565, 213)
        self.drive8Button.resize(45, 20)
        self.drive8Button.setText(' 8')
        self.drive8Button.clicked.connect(self.indexDrive8ConfigurationFunction)
        self.drive8Button.setStyleSheet(
            """QPushButton {background-color: rgb(0, 0, 0);
           color: green;
           border: false;}"""
        )
        self.drive8TextEdit = QLineEdit(self)
        self.drive8TextEdit.move(610, 213)
        self.drive8TextEdit.resize(100, 20)
        self.drive8TextEdit.setReadOnly(True)
        self.drive8TextEdit.setText(drive8_configuration.replace('DRIVE8: ', ''))
        self.drive8TextEdit.returnPressed.connect(self.writeDrive8PathFunction)
        self.drive8TextEdit.setStyleSheet(
            """QLineEdit {background-color: rgb(15, 14, 15);
            border:5px solid rgb(0, 0, 0);
            selection-color: black;
            selection-background-color: black;
            color: grey;}"""
        )
        self.drive8EnableDisableButton = QPushButton(self)
        self.drive8EnableDisableButton.move(710, 213)
        self.drive8EnableDisableButton.resize(45, 20)
        self.drive8EnableDisableButton.setText(drive_8_active_config)
        self.drive8EnableDisableButton.clicked.connect(configInteractionPermissionFunction)
        self.drive8EnableDisableButton.clicked.connect(self.drive8EnableDisableFunction)
        if drive_8_active_config_Bool == False:
            self.drive8EnableDisableButton.setStyleSheet(
                """QPushButton {background-color: rgb(0, 0, 0);
               color: red;
               border: false;}"""
            )
        elif drive_8_active_config_Bool == True:
            self.drive8EnableDisableButton.setStyleSheet(
                """QPushButton {background-color: rgb(0, 0, 0);
               color: green;
               border: false;}"""
            )

        # self.settingsTitle.hide()
        self.indexTitle.hide()
        self.indexTitle2.hide()
        self.wikiSettingsLabel.hide()
        self.wikiShowBrowserLabel.hide()
        self.wikiShowBrowserButton.hide()
        self.dictateWikiLabel.hide()
        self.dictateWikiButton.hide()
        self.useLocalWikiLabel.hide()
        self.useLocalWikiButton.hide()
        self.wikiServerIPButton.hide()
        self.wikiServerIPEdit.hide()
        self.wikiServerPortButton.hide()
        self.wikiServerPortEdit.hide()
        self.symbiotTitle.hide()
        self.symbiotServerIPButton.hide()
        self.symbiotServerIPEdit.hide()
        self.symbiotServerIPEdit.hide()
        self.symbiotServerPortButton.hide()
        self.symbiotServerPortEdit.hide()
        self.symbiotIPButton.hide()
        self.symbiotIPEdit.hide()
        self.symbiotMACButton.hide()
        self.symbiotMACEdit.hide()
        self.indexAudioButton.hide()
        self.indexAudioEdit.hide()
        self.indexAudioEnableDisableButton.hide()
        self.indexVideoButton.hide()
        self.indexVideoEdit.hide()
        self.indexVideoEnableDisableButton.hide()
        self.indexImagesButton.hide()
        self.indexImagesEdit.hide()
        self.indexImageEnableDisableButton.hide()
        self.indexTextButton.hide()
        self.indexTextEdit.hide()
        self.indexTextEnableDisableButton.hide()
        self.drive1Button.hide()
        self.drive1TextEdit.hide()
        self.drive1EnableDisableButton.hide()
        self.drive2Button.hide()
        self.drive2TextEdit.hide()
        self.drive2EnableDisableButton.hide()
        self.drive3Button.hide()
        self.drive3TextEdit.hide()
        self.drive3EnableDisableButton.hide()
        self.drive4Button.hide()
        self.drive4TextEdit.hide()
        self.drive4EnableDisableButton.hide()
        self.drive5Button.hide()
        self.drive5TextEdit.hide()
        self.drive5EnableDisableButton.hide()
        self.drive6Button.hide()
        self.drive6TextEdit.hide()
        self.drive6EnableDisableButton.hide()
        self.drive7Button.hide()
        self.drive7TextEdit.hide()
        self.drive7EnableDisableButton.hide()
        self.drive8Button.hide()
        self.drive8TextEdit.hide()
        self.drive8EnableDisableButton.hide()


        # Threads
        symbiotServerThread = symbiotServerClass(speechRecognitionThread, symbiotButton, speechRecognitionOffFunction,
                                                 speechRecognitionOnFunction)
        openDirectoryThread = openDirectoryClass(self.textBoxVerbose1, self.textBoxVerbose2)
        findOpenImageThread = findOpenImageClass()
        findOpenTextThread = findOpenTextClass()
        findOpenVideoThread = findOpenVideoClass()
        findOpenProgramThread = findOpenProgramClass()
        guiControllerThread = guiControllerClass(self.srInfo,
                                                 self.textBoxValue,
                                                 self.textBoxVerbose1,
                                                 self.textBoxVerbose2)
        textBoxVerbose2Thread = textBoxVerbose2Class(self.textBoxVerbose2)
        findOpenAudioThread = findOpenAudioClass(target_index,
                                                 multiple_matches,
                                                 target_match,
                                                 self.textBoxVerbose1)
        commandSearchThread = commandSearchClass(self.textBoxVerbose1,
                                                 self.textBoxVerbose2,
                                                 textBoxVerbose2Thread)
        speechRecognitionThread = speechRecognitionClass(self.srIndicator,
                                                         self.textBoxValue,
                                                         self.textBoxVerbose1,
                                                         self.textBoxVerbose2,
                                                         textBoxVerbose2Thread,
                                                         self.srInfo,
                                                         guiControllerThread,
                                                         commandSearchThread,
                                                         self.srOnButton)
        configInteractionPermissionThread = configInteractionPermissionClass(self.indexAudioEnableDisableButton,
                                                                             self.indexVideoEnableDisableButton,
                                                                             self.indexImageEnableDisableButton,
                                                                             self.indexTextEnableDisableButton,
                                                                             self.indexAudioEdit,
                                                                             self.indexVideoEdit,
                                                                             self.indexImagesEdit,
                                                                             self.indexTextEdit,
                                                                             self.indexAudioButton,
                                                                             self.indexVideoButton,
                                                                             self.indexImagesButton,
                                                                             self.indexTextButton,
                                                                             self.drive1EnableDisableButton,
                                                                             self.drive2EnableDisableButton,
                                                                             self.drive3EnableDisableButton,
                                                                             self.drive4EnableDisableButton,
                                                                             self.drive1TextEdit,
                                                                             self.drive2TextEdit,
                                                                             self.drive3TextEdit,
                                                                             self.drive4TextEdit,
                                                                             self.drive1Button,
                                                                             self.drive2Button,
                                                                             self.drive3Button,
                                                                             self.drive4Button)
        self.show()


    def audioIndexEnableDisableFunction(self):
        global audio_active_config_Bool
        global check_index_audio_config
        enabled_str = 'INDEXENGINE_AUDIO: enabled'
        disabled_str = 'INDEXENGINE_AUDIO: disabled'

        if audio_active_config_Bool == False:
            if check_index_audio_config == True:
                print('enabling audio index engine')
                line_list = []
                with codecs.open(config_file, 'r') as fo:
                    for line in fo:
                        line.strip()
                        line_list.append(line)
                    fo.close()
                i = 0
                for line_lists in line_list:
                    if line_list[i].startswith('INDEXENGINE_AUDIO: '):
                        line_list[i] = str(enabled_str + '\n')
                    i += 1
                i = 0
                with open('config.conf', 'w') as fo:
                    for line_lists in line_list:
                        fo.writelines(line_list[i])
                        # print('writing:', line_list[i])
                        i += 1
                    fo.close()
                audio_active_config_Bool = True
                audioIndexEngineFunction()
                self.indexAudioEnableDisableButton.setText('Enabled')
                self.indexAudioEnableDisableButton.setStyleSheet(
                    """QPushButton {background-color: rgb(0, 0, 0);
                   color: green;
                   border: false;}"""
                )
        elif audio_active_config_Bool == True:
            if check_index_audio_config == True:
                print('disabling audio index engine')
                line_list = []
                with codecs.open(config_file, 'r') as fo:
                    for line in fo:
                        line.strip()
                        line_list.append(line)
                    fo.close()
                i = 0
                for line_lists in line_list:
                    if line_list[i].startswith('INDEXENGINE_AUDIO: '):
                        line_list[i] = str(disabled_str + '\n')
                    i += 1
                i = 0
                with open('config.conf', 'w') as fo:
                    for line_lists in line_list:
                        fo.writelines(line_list[i])
                        # print('writing:', line_list[i])
                        i += 1
                    fo.close()
                audio_active_config_Bool = False
                audio_index_psutil.kill()
                self.indexAudioEnableDisableButton.setText('Disabled')
                self.indexAudioEnableDisableButton.setStyleSheet(
                    """QPushButton {background-color: rgb(0, 0, 0);
                   color: red;
                   border: false;}"""
                )

    def videoIndexEnableDisableFunction(self):
        global video_active_config_Bool
        global check_index_video_config
        enabled_str = 'INDEXENGINE_VIDEO: enabled'
        disabled_str = 'INDEXENGINE_VIDEO: disabled'
        if video_active_config_Bool == False:
            if check_index_video_config == True:
                print('enabling video index engine')
                line_list = []
                with codecs.open(config_file, 'r') as fo:
                    for line in fo:
                        line.strip()
                        line_list.append(line)
                    fo.close()
                i = 0
                for line_lists in line_list:
                    if line_list[i].startswith('INDEXENGINE_VIDEO: '):
                        line_list[i] = str(enabled_str + '\n')
                    i += 1
                i = 0
                with open('config.conf', 'w') as fo:
                    for line_lists in line_list:
                        fo.writelines(line_list[i])
                        # print('writing:', line_list[i])
                        i += 1
                    fo.close()
                video_active_config_Bool = True
                videoIndexEngineFunction()
                self.indexVideoEnableDisableButton.setText('Enabled')
                self.indexVideoEnableDisableButton.setStyleSheet(
                    """QPushButton {background-color: rgb(0, 0, 0);
                   color: green;
                   border: false;}"""
                )
        elif video_active_config_Bool == True:
            if check_index_video_config == True:
                print('disabling video index engine')
                line_list = []
                with codecs.open(config_file, 'r') as fo:
                    for line in fo:
                        line.strip()
                        line_list.append(line)
                    fo.close()
                i = 0
                for line_lists in line_list:
                    if line_list[i].startswith('INDEXENGINE_VIDEO: '):
                        line_list[i] = str(disabled_str + '\n')
                    i += 1
                i = 0
                with open('config.conf', 'w') as fo:
                    for line_lists in line_list:
                        fo.writelines(line_list[i])
                        # print('writing:', line_list[i])
                        i += 1
                    fo.close()
                video_active_config_Bool = False
                video_index_psutil.kill()
                self.indexVideoEnableDisableButton.setText('Disabled')
                self.indexVideoEnableDisableButton.setStyleSheet(
                    """QPushButton {background-color: rgb(0, 0, 0);
                   color: red;
                   border: false;}"""
                )

    def imageIndexEnableDisableFunction(self):
        global image_active_config_Bool
        global check_index_image_config
        enabled_str = 'INDEXENGINE_IMAGE: enabled'
        disabled_str = 'INDEXENGINE_IMAGE: disabled'
        if image_active_config_Bool == False:
            if check_index_image_config == True:
                print('enabling image index engine')
                line_list = []
                with codecs.open(config_file, 'r') as fo:
                    for line in fo:
                        line.strip()
                        line_list.append(line)
                    fo.close()
                i = 0
                for line_lists in line_list:
                    if line_list[i].startswith('INDEXENGINE_IMAGE: '):
                        line_list[i] = str(enabled_str + '\n')
                    i += 1
                i = 0
                with open('config.conf', 'w') as fo:
                    for line_lists in line_list:
                        fo.writelines(line_list[i])
                        # print('writing:', line_list[i])
                        i += 1
                    fo.close()
                image_active_config_Bool = True
                imageIndexEngineFunction()
                self.indexImageEnableDisableButton.setText('Enabled')
                self.indexImageEnableDisableButton.setStyleSheet(
                    """QPushButton {background-color: rgb(0, 0, 0);
                   color: green;
                   border: false;}"""
                )
        elif image_active_config_Bool == True:
            if check_index_image_config == True:
                print('disabling image index engine')
                line_list = []
                with codecs.open(config_file, 'r') as fo:
                    for line in fo:
                        line.strip()
                        line_list.append(line)
                    fo.close()
                i = 0
                for line_lists in line_list:
                    if line_list[i].startswith('INDEXENGINE_IMAGE: '):
                        line_list[i] = str(disabled_str + '\n')
                    i += 1
                i = 0
                with open('config.conf', 'w') as fo:
                    for line_lists in line_list:
                        fo.writelines(line_list[i])
                        # print('writing:', line_list[i])
                        i += 1
                    fo.close()
                image_active_config_Bool = False
                image_index_psutil.kill()
                self.indexImageEnableDisableButton.setText('Disabled')
                self.indexImageEnableDisableButton.setStyleSheet(
                    """QPushButton {background-color: rgb(0, 0, 0);
                   color: red;
                   border: false;}"""
                )

    def textIndexEnableDisableFunction(self):
        global text_active_config_Bool
        global check_index_text_config
        enabled_str = 'INDEXENGINE_TEXT: enabled'
        disabled_str = 'INDEXENGINE_TEXT: disabled'
        if text_active_config_Bool == False:
            if check_index_text_config == True:
                print('enabling text index engine')
                line_list = []
                with codecs.open(config_file, 'r') as fo:
                    for line in fo:
                        line.strip()
                        line_list.append(line)
                    fo.close()
                i = 0
                for line_lists in line_list:
                    if line_list[i].startswith('INDEXENGINE_TEXT: '):
                        line_list[i] = str(enabled_str + '\n')
                    i += 1
                i = 0
                with open('config.conf', 'w') as fo:
                    for line_lists in line_list:
                        fo.writelines(line_list[i])
                        # print('writing:', line_list[i])
                        i += 1
                    fo.close()
                text_active_config_Bool = True
                textIndexEngineFunction()
                self.indexTextEnableDisableButton.setText('Enabled')
                self.indexTextEnableDisableButton.setStyleSheet(
                    """QPushButton {background-color: rgb(0, 0, 0);
                   color: green;
                   border: false;}"""
                )
        elif text_active_config_Bool == True:
            if check_index_text_config == True:
                print('disabling text index engine')
                line_list = []
                with codecs.open(config_file, 'r') as fo:
                    for line in fo:
                        line.strip()
                        line_list.append(line)
                    fo.close()
                i = 0
                for line_lists in line_list:
                    if line_list[i].startswith('INDEXENGINE_TEXT: '):
                        line_list[i] = str(disabled_str + '\n')
                    i += 1
                i = 0
                with open('config.conf', 'w') as fo:
                    for line_lists in line_list:
                        fo.writelines(line_list[i])
                        # print('writing:', line_list[i])
                        i += 1
                    fo.close()
                text_active_config_Bool = False
                text_index_psutil.kill()
                self.indexTextEnableDisableButton.setText('Disabled')
                self.indexTextEnableDisableButton.setStyleSheet(
                    """QPushButton {background-color: rgb(0, 0, 0);
                   color: red;
                   border: false;}"""
                )

    def drive1EnableDisableFunction(self):
        global drive_1_active_config_Bool
        global check_index_drive1_config
        enabled_str = 'INDEXENGINE_DRIVE1: enabled'
        disabled_str = 'INDEXENGINE_DRIVE1: disabled'
        if drive_1_active_config_Bool == False:
            if check_index_drive1_config == True:
                print('enabling drive1 index engine')
                line_list = []
                with codecs.open(config_file, 'r') as fo:
                    for line in fo:
                        line.strip()
                        line_list.append(line)
                    fo.close()
                i = 0
                for line_lists in line_list:
                    if line_list[i].startswith('INDEXENGINE_DRIVE1: '):
                        line_list[i] = str(enabled_str + '\n')
                    i += 1
                i = 0
                with open('config.conf', 'w') as fo:
                    for line_lists in line_list:
                        fo.writelines(line_list[i])
                        # print('writing:', line_list[i])
                        i += 1
                    fo.close()
                drive_1_active_config_Bool = True
                drive1IndexEngineFunction()
                self.drive1EnableDisableButton.setText('Enabled')
                self.drive1EnableDisableButton.setStyleSheet(
                    """QPushButton {background-color: rgb(0, 0, 0);
                   color: green;
                   border: false;}"""
                )
        elif drive_1_active_config_Bool == True:
            if check_index_drive1_config == True:
                print('disabling drive1 index engine')
                line_list = []
                with codecs.open(config_file, 'r') as fo:
                    for line in fo:
                        line.strip()
                        line_list.append(line)
                    fo.close()
                i = 0
                for line_lists in line_list:
                    if line_list[i].startswith('INDEXENGINE_DRIVE1: '):
                        line_list[i] = str(disabled_str + '\n')
                    i += 1
                i = 0
                with open('config.conf', 'w') as fo:
                    for line_lists in line_list:
                        fo.writelines(line_list[i])
                        # print('writing:', line_list[i])
                        i += 1
                    fo.close()
                drive_1_active_config_Bool = False
                drive1_index_psutil.kill()
                self.drive1EnableDisableButton.setText('Disabled')
                self.drive1EnableDisableButton.setStyleSheet(
                    """QPushButton {background-color: rgb(0, 0, 0);
                   color: red;
                   border: false;}"""
                )

    def drive2EnableDisableFunction(self):
        global drive_2_active_config_Bool
        global check_index_drive2_config
        enabled_str = 'INDEXENGINE_DRIVE2: enabled'
        disabled_str = 'INDEXENGINE_DRIVE2: disabled'
        if drive_2_active_config_Bool == False:
            if check_index_drive2_config == True:
                print('enabling drive2 index engine')
                line_list = []
                with codecs.open(config_file, 'r') as fo:
                    for line in fo:
                        line.strip()
                        line_list.append(line)
                    fo.close()
                i = 0
                for line_lists in line_list:
                    if line_list[i].startswith('INDEXENGINE_DRIVE2: '):
                        line_list[i] = str(enabled_str + '\n')
                    i += 1
                i = 0
                with open('config.conf', 'w') as fo:
                    for line_lists in line_list:
                        fo.writelines(line_list[i])
                        # print('writing:', line_list[i])
                        i += 1
                    fo.close()
                drive_2_active_config_Bool = True
                drive2IndexEngineFunction()
                self.drive2EnableDisableButton.setText('Enabled')
                self.drive2EnableDisableButton.setStyleSheet(
                    """QPushButton {background-color: rgb(0, 0, 0);
                   color: green;
                   border: false;}"""
                )
        elif drive_2_active_config_Bool == True:
            if check_index_drive2_config == True:
                print('disabling drive2 index engine')
                line_list = []
                with codecs.open(config_file, 'r') as fo:
                    for line in fo:
                        line.strip()
                        line_list.append(line)
                    fo.close()
                i = 0
                for line_lists in line_list:
                    if line_list[i].startswith('INDEXENGINE_DRIVE2: '):
                        line_list[i] = str(disabled_str + '\n')
                    i += 1
                i = 0
                with open('config.conf', 'w') as fo:
                    for line_lists in line_list:
                        fo.writelines(line_list[i])
                        # print('writing:', line_list[i])
                        i += 1
                    fo.close()
                drive_2_active_config_Bool = False
                drive2_index_psutil.kill()
                self.drive2EnableDisableButton.setText('Disabled')
                self.drive2EnableDisableButton.setStyleSheet(
                    """QPushButton {background-color: rgb(0, 0, 0);
                   color: red;
                   border: false;}"""
                )

    def drive3EnableDisableFunction(self):
        global drive_3_active_config_Bool
        global check_index_drive3_config
        enabled_str = 'INDEXENGINE_DRIVE3: enabled'
        disabled_str = 'INDEXENGINE_DRIVE3: disabled'
        if drive_3_active_config_Bool == False:
            if check_index_drive3_config == True:
                print('enabling drive3 index engine')
                line_list = []
                with codecs.open(config_file, 'r') as fo:
                    for line in fo:
                        line.strip()
                        line_list.append(line)
                    fo.close()
                i = 0
                for line_lists in line_list:
                    if line_list[i].startswith('INDEXENGINE_DRIVE3: '):
                        line_list[i] = str(enabled_str + '\n')
                    i += 1
                i = 0
                with open('config.conf', 'w') as fo:
                    for line_lists in line_list:
                        fo.writelines(line_list[i])
                        # print('writing:', line_list[i])
                        i += 1
                    fo.close()
                drive_3_active_config_Bool = True
                drive3IndexEngineFunction()
                self.drive3EnableDisableButton.setText('Enabled')
                self.drive3EnableDisableButton.setStyleSheet(
                    """QPushButton {background-color: rgb(0, 0, 0);
                   color: green;
                   border: false;}"""
                )
        elif drive_3_active_config_Bool == True:
            if check_index_drive3_config == True:
                print('disabling drive3 index engine')
                line_list = []
                with codecs.open(config_file, 'r') as fo:
                    for line in fo:
                        line.strip()
                        line_list.append(line)
                    fo.close()
                i = 0
                for line_lists in line_list:
                    if line_list[i].startswith('INDEXENGINE_DRIVE3: '):
                        line_list[i] = str(disabled_str + '\n')
                    i += 1
                i = 0
                with open('config.conf', 'w') as fo:
                    for line_lists in line_list:
                        fo.writelines(line_list[i])
                        # print('writing:', line_list[i])
                        i += 1
                    fo.close()
                drive_3_active_config_Bool = False
                drive3_index_psutil.kill()
                self.drive3EnableDisableButton.setText('Disabled')
                self.drive3EnableDisableButton.setStyleSheet(
                    """QPushButton {background-color: rgb(0, 0, 0);
                   color: red;
                   border: false;}"""
                )

    def drive4EnableDisableFunction(self):
        global drive_4_active_config_Bool
        global check_index_drive4_config
        enabled_str = 'INDEXENGINE_DRIVE4: enabled'
        disabled_str = 'INDEXENGINE_DRIVE4: disabled'
        if drive_4_active_config_Bool == False:
            if check_index_drive4_config == True:
                print('enabling drive4 index engine')
                line_list = []
                with codecs.open(config_file, 'r') as fo:
                    for line in fo:
                        line.strip()
                        line_list.append(line)
                    fo.close()
                i = 0
                for line_lists in line_list:
                    if line_list[i].startswith('INDEXENGINE_DRIVE4: '):
                        line_list[i] = str(enabled_str + '\n')
                    i += 1
                i = 0
                with open('config.conf', 'w') as fo:
                    for line_lists in line_list:
                        fo.writelines(line_list[i])
                        # print('writing:', line_list[i])
                        i += 1
                    fo.close()
                drive_4_active_config_Bool = True
                drive4IndexEngineFunction()
                self.drive4EnableDisableButton.setText('Enabled')
                self.drive4EnableDisableButton.setStyleSheet(
                    """QPushButton {background-color: rgb(0, 0, 0);
                   color: green;
                   border: false;}"""
                )
        elif drive_4_active_config_Bool == True:
            if check_index_drive4_config == True:
                print('disabling drive4 index engine')
                line_list = []
                with codecs.open(config_file, 'r') as fo:
                    for line in fo:
                        line.strip()
                        line_list.append(line)
                    fo.close()
                i = 0
                for line_lists in line_list:
                    if line_list[i].startswith('INDEXENGINE_DRIVE4: '):
                        line_list[i] = str(disabled_str + '\n')
                    i += 1
                i = 0
                with open('config.conf', 'w') as fo:
                    for line_lists in line_list:
                        fo.writelines(line_list[i])
                        # print('writing:', line_list[i])
                        i += 1
                    fo.close()
                drive_4_active_config_Bool = False
                drive4_index_psutil.kill()
                self.drive4EnableDisableButton.setText('Disabled')
                self.drive4EnableDisableButton.setStyleSheet(
                    """QPushButton {background-color: rgb(0, 0, 0);
                   color: red;
                   border: false;}"""
                )

    def drive5EnableDisableFunction(self):
        global drive_5_active_config_Bool
        global check_index_drive5_config
        enabled_str = 'INDEXENGINE_DRIVE5: enabled'
        disabled_str = 'INDEXENGINE_DRIVE5: disabled'
        if drive_5_active_config_Bool == False:
            if check_index_drive5_config == True:
                print('enabling drive5 index engine')
                line_list = []
                with codecs.open(config_file, 'r') as fo:
                    for line in fo:
                        line.strip()
                        line_list.append(line)
                    fo.close()
                i = 0
                for line_lists in line_list:
                    if line_list[i].startswith('INDEXENGINE_DRIVE5: '):
                        line_list[i] = str(enabled_str + '\n')
                    i += 1
                i = 0
                with open('config.conf', 'w') as fo:
                    for line_lists in line_list:
                        fo.writelines(line_list[i])
                        # print('writing:', line_list[i])
                        i += 1
                    fo.close()
                drive_5_active_config_Bool = True
                drive5IndexEngineFunction()
                self.drive5EnableDisableButton.setText('Enabled')
                self.drive5EnableDisableButton.setStyleSheet(
                    """QPushButton {background-color: rgb(0, 0, 0);
                   color: green;
                   border: false;}"""
                )
        elif drive_5_active_config_Bool == True:
            if check_index_drive4_config == True:
                print('disabling drive5 index engine')
                line_list = []
                with codecs.open(config_file, 'r') as fo:
                    for line in fo:
                        line.strip()
                        line_list.append(line)
                    fo.close()
                i = 0
                for line_lists in line_list:
                    if line_list[i].startswith('INDEXENGINE_DRIVE5: '):
                        line_list[i] = str(disabled_str + '\n')
                    i += 1
                i = 0
                with open('config.conf', 'w') as fo:
                    for line_lists in line_list:
                        fo.writelines(line_list[i])
                        # print('writing:', line_list[i])
                        i += 1
                    fo.close()
                drive_5_active_config_Bool = False
                drive5_index_psutil.kill()
                self.drive5EnableDisableButton.setText('Disabled')
                self.drive5EnableDisableButton.setStyleSheet(
                    """QPushButton {background-color: rgb(0, 0, 0);
                   color: red;
                   border: false;}"""
                )

    def drive6EnableDisableFunction(self):
        global drive_6_active_config_Bool
        global check_index_drive6_config
        enabled_str = 'INDEXENGINE_DRIVE6: enabled'
        disabled_str = 'INDEXENGINE_DRIVE6: disabled'
        if drive_6_active_config_Bool == False:
            if check_index_drive4_config == True:
                print('enabling drive6 index engine')
                line_list = []
                with codecs.open(config_file, 'r') as fo:
                    for line in fo:
                        line.strip()
                        line_list.append(line)
                    fo.close()
                i = 0
                for line_lists in line_list:
                    if line_list[i].startswith('INDEXENGINE_DRIVE6: '):
                        line_list[i] = str(enabled_str + '\n')
                    i += 1
                i = 0
                with open('config.conf', 'w') as fo:
                    for line_lists in line_list:
                        fo.writelines(line_list[i])
                        # print('writing:', line_list[i])
                        i += 1
                    fo.close()
                drive_6_active_config_Bool = True
                drive6IndexEngineFunction()
                self.drive6EnableDisableButton.setText('Enabled')
                self.drive6EnableDisableButton.setStyleSheet(
                    """QPushButton {background-color: rgb(0, 0, 0);
                   color: green;
                   border: false;}"""
                )
        elif drive_6_active_config_Bool == True:
            if check_index_drive4_config == True:
                print('disabling drive6 index engine')
                line_list = []
                with codecs.open(config_file, 'r') as fo:
                    for line in fo:
                        line.strip()
                        line_list.append(line)
                    fo.close()
                i = 0
                for line_lists in line_list:
                    if line_list[i].startswith('INDEXENGINE_DRIVE6: '):
                        line_list[i] = str(disabled_str + '\n')
                    i += 1
                i = 0
                with open('config.conf', 'w') as fo:
                    for line_lists in line_list:
                        fo.writelines(line_list[i])
                        # print('writing:', line_list[i])
                        i += 1
                    fo.close()
                drive_6_active_config_Bool = False
                drive6_index_psutil.kill()
                self.drive6EnableDisableButton.setText('Disabled')
                self.drive6EnableDisableButton.setStyleSheet(
                    """QPushButton {background-color: rgb(0, 0, 0);
                   color: red;
                   border: false;}"""
                )

    def drive7EnableDisableFunction(self):
        global drive_7_active_config_Bool
        global check_index_drive7_config
        enabled_str = 'INDEXENGINE_DRIVE7: enabled'
        disabled_str = 'INDEXENGINE_DRIVE7: disabled'
        if drive_7_active_config_Bool == False:
            if check_index_drive7_config == True:
                print('enabling drive7 index engine')
                line_list = []
                with codecs.open(config_file, 'r') as fo:
                    for line in fo:
                        line.strip()
                        line_list.append(line)
                    fo.close()
                i = 0
                for line_lists in line_list:
                    if line_list[i].startswith('INDEXENGINE_DRIVE7: '):
                        line_list[i] = str(enabled_str + '\n')
                    i += 1
                i = 0
                with open('config.conf', 'w') as fo:
                    for line_lists in line_list:
                        fo.writelines(line_list[i])
                        # print('writing:', line_list[i])
                        i += 1
                    fo.close()
                drive_7_active_config_Bool = True
                drive7IndexEngineFunction()
                self.drive7EnableDisableButton.setText('Enabled')
                self.drive7EnableDisableButton.setStyleSheet(
                    """QPushButton {background-color: rgb(0, 0, 0);
                   color: green;
                   border: false;}"""
                )
        elif drive_7_active_config_Bool == True:
            if check_index_drive7_config == True:
                print('disabling drive7 index engine')
                line_list = []
                with codecs.open(config_file, 'r') as fo:
                    for line in fo:
                        line.strip()
                        line_list.append(line)
                    fo.close()
                i = 0
                for line_lists in line_list:
                    if line_list[i].startswith('INDEXENGINE_DRIVE7: '):
                        line_list[i] = str(disabled_str + '\n')
                    i += 1
                i = 0
                with open('config.conf', 'w') as fo:
                    for line_lists in line_list:
                        fo.writelines(line_list[i])
                        # print('writing:', line_list[i])
                        i += 1
                    fo.close()
                drive_7_active_config_Bool = False
                drive7_index_psutil.kill()
                self.drive7EnableDisableButton.setText('Disabled')
                self.drive7EnableDisableButton.setStyleSheet(
                    """QPushButton {background-color: rgb(0, 0, 0);
                   color: red;
                   border: false;}"""
                )

    def drive8EnableDisableFunction(self):
        global drive_8_active_config_Bool
        global check_index_drive8_config
        enabled_str = 'INDEXENGINE_DRIVE8: enabled'
        disabled_str = 'INDEXENGINE_DRIVE8: disabled'
        if drive_8_active_config_Bool == False:
            if check_index_drive8_config == True:
                print('enabling drive8 index engine')
                line_list = []
                with codecs.open(config_file, 'r') as fo:
                    for line in fo:
                        line.strip()
                        line_list.append(line)
                    fo.close()
                i = 0
                for line_lists in line_list:
                    if line_list[i].startswith('INDEXENGINE_DRIVE8: '):
                        line_list[i] = str(enabled_str + '\n')
                    i += 1
                i = 0
                with open('config.conf', 'w') as fo:
                    for line_lists in line_list:
                        fo.writelines(line_list[i])
                        # print('writing:', line_list[i])
                        i += 1
                    fo.close()
                drive_8_active_config_Bool = True
                drive8IndexEngineFunction()
                self.drive8EnableDisableButton.setText('Enabled')
                self.drive8EnableDisableButton.setStyleSheet(
                    """QPushButton {background-color: rgb(0, 0, 0);
                   color: green;
                   border: false;}"""
                )
        elif drive_8_active_config_Bool == True:
            if check_index_drive8_config == True:
                print('disabling drive8 index engine')
                line_list = []
                with codecs.open(config_file, 'r') as fo:
                    for line in fo:
                        line.strip()
                        line_list.append(line)
                    fo.close()
                i = 0
                for line_lists in line_list:
                    if line_list[i].startswith('INDEXENGINE_DRIVE8: '):
                        line_list[i] = str(disabled_str + '\n')
                    i += 1
                i = 0
                with open('config.conf', 'w') as fo:
                    for line_lists in line_list:
                        fo.writelines(line_list[i])
                        # print('writing:', line_list[i])
                        i += 1
                    fo.close()
                drive_8_active_config_Bool = False
                drive8_index_psutil.kill()
                self.drive8EnableDisableButton.setText('Disabled')
                self.drive8EnableDisableButton.setStyleSheet(
                    """QPushButton {background-color: rgb(0, 0, 0);
                   color: red;
                   border: false;}"""
                )

    def showHideSettingsFunction(self):
        global showHideValue
        global show_hide_settings
        # global drawRectangles

        if showHideValue == 0:
            showHideValue = 1
            print('-- opening menu')

            show_hide_settings.setIcon(QIcon("./Resources/image/setting_menu_icon.png"))
            show_hide_settings.setStyleSheet(
                """QPushButton{background-color: rgb(0, 0, 0);
               border:1px solid rgb(0, 255, 0);}"""
            )

            # self.srInfo.hide()
            # self.textBoxValue.hide()
            # self.textBoxVerbose1.hide()
            # self.textBoxVerbose2.hide()
            # self.srOnButton.hide()
            self.srIndicator.hide()

            self.setGeometry(self.minimal_extra_left, self.minimal_extra_top, self.minimal_extra_width, self.minimal_extra_height)
            self.setFixedSize(self.minimal_extra_width, self.minimal_extra_height)


            # self.settingsTitle.show()
            # self.settings_menu_title.show()
            self.indexTitle.show()
            self.indexTitle2.show()
            self.wikiSettingsLabel.show()
            self.wikiShowBrowserLabel.show()
            self.wikiShowBrowserButton.show()
            self.dictateWikiLabel.show()
            self.dictateWikiButton.show()
            self.useLocalWikiLabel.show()
            self.useLocalWikiButton.show()
            self.wikiServerIPButton.show()
            self.wikiServerIPEdit.show()
            self.wikiServerPortButton.show()
            self.wikiServerPortEdit.show()
            self.symbiotTitle.show()
            self.symbiotServerIPButton.show()
            self.symbiotServerIPEdit.show()
            self.symbiotServerIPEdit.show()
            self.symbiotServerPortButton.show()
            self.symbiotServerPortEdit.show()
            self.symbiotIPButton.show()
            self.symbiotIPEdit.show()
            self.symbiotMACButton.show()
            self.symbiotMACEdit.show()
            self.indexAudioButton.show()
            self.indexAudioEdit.show()
            self.indexAudioEnableDisableButton.show()
            self.indexVideoButton.show()
            self.indexVideoEdit.show()
            self.indexVideoEnableDisableButton.show()
            self.indexImagesButton.show()
            self.indexImagesEdit.show()
            self.indexImageEnableDisableButton.show()
            self.indexTextButton.show()
            self.indexTextEdit.show()
            self.indexTextEnableDisableButton.show()
            self.drive1Button.show()
            self.drive1TextEdit.show()
            self.drive1EnableDisableButton.show()
            self.drive2Button.show()
            self.drive2TextEdit.show()
            self.drive2EnableDisableButton.show()
            self.drive3Button.show()
            self.drive3TextEdit.show()
            self.drive3EnableDisableButton.show()
            self.drive4Button.show()
            self.drive4TextEdit.show()
            self.drive4EnableDisableButton.show()
            self.drive5Button.show()
            self.drive5TextEdit.show()
            self.drive5EnableDisableButton.show()
            self.drive6Button.show()
            self.drive6TextEdit.show()
            self.drive6EnableDisableButton.show()
            self.drive7Button.show()
            self.drive7TextEdit.show()
            self.drive7EnableDisableButton.show()
            self.drive8Button.show()
            self.drive8TextEdit.show()
            self.drive8EnableDisableButton.show()

        elif showHideValue == 1:
            showHideValue = 0
            print('-- closing menu')

            show_hide_settings.setIcon(QIcon("./Resources/image/setting_menu_icon.png"))
            show_hide_settings.setStyleSheet(
                """QPushButton{background-color: rgb(0, 0, 0);
               border:1px solid rgb(0, 0, 255);}"""
            )

            self.srInfo.show()
            self.textBoxValue.show()
            self.textBoxVerbose1.show()
            self.textBoxVerbose2.show()
            self.srOnButton.show()
            self.srIndicator.hide()

            self.setGeometry(self.minimal_left, self.minimal_top, self.minimal_width, self.minimal_height)
            self.setFixedSize(self.minimal_width, self.minimal_height)

            self.settings_menu_title.hide()
            self.indexTitle.hide()
            self.indexTitle2.hide()
            self.wikiSettingsLabel.hide()
            self.wikiShowBrowserLabel.hide()
            self.wikiShowBrowserButton.hide()
            self.dictateWikiLabel.hide()
            self.dictateWikiButton.hide()
            self.useLocalWikiLabel.hide()
            self.useLocalWikiButton.hide()
            self.wikiServerIPButton.hide()
            self.wikiServerIPEdit.hide()
            self.wikiServerPortButton.hide()
            self.wikiServerPortEdit.hide()
            self.symbiotTitle.hide()
            self.symbiotServerIPButton.hide()
            self.symbiotServerIPEdit.hide()
            self.symbiotServerIPEdit.hide()
            self.symbiotServerPortButton.hide()
            self.symbiotServerPortEdit.hide()
            self.symbiotIPButton.hide()
            self.symbiotIPEdit.hide()
            self.symbiotMACButton.hide()
            self.symbiotMACEdit.hide()
            self.indexAudioButton.hide()
            self.indexAudioEdit.hide()
            self.indexAudioEnableDisableButton.hide()
            self.indexVideoButton.hide()
            self.indexVideoEdit.hide()
            self.indexVideoEnableDisableButton.hide()
            self.indexImagesButton.hide()
            self.indexImagesEdit.hide()
            self.indexImageEnableDisableButton.hide()
            self.indexTextButton.hide()
            self.indexTextEdit.hide()
            self.indexTextEnableDisableButton.hide()
            self.drive1Button.hide()
            self.drive1TextEdit.hide()
            self.drive1EnableDisableButton.hide()
            self.drive2Button.hide()
            self.drive2TextEdit.hide()
            self.drive2EnableDisableButton.hide()
            self.drive3Button.hide()
            self.drive3TextEdit.hide()
            self.drive3EnableDisableButton.hide()
            self.drive4Button.hide()
            self.drive4TextEdit.hide()
            self.drive4EnableDisableButton.hide()
            self.drive5Button.hide()
            self.drive5TextEdit.hide()
            self.drive5EnableDisableButton.hide()
            self.drive6Button.hide()
            self.drive6TextEdit.hide()
            self.drive6EnableDisableButton.hide()
            self.drive7Button.hide()
            self.drive7TextEdit.hide()
            self.drive7EnableDisableButton.hide()
            self.drive8Button.hide()
            self.drive8TextEdit.hide()
            self.drive8EnableDisableButton.hide()

    # wiki
    def useLocalWikiFunction(self):
        global allow_wiki_local_server_Bool
        global allow_wiki_local_server_configuration

        if allow_wiki_local_server_Bool == True:
            self.useLocalWikiButton.setText('Disabled')
            self.useLocalWikiButton.setStyleSheet(
                """QPushButton {background-color: rgb(0, 0, 0);
               color: red;
               border: false;}"""
            )
            allow_wiki_local_server_Bool = False

        elif allow_wiki_local_server_Bool == False:
            self.useLocalWikiButton.setText('Enabled')
            self.useLocalWikiButton.setStyleSheet(
                """QPushButton {background-color: rgb(0, 0, 0);
               color: green;
               border: false;}"""
            )
            allow_wiki_local_server_Bool = True

        line_list = []
        path_text = ''
        if allow_wiki_local_server_Bool == True:
            path_text = 'enabled'
        elif allow_wiki_local_server_Bool == False:
            path_text = 'disabled'

        print('use local wiki server:', path_text)
        with codecs.open('config.conf', 'r', encoding="utf-8") as fo:
            for line in fo:
                line_list.append(line)
        i = 0
        for line_lists in line_list:
            if line_list[i].startswith('ALLOW_WIKI_LOCAL_SERVER: '):
                print('Replacing list item:', line_list[i], 'with', path_text)
                line_list[i] = str('ALLOW_WIKI_LOCAL_SERVER: ' + path_text + '\n')
            i += 1
        fo.close()
        i = 0
        with codecs.open('config.conf', 'w', encoding="utf-8") as fo:
            for line_lists in line_list:
                fo.writelines(line_list[i])
                # print('writing:', line_list[i])
                i += 1
        fo.close()
        print('updated: configuration')
        # = True
        allow_wiki_local_server_configuration = path_text

    def dictateWikiFunction(self):
        global wiki_dictate_Bool
        global wiki_dictate_configuration

        if wiki_dictate_Bool == True:
            self.dictateWikiButton.setText('Disabled')
            self.dictateWikiButton.setStyleSheet(
                """QPushButton {background-color: rgb(0, 0, 0);
               color: red;
               border: false;}"""
            )
            wiki_dictate_Bool = False

        elif wiki_dictate_Bool == False:
            self.dictateWikiButton.setText('Enabled')
            self.dictateWikiButton.setStyleSheet(
                """QPushButton {background-color: rgb(0, 0, 0);
               color: green;
               border: false;}"""
            )
            wiki_dictate_Bool = True

        line_list = []
        path_text = ''
        if wiki_dictate_Bool == True:
            path_text = 'enabled'
        elif wiki_dictate_Bool == False:
            path_text = 'disabled'

        print('dictate wiki transcripts:', path_text)
        with codecs.open('config.conf', 'r', encoding="utf-8") as fo:
            for line in fo:
                line_list.append(line)
        i = 0
        for line_lists in line_list:
            if line_list[i].startswith('WIKI_TRANSCRIPT_DICTATE: '):
                print('Replacing list item:', line_list[i], 'with', path_text)
                line_list[i] = str('WIKI_TRANSCRIPT_DICTATE: ' + path_text + '\n')
            i += 1
        fo.close()
        i = 0
        with codecs.open('config.conf', 'w', encoding="utf-8") as fo:
            for line_lists in line_list:
                fo.writelines(line_list[i])
                # print('writing:', line_list[i])
                i += 1
        fo.close()
        print('updated: configuration')
        # = True
        wiki_dictate_configuration = path_text

    def wikiShowBrowserFunction(self):
        global wiki_show_browser_Bool
        global wiki_show_browser_configuration

        if wiki_show_browser_Bool == True:
            self.wikiShowBrowserButton.setText('Disabled')
            self.wikiShowBrowserButton.setStyleSheet(
                """QPushButton {background-color: rgb(0, 0, 0);
               color: red;
               border: false;}"""
            )
            wiki_show_browser_Bool = False

        elif wiki_show_browser_Bool == False:
            self.wikiShowBrowserButton.setText('Enabled')
            self.wikiShowBrowserButton.setStyleSheet(
                """QPushButton {background-color: rgb(0, 0, 0);
               color: green;
               border: false;}"""
            )
            wiki_show_browser_Bool = True

        line_list = []
        path_text = ''
        if wiki_show_browser_Bool == True:
            path_text = 'enabled'
        elif wiki_show_browser_Bool == False:
            path_text = 'disabled'

        print('show wiki in browser:', path_text)
        with codecs.open('config.conf', 'r', encoding="utf-8") as fo:
            for line in fo:
                line_list.append(line)
        i = 0
        for line_lists in line_list:
            if line_list[i].startswith('WIKI_TRANSCRIPT_SHOW_BROWSER: '):
                print('Replacing list item:', line_list[i], 'with', path_text)
                line_list[i] = str('WIKI_TRANSCRIPT_SHOW_BROWSER: ' + path_text + '\n')
            i += 1
        fo.close()
        i = 0
        with codecs.open('config.conf', 'w', encoding="utf-8") as fo:
            for line_lists in line_list:
                fo.writelines(line_list[i])
                # print('writing:', line_list[i])
                i += 1
        fo.close()
        print('updated: configuration')
        # = True
        wiki_show_browser_configuration = path_text

    # Symbiot Server IP Configuration
    def symbiotServerIPFunction(self):
        global symbiot_server_ip_configuration
        if self.symbiotServerIPEditable == True:
            print('setting symbiot server ip line edit: false')
            self.symbiotServerIPEdit.setReadOnly(False)
            self.symbiotServerIPEdit.setStyleSheet(
                """QLineEdit {background-color: rgb(25, 24, 25);
                border:5px solid rgb(0, 0, 0);
                selection-color: black;
                selection-background-color: black;
                color: white;}"""
            )
            self.symbiotServerIPEditable = False
        elif self.symbiotServerIPEditable == False:
            print('setting asymbiot server ip line edit: true')
            self.symbiotServerIPEdit.setReadOnly(True)
            self.symbiotServerIPEdit.setStyleSheet(
                """QLineEdit {background-color: rgb(15, 14, 15);
                border:5px solid rgb(0, 0, 0);
                selection-color: black;
                selection-background-color: black;
                color: grey;}"""
            )
            self.symbiotServerIPEdit.setText(symbiot_server_ip_configuration)  # .replace('DIRAUD: ', ''))
            self.symbiotServerIPEditable = True

    def writeSymbiotServerIPFunction(self):
        global symbiot_server_ip_configuration
        line_list = []
        path_text = self.symbiotServerIPEdit.text()
        print('IP Entered:', path_text)
        with codecs.open('config.conf', 'r', encoding="utf-8") as fo:
            for line in fo:
                line_list.append(line)
        i = 0
        for line_lists in line_list:
            if line_list[i].startswith('SYMBIOT_SERVER: '):
                print('Replacing list item:', line_list[i], 'with', path_text)
                line_list[i] = str('SYMBIOT_SERVER: ' + path_text + '\n')
            i += 1
        fo.close()
        i = 0
        with codecs.open('config.conf', 'w', encoding="utf-8") as fo:
            for line_lists in line_list:
                fo.writelines(line_list[i])
                # print('writing:', line_list[i])
                i += 1
        fo.close()
        print('updated: symbiot server ip configuration')
        # = True
        symbiot_server_ip_configuration = path_text
        self.symbiotServerIPFunction()

    # Symbiot Server Port Configuration
    def symbiotServerPortFunction(self):
        global symbiot_server_port_configuration
        if self.symbiotServerPortEditable == True:
            print('setting symbiot server port line edit: false')
            self.symbiotServerPortEdit.setReadOnly(False)
            self.symbiotServerPortEdit.setStyleSheet(
                """QLineEdit {background-color: rgb(25, 24, 25);
                border:5px solid rgb(0, 0, 0);
                selection-color: black;
                selection-background-color: black;
                color: white;}"""
            )
            self.symbiotServerPortEditable = False
        elif self.symbiotServerPortEditable == False:
            print('setting symbiot server port line edit: true')
            self.symbiotServerPortEdit.setReadOnly(True)
            self.symbiotServerPortEdit.setStyleSheet(
                """QLineEdit {background-color: rgb(15, 14, 15);
                border:5px solid rgb(0, 0, 0);
                selection-color: black;
                selection-background-color: black;
                color: grey;}"""
            )
            self.symbiotServerPortEdit.setText(symbiot_server_port_configuration)  # .replace('DIRAUD: ', ''))
            self.symbiotServerPortEditable = True

    def writeSymbiotServerPortFunction(self):
        global symbiot_server_port_configuration
        line_list = []
        path_text = self.symbiotServerPortEdit.text()
        print('Port Entered:', path_text)
        with codecs.open('config.conf', 'r', encoding="utf-8") as fo:
            for line in fo:
                line_list.append(line)
        i = 0
        for line_lists in line_list:
            if line_list[i].startswith('SYMBIOT_SERVER_PORT: '):
                print('Replacing list item:', line_list[i], 'with', path_text)
                line_list[i] = str('SYMBIOT_SERVER_PORT: ' + path_text + '\n')
            i += 1
        fo.close()
        i = 0
        with codecs.open('config.conf', 'w', encoding="utf-8") as fo:
            for line_lists in line_list:
                fo.writelines(line_list[i])
                # print('writing:', line_list[i])
                i += 1
        fo.close()
        print('updated: symbiot server port configuration')
        # = True
        symbiot_server_port_configuration = path_text
        self.symbiotServerPortFunction()

    def wikiServerIPFunction(self):
        global wiki_local_server_ip_configuration
        if self.wikiServerIPEditable == True:
            self.wikiServerIPEdit.setReadOnly(False)
            self.wikiServerIPEdit.setStyleSheet(
                """QLineEdit {background-color: rgb(25, 24, 25);
                border:5px solid rgb(0, 0, 0);
                selection-color: black;
                selection-background-color: black;
                color: white;}"""
            )
            self.wikiServerIPEditable = False
        elif self.wikiServerIPEditable == False:
            print('setting symbiot ip line edit: true')
            self.wikiServerIPEdit.setReadOnly(True)
            self.wikiServerIPEdit.setStyleSheet(
                """QLineEdit {background-color: rgb(15, 14, 15);
                border:5px solid rgb(0, 0, 0);
                selection-color: black;
                selection-background-color: black;
                color: grey;}"""
            )
            self.wikiServerIPEdit.setText(wiki_local_server_ip_configuration)  # .replace('DIRAUD: ', ''))
            self.wikiServerIPEditable = True

    def writeWikiServerFunction(self):
        global wiki_local_server_ip_configuration
        line_list = []
        path_text = self.wikiServerIPEdit.text()
        print('wiki ip entered:', path_text)
        with codecs.open('config.conf', 'r', encoding="utf-8") as fo:
            for line in fo:
                line_list.append(line)
        i = 0
        for line_lists in line_list:
            if line_list[i].startswith('WIKI_LOCAL_SERVER: '):
                print('Replacing list item:', line_list[i], 'with', path_text)
                line_list[i] = str('WIKI_LOCAL_SERVER: ' + path_text + '\n')
            i += 1
        fo.close()
        i = 0
        with codecs.open('config.conf', 'w', encoding="utf-8") as fo:
            for line_lists in line_list:
                fo.writelines(line_list[i])
                # print('writing:', line_list[i])
                i += 1
        fo.close()
        print('updated: wiki server ip configuration')
        # = True
        wiki_local_server_ip_configuration = path_text
        self.wikiServerIPFunction()

    def wikiServerPortFunction(self):
        global wiki_local_server_port_configuration
        if self.wikiServerPortEditable == True:
            print('setting symbiot port line edit: false')
            self.wikiServerPortEdit.setReadOnly(False)
            self.wikiServerPortEdit.setStyleSheet(
                """QLineEdit {background-color: rgb(25, 24, 25);
                border:5px solid rgb(0, 0, 0);
                selection-color: black;
                selection-background-color: black;
                color: white;}"""
            )
            self.wikiServerPortEditable = False
        elif self.wikiServerPortEditable == False:
            print('setting symbiot ip line edit: true')
            self.wikiServerPortEdit.setReadOnly(True)
            self.wikiServerPortEdit.setStyleSheet(
                """QLineEdit {background-color: rgb(15, 14, 15);
                border:5px solid rgb(0, 0, 0);
                selection-color: black;
                selection-background-color: black;
                color: grey;}"""
            )
            self.wikiServerPortEdit.setText(wiki_local_server_port_configuration)  # .replace('DIRAUD: ', ''))
            self.wikiServerPortEditable = True

    def writeWikiServerPortFunction(self):
        global wiki_local_server_port_configuration
        line_list = []
        path_text = self.wikiServerPortEdit.text()
        print('wiki server port entered:', path_text)
        with codecs.open('config.conf', 'r', encoding="utf-8") as fo:
            for line in fo:
                line_list.append(line)
        i = 0
        for line_lists in line_list:
            if line_list[i].startswith('WIKI_LOCAL_SERVER_PORT: '):
                print('Replacing list item:', line_list[i], 'with', path_text)
                line_list[i] = str('WIKI_LOCAL_SERVER_PORT: ' + path_text + '\n')
            i += 1
        fo.close()
        i = 0
        with codecs.open('config.conf', 'w', encoding="utf-8") as fo:
            for line_lists in line_list:
                fo.writelines(line_list[i])
                # print('writing:', line_list[i])
                i += 1
        fo.close()
        print('updated: wiki server port configuration')
        # = True
        wiki_local_server_port_configuration = path_text
        self.wikiServerPortFunction()

    # Symbiot IP Configuration
    def symbiotIPFunction(self):
        global symbiot_ip_configuration
        if self.symbiotIPEditable == True:
            print('setting symbiot ip line edit: false')
            self.symbiotIPEdit.setReadOnly(False)
            self.symbiotIPEdit.setStyleSheet(
                """QLineEdit {background-color: rgb(25, 24, 25);
                border:5px solid rgb(0, 0, 0);
                selection-color: black;
                selection-background-color: black;
                color: white;}"""
            )
            self.symbiotIPEditable = False
        elif self.symbiotIPEditable == False:
            print('setting symbiot ip line edit: true')
            self.symbiotIPEdit.setReadOnly(True)
            self.symbiotIPEdit.setStyleSheet(
                """QLineEdit {background-color: rgb(15, 14, 15);
                border:5px solid rgb(0, 0, 0);
                selection-color: black;
                selection-background-color: black;
                color: grey;}"""
            )
            self.symbiotIPEdit.setText(symbiot_ip_configuration)  # .replace('DIRAUD: ', ''))
            self.symbiotIPEditable = True

    def writeSymbiotIPFunction(self):
        global symbiot_ip_configuration
        line_list = []
        path_text = self.symbiotIPEdit.text()
        print('symbiot ip entered:', path_text)
        with codecs.open('config.conf', 'r', encoding="utf-8") as fo:
            for line in fo:
                line_list.append(line)
        i = 0
        for line_lists in line_list:
            if line_list[i].startswith('SYMBIOT_IP: '):
                print('Replacing list item:', line_list[i], 'with', path_text)
                line_list[i] = str('SYMBIOT_IP: ' + path_text + '\n')
            i += 1
        fo.close()
        i = 0
        with codecs.open('config.conf', 'w', encoding="utf-8") as fo:
            for line_lists in line_list:
                fo.writelines(line_list[i])
                # print('writing:', line_list[i])
                i += 1
        fo.close()
        print('updated: symbiot ip configuration')
        # = True
        symbiot_ip_configuration = path_text
        self.symbiotIPFunction()

    # Symbiot IP Configuration
    def symbiotMACFunction(self):
        global symbiot_mac_configuration
        if self.symbiotMACEditable == True:
            print('setting symbiot mac line edit: false')
            self.symbiotMACEdit.setReadOnly(False)
            self.symbiotMACEdit.setStyleSheet(
                """QLineEdit {background-color: rgb(25, 24, 25);
                border:5px solid rgb(0, 0, 0);
                selection-color: black;
                selection-background-color: black;
                color: white;}"""
            )
            self.symbiotMACEditable = False
        elif self.symbiotMACEditable == False:
            print('setting symbiot mac line edit: true')
            self.symbiotMACEdit.setReadOnly(True)
            self.symbiotMACEdit.setStyleSheet(
                """QLineEdit {background-color: rgb(15, 14, 15);
                border:5px solid rgb(0, 0, 0);
                selection-color: black;
                selection-background-color: black;
                color: grey;}"""
            )
            self.symbiotMACEdit.setText(symbiot_mac_configuration)  # .replace('DIRAUD: ', ''))
            self.symbiotMACEditable = True

    def writeSymbiotMACFunction(self):
        global symbiot_mac_configuration
        line_list = []
        path_text = self.symbiotMACEdit.text()
        print('symbiot mac entered:', path_text)
        with codecs.open('config.conf', 'r', encoding="utf-8") as fo:
            for line in fo:
                line_list.append(line)
        i = 0
        for line_lists in line_list:
            if line_list[i].startswith('SYMBIOT_MAC: '):
                print('Replacing list item:', line_list[i], 'with', path_text)
                line_list[i] = str('SYMBIOT_MAC: ' + path_text + '\n')
            i += 1
        fo.close()
        i = 0
        with codecs.open('config.conf', 'w', encoding="utf-8") as fo:
            for line_lists in line_list:
                fo.writelines(line_list[i])
                # print('writing:', line_list[i])
                i += 1
        fo.close()
        print('updated: symbiot mac configuration')
        # = True
        symbiot_mac_configuration = path_text
        self.symbiotMACFunction()

    # Audio Index Settings
    def indexAudioConfigurationFunction(self):
        global audio_configuration
        if self.indexAudioEditable == True:
            print('setting audio index path line edit: false')
            self.indexAudioEdit.setReadOnly(False)
            self.indexAudioEdit.setStyleSheet(
                """QLineEdit {background-color: rgb(25, 24, 25);
                border:5px solid rgb(0, 0, 0);
                selection-color: black;
                selection-background-color: black;
                color: white;}"""
            )
            self.indexAudioEditable = False
        elif self.indexAudioEditable == False:
            print('setting audio index path line edit: true')
            self.indexAudioEdit.setReadOnly(True)
            self.indexAudioEdit.setStyleSheet(
                """QLineEdit {background-color: rgb(15, 14, 15);
                border:5px solid rgb(0, 0, 0);
                selection-color: black;
                selection-background-color: black;
                color: grey;}"""
            )
            self.indexAudioEdit.setText(audio_configuration.replace('DIRAUD: ', ''))
            self.indexAudioEditable = True

    def writeAudioPathFunction(self):
        global check_index_audio_config
        global audio_configuration
        line_list = []
        path_text = self.indexAudioEdit.text()
        print('Path Entered:', path_text)
        if os.path.exists(path_text):
            print('Path Exists:', path_text)
            with open('config.conf', 'r') as fo:
                for line in fo:
                    line_list.append(line)
            i = 0
            for line_lists in line_list:
                if line_list[i].startswith('DIRAUD:'):
                    print('Replacing list item:', line_list[i], 'with', path_text)
                    line_list[i] = str('DIRAUD: ' + path_text + '\n')
                i += 1
            fo.close()
            i = 0
            with open('config.conf', 'w') as fo:
                for line_lists in line_list:
                    fo.writelines(line_list[i])
                    # print('writing:', line_list[i])
                    i += 1
            fo.close()
            print('updated: audio path configuration')
            check_index_audio_config = True
            audio_configuration = path_text

        elif not os.path.exists(path_text):
            print('Path does not exist')
            self.indexAudioEdit.setText(audio_configuration.replace('DIRAUD: ', ''))
            check_index_audio_config = False
        self.indexAudioConfigurationFunction()

    # Video Index Settings
    def indexVideoConfigurationFunction(self):
        global video_configuration
        if self.indexVideoEditable == True:
            print('setting video index path line edit: false')
            self.indexVideoEdit.setReadOnly(False)
            self.indexVideoEdit.setStyleSheet(
                """QLineEdit {background-color: rgb(25, 24, 25);
                border:5px solid rgb(0, 0, 0);
                selection-color: black;
                selection-background-color: black;
                color: white;}"""
            )
            self.indexVideoEditable = False
        elif self.indexVideoEditable == False:
            print('setting video index path line edit: true')
            self.indexVideoEdit.setReadOnly(True)
            self.indexVideoEdit.setStyleSheet(
                """QLineEdit {background-color: rgb(15, 14, 15);
                border:5px solid rgb(0, 0, 0);
                selection-color: black;
                selection-background-color: black;
                color: grey;}"""
            )
            self.indexVideoEdit.setText(video_configuration.replace('DIRVID: ', ''))
            self.indexVideoEditable = True

    def writeVideoPathFunction(self):
        global check_index_video_config
        global video_configuration
        line_list = []
        path_text = self.indexVideoEdit.text()
        print('Path Entered:', path_text)
        if os.path.exists(path_text):
            print('Path Exists:', path_text)
            with open('config.conf', 'r') as fo:
                for line in fo:
                    line_list.append(line)
            i = 0
            for line_lists in line_list:
                if line_list[i].startswith('DIRVID:'):
                    print('Replacing list item:', line_list[i], 'with', path_text)
                    line_list[i] = str('DIRVID: ' + path_text + '\n')
                i += 1
            fo.close()
            i = 0
            with open('config.conf', 'w') as fo:
                for line_lists in line_list:
                    fo.writelines(line_list[i])
                    # print('writing:', line_list[i])
                    i += 1
            fo.close()
            print('updated: video path configuration')
            check_index_video_config = True
            video_configuration = path_text

        elif not os.path.exists(path_text):
            print('Path does not exist')
            self.indexVideoEdit.setText(video_configuration.replace('DIRVID: ', ''))
            check_index_video_config = False
        self.indexVideoConfigurationFunction()

    # Image Index Settings
    def indexImagesConfigurationFunction(self):
        global image_configuration
        if self.indexImageEditable == True:
            print('setting image index path line edit: false')
            self.indexImagesEdit.setReadOnly(False)
            self.indexImagesEdit.setStyleSheet(
                """QLineEdit {background-color: rgb(25, 24, 25);
                border:5px solid rgb(0, 0, 0);
                selection-color: black;
                selection-background-color: black;
                color: white;}"""
            )
            self.indexImageEditable = False
        elif self.indexImageEditable == False:
            print('setting image index path line edit: true')
            self.indexImagesEdit.setReadOnly(True)
            self.indexImagesEdit.setStyleSheet(
                """QLineEdit {background-color: rgb(15, 14, 15);
                border:5px solid rgb(0, 0, 0);
                selection-color: black;
                selection-background-color: black;
                color: grey;}"""
            )
            self.indexImagesEdit.setText(image_configuration.replace('DIRIMG: ', ''))
            self.indexImageEditable = True

    def writeImagesPathFunction(self):
        global check_index_image_config
        global image_configuration
        line_list = []
        path_text = self.indexImagesEdit.text()
        print('Path Entered:', path_text)
        if os.path.exists(path_text):
            print('Path Exists:', path_text)
            with open('config.conf', 'r') as fo:
                for line in fo:
                    line_list.append(line)
            i = 0
            for line_lists in line_list:
                if line_list[i].startswith('DIRIMG:'):
                    print('Replacing list item:', line_list[i], 'with', path_text)
                    line_list[i] = str('DIRIMG: ' + path_text + '\n')
                i += 1
            fo.close()
            i = 0
            with open('config.conf', 'w') as fo:
                for line_lists in line_list:
                    fo.writelines(line_list[i])
                    # print('writing:', line_list[i])
                    i += 1
            fo.close()
            print('updated: images path configuration')
            check_index_image_config = True
            image_configuration = path_text

        elif not os.path.exists(path_text):
            print('Path does not exist')
            self.indexImagesEdit.setText(image_configuration.replace('DIRIMG: ', ''))
            check_index_image_config = False
        self.indexImagesConfigurationFunction()

    # Text Index Settings
    def indexTextConfigurationFunction(self):
        global text_configuration
        if self.indexTextEditable == True:
            print('setting text index path line edit: false')
            self.indexTextEdit.setReadOnly(False)
            self.indexTextEdit.setStyleSheet(
                """QLineEdit {background-color: rgb(25, 24, 25);
                border:5px solid rgb(0, 0, 0);
                selection-color: black;
                selection-background-color: black;
                color: white;}"""
            )
            self.indexTextEditable = False
        elif self.indexTextEditable == False:
            print('setting text index path line edit: true')
            self.indexTextEdit.setReadOnly(True)
            self.indexTextEdit.setStyleSheet(
                """QLineEdit {background-color: rgb(15, 14, 15);
                border:5px solid rgb(0, 0, 0);
                selection-color: black;
                selection-background-color: black;
                color: grey;}"""
            )
            self.indexTextEdit.setText(text_configuration.replace('DIRTXT: ', ''))
            self.indexTextEditable = True

    def writeTextPathFunction(self):
        global check_index_text_config
        global text_configuration
        line_list = []
        path_text = self.indexTextEdit.text()
        print('Path Entered:', path_text)
        if os.path.exists(path_text):
            print('Path Exists:', path_text)
            with open('config.conf', 'r') as fo:
                for line in fo:
                    line_list.append(line)
            i = 0
            for line_lists in line_list:
                if line_list[i].startswith('DIRTXT:'):
                    print('Replacing list item:', line_list[i], 'with', path_text)
                    line_list[i] = str('DIRTXT: ' + path_text + '\n')
                i += 1
            fo.close()
            i = 0
            with open('config.conf', 'w') as fo:
                for line_lists in line_list:
                    fo.writelines(line_list[i])
                    # print('writing:', line_list[i])
                    i += 1
            fo.close()
            print('updated: text path configuration')
            check_index_text_config = True
            text_configuration = path_text

        elif not os.path.exists(path_text):
            print('Path does not exist')
            self.indexTextEdit.setText(text_configuration.replace('DIRTXT: ', ''))
            check_index_text_config = False
        self.indexTextConfigurationFunction()

    # Drive1 Index Settings
    def indexDrive1ConfigurationFunction(self):
        global drive1_configuration
        if self.indexDrive1Editable == False:
            print('setting drive1 index path line edit: true')
            self.drive1TextEdit.setReadOnly(False)
            self.drive1TextEdit.setStyleSheet(
                """QLineEdit {background-color: rgb(25, 24, 25);
                border:5px solid rgb(0, 0, 0);
                selection-color: black;
                selection-background-color: black;
                color: white;}"""
            )
            self.indexDrive1Editable = True
        elif self.indexDrive1Editable == True:
            print('setting drive1 index path line edit: false')
            self.drive1TextEdit.setReadOnly(True)
            self.drive1TextEdit.setStyleSheet(
                """QLineEdit {background-color: rgb(15, 14, 15);
                border:5px solid rgb(0, 0, 0);
                selection-color: black;
                selection-background-color: black;
                color: grey;}"""
            )
            self.drive1TextEdit.setText(drive1_configuration.replace('DRIVE1: ', ''))
            self.indexDrive1Editable = False

    def writeDrive1PathFunction(self):
        global check_index_drive1_config
        global drive1_configuration
        line_list = []
        path_text = self.drive1TextEdit.text()
        print('Path Entered:', path_text)
        if os.path.exists(path_text):
            print('Path Exists:', path_text)
            with open('config.conf', 'r') as fo:
                for line in fo:
                    line_list.append(line)
            i = 0
            for line_lists in line_list:
                if line_list[i].startswith('DRIVE1: '):
                    print('Replacing list item:', line_list[i], 'with', path_text)
                    line_list[i] = str('DRIVE1: ' + path_text + '\n')
                i += 1
            fo.close()
            i = 0
            with open('config.conf', 'w') as fo:
                for line_lists in line_list:
                    fo.writelines(line_list[i])
                    # print('writing:', line_list[i])
                    i += 1
            fo.close()
            print('updated: drive 1 path configuration')
            check_index_drive1_config = True
            drive1_configuration = path_text

        elif not os.path.exists(path_text):
            print('Path does not exist')
            self.drive1TextEdit.setText(drive1_configuration.replace('DRIVE1: ', ''))
            check_index_drive1_config = False
        self.indexDrive1ConfigurationFunction()

    # Drive2 Index Settings
    def indexDrive2ConfigurationFunction(self):
        global drive2_configuration
        if self.indexDrive2Editable == False:
            print('setting drive2 index path line edit: true')
            self.drive2TextEdit.setReadOnly(False)
            self.drive2TextEdit.setStyleSheet(
                """QLineEdit {background-color: rgb(25, 24, 25);
                border:5px solid rgb(0, 0, 0);
                selection-color: black;
                selection-background-color: black;
                color: white;}"""
            )
            self.indexDrive2Editable = True
        elif self.indexDrive2Editable == True:
            print('setting drive2 index path line edit: false')
            self.drive2TextEdit.setReadOnly(True)
            self.drive2TextEdit.setStyleSheet(
                """QLineEdit {background-color: rgb(15, 14, 15);
                border:5px solid rgb(0, 0, 0);
                selection-color: black;
                selection-background-color: black;
                color: grey;}"""
            )
            self.drive2TextEdit.setText(drive2_configuration.replace('DRIVE2: ', ''))
            self.indexDrive2Editable = False

    def writeDrive2PathFunction(self):
        global check_index_drive2_config
        global drive2_configuration
        line_list = []
        path_text = self.drive2TextEdit.text()
        print('Path Entered:', path_text)
        if os.path.exists(path_text):
            print('Path Exists:', path_text)
            with open('config.conf', 'r') as fo:
                for line in fo:
                    line_list.append(line)
            i = 0
            for line_lists in line_list:
                if line_list[i].startswith('DRIVE2: '):
                    print('Replacing list item:', line_list[i], 'with', path_text)
                    line_list[i] = str('DRIVE2: ' + path_text + '\n')
                i += 1
            fo.close()
            i = 0
            with open('config.conf', 'w') as fo:
                for line_lists in line_list:
                    fo.writelines(line_list[i])
                    # print('writing:', line_list[i])
                    i += 1
            fo.close()
            print('updated: drive 2 path configuration')
            check_index_drive2_config = True
            drive2_configuration = path_text

        elif not os.path.exists(path_text):
            print('Path does not exist')
            self.drive2TextEdit.setText(drive2_configuration.replace('DRIVE2: ', ''))
            check_index_drive2_config = False
        self.indexDrive2ConfigurationFunction()

    # Drive3 Index Settings
    def indexDrive3ConfigurationFunction(self):
        global drive3_configuration
        if self.indexDrive3Editable == False:
            print('setting drive3 index path line edit: true')
            self.drive3TextEdit.setReadOnly(False)
            self.drive3TextEdit.setStyleSheet(
                """QLineEdit {background-color: rgb(25, 24, 25);
                border:5px solid rgb(0, 0, 0);
                selection-color: black;
                selection-background-color: black;
                color: white;}"""
            )
            self.indexDrive3Editable = True
        elif self.indexDrive3Editable == True:
            print('setting drive3 index path line edit: false')
            self.drive3TextEdit.setReadOnly(True)
            self.drive3TextEdit.setStyleSheet(
                """QLineEdit {background-color: rgb(15, 14, 15);
                border:5px solid rgb(0, 0, 0);
                selection-color: black;
                selection-background-color: black;
                color: grey;}"""
            )
            self.drive3TextEdit.setText(drive3_configuration.replace('DRIVE3: ', ''))
            self.indexDrive3Editable = False

    def writeDrive3PathFunction(self):
        global check_index_drive3_config
        global drive3_configuration
        line_list = []
        path_text = self.drive3TextEdit.text()
        print('Path Entered:', path_text)
        if os.path.exists(path_text):
            print('Path Exists:', path_text)
            with open('config.conf', 'r') as fo:
                for line in fo:
                    line_list.append(line)
            i = 0
            for line_lists in line_list:
                if line_list[i].startswith('DRIVE3: '):
                    print('Replacing list item:', line_list[i], 'with', path_text)
                    line_list[i] = str('DRIVE3: ' + path_text + '\n')
                i += 1
            fo.close()
            i = 0
            with open('config.conf', 'w') as fo:
                for line_lists in line_list:
                    fo.writelines(line_list[i])
                    # print('writing:', line_list[i])
                    i += 1
            fo.close()
            print('updated: drive 3 path configuration')
            check_index_drive3_config = True
            drive3_configuration = path_text

        elif not os.path.exists(path_text):
            print('Path does not exist')
            self.drive3TextEdit.setText(drive3_configuration.replace('DRIVE3: ', ''))
            check_index_drive3_config = False
        self.indexDrive3ConfigurationFunction()

    # Drive4 Index Settings
    def indexDrive4ConfigurationFunction(self):
        global drive4_configuration
        if self.indexDrive4Editable == False:
            print('setting drive4 index path line edit: true')
            self.drive4TextEdit.setReadOnly(False)
            self.drive4TextEdit.setStyleSheet(
                """QLineEdit {background-color: rgb(25, 24, 25);
                border:5px solid rgb(0, 0, 0);
                selection-color: black;
                selection-background-color: black;
                color: white;}"""
            )
            self.indexDrive4Editable = True
        elif self.indexDrive4Editable == True:
            print('setting drive4 index path line edit: false')
            self.drive4TextEdit.setReadOnly(True)
            self.drive4TextEdit.setStyleSheet(
                """QLineEdit {background-color: rgb(15, 14, 15);
                border:5px solid rgb(0, 0, 0);
                selection-color: black;
                selection-background-color: black;
                color: grey;}"""
            )
            self.drive4TextEdit.setText(drive4_configuration.replace('DRIVE4: ', ''))
            self.indexDrive4Editable = False

    def writeDrive4PathFunction(self):
        global check_index_drive4_config
        global drive4_configuration
        line_list = []
        path_text = self.drive4TextEdit.text()
        print('Path Entered:', path_text)
        if os.path.exists(path_text):
            print('Path Exists:', path_text)
            with open('config.conf', 'r') as fo:
                for line in fo:
                    line_list.append(line)
            i = 0
            for line_lists in line_list:
                if line_list[i].startswith('DRIVE4: '):
                    print('Replacing list item:', line_list[i], 'with', path_text)
                    line_list[i] = str('DRIVE4: ' + path_text + '\n')
                i += 1
            fo.close()
            i = 0
            with open('config.conf', 'w') as fo:
                for line_lists in line_list:
                    fo.writelines(line_list[i])
                    # print('writing:', line_list[i])
                    i += 1
            fo.close()
            print('updated: drive 4 path configuration')
            check_index_drive4_config = True
            drive4_configuration = path_text

        elif not os.path.exists(path_text):
            print('Path does not exist')
            self.drive4TextEdit.setText(drive4_configuration.replace('DRIVE4: ', ''))
            check_index_drive4_config = False
        self.indexDrive4ConfigurationFunction()

    # Drive5 Index Settings
    def indexDrive5ConfigurationFunction(self):
        global drive5_configuration
        if self.indexDrive5Editable == False:
            print('setting drive5 index path line edit: true')
            self.drive5TextEdit.setReadOnly(False)
            self.drive5TextEdit.setStyleSheet(
                """QLineEdit {background-color: rgb(25, 24, 25);
                border:5px solid rgb(0, 0, 0);
                selection-color: black;
                selection-background-color: black;
                color: white;}"""
            )
            self.indexDrive5Editable = True
        elif self.indexDrive5Editable == True:
            print('setting drive5 index path line edit: false')
            self.drive5TextEdit.setReadOnly(True)
            self.drive5TextEdit.setStyleSheet(
                """QLineEdit {background-color: rgb(15, 14, 15);
                border:5px solid rgb(0, 0, 0);
                selection-color: black;
                selection-background-color: black;
                color: grey;}"""
            )
            self.drive5TextEdit.setText(drive5_configuration.replace('DRIVE5: ', ''))
            self.indexDrive5Editable = False

    def writeDrive5PathFunction(self):
        global check_index_drive5_config
        global drive5_configuration
        line_list = []
        path_text = self.drive5TextEdit.text()
        print('Path Entered:', path_text)
        if os.path.exists(path_text):
            print('Path Exists:', path_text)
            with open('config.conf', 'r') as fo:
                for line in fo:
                    line_list.append(line)
            i = 0
            for line_lists in line_list:
                if line_list[i].startswith('DRIVE5: '):
                    print('Replacing list item:', line_list[i], 'with', path_text)
                    line_list[i] = str('DRIVE5: ' + path_text + '\n')
                i += 1
            fo.close()
            i = 0
            with open('config.conf', 'w') as fo:
                for line_lists in line_list:
                    fo.writelines(line_list[i])
                    # print('writing:', line_list[i])
                    i += 1
            fo.close()
            print('updated: drive 5 path configuration')
            check_index_drive5_config = True
            drive5_configuration = path_text

        elif not os.path.exists(path_text):
            print('Path does not exist')
            self.drive5TextEdit.setText(drive5_configuration.replace('DRIVE5: ', ''))
            check_index_drive5_config = False
        self.indexDrive5ConfigurationFunction()

    # Drive6 Index Settings
    def indexDrive6ConfigurationFunction(self):
        global drive6_configuration
        if self.indexDrive6Editable == False:
            print('setting drive6 index path line edit: true')
            self.drive6TextEdit.setReadOnly(False)
            self.drive6TextEdit.setStyleSheet(
                """QLineEdit {background-color: rgb(25, 24, 25);
                border:5px solid rgb(0, 0, 0);
                selection-color: black;
                selection-background-color: black;
                color: white;}"""
            )
            self.indexDrive6Editable = True
        elif self.indexDrive6Editable == True:
            print('setting drive6 index path line edit: false')
            self.drive6TextEdit.setReadOnly(True)
            self.drive6TextEdit.setStyleSheet(
                """QLineEdit {background-color: rgb(15, 14, 15);
                border:5px solid rgb(0, 0, 0);
                selection-color: black;
                selection-background-color: black;
                color: grey;}"""
            )
            self.drive6TextEdit.setText(drive6_configuration.replace('DRIVE6: ', ''))
            self.indexDrive6Editable = False

    def writeDrive6PathFunction(self):
        global check_index_drive6_config
        global drive6_configuration
        line_list = []
        path_text = self.drive6TextEdit.text()
        print('Path Entered:', path_text)
        if os.path.exists(path_text):
            print('Path Exists:', path_text)
            with open('config.conf', 'r') as fo:
                for line in fo:
                    line_list.append(line)
            i = 0
            for line_lists in line_list:
                if line_list[i].startswith('DRIVE6: '):
                    print('Replacing list item:', line_list[i], 'with', path_text)
                    line_list[i] = str('DRIVE6: ' + path_text + '\n')
                i += 1
            fo.close()
            i = 0
            with open('config.conf', 'w') as fo:
                for line_lists in line_list:
                    fo.writelines(line_list[i])
                    # print('writing:', line_list[i])
                    i += 1
            fo.close()
            print('updated: drive 6 path configuration')
            check_index_drive6_config = True
            drive6_configuration = path_text

        elif not os.path.exists(path_text):
            print('Path does not exist')
            self.drive6TextEdit.setText(drive6_configuration.replace('DRIVE6: ', ''))
            check_index_drive6_config = False
        self.indexDrive6ConfigurationFunction()

    # Drive7 Index Settings
    def indexDrive7ConfigurationFunction(self):
        global drive7_configuration
        if self.indexDrive7Editable == False:
            print('setting drive7 index path line edit: true')
            self.drive7TextEdit.setReadOnly(False)
            self.drive7TextEdit.setStyleSheet(
                """QLineEdit {background-color: rgb(25, 24, 25);
                border:5px solid rgb(0, 0, 0);
                selection-color: black;
                selection-background-color: black;
                color: white;}"""
            )
            self.indexDrive7Editable = True
        elif self.indexDrive7Editable == True:
            print('setting drive7 index path line edit: false')
            self.drive7TextEdit.setReadOnly(True)
            self.drive7TextEdit.setStyleSheet(
                """QLineEdit {background-color: rgb(15, 14, 15);
                border:5px solid rgb(0, 0, 0);
                selection-color: black;
                selection-background-color: black;
                color: grey;}"""
            )
            self.drive7TextEdit.setText(drive7_configuration.replace('DRIVE7: ', ''))
            self.indexDrive7Editable = False

    def writeDrive7PathFunction(self):
        global check_index_drive7_config
        global drive7_configuration
        line_list = []
        path_text = self.drive7TextEdit.text()
        print('Path Entered:', path_text)
        if os.path.exists(path_text):
            print('Path Exists:', path_text)
            with open('config.conf', 'r') as fo:
                for line in fo:
                    line_list.append(line)
            i = 0
            for line_lists in line_list:
                if line_list[i].startswith('DRIVE7: '):
                    print('Replacing list item:', line_list[i], 'with', path_text)
                    line_list[i] = str('DRIVE7: ' + path_text + '\n')
                i += 1
            fo.close()
            i = 0
            with open('config.conf', 'w') as fo:
                for line_lists in line_list:
                    fo.writelines(line_list[i])
                    # print('writing:', line_list[i])
                    i += 1
            fo.close()
            print('updated: drive 7 path configuration')
            check_index_drive7_config = True
            drive7_configuration = path_text

        elif not os.path.exists(path_text):
            print('Path does not exist')
            self.drive7TextEdit.setText(drive7_configuration.replace('DRIVE7: ', ''))
            check_index_drive7_config = False
        self.indexDrive7ConfigurationFunction()

    # Drive8 Index Settings
    def indexDrive8ConfigurationFunction(self):
        global drive8_configuration
        if self.indexDrive8Editable == False:
            print('setting drive8 index path line edit: true')
            self.drive8TextEdit.setReadOnly(False)
            self.drive8TextEdit.setStyleSheet(
                """QLineEdit {background-color: rgb(25, 24, 25);
                border:5px solid rgb(0, 0, 0);
                selection-color: black;
                selection-background-color: black;
                color: white;}"""
            )
            self.indexDrive8Editable = True
        elif self.indexDrive8Editable == True:
            print('setting drive8 index path line edit: false')
            self.drive8TextEdit.setReadOnly(True)
            self.drive8TextEdit.setStyleSheet(
                """QLineEdit {background-color: rgb(15, 14, 15);
                border:5px solid rgb(0, 0, 0);
                selection-color: black;
                selection-background-color: black;
                color: grey;}"""
            )
            self.drive8TextEdit.setText(drive8_configuration.replace('DRIVE8: ', ''))
            self.indexDrive8Editable = False

    def writeDrive8PathFunction(self):
        global check_index_drive8_config
        global drive8_configuration
        line_list = []
        path_text = self.drive8TextEdit.text()
        print('Path Entered:', path_text)
        if os.path.exists(path_text):
            print('Path Exists:', path_text)
            with open('config.conf', 'r') as fo:
                for line in fo:
                    line_list.append(line)
            i = 0
            for line_lists in line_list:
                if line_list[i].startswith('DRIVE8: '):
                    print('Replacing list item:', line_list[i], 'with', path_text)
                    line_list[i] = str('DRIVE8: ' + path_text + '\n')
                i += 1
            fo.close()
            i = 0
            with open('config.conf', 'w') as fo:
                for line_lists in line_list:
                    fo.writelines(line_list[i])
                    # print('writing:', line_list[i])
                    i += 1
            fo.close()
            print('updated: drive 8 path configuration')
            check_index_drive8_config = True
            drive8_configuration = path_text

        elif not os.path.exists(path_text):
            print('Path does not exist')
            self.drive8TextEdit.setText(drive6_configuration.replace('DRIVE8: ', ''))
            check_index_drive8_config = False
        self.indexDrive8ConfigurationFunction()

    # def drawRectangles(self, qp):
    #
    #
    #     # # SpeechRecognition Color
    #     # qp.setBrush(QColor(25, 24, 25)) # 1
    #     # # Dimensions: MOVE: width, height. RECT-SIZE: width height
    #     # qp.drawRect(20, 45, 740, 120) # 1
    #
    #     # qp.setBrush(QColor(0, 255, 0))  # 2a
    #     # qp.drawRect(16, 41, 748, 4)  # 2a
    #     #
    #     # qp.setBrush(QColor(0, 255, 0))  # 2b
    #     # qp.drawRect(16, 45, 4, 120)  # 2b
    # # Settings Index Engine Configuration

    def drawRectangles(self, qp):
        if showHideValue == 1:
            qp.setBrush(QColor(25, 24, 25))
            qp.drawRect(20, 200, 740, 90)

            # Settings Top Divider
            qp.setBrush(QColor(0, 0, 0))
            qp.drawRect(358, 200, 4, 90)

            # Symbiot Settings
            qp.setBrush(QColor(25, 24, 25))
            qp.drawRect(20, 320, 740, 100)

            # Symbiot Top Divider
            qp.setBrush(QColor(0, 0, 0))
            qp.drawRect(358, 320, 4, 100)


runIndexEnginesFunction()
time.sleep(1)


class guiControllerClass(QThread):
    def __init__(self, srInfo, textBoxValue, textBoxVerbose1, textBoxVerbose2):
        QThread.__init__(self)
        self.srInfo = srInfo
        self.textBoxValue = textBoxValue
        self.textBoxVerbose1 = textBoxVerbose1
        self.textBoxVerbose2 = textBoxVerbose2
        self.guiControllerCount = 0

    def run(self):
        while self.guiControllerCount <= 1:
            if self.guiControllerCount == 1:
                self.srInfo.setText("")
                self.textBoxValue.setText("")
                self.textBoxVerbose1.setText("")
                self.textBoxVerbose2.setText("")
                self.guiControllerCount = 0
                break
            else:
                time.sleep(4)
                self.guiControllerCount += 1

    def stop_guiController(self):
        self.srInfo.setText("")
        self.textBoxValue.setText("")
        self.textBoxVerbose1.setText("")
        self.textBoxVerbose2.setText("")
        self.terminate()


class configInteractionPermissionClass(QThread):
    def __init__(self, indexAudioEnableDisableButton, indexVideoEnableDisableButton, indexImageEnableDisableButton,
                 indexTextEnableDisableButton, indexAudioEdit, indexVideoEdit, indexImagesEdit, indexTextEdit,
                 indexAudioButton, indexVideoButton, indexImageButton, indexTextButton, drive1EnableDisableButton,
                 drive2EnableDisableButton, drive3EnableDisableButton, drive4EnableDisableButton, drive1TextEdit,
                 drive2TextEdit, drive3TextEdit, drive4TextEdit, drive1Button, drive2Button, drive3Button,
                 drive4Button):
        QThread.__init__(self)
        self.indexAudioEnableDisableButton = indexAudioEnableDisableButton
        self.indexVideoEnableDisableButton = indexVideoEnableDisableButton
        self.indexImageEnableDisableButton = indexImageEnableDisableButton
        self.indexTextEnableDisableButton = indexTextEnableDisableButton
        self.indexAudioEdit = indexAudioEdit
        self.indexVideoEdit = indexVideoEdit
        self.indexImagesEdit = indexImagesEdit
        self.indexTextEdit = indexTextEdit
        self.indexAudioButton = indexAudioButton
        self.indexVideoButton = indexVideoButton
        self.indexImageButton = indexImageButton
        self.indexTextButton = indexTextButton

        self.drive1EnableDisableButton = drive1EnableDisableButton
        self.drive2EnableDisableButton = drive2EnableDisableButton
        self.drive3EnableDisableButton = drive3EnableDisableButton
        self.drive4EnableDisableButton = drive4EnableDisableButton
        self.drive1TextEdit = drive1TextEdit
        self.drive2TextEdit = drive2TextEdit
        self.drive3TextEdit = drive3TextEdit
        self.drive4TextEdit = drive4TextEdit
        self.drive1Button = drive1Button
        self.drive2Button = drive2Button
        self.drive3Button = drive3Button
        self.drive4Button = drive4Button

    def run(self):
        # This Class runs on a thread to prevent spamming writes to config via enable/disable button. minus the
        # nice graphics like a loading/waiting spinning circle.
        print('plugged in: configInteractionPermissionClass')
        print('temporarily disabling configuration settings: writing to config...')
        index_enable_disable_button_item = [self.indexAudioEnableDisableButton,
                                            self.indexVideoEnableDisableButton,
                                            self.indexImageEnableDisableButton,
                                            self.indexTextEnableDisableButton,
                                            self.indexAudioEdit,
                                            self.indexVideoEdit,
                                            self.indexImagesEdit,
                                            self.indexTextEdit,
                                            self.indexAudioButton,
                                            self.indexVideoButton,
                                            self.indexImageButton,
                                            self.indexTextButton,
                                            self.drive1EnableDisableButton,
                                            self.drive2EnableDisableButton,
                                            self.drive3EnableDisableButton,
                                            self.drive4EnableDisableButton,
                                            self.drive1TextEdit,
                                            self.drive2TextEdit,
                                            self.drive3TextEdit,
                                            self.drive4TextEdit,
                                            self.drive1Button,
                                            self.drive2Button,
                                            self.drive3Button,
                                            self.drive4Button
                                            ]
        i = 0
        for index_enable_disable_button_items in index_enable_disable_button_item:
            index_enable_disable_button_item[i].setEnabled(False)
            # print('locking:',index_enable_disable_button_item[i])
            i += 1

        time.sleep(2)

        print('enabling configuration settings: finished write')
        i = 0
        for index_enable_disable_button_items in index_enable_disable_button_item:
            index_enable_disable_button_item[i].setEnabled(True)
            # print('unlocking:',index_enable_disable_button_item[i])
            i += 1


class textBoxVerbose2Class(QThread):
    def __init__(self, textBoxVerbose2):
        QThread.__init__(self)
        self.textBoxVerbose2 = textBoxVerbose2

    def __del__(self):
        self.wait()

    def run(self):
        global sppid
        sppid_str = str(sppid)
        sppid_str2 = str('subprocess PID: ')
        self.textBoxVerbose2.setText(sppid_str2 + sppid_str)


class openDirectoryClass(QThread):
    def __init__(self, textBoxVerbose, textBoxVerbose2):
        QThread.__init__(self)
        self.textBoxVerbose = textBoxVerbose
        self.textBoxVerbose2 = textBoxVerbose

    def __del__(self):
        self.wait()

    def run(self):
        global secondary_key
        global directory_index_file
        secondary_key_no_space = secondary_key.replace(' ', '')
        print('plugged in: openDirectoryClass')
        found_list = []
        dir_i = 0
        for directory_index_files in directory_index_file:
            print('searching directory index file:', dir_i)
            if os.path.exists(directory_index_file[dir_i]):
                with codecs.open(directory_index_file[dir_i], 'r', encoding='utf-8') as fo:
                    for line in fo:
                        line = line.strip()
                        line2 = line.strip()
                        line2 = line2.lower()
                        line2 = line2.replace('\\', '')
                        line2 = line2.replace('_', '')
                        line2 = line2.replace('-', '')
                        line2 = line2.replace('&', 'and')
                        line2 = line2.replace(']', '')
                        line2 = line2.replace('[', '')
                        line2 = line2.replace(')', '')
                        line2 = line2.replace('(', '')
                        line2 = line2.replace(' ', '')

                        if line2.endswith(secondary_key_no_space + '"'):
                            print(line)
                            found_list.append(line)
                dir_i += 1

            else:
                print('skipping, directory index file', dir_i, 'does not exist...')
                dir_i += 1

        print('search complete...')

        # Currently, ensure only one result will open. (later, better formula for best match in found_list instead [0])
        if len(found_list) >= 1:
            os.startfile(found_list[0])
            found_list = []


class findOpenAudioClass(QThread):
    def __init__(self, target_index, multiple_matches, target_match, textBoxVerbose1):
        QThread.__init__(self)
        self.target_index = target_index
        self.multiple_matches = multiple_matches
        self.target_match = target_match
        self.textBoxVerbose1 = textBoxVerbose1

    def __del__(self):
        self.wait()

    def run(self):
        print('plugged in thread: findOpenAudioClass')
        global multiple_matches
        global secondary_key
        global audio_index_file
        result_count = 0
        with codecs.open(audio_index_file, 'r', encoding='utf-8') as fo:
            for line in fo:
                line = line.strip()
                line = line.lower()
                line = line.replace('"', '')
                line = str('"' + line + '"')
                human_name = line
                idx = human_name.find('\\')
                human_name = human_name[idx:]
                if secondary_key in line:
                    result_count += 1
                    idx = line.rfind('\\')
                    human_name = line[idx:]
                    human_name = human_name.replace('\\', '')
                    human_name = human_name.replace('"', '')
                    multiple_matches.append(human_name)
                    target_match = line
                else:
                    pass
        # Check for matches
        if result_count == 0:
            # speaker.Speak("nothing found for "+secondary_key)
            print("nothing found for", secondary_key)
            self.textBoxVerbose1.setText("nothing found for: " + secondary_key)
        else:
            i = 0
            # More than one result
            if result_count > 1:
                print('matching results:', result_count)
                string_result_count = str(result_count)
                # speaker.Speak(string_result_count + ' matches for ' + secondary_key)
                for multiple_matchess in multiple_matches:
                    print(multiple_matches[i])
                    i += 1
            # Exactly One Result
            if result_count == 1:
                print('matching results:', result_count)
                print('found:', target_match)
                self.textBoxVerbose1.setText("Found")
                target_match = target_match.strip()
                print("running:", target_match)
                # Users Default Player (Option 1)
                os.startfile(target_match)


class findOpenImageClass(QThread):
    def __init__(self):
        QThread.__init__(self)

    def run(self):
        global image_index_file
        global secondary_key
        found_file = []
        print('plugged in: fileOpenImageClass')
        with open(image_index_file, 'r') as fo:
            for line in fo:
                line = line.strip()
                line = line.lower()
                if secondary_key in line:
                    found_file.append(line)
            fo.close()
        if len(found_file) == 1:
            os.startfile(found_file[0])
        else:
            i = 0
            for found_files in found_file:
                print(found_file[i])
                i += 1


class findOpenTextClass(QThread):
    def __init__(self):
        QThread.__init__(self)

    def run(self):
        global text_index_file
        global secondary_key
        found_file = []
        print('plugged in: fileOpenTextClass')
        with open(text_index_file, 'r') as fo:
            for line in fo:
                line = line.strip()
                line = line.lower()
                if secondary_key in line:
                    found_file.append(line)
            fo.close()
        if len(found_file) == 1:
            os.startfile(found_file[0])
        else:
            i = 0
            for found_files in found_file:
                print(found_file[i])
                i += 1


class findOpenVideoClass(QThread):
    def __init__(self):
        QThread.__init__(self)

    def run(self):
        global video_index_file
        global secondary_key
        found_file = []
        print('plugged in: fileOpenVideoClass')
        with codecs.open(video_index_file, 'r', encoding='utf-8') as fo:
            for line in fo:
                print(line)
                line = line.strip()
                line = line.lower()
                if secondary_key in line:
                    found_file.append(line)
            fo.close()
        if len(found_file) == 1:
            os.startfile(found_file[0])
        else:
            i = 0
            for found_files in found_file:
                print(found_file[i])
                i += 1


class findOpenProgramClass(QThread):
    def __init__(self):
        QThread.__init__(self)

    def run(self):
        global program_index_file
        global secondary_key
        found_file = []
        print('plugged in: findOpenProgramClass')
        with codecs.open(program_index_file, 'r', encoding='utf-8') as fo:
            for line in fo:
                print(line)
                line = line.strip()
                line = line.lower()
                if secondary_key in line:
                    found_file.append(line)
            fo.close()
        if len(found_file) == 1:
            os.startfile(found_file[0])
        else:
            i = 0
            for found_files in found_file:
                print(found_file[i])
                i += 1


class commandSearchClass(QThread):
    def __init__(self, textBoxVerbose1, textBoxVerbose2, textBoxVerbose2Thread):
        QThread.__init__(self)
        self.textBoxVerbose1 = textBoxVerbose1
        self.textBoxVerbose2 = textBoxVerbose2
        self.textBoxVerbose2Thread = textBoxVerbose2Thread

    def __del__(self):
        self.wait()

    def run(self):
        print('plugged in thread: commandSearch')
        global value
        global currentAudioMedia
        global sppid
        found = False
        search_str = value
        search_str = search_str.replace(' ', '')
        search_str = search_str.strip()
        with open(plugin_index, 'r') as infile:
            for line in infile:
                line = line.strip()
                idx = line.rfind('\\') + 1
                linefind = line[idx:].replace('.py"', '')
                if search_str.startswith(linefind):
                    self.textBoxVerbose1.setText('running command: python ' + linefind + '.py')
                    print('found command file:', line)
                    line = line.strip()
                    cmd = ('python ' + line)
                    print('running command:', cmd)
                    sp = subprocess.Popen(cmd, shell=False, startupinfo=info)
                    sppid = sp.pid
                    sppsutil = psutil.Process(sppid)
                    print('subprocess PID:', sppid)
                    found = True
                    self.textBoxVerbose2Thread.start()

            if found == False:
                self.textBoxVerbose1.setText("command not found")


# Store socket here for closing when thread is stopped
sock_con = ()


class symbiotServerClass(QThread):
    def __init__(self, speechRecognitionThread, symbiotButton, speechRecognitionOffFunction, speechRecognitionOnFunction):
        QThread.__init__(self)
        self.symbiotButton = symbiotButton
        self.speechRecognitionOffFunction = speechRecognitionOffFunction
        self.speechRecognitionOnFunction = speechRecognitionOnFunction

    def run(self):
        global sock_con
        symbiot_log = 'symbiot_server.log'
        if not os.path.exists(symbiot_log):
            open(symbiot_log, 'w').close()
        host = ''
        port = ''
        on = 0
        print('plugged in: symbiotServerClass')
        sr_on_message = str('DSFLJdfsdfknsdfDfsdlfDSLfjLSDFjsdfsdfgSDfgG')
        sr_off_message = str('ADfeFArgDHBtHaGafdGagadfaDfgASDfaaDGfadfa')
        s = socket.socket()
        sock_con = s
        with codecs.open('config.conf', 'r', encoding="utf-8") as fo:
            for line in fo:
                if line.startswith('SYMBIOT_SERVER: '):
                    host = line.replace('SYMBIOT_SERVER: ', '')
                    host = host.strip()
                    print('symbiot server ip configuration:', host)
                if line.startswith('SYMBIOT_SERVER_PORT: '):
                    port = line.replace('SYMBIOT_SERVER_PORT: ', '')
                    port = port.strip()
                    port = int(port)
                    if port == 0:
                        print('symbiot server port configuration:', port, '/ any available port')
                    else:
                        print('symbiot server port configuration:', port)
                if line.startswith('SYMBIOT_IP: '):
                    symbiot_ip = line.replace('SYMBIOT_IP: ', '')
                    symbiot_ip = symbiot_ip.strip()
                if line.startswith('SYMBIOT_MAC: '):
                    symbiot_mac = line.replace('SYMBIOT_MAC: ', '')
                    symbiot_mac = symbiot_mac.strip()
        try:
            s.bind((host, port))
            on = 1
            print('symbiot server successfully binded to', s.getsockname()[1])
        except socket.error as msg:
            print('symbiot server failed to bind to', port, '. Error Code : ', msg)

        while on == 1:

            # Wait for incoming client
            print('symbiot server enabled')
            print('symbiot server listening:')
            s.listen(5)

            try:
                c, addr = s.accept()

                # Print Client IP and Port
                ip = str(addr[0])
                port = str(addr[1])
                client_info = ('ip=' + ip + '  ' + 'port=' + str(port))
                print('client connected: ', client_info)

                # log here later

                # scan for mac as a security measure. mac spoofing is easy so later read a pw from ssl wrapped message.
                cmd = 'arp -a ' + addr[0]
                print('scanning client:', cmd)
                xcmd = subprocess.check_output(cmd, shell=False, startupinfo=info)

                cmd_output = str(xcmd)
                cmd_output = cmd_output.split("\\r\\n")

                device = cmd_output[3]
                device = device.split()

                device_ip = device[0]
                device_mac = device[1]

                # Compare ip and mac to trusted device list
                print('checking validitity of client:')
                if device_ip == symbiot_ip:
                    if device_mac == symbiot_mac:
                        print('client validated: client will be treated as valid symbiot')

                        # Recieve magic-key/message from Client
                        connection_message = c.recv(1024)
                        connection_message = str(connection_message)
                        connection_message = connection_message.strip('\'b')
                        connection_message = connection_message.strip('"')

                        # Compare magic-key message to local magic key
                        if connection_message == sr_on_message:
                            print('client', addr[0], 'has command-string')
                            print('starting speech recognition thread...')
                            # speechRecognitionThread.start()
                            self.speechRecognitionOnFunction()
                        elif connection_message == sr_off_message:
                            print('client', addr[0], 'has command-string')
                            print('stopping speech recognition thread...')
                            self.speechRecognitionOffFunction()

                        # Disconect
                        print('disconnecting from client')
                        c.close()
                    elif device_mac != symbiot_mac:
                        print('mac of client does not match trusted symbiot mac, refusing message')
                elif device_ip != symbiot_ip:
                    print('ip of client does not match trusted symbiot ip, refusing message')


            except ConnectionRefusedError:
                print('target machine actively refused conection...')
            except ConnectionResetError:
                print('an existing connection was forcibly closed by the remote host')
            except OSError:
                print('a connect request was made on an already connected socket')

    def symbiot_server_off(self):
        global sock_con
        sock_con.close()
        self.terminate()


class speechRecognitionClass(QThread):
    def __init__(self, srIndicator, textBoxValue, textBoxVerbose1, textBoxVerbose2, textBoxVerbose2Thread, srInfo,
                 guiControllerThread, commandSearchThread, srOnButton):
        QThread.__init__(self)
        self.srInfo = srInfo
        self.textBoxValue = textBoxValue
        self.guiControllerThread = guiControllerThread
        self.textBoxVerbose = textBoxVerbose1
        self.textBoxVerbose2 = textBoxVerbose2
        self.textBoxVerbose2Thread = textBoxVerbose2Thread
        self.commandSearchThread = commandSearchThread
        self.srIndicator = srIndicator
        self.srOnButton = srOnButton

    def run(self):
        print('plugged in thread: speechRecognitionThread')
        global secondary_key
        global value
        global sppid
        global currentAudioMedia

        r = sr.Recognizer()
        m = sr.Microphone()


        try:
            pixmap = QPixmap('./Resources/image/sr_indicator_on_icon.png')
            self.srIndicator.setPixmap(pixmap)
            self.srInfo.setText("A moment of silence please...")
            with m as source:
                r.adjust_for_ambient_noise(source)
            self.srInfo.setText("Set minimum energy threshold to {}".format(r.energy_threshold))

            while True:
                self.srInfo.setText("Waiting for command")
                with m as source:
                    audio = r.listen(source)
                self.srInfo.setText("Attempting to recognize audio...")

                try:
                    value = r.recognize_google(audio).lower()
                    self.textBoxValue.setText('Interpretation: ' + value)
                    self.guiControllerThread.start()

                    with codecs.open(secondary_key_store, 'w', encoding='utf-8') as fo:
                        fo.write(value)
                        fo.close()
                    with codecs.open('Plugins/Windows10Host/secondary-key.tmp', 'w', encoding='utf-8') as fo:
                        fo.write(value)
                        fo.close()

                    i = 0
                    key_word_check = False
                    for key_words in key_word:

                        if value.startswith(key_word[i]):

                            key_word_length = len(key_word[i])

                            primary_key = key_word[i][:key_word_length]

                            secondary_key = value[key_word_length:]
                            secondary_key = secondary_key.strip()

                            print('Primary Key: ', primary_key)
                            print('Secondary Key: ', secondary_key)

                            with codecs.open(secondary_key_store, 'w', encoding='utf-8') as fo:
                                fo.write(secondary_key)
                                fo.close()

                            if primary_key in internal_commands_list:
                                execute_funk = internal_commands_list[primary_key]
                                key_word_check = True
                                execute_funk()
                            else:
                                key_word_check = False
                        i += 1

                    if key_word_check == False:
                        self.commandSearchThread.start()

                except sr.UnknownValueError:
                    self.srInfo.setText("ignoring background noise...")
                except sr.RequestError as e:
                    self.srInfo.setText("Google Speech Recognition service unavailable...Offline?")
        except KeyboardInterrupt:
            pass

    def stop_sr(self):
        pixmap = QPixmap('./Resources/image/sr_indicator_off_icon.png')
        self.srIndicator.setPixmap(pixmap)
        self.terminate()


if __name__ == '__main__':
    app = QApplication(sys.argv)
    ex = App()
    sys.exit(app.exec_())
