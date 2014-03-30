# -*- coding: utf-8 -*-
import datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models


class Migration(SchemaMigration):

    def forwards(self, orm):
        # Adding model 'Group'
        db.create_table('groups', (
            ('gid', self.gf('django.db.models.fields.IntegerField')(primary_key=True)),
            ('type', self.gf('django.db.models.fields.IntegerField')(db_index=True)),
            ('members_count', self.gf('django.db.models.fields.IntegerField')(default=0, db_index=True)),
            ('is_closed', self.gf('django.db.models.fields.IntegerField')(default=0, db_index=True)),
            ('name', self.gf('django.db.models.fields.CharField')(max_length=512)),
            ('country', self.gf('django.db.models.fields.IntegerField')(default=0, db_index=True)),
            ('city', self.gf('django.db.models.fields.IntegerField')(default=0, db_index=True)),
        ))
        db.send_create_signal(u'search', ['Group'])


    def backwards(self, orm):
        # Deleting model 'Group'
        db.delete_table('groups')


    models = {
        u'search.group': {
            'Meta': {'object_name': 'Group', 'db_table': "'groups'"},
            'city': ('django.db.models.fields.IntegerField', [], {'default': '0', 'db_index': 'True'}),
            'country': ('django.db.models.fields.IntegerField', [], {'default': '0', 'db_index': 'True'}),
            'gid': ('django.db.models.fields.IntegerField', [], {'primary_key': 'True'}),
            'is_closed': ('django.db.models.fields.IntegerField', [], {'default': '0', 'db_index': 'True'}),
            'members_count': ('django.db.models.fields.IntegerField', [], {'default': '0', 'db_index': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '512'}),
            'type': ('django.db.models.fields.IntegerField', [], {'db_index': 'True'})
        }
    }

    complete_apps = ['search']
