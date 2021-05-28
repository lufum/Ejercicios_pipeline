import pymel.core as pm


class checks():

    def __init__(self):

        self.geo = []
        self.objs = pm.ls(geometry=1)
        for i in self.objs:
            par_ = i.getAllParents()
            top_par = par_[len(par_)-1]
            if top_par not in self.geo:
                self.geo.append(top_par)
        self.y_errors = []
        self.f_errors = []
        self.uv_errors = []

    def check_for_ngons(self):
        """
        Verifica que las geometrias no tengan caras con mas de 4 vertices
        """
        _geo = self.geo
        if _geo:
            for i in _geo:
                pm.select(i)
                pm.polySelectConstraint(m=3, t=8, sz=3)
                ngn = pm.selected()
                if ngn:
                    print 'hay Ngons en: ---' + str(i) + "---"
                    set_name = "set_"+str(i)
                    set = pm.ls(set_name)
                    if set:
                        print 'set existe'
                        print set_name
                        pm.sets(set_name, cl=True)
                        pm.sets(set_name, add=True)

                    else:
                        pm.sets(n=set_name, text='gCharacterSet')
                        print 'se creo un set con las caras con error'
                else:
                    print 'geo ok'
                pm.select(cl=1)
        else:
            print "no hay geo"
        pm.polySelectConstraint(mode=0, sz=0)

    def check_over_Y(self):
        objs = self.geo
        errors = self.y_errors
        for i in objs:
            pm.select(i, add=1)
            obj_bb = pm.xform(bb=1, ws=1, q=1)
            min_y = obj_bb[1]
            if min_y < 0:
                if i not in errors:
                    errors.append(i)
            pm.select(cl=1)
        if errors:
            print "Los siguientes elementos estan bajo Y\n"
            for i in errors:
                print ">>>", i

    def move_over_y(self):
        objs = self.y_errors
        for i in objs:
            pm.select(i, add=1)
            obj_bb = pm.xform(bb=1, ws=1, q=1)
            min_y = obj_bb[1]
            y_pos = i.translate.get()[1]
            pm.move(y_pos+min_y*-1, y=True)
            pm.select(cl=1)

    def check_freeze(self):
        objs = self.geo
        errors = self.f_errors
   
        for i in objs:
            trans_val = list(i.translate.get())
            rot_val = list(i.rotate.get())
            sc_val = list(i.scale.get())
            obj_vals = trans_val+rot_val+sc_val
            comp_vals = [0, 0, 0, 0, 0, 0, 1, 1, 1]
            for ov, cv in zip(obj_vals, comp_vals):
                if ov!=cv:
                    if i not in errors:
                        errors.append(i)
                        print '\n >>>', i, " necesita freezear trasnformaciones"
    
    def freeze_objs(self):
        objs = self.f_errors
        if objs:
            for i in objs:
                pm.makeIdentity(i, apply=True, t=1, r=1, s=1)
        else:
            print "no freeze errors"
    
    def check_uvs(self):
        objs = self.objs
        errors = self.uv_errors[]
        if objs:
            for i in objs:
                uv_set = pm.polyUVSet(i, q=1, auv=1)
                print '\n ', i, '\n'
                if uv_set:
                    print uv_set
                else:
                    errors.append[i]
                    print "no UV set"
            
