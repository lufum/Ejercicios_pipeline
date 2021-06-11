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

                        if ($cur_cam == "ubercam"){
                            float $uber_rotate = `getAttr ($cur_cam + ".rotateX")`;
                            float $uber_translate = `getAttr ($cur_cam + ".translateY")`;
                            string $cam_ls[]= `ls  -type "camera"`;
                            float $max_dif = 0.2;
                            for ($cam in $cam_ls) {
                                $cam_t= `listRelatives -p -f $cam`;
                                
                                if ($cam_t[0] != "|ubercam"){                           
                                    float $cam_rotate= `getAttr ($cam_t[0] + ".rotateX")`;
                                    float $cam_translate= `getAttr ($cam_t[0] + ".translateY")`;
                                    if ($cam_rotate < 0) { $cam_rotate = $cam_rotate*-1; }
                                    if ($cam_translate < 0) { $cam_translate = $cam_translate*-1; }
                                    if ($uber_rotate < 0) { $uber_rotate = $uber_rotate*-1; }
                                    if ($uber_translate < 0) { $uber_translate = $uber_translate*-1; }                                    
                                    float $dif_R = $uber_rotate - $cam_rotate; 
                                    if ($dif_R < 0) { $dif_R = $dif_R*-1; }
                                    float $dif_t = $uber_translate - $cam_translate;
                                    if ($dif_t < 0) { $dif_t = $dif_t*-1; }
                                    
                                    if ($dif_R <= $max_dif && $dif_t <= $max_dif ){
                                        string $name = $cam_t[0];
                                        string $tokenized[];
                                        tokenize $name "|" $tokenized;
                                        string $final_name = $tokenized[size($tokenized) - 1];
                                        setAttr -type "string" zshotmask_shape.topCenterText $final_name;
                                        break;
                                    }
                                }
                            }
                        }
                        else{
                            setAttr -type "string" zshotmask_shape.topCenterText $final_name;                   
                        }
                        
                        float $cam_rotate =  `getAttr ($cur_cam + ".rotateX")`;
                        float $cam_translate =   `getAttr ($cur_cam + ".translateY")`;
                        float $lens_info= `camera -q -fl $cur_cam`;
                        float $truc_lens= trunc($lens_info * pow(10, 2))/pow(10,2);
                        float $cam_angle= trunc($cam_rotate * pow(10, 2))/pow(10,2);
                        float $cam_height= trunc($cam_translate * pow(10, 2))/pow(10,2);
                        string $pad_angle= `python ("'%04.2f' % "+$cam_angle)`;
                        string $pad_height= `python ("'%05.2f' % "+$cam_height)`;
                        string $cam_info= "h: " + $pad_height + "  tilt: " + $cam_angle;
                        string $lens_mm= "lens: " + $truc_lens +" mm";

                        setAttr -type "string" zshotmask_shape.bottomLeftText $cam_info;
                        setAttr -type "string" zshotmask_shape.bottomCenterText $lens_mm;
                        setAttr -type "string" zshotmask_shape.camera cur_cam
                    """)
                        
    
    def updateDate(self):
        fecha= datetime.datetime.now()
        day= str(fecha.day)
        month= str(fecha.month).zfill(2)
        year= str(fecha.year).zfill(2)
        hour= str(fecha.hour).zfill(2)+':'+str(fecha.minute).zfill(2)
        fecha_disp= year+'/'+month+'/'+day+' - '+hour
        cmds.setAttr( "zshotmask_shape.topRightText", fecha_disp, type="string")