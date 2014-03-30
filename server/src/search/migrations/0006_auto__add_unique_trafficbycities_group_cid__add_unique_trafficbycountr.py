# -*- coding: utf-8 -*-
import datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models


class Migration(SchemaMigration):

    def forwards(self, orm):
        # Adding unique constraint on 'TrafficByCities', fields ['group', 'cid']
        db.create_unique(u'search_trafficbycities', ['group_id', 'cid'])

        # Adding unique constraint on 'TrafficByCountries', fields ['group', 'cid']
        db.create_unique(u'search_trafficbycountries', ['group_id', 'cid'])


    def backwards(self, orm):
        # Removing unique constraint on 'TrafficByCountries', fields ['group', 'cid']
        db.delete_unique(u'search_trafficbycountries', ['group_id', 'cid'])

        # Removing unique constraint on 'TrafficByCities', fields ['group', 'cid']
        db.delete_unique(u'search_trafficbycities', ['group_id', 'cid'])


    models = {
        u'search.audience': {
            'Meta': {'object_name': 'Audience'},
            'female': ('django.db.models.fields.FloatField', [], {'default': '0.0', 'db_index': 'True'}),
            'group': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['search.Group']"}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'male': ('django.db.models.fields.FloatField', [], {'default': '0.0', 'db_index': 'True'}),
            'over18': ('django.db.models.fields.FloatField', [], {'default': '0.0', 'db_index': 'True'}),
            'reach': ('django.db.models.fields.IntegerField', [], {'default': '0', 'db_index': 'True'}),
            'reach_subscribers': ('django.db.models.fields.IntegerField', [], {'default': '0', 'db_index': 'True'}),
            'views': ('django.db.models.fields.IntegerField', [], {'default': '0', 'db_index': 'True'}),
            'visitors': ('django.db.models.fields.IntegerField', [], {'default': '0', 'db_index': 'True'})
        },
        u'search.group': {
            'Meta': {'object_name': 'Group', 'db_table': "'groups'"},
            'city': ('django.db.models.fields.IntegerField', [], {'default': '0', 'db_index': 'True'}),
            'country': ('django.db.models.fields.IntegerField', [], {'default': '0', 'db_index': 'True'}),
            'gid': ('django.db.models.fields.IntegerField', [], {'primary_key': 'True'}),
            'is_closed': ('django.db.models.fields.IntegerField', [], {'default': '0', 'db_index': 'True'}),
            'members_count': ('django.db.models.fields.IntegerField', [], {'default': '0', 'db_index': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '512'}),
            'type': ('django.db.models.fields.IntegerField', [], {'db_index': 'True'})
        },
        u'search.trafficbycities': {
            'Meta': {'unique_together': "(('group', 'cid'),)", 'object_name': 'TrafficByCities'},
            'cid': ('django.db.models.fields.IntegerField', [], {'default': '0', 'db_index': 'True'}),
            'group': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['search.Group']"}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'visitors': ('django.db.models.fields.FloatField', [], {'default': '0.0', 'db_index': 'True'})
        },
        u'search.trafficbycountries': {
            'Meta': {'unique_together': "(('group', 'cid'),)", 'object_name': 'TrafficByCountries'},
            'cid': ('django.db.models.fields.IntegerField', [], {'default': '0', 'db_index': 'True'}),
            'group': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['search.Group']"}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'visitors': ('django.db.models.fields.FloatField', [], {'default': '0.0', 'db_index': 'True'})
        }
    }

    complete_apps = ['search']