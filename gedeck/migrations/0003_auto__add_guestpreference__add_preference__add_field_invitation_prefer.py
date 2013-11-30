# -*- coding: utf-8 -*-
import datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models


class Migration(SchemaMigration):

    def forwards(self, orm):
        # Adding model 'GuestPreference'
        db.create_table(u'gedeck_guestpreference', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('created', self.gf('django.db.models.fields.DateTimeField')(auto_now_add=True, blank=True)),
            ('modified', self.gf('django.db.models.fields.DateTimeField')(auto_now=True, blank=True)),
            ('guest', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['gedeck.Guest'])),
            ('preference', self.gf('django.db.models.fields.TextField')()),
        ))
        db.send_create_signal(u'gedeck', ['GuestPreference'])

        # Adding model 'Preference'
        db.create_table(u'gedeck_preference', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('active', self.gf('django.db.models.fields.BooleanField')(default=True)),
            ('title', self.gf('django.db.models.fields.CharField')(max_length=200)),
            ('description', self.gf('django.db.models.fields.TextField')(blank=True)),
        ))
        db.send_create_signal(u'gedeck', ['Preference'])

        # Adding field 'Invitation.preference'
        db.add_column(u'gedeck_invitation', 'preference',
                      self.gf('django.db.models.fields.related.ForeignKey')(to=orm['gedeck.Preference'], null=True, blank=True),
                      keep_default=False)


        # Changing field 'Invitation.event'
        db.alter_column(u'gedeck_invitation', 'event_id', self.gf('django.db.models.fields.related.ForeignKey')(default=1, to=orm['gedeck.Event']))

    def backwards(self, orm):
        # Deleting model 'GuestPreference'
        db.delete_table(u'gedeck_guestpreference')

        # Deleting model 'Preference'
        db.delete_table(u'gedeck_preference')

        # Deleting field 'Invitation.preference'
        db.delete_column(u'gedeck_invitation', 'preference_id')


        # Changing field 'Invitation.event'
        db.alter_column(u'gedeck_invitation', 'event_id', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['gedeck.Event'], null=True))

    models = {
        u'gedeck.event': {
            'Meta': {'object_name': 'Event'},
            'active': ('django.db.models.fields.BooleanField', [], {'default': 'True'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '200'})
        },
        u'gedeck.guest': {
            'Meta': {'object_name': 'Guest'},
            'email': ('django.db.models.fields.EmailField', [], {'max_length': '75'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '150'}),
            'notify': ('django.db.models.fields.BooleanField', [], {'default': 'True'}),
            'rsvp': ('django.db.models.fields.BooleanField', [], {'default': 'False'})
        },
        u'gedeck.guestpreference': {
            'Meta': {'object_name': 'GuestPreference'},
            'created': ('django.db.models.fields.DateTimeField', [], {'auto_now_add': 'True', 'blank': 'True'}),
            'guest': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['gedeck.Guest']"}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'modified': ('django.db.models.fields.DateTimeField', [], {'auto_now': 'True', 'blank': 'True'}),
            'preference': ('django.db.models.fields.TextField', [], {})
        },
        u'gedeck.guestselection': {
            'Meta': {'object_name': 'GuestSelection'},
            'created': ('django.db.models.fields.DateTimeField', [], {'auto_now_add': 'True', 'blank': 'True'}),
            'guest': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['gedeck.Guest']"}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'items': ('django.db.models.fields.related.ManyToManyField', [], {'to': u"orm['gedeck.MenuItem']", 'symmetrical': 'False', 'blank': 'True'}),
            'modified': ('django.db.models.fields.DateTimeField', [], {'auto_now': 'True', 'blank': 'True'})
        },
        u'gedeck.invitation': {
            'Meta': {'object_name': 'Invitation'},
            'active': ('django.db.models.fields.BooleanField', [], {'default': 'True'}),
            'created': ('django.db.models.fields.DateTimeField', [], {'auto_now_add': 'True', 'blank': 'True'}),
            'event': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['gedeck.Event']"}),
            'guests': ('django.db.models.fields.related.ManyToManyField', [], {'to': u"orm['gedeck.Guest']", 'symmetrical': 'False', 'blank': 'True'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'menu': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['gedeck.Menu']", 'null': 'True', 'blank': 'True'}),
            'modified': ('django.db.models.fields.DateTimeField', [], {'auto_now': 'True', 'blank': 'True'}),
            'preference': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['gedeck.Preference']", 'null': 'True', 'blank': 'True'}),
            'ref': ('django.db.models.fields.CharField', [], {'max_length': '100'})
        },
        u'gedeck.menu': {
            'Meta': {'object_name': 'Menu'},
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '150'})
        },
        u'gedeck.menuitem': {
            'Meta': {'object_name': 'MenuItem'},
            'active': ('django.db.models.fields.BooleanField', [], {'default': 'True'}),
            'description': ('django.db.models.fields.TextField', [], {'blank': 'True'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'menu': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['gedeck.Menu']"}),
            'order': ('django.db.models.fields.IntegerField', [], {'default': '0'}),
            'title': ('django.db.models.fields.CharField', [], {'max_length': '200'}),
            'type': ('django.db.models.fields.CharField', [], {'max_length': '10'})
        },
        u'gedeck.preference': {
            'Meta': {'object_name': 'Preference'},
            'active': ('django.db.models.fields.BooleanField', [], {'default': 'True'}),
            'description': ('django.db.models.fields.TextField', [], {'blank': 'True'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'title': ('django.db.models.fields.CharField', [], {'max_length': '200'})
        }
    }

    complete_apps = ['gedeck']