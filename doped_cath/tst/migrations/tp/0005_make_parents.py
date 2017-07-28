
# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from tst.models import *
from django.db import models, migrations
from django.forms.models import model_to_dict
import sys
from copy import copy
def verify_root(node):
    return not( node.Class 
            or  node.arch
            or  node.topo
            or  node.homsf
            or  node.s35
            or  node.s60
            or  node.s95
            or  node.s100)

levels=[ None,
        'root',
        'Class',
        'arch',
        'topo',
        'homsf',
        's35',
        's60',
        's95',
        's100'];
def create_parent(apps, schema_editor):
    # classification = apps.get_model("tst", "classification")
    
    # print( len(classification.objects.all()),
        # file=sys.stdout )
    # for i in 

    for lv_id,level in list(enumerate(levels))[::-1]:
        if lv_id == 1:
            #### Stop if at root already
            # continue
            break
        plevel=levels[lv_id-1]
        print >>sys.stdout,plevel

        print >>sys.stdout, 'constructing %s' % (plevel);
        nodes = classification.objects.filter(level_id=lv_id);
        pnodes = classification.objects.filter(level_id=lv_id-1);
        imax = len(nodes);
        for (i,node) in enumerate(nodes):
            if not i % 50:
                print >>sys.stdout, 'Sweeping %d of %d %s' % (i,imax,level)
            if node.parent:
                continue #### skip this node if already with a parent
            else:
                
                #### Make a parent node inheriting the attributes
                pnode = copy(node)
                # if lv_id >=7:
                    # setattr( pnode,  level,  1)
                # elif level_id <7:
                setattr( pnode,  level,  0)
                pnode.level_id = lv_id-1  

                
                # q = pnodes.filter(**pnode.node_dict());
                if lv_id == 2:
                    #### Classes level directly stem from the root.
                    # q = pnodes.filter(**pnode.node_dict());
                    pass
                else:
                    # q = pnodes.filter(**{plevel:getattr(  pnode,  plevel)});
                    q = pnodes.filter( **pnode.node_dict() );

                if not q.exists():
                #### Create this putative node if not in the database                   
                    pnode.pk = None
                    pnode.id = None

                    if not pnode.level_id:
                        print >> sys.stdout,'\n Dropped to zero!!!'
                        print >> sys.stdout, str(node.__dict__)

                    pnode.save()
                                
                    ### Add newly created node to Parent Nodes List
                    newqset = classification.objects.filter(id=pnode.id)
                    pnodes = pnodes | newqset
                else:
                #### Link to existing node in the dataset.
                    pnode = q[0]
                if not i % 50: 
                    if node.Class != pnode.Class or node.arch != pnode.arch or node.topo != pnode.topo or node.homsf != pnode.homsf :
                        print >> sys.stdout,'assigning %s to %s' %(node.superfamily(),pnode.superfamily())


                #### In all casees, save the newly identified link
                node.parent_id = pnode.id;
                node.save()
                # node = pnode;

    #### Old slow algorithms: No Backprop.
    # nodes = classification.objects.all();
    # cnt = 0;
    # imax = len(nodes);
    
    # for (i,node) in enumerate(nodes):
    #     if not i % 50:
    #         print >>sys.stdout, '%d of %d' % (i,imax)
    #     while not node.level_id == 1:

    #         if node.parent:
    #             node = node.parent;
    #         else:
    #             pnode = copy(node)
    #             setattr( pnode,  levels[pnode.level_id],  None)
    #             pnode.level_id += -1
                
    #             # q = classification.objects.filter(level_id=pnode.level_id).filter(**pnode.node_dict());
    #             q = classification.objects.filter(**pnode.node_dict());
    #             if not q.exists():                                   
    #                 pnode.pk = None
    #                 pnode.id = None
    #                 # print >> sys.stdout, str(node.__dict__)
    #                 # node.classification_id = 1;
    #                 if not pnode.level_id:
    #                     print >> sys.stdout,'\n Dropped to zero!!!'
    #                     print >> sys.stdout, str(node.__dict__)

    #                 pnode.save()
    #                 # print >> sys.stdout,pnode
    #                 # classification.objects.update()
    #                 # cnt += 1
    #                 # if not cnt%20:
    #                     # print >> sys.stdout,cnt
    #                     # print >> sys.stdout, node.id

    #             else:
    #                 pnode = q[0]
    #                 # print >> sys.stdout, 'clashed node detected'

    #             # print >> sys.stdout, (pnode.homsf)      
    #             node.parent_id = pnode.id;
    #             node.save()
    #             node = pnode;


    msg = '\n MSG: found %d classification nodes'% len(classification.objects.all());
    print >> sys.stdout, msg

def do_nothing( apps, schema_editor):
    # msg = '\n MSG: found %d classification nodes'% len(classification.objects.all());
    msg = 'parents node are not rolled back'
    # print >> sys.stdout, msg

    # with open(sys.stdout,'a') as f:
        # f.write(len(classification.objects.all()))
# def load_classes_sql():
#     from coffeehouse.settings import PROJECT_DIR
#     import os
#     sql_statements = open(os.path.join(PROJECT_DIR,'tst/sql/load_classes.sql'), 'r').read()
#     return sql_statements

class Migration(migrations.Migration):

    dependencies = [('tst', '0004_load_classes'),]

    operations = [
        migrations.RunPython(create_parent,do_nothing),
    ]
