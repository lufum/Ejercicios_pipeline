import pymel.core as pm


def check_for_ngons():

    """
    verifica que las geometrias no tengan caras con mas de 4 vertices
    """

    _geo = pm.ls(type="mesh")
    if _geo:
        for i in _geo:
            pm.select(i)
            pm.polySelectConstraint(m=3, t=8, sz=3)
            ngn = pm.selected()
            if ngn:
                print 'hay Ngons en: ---' + str(i) + "---"
                set_name = "set_"+str(i)
                set = pm.ls(set_name)
                print set
                if set:
                    print 'set existe'
                    print set_name
                    pm.sets(set_name, cl=True)
                    pm.sets(set_name, add=True)

                else:
                    pm.sets(n=set_name, text='gCharacterSet')
                    print 'se creo un set con las caras con error'
            pm.select (cl=1)
    else:
        print "no hay _geo"
    pm.polySelectConstraint(mode=0, sz=0)
    
    
"""  
def check_for_ngons(_geo):
    mesh_list = _geo
    if mesh_list:
        ngns = []
        for i in mesh_list:
            pm.select(i)
            pm.polySelectConstraint(m=3, sz=3)
            ngn = pm.selected()
            if ngn:
                for i in ngn:
                    ngns.append(i)
    #            print (ngn, " tiene ngons")
            pm.select(cl=1)
    else:
        print("no mesh")
    if ngns:
        pm.select(ngns)
        print('>>>Hay Ngons<<<')
    pm.polySelectConstraint(mode=0, sz=0)


import pymel.core as pm
skCl = pm.ls(type="skinCluster")
pm.copySkinWeights( ss=skCl[0], ds=skCl[1], noMirror=True, sa = 'closestPoint')



for i in skCl:
    mesh=pm.skinCluster(i, q=True, geometry=True)
    vert = pm.selected()
    info=pm.skinPercent(i, vert, transform=None, query=True)
    print (info)



pm.skinCluster( "skinCluster1", e=True, selectInfluenceVerts='joint1_old',)
old_joints = pm.ls("*_old", type='joint')
new_joints = pm.ls("*_new", type='joint')
zipped = zip(old_joints, new_joints)
con0 = old_joints[0].mesh_listConnections(t="skinCluster")
con1 = new_joints[0].mesh_listConnections(t="skinCluster")
skCl0=con0[0]
skCl1 = con1[0]
print (skCl0)
print(skCl1)


for i in zipped:
    vert1 = pm.skinCluster(selectInfluenceVerts = 1, i[0],skCl0 )
    vert = pm.selected(fl = True)
    print vert
    pm.select(cl=1)


vert = pm.selected(fl = True)
print (vert[0])"""
