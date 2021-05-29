import os
import datetime
import maya.cmds as cmds
import zshotmask_ui

class previsMask():
    def __init__(self):
        self.crateMask()
        self.updateDate()
    
    def crateMask(self):
        ZShotMask=zshotmask_ui.ZShotMask()
        ZShotMask.create_mask()
        cur_mp = ""
        for mp in cmds.getPanel(type="modelPanel"):
            if cmds.modelEditor(mp, q=1, av=1):
                cur_mp = mp
                break

        cur_cam= cmds.modelEditor(cur_mp, q=1, av =1, cam=1)
        cur_cam= cmds.modelEditor(cur_mp, q=1, av =1, cam=1)
        if cmds.objectType(cur_cam) != "transform":
            par = cmds.listRelatives(cur_cam, p=1, f=1)
            cur_cam = par[0]
        
        file_=os.path.basename(cmds.file(q=True, sn=True))
        
        #Info
        cmds.setAttr( "zshotmask_shape.camera", cur_cam, type="string")
        cmds.setAttr( "zshotmask_shape.topLeftText", file_, type="string")
        
        #General Settings
        cmds.setAttr( "zshotmask_shape.borderScale", .9)
        cmds.setAttr( "zshotmask_shape.fontScale", .6)
        cmds.setAttr( "zshotmask_shape.borderAlpha", .15)
        cmds.setAttr( "zshotmask_shape.fontName", "Source Code Pro Light", type = "string")
        cmds.setAttr( "zshotmask_shape.counterPadding", 5)
        
        #date
        try:
            cmds.scriptJob(kill=job_id )
        except:
            pass
            
        job_id = cmds.scriptJob(event= ["timeChanged", "previs.updateDate()"])
            
        #Expression
        exp=cmds.objExists("mask_exp")
        if exp == True:
            cmds.delete("mask_exp")
    
        cmds.expression(n= "mask_exp", ae=1, s=
                        
                        """
                        string $cur_mp;
                        for ($mp in `getPanel -typ "modelPanel"`){
                            if (`modelEditor -q -av $mp`){
                                $cur_mp = $mp;
                            }
                        }
                        string $cur_cam= `modelEditor -q -cam $cur_mp`; 
                        if (`objectType $cur_cam` != "transform"){
                            string $par [] = `listRelatives -p -f $cur_cam `;
                            $cur_cam = $par[0];
												
                        }
						string $name = $cur_cam;
						string $tokenized[];
						tokenize $name "|" $tokenized;
						string $final_name = $tokenized[size($tokenized) - 1];						
                        float $cam_rotate =  `getAttr ($cur_cam + ".rotateX")`;
                        float $cam_translate =   `getAttr ($cur_cam + ".rotateX")`;
                        float $lens_info= `camera -q -fl $cur_cam`;
                        float $truc_lens= trunc($lens_info * pow(10, 2))/pow(10,2);
                        float $cam_angle= trunc($cam_rotate * pow(10, 2))/pow(10,2);
                        float $cam_height= trunc($cam_translate * pow(10, 2))/pow(10,2);
                        string $pad_angle= `python ("'%04d' % "+$cam_angle)`;
                        string $pad_height= `python ("'%05d' % "+$cam_height)`;
                        string $cam_info= "h: " + $pad_height + "  tilt: " + $cam_angle;
                        string $lens_mm= "lens: " + $truc_lens +" mm";
						
                    
                        setAttr -type "string" zshotmask_shape.topCenterText $final_name;
                        setAttr -type "string" zshotmask_shape.bottomLeftText $cam_info;
                        setAttr -type "string" zshotmask_shape.bottomCenterText $lens_mm;
                        setAttr -type "string" zshotmask_shape.camera cur_cam""")
    
    def updateDate(self):
        fecha= datetime.datetime.now()
        day= str(fecha.day)
        month= str(fecha.month).zfill(2)
        year= str(fecha.year).zfill(2)
        hour= str(fecha.hour).zfill(2)+':'+str(fecha.minute).zfill(2)
        fecha_disp= year+'/'+month+'/'+day+' - '+hour
        cmds.setAttr( "zshotmask_shape.topRightText", fecha_disp, type="string")
