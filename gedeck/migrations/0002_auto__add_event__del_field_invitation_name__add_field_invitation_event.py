# -*- coding: utf-8 -*-
import datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models


class Migration(SchemaMigration):

    def forwards(self, orm):
        # Adding model 'Event'
        db.create_table(u'gedeck_event', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('active', self.gf('django.db.models.fields.BooleanField')(default=True)),
            ('name', self.gf('django.db.models.fields.CharField')(max_length=200)),
        ))
        db.send_create_signal(u'gedeck', ['Event'])

        # Deleting field 'Invitation.name'
        db.delete_column(u'gedeck_invitation', 'name')

        # Adding field 'Invitation.event'
        db.add_column(u'gedeck_invitation', 'event',
                      self.gf('django.db.models.fields.related.ForeignKey')(to=orm['gedeck.Event'], null=True, blank=True),
                      keep_default=False)


    def backwards(self, orm):
        # Deleting model 'Event'
        db.delete_table(u'gedeck_event')


        # User chose to not deal with backwards NULL issues for 'Invitation.name'
        raise RuntimeError("Cannot reverse this migration. 'Invitation.name' and its values cannot be restored.")
        # Deleting field 'Invitation.event'
        db.delete_column(u'gedeck_invitation', 'event_id')


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
            'event': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['gedeck.Event']", 'null': 'True', 'blank': 'True'}),
            'guests': ('django.db.models.fields.related.ManyToManyField', [], {'to': u"orm['gedeck.Guest']", 'symmetrical': 'False', 'blank': 'True'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'menu': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['gedeck.Menu']", 'null': 'True', 'blank': 'True'}),
            'modified': ('django.db.models.fields.DateTimeField', [], {'auto_now': 'True', 'blank': 'True'}),
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
        }
    }

    complete_apps = ['gedeck']