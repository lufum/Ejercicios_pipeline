import maya.cmds as cmds
import os
import datetime
import sys
import subprocess

class cstm_playblast():
    
    def __init__(self):
        
        #self.create_playblast()
        full_path = cmds.file(q=True, sn=True)
        self.in_path = os.path.dirname(full_path)
        self.qlt = 90
        self.win = 'path_win'
        self.title = 'Playblast path'
        self.size = (450, 250)
        
        #crea la ventana
        if cmds.window(self.win, exists = True):
            cmds.deleteUI(self.win, window = True)
        cmds.window(self.win, t = self.title, wh= self.size)
        cmds.columnLayout(adjustableColumn = 1)
        cmds.separator(h=40)
        self.path_dir = cmds.textFieldGrp(l = "Save to", tx= self.in_path)
        cmds.separator(h=20)
        self.qlt_field = cmds.textFieldGrp(l = "Set Quality", tx= self.qlt)
        cmds.separator(h=20)
        self.check_os = cmds.checkBox( label='Playblast offScreen' )
        cmds.separator(h=20)
        cmds.button( label='PLAYBLAST', command=(self.create_playblast))
        cmds.showWindow( self.win )

        self.sel = cmds.ls(sl = 1)


    def create_playblast(self, *args):

        self.in_path = cmds.textFieldGrp(self.path_dir, q=1, tx=1)
        self.qlt = float (cmds.textFieldGrp(self.qlt_field, q=1, tx=1))
        os_opt =  cmds.checkBox(self.check_os, q=1, v=1)
        cmds.deleteUI(self.win, window = True)

        #get info for name
        file_=os.path.basename(cmds.file(q=True, sn=True))
        """
        fecha= datetime.datetime.now()
        day= str(fecha.day)
        month= str(fecha.month)
        year= str(fecha.year)
        hour= str(fecha.hour)+'-'+str(fecha.minute)
        fecha_disp= year+'_'+month+'_'+day+'--'+hour
        """
        os_sys = sys.platform
        # name of the file
        f_name = self.in_path +'/'+ file_.split('.')[0]

        # playblast dimensions
        fr_width = 1920
        fr_height = 1080

        # camera Attributes
        cur_mp = ""
        for mp in cmds.getPanel(type="modelPanel"):
            if cmds.modelEditor(mp, q=1, av=1):
                cur_mp = mp
        cur_cam= cmds.modelEditor(cur_mp, q=1, av =1, cam=1)
        res_gate_attr= cmds.getAttr(cur_cam+'.filmFit')
        ovscn_attr=  cmds.getAttr(cur_cam+'.overscan')
        film_gate_attr=  cmds.getAttr(cur_cam+'.displayFilmGate')

        # check for shots selected in the camera sequencer
        pb_shots = False
        shots = []
        if len(self.sel)>0 :
            for i in self.sel:
                if cmds.objectType(i) == 'shot':
                    shots.append(i)
                    pb_shots =  True
                    print "Shot pass"
                else:
                    pass

        if pb_shots == True:
            print "---shots"
            for i in shots:
                start_frame = cmds.getAttr("{}.startFrame".format(i))
                end_frame = cmds.getAttr("{}.endFrame".format(i))
                shot_cam = cmds.shot(i, cc = 1, q = 1)
                cmds.lookThru( shot_cam, cur_mp)
                cur_cam= cmds.modelEditor(cur_mp, q=1, av =1, cam=1)
                res_gate_attr= cmds.getAttr(cur_cam+'.filmFit')
                ovscn_attr=  cmds.getAttr(cur_cam+'.overscan')
                film_gate_attr=  cmds.getAttr(cur_cam+'.displayFilmGate')
                change = False
                while change == False:
                    try:
                        cmds.setAttr(cur_cam+'.filmFit', 3)
                        cmds.setAttr(cur_cam+'.overscan', 1)
                        cmds.setAttr(cur_cam+'.displayFilmGate', 0)
                        change = True

                    except:
                        con_list =  cmds.listConnections(cur_cam+ '.overscan')
                        cur_cam = con_list[0]

                f_name = self.in_path +'/'+ file_.split('.')[0]+'-'+i
                cmds.playblast(fmt= "qt", f= f_name, wh= [fr_width, fr_height], p= 100, cc= 1, v=1, c= "H.264", qlt=self.qlt, fo=1, st=start_frame, et=end_frame, os=os_opt)
                cmds.setAttr(cur_cam+'.filmFit', res_gate_attr)
                cmds.setAttr(cur_cam+'.overscan', ovscn_attr)
                cmds.setAttr(cur_cam+'.displayFilmGate', film_gate_attr)

        else:
            # check if the attributes are connected and set the camera and create the playblast
            change = False
            while change is False:
                try:
                    cmds.setAttr(cur_cam+'.filmFit', 3)
                    cmds.setAttr(cur_cam+'.overscan', 1)
                    cmds.setAttr(cur_cam+'.displayFilmGate', 0)
                    #print "---no error"                                            
                    change = True
                except:
                    con_list =  cmds.listConnections(cur_cam+ '.overscan')
                    cur_cam = con_list[0]
                    #sprint "---error"
            """             
            con_list =  cmds.listConnections(cur_cam+ '.overscan')
            con = False
            if con_list:
                con=True
                cur_cam = con_list[0]

            cmds.setAttr(cur_cam+'.filmFit', 3)
            cmds.setAttr(cur_cam+'.overscan', 1)
            cmds.setAttr(cur_cam+'.displayFilmGate', 0) """

            if 'linux' in os_sys:
                #print "\n --- Estas en Linux ---\n"
                user_name=subprocess.check_output("whoami").split("\n")[0]
                pb_name = file_.split('.')[0] + "temp"
                final_name = file_.split('.')[0]
                temp_name = '/home/{}/Desktop/{}'.format(user_name, pb_name)
                print temp_name
                temp_name2 = '/home/{}/Desktop/{}'.format(user_name, final_name)
                print temp_name2
                pb = cmds.playblast(fmt= "qt", f= temp_name, wh= [fr_width, fr_height], p= 100, cc= 1, v=0, c= "jpeg", qlt= self.qlt , fo=1, os=os_opt)
                ffmpeg_cmd = 'ffmpeg -y -i "{0}".mov'.format(pb)
                ffmpeg_cmd += ' -c:v libx264 "{0}.mov"'.format(temp_name2)
                subprocess.call(ffmpeg_cmd, shell= True)
                #os.remove(pb+".mov")
            else:
                #print "\n --- No estas en Linux ---\n"
                pb = cmds.playblast(fmt= "qt", f= f_name, wh= [fr_width, fr_height], p= 100, cc= 1, v=0, c= "h.264", qlt= self.qlt , fo=1, os=os_opt)

            #return camera to previous state
            cmds.setAttr(cur_cam+'.filmFit', res_gate_attr)
            cmds.setAttr(cur_cam+'.overscan', ovscn_attr)
            cmds.setAttr(cur_cam+'.displayFilmGate', film_gate_attr)
