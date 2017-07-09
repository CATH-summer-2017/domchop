
# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
import sys

def verify_root(node):
    return not( node.Class 
            or  node.arch
            or  node.topo
            or  node.homsf
            or  node.s35
            or  node.s60
            or  node.s95
            or  node.s100)

levels=[None,
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
    for node in nodes:
        while node.level_id is not 0:
        # while not verify_root(node):
            if not node.parent:
                old_pk = node.pk
                node.pk = None
                setattr(  node,  levels[node.level_id],  None)
                node.level_id += -1
                node.save()
                onode = classification.objects.get(id=old_pk)
                onode.classification_id = node.pk
                onode.save()
            else:
                node = node.parent;
                # classification.objects.create(
                    # )
                # node.
                # pass

    msg = '\n MSG: found %d classification nodes'% len(classification.objects.all());
    print >> sys.stdout, msg

def do_nothing():
    msg = '\n MSG: found %d classification nodes'% len(classification.objects.all());
    print >> sys.stdout, msg

    # with open(sys.stdout,'a') as f:
        # f.write(len(classification.objects.all()))
# def load_classes_sql():
#     from coffeehouse.settings import PROJECT_DIR
#     import os
#     sql_statements = open(os.path.join(PROJECT_DIR,'tst/sql/load_classes.sql'), 'r').read()
#     return sql_statements

class Migration(migrations.Migration):

    dependencies = [('tst', '0003_load_classes'),]

    operations = [
        migrations.RunPython(create_parent,do_nothing),
    ]
