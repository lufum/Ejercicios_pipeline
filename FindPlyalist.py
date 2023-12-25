import sys
sys.path.append("E:/Programas/Shotgun/python-api-master")
from shotgun_api3 import Shotgun
SERVER_PATH = 'https://0vfx.shotgunstudio.com'
SCRIPT_NAME = "playlist validacion"
#SCRIPT_KEY = 'q@xvuwvvupiIqsemtapwc6mrh'
SCRIPT_KEY  = '!sgwmdkfjayvkgarr3xwCours'

sg = Shotgun(SERVER_PATH, SCRIPT_NAME, SCRIPT_KEY)

project_id = 1352

fields =  ['id', 'code', 'sg_date_and_time', 'versions', 'sg_head_in', 'sg_tail_out']
filters =  [['project', 'is', {'type': 'Project', 'id': project_id}]]
shot =  sg.find("Shot", filters, fields)

for i in shot:
    print i
