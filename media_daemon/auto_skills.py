import os
from glob import glob
import shutil
from subprocess import check_output #nosec #pylint-disable type: ignore

# To get media_daemon folder
media_daemon_folder = os.path.dirname(os.path.abspath(__file__))
base_folder = os.path.dirname(media_daemon_folder)
server_skill_folder = os.path.join(base_folder, 'susi_server/susi_server/data/generic_skills/media_discovery')
server_settings_folder = os.path.join(base_folder, 'susi_server/susi_server/data/settings')

def make_skill(): # pylint-enable
    name_of_usb = get_mount_points()
    print(type(name_of_usb))
    print(name_of_usb[0])
    x = name_of_usb[0]
    os.chdir('{}'.format(x[1]))
    USB = name_of_usb[0]
    mp3 = [file for file in glob("*.mp3")]
    f = open( media_daemon_folder +'/custom_skill.txt','w')
    music_path = list()
    for mp in mp3:
        music_path.append("{}".format(USB[1]) + "/{}".format(mp))

    song_list = " ".join(music_path)
    skills = ['play audio','!console:Playing audio from your usb device','{"actions":[','{"type":"audio_play", "identifier_type":"url", "identifier":"file://'+str(song_list) +'"}',']}','eol']
    for skill in skills:
        f.write(skill + '\n')
    f.close()
    shutil.move( media_daemon_folder + 'custom_skill.txt', server_skill_folder)
    f2 = open(server_settings_folder + 'customized_config.properties','a')
    f2.write('local.mode = true')
    f2.close()

def get_usb_devices():
    sdb_devices = map(os.path.realpath, glob('/sys/block/sd*'))
    usb_devices = (dev for dev in sdb_devices
        if 'usb' in dev.split('/')[5])
    return dict((os.path.basename(dev), dev) for dev in usb_devices)

def get_mount_points(devices=None):
    devices = devices or get_usb_devices() # if devices are None: get_usb_devices
    output = check_output(['mount']).splitlines() #nosec #pylint-disable type: ignore
    output = [tmp.decode('UTF-8') for tmp in output ] # pytlint-enable
    def is_usb(path):
        return any(dev in path for dev in devices)
    usb_info = (line for line in output if is_usb(line.split()[0]))
    return [(info.split()[0], info.split()[2]) for info in usb_info]

if __name__ == '__main__':
    print(get_mount_points())
    name_of_usb = get_mount_points()
    print(type(name_of_usb))
    make_skill()
