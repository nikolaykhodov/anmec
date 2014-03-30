# -*- coding: utf-8 -*-
import datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models


class Migration(SchemaMigration):

    def forwards(self, orm):
        # Deleting model 'CountryStat'
        db.delete_table(u'search_countrystat')

        # Deleting model 'BasicStat'
        db.delete_table(u'search_basicstat')

        # Deleting model 'CityStat'
        db.delete_table(u'search_citystat')

        # Adding model 'TrafficByCities'
        db.create_table(u'search_trafficbycities', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('gid', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['search.Group'])),
            ('cid', self.gf('django.db.models.fields.IntegerField')(default=0, db_index=True)),
            ('visitors', self.gf('django.db.models.fields.FloatField')(default=0.0, db_index=True)),
        ))
        db.send_create_signal(u'search', ['TrafficByCities'])

        # Adding model 'Audience'
        db.create_table(u'search_audience', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('gid', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['search.Group'])),
            ('reach', self.gf('django.db.models.fields.IntegerField')(default=0, db_index=True)),
            ('reach_subscribers', self.gf('django.db.models.fields.IntegerField')(default=0, db_index=True)),
            ('views', self.gf('django.db.models.fields.IntegerField')(default=0, db_index=True)),
            ('visitors', self.gf('django.db.models.fields.IntegerField')(default=0, db_index=True)),
            ('female', self.gf('django.db.models.fields.FloatField')(default=0.0, db_index=True)),
            ('male', self.gf('django.db.models.fields.FloatField')(default=0.0, db_index=True)),
            ('over18', self.gf('django.db.models.fields.FloatField')(default=0.0, db_index=True)),
        ))
        db.send_create_signal(u'search', ['Audience'])

        # Adding model 'TrafficByCountries'
        db.create_table(u'search_trafficbycountries', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('gid', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['search.Group'])),
            ('cid', self.gf('django.db.models.fields.IntegerField')(default=0, db_index=True)),
            ('visitors', self.gf('django.db.models.fields.FloatField')(default=0.0, db_index=True)),
        ))
        db.send_create_signal(u'search', ['TrafficByCountries'])


    def backwards(self, orm):
        # Adding model 'CountryStat'
        db.create_table(u'search_countrystat', (
            ('gid', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['search.Group'])),
            ('visitors', self.gf('django.db.models.fields.FloatField')(default=0.0, db_index=True)),
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('cid', self.gf('django.db.models.fields.IntegerField')(default=0, db_index=True)),
        ))
        db.send_create_signal(u'search', ['CountryStat'])

        # Adding model 'BasicStat'
        db.create_table(u'search_basicstat', (
            ('visitors', self.gf('django.db.models.fields.IntegerField')(default=0, db_index=True)),
            ('female', self.gf('django.db.models.fields.FloatField')(default=0.0, db_index=True)),
            ('views', self.gf('django.db.models.fields.IntegerField')(default=0, db_index=True)),
            ('reach_subscribers', self.gf('django.db.models.fields.IntegerField')(default=0, db_index=True)),
            ('gid', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['search.Group'])),
            ('male', self.gf('django.db.models.fields.FloatField')(default=0.0, db_index=True)),
            ('reach', self.gf('django.db.models.fields.IntegerField')(default=0, db_index=True)),
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('over18', self.gf('django.db.models.fields.FloatField')(default=0.0, db_index=True)),
        ))
        db.send_create_signal(u'search', ['BasicStat'])

        # Adding model 'CityStat'
        db.create_table(u'search_citystat', (
            ('gid', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['search.Group'])),
            ('visitors', self.gf('django.db.models.fields.FloatField')(default=0.0, db_index=True)),
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('cid', self.gf('django.db.models.fields.IntegerField')(default=0, db_index=True)),
        ))
        db.send_create_signal(u'search', ['CityStat'])

        # Deleting model 'TrafficByCities'
        db.delete_table(u'search_trafficbycities')

        # Deleting model 'Audience'
        db.delete_table(u'search_audience')

        # Deleting model 'TrafficByCountries'
        db.delete_table(u'search_trafficbycountries')


    models = {
        u'search.audience': {
            'Meta': {'object_name': 'Audience'},
            'female': ('django.db.models.fields.FloatField', [], {'default': '0.0', 'db_index': 'True'}),
            'gid': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['search.Group']"}),
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
            'Meta': {'object_name': 'TrafficByCities'},
            'cid': ('django.db.models.fields.IntegerField', [], {'default': '0', 'db_index': 'True'}),
            'gid': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['search.Group']"}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'visitors': ('django.db.models.fields.FloatField', [], {'default': '0.0', 'db_index': 'True'})
        },
        u'search.trafficbycountries': {
            'Meta': {'object_name': 'TrafficByCountries'},
            'cid': ('django.db.models.fields.IntegerField', [], {'default': '0', 'db_index': 'True'}),
            'gid': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['search.Group']"}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'visitors': ('django.db.models.fields.FloatField', [], {'default': '0.0', 'db_index': 'True'})
        }
    }

    complete_apps = ['search']