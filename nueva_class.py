import sys
sys.path.append("E:/Programas/Shotgun/python-api-master")
from shotgun_api3 import shotgun
import pymel.core as pymel

class miclase():

    def __init__(self):

        self.nom_assets = []

    def centrar (self, ob_ls):
        
        for i in ob_ls:
            pymel.select(cl=1)
            pymel.select(i, add = 1)
            #print (pymel.selected())
            #centrar pivote
            pymel.xform (cp = 1)
            pymel.makeIdentity( apply=True, t=1, r=1, s=1)
            #Get the pivot position in the bounding box 
            pos1 = pymel.xform ( piv = 1, os = 1, q = 1 )
            #Get the position of the bounding Box in world spacve
            pos2 = pymel.xform ( bb = 1, ws = 1, q = 1 )
            #set the pivots to the base center of the bounding box
            pymel.xform (p = 1, ws = 1, piv = (pos1[0], pos2[1], pos1[2]))
            #move the object to the center of the scene
            pymel.move(pos1[0]*-1, pos1[1]*-1, pos1[2]*-1)
            #get the new bounding box position
            pos2 = pymel.xform ( bb = 1, ws = 1, q = 1 )
            #Freze transformations
            pymel.makeIdentity( apply=True, t=1, r=1, s=1)
            #move to the floor
            pymel.xform (t = (0,pos2[1]*-1,0))
            #Freze transformations  
            pymel.makeIdentity( apply=True, t=1, r=1, s=1)
            #Reset pivots
            pymel.xform ( p=1, ws=1, piv = (0,0,0))
            #clear history
            pymel.delete(ch = True)
            #pymel.select(cl=1)

    def get_assets (self):
        geo_=pymel.ls(geometry=1)
        obj_ls = []
        for i in geo_:
            par_= i.getAllParents()
            top_par = par_[len(par_)-1]
            if top_par not in obj_ls:
                obj_ls.append(top_par)
                
        for i in obj_ls:
            lista = []
            lista.append(i)
            pymel.select(i, add = 1)
            name = str(pymel.ls (sl = 1)[0])
            #print ("nombre= " + name)
            self.nom_assets.append(name)
            #print (self.nom_assets)
            self.centrar(lista)
            pymel.exportSelected("E:/Ollin VFX/Py files/Assets/" + name, force = 1, typ = "mayaAscii")
            pymel.select(cl=1)

    
    def create_assets (self):
        
        url_="https://lufum.shotgunstudio.com/"
        scr_name="ScriptTest2"
        scr_key="Aotkxdzdma7xmjc!heixirfsp"

        sg  = shotgun.Shotgun(url_, script_name=scr_name, 
                              api_key=scr_key, 
                              connect=True)

        for i in self.nom_assets:
            asset_name=i
            print (asset_name)

            data={"project"     : {"type": "Project",  "id": 70},
                #sg_sequence"   : {"type": "Sequence", "id": 41},
                "code"          : i,
                'description'   : "Asset creado por script",
                "shots"         : [{'id': 1208, 'type': 'Shot'}],
                "sequences"     : [{'id': 41, 'type': 'Sequence'}],  
                'sg_status_list': "ip"}

            new_asset=sg.create("Asset", data)
            print (new_asset)
""" """


