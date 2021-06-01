import maya.cmds as cmds
import os
import datetime


class cstm_playblast():
    
    def __init__(self):
        #self.create_playblast()
        full_path = cmds.file(q=True, sn=True)
        self.in_path = os.path.dirname(full_path)
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
        cmds.button( label='Set Path', command=(self.create_playblast))
        cmds.showWindow( self.win )
        
        self.sel = cmds.ls(sl = 1)


    def create_playblast(self, *args):
        
        self.in_path = cmds.textFieldGrp(self.path_dir, q=1, tx=1)
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

        #name of the file
        f_name = self.in_path +'/'+ file_.split('.')[0]
        print (f_name)

        #playblast dimensions
        fr_width = 1920
        fr_height = 1080
                
        #camera Attributes
        cur_mp = ""
        for mp in cmds.getPanel(type="modelPanel"):
            if cmds.modelEditor(mp, q=1, av=1):
                cur_mp = mp
        cur_cam= cmds.modelEditor(cur_mp, q=1, av =1, cam=1)
        cur_cam= cmds.modelEditor('modelPanel4', q=1, av =1, cam=1)
        res_gate_attr= cmds.getAttr(cur_cam+'.filmFit')
        ovscn_attr=  cmds.getAttr(cur_cam+'.overscan')
        film_gate_attr=  cmds.getAttr(cur_cam+'.displayFilmGate')

        #set the camera and create the playblast
        cmds.setAttr(cur_cam+'.filmFit', 3)
        cmds.setAttr(cur_cam+'.overscan', 1)
        cmds.setAttr(cur_cam+'.displayFilmGate', 0)
        
        #check for shots selected in the camera sequencer
        if len(self.sel)>0 :
            for i in self.sel:
                if cmds.objectType(i) == 'shot':
                    start_frame = cmds.getAttr("{}.startFrame".format(i))
                    end_frame = cmds.getAttr("{}.endFrame".format(i))
                    shot_cam = cmds.shot(i, cc = 1, q = 1)
                    cmds.lookThru( shot_cam, cur_mp)
                    cur_cam= cmds.modelEditor(cur_mp, q=1, av =1, cam=1)
                    cur_cam= cmds.modelEditor('modelPanel4', q=1, av =1, cam=1)
                    res_gate_attr= cmds.getAttr(cur_cam+'.filmFit')
                    ovscn_attr=  cmds.getAttr(cur_cam+'.overscan')
                    film_gate_attr=  cmds.getAttr(cur_cam+'.displayFilmGate')                                    
                    f_name = self.in_path +'/'+ file_.split('.')[0]+'-'+i
                    pb_=cmds.playblast(fmt= "qt", f= f_name, wh= [fr_width, fr_height], p= 100, cc= 1, v=1, c= "H.264", qlt=90, fo=1, st=start_frame, et=end_frame)
                    cmds.setAttr(cur_cam+'.filmFit', res_gate_attr)
                    cmds.setAttr(cur_cam+'.overscan', ovscn_attr)
                    cmds.setAttr(cur_cam+'.displayFilmGate', film_gate_attr)
                else:
                    pass
        else:
            pb_=cmds.playblast(fmt= "qt", f= f_name, wh= [fr_width, fr_height], p= 100, cc= 1, v=1, c= "H.264", qlt=90, fo=1)

            #return camera to previous state
            cmds.setAttr(cur_cam+'.filmFit', res_gate_attr)
            cmds.setAttr(cur_cam+'.overscan', ovscn_attr)
            cmds.setAttr(cur_cam+'.displayFilmGate', film_gate_attr)
