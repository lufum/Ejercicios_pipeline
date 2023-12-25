import os

scene_path = 'IAV1/sequences/IAV000_0it/IAV000_0it_010/cmp/publish/maya/IAV1_IAV000_0it_010_cmp_test_master_v001.ma'
publish_name = os.path.basename(scene_path).split('.')[0][:-4]

print (publish_name)