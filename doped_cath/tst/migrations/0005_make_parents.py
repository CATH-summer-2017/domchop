
# -*- coding: utf-8 -*-
from __future__ import unicode_literals

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

levels=['root',
        'Class',
        'arch',
        'topo',
        'homsf',
        's35',
        's60',
        's95',
        's100'];
def create_parent(apps, schema_editor):
    classification = apps.get_model("tst", "classification")
    
    # print( len(classification.objects.all()),
        # file=sys.stdout )
    nodes = classification.objects.all();
    cnt = 0;
    imax = len(nodes);
    for (i,node) in enumerate(nodes):
        if not i % 50:
            print >>sys.stdout, '%d of %d' % (i,imax)
        while not node.level_id == 1:
        # while not verify_root(node):

            if node.parent:
                node = node.parent;
            else:
                pnode = copy(node)
                setattr( pnode,  levels[pnode.level_id],  None)
                pnode.level_id += -1
                
                # q = classification.objects.filter(level_id=pnode.level_id).filter(**pnode.node_dict());
                q = classification.objects.filter(**pnode.node_dict());
                if not q.exists():                                   
                    pnode.pk = None
                    pnode.id = None
                    # print >> sys.stdout, str(node.__dict__)
                    # node.classification_id = 1;
                    if not pnode.level_id:
                        print >> sys.stdout,'\n Dropped to zero!!!'
                        print >> sys.stdout, str(node.__dict__)

                    pnode.save()
                    # print >> sys.stdout,pnode
                    # classification.objects.update()
                    # cnt += 1
                    # if not cnt%20:
                        # print >> sys.stdout,cnt
                        # print >> sys.stdout, node.id

                else:
                    pnode = q[0]
                    # print >> sys.stdout, 'clashed node detected'

                # print >> sys.stdout, (pnode.homsf)      
                node.parent_id = pnode.id;
                node.save()
                node = pnode;
                # pnode
                # pnode.classification_set.add(node)
                # node.save()

                #     node.classification_id = pnode.pk
                #     onode.save()  
                # if created:


                
                # classification.objects.create(
                    # )
                # node.
                # pass

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
