# -*- coding: utf-8 -*-
import datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models


class Migration(SchemaMigration):

    def forwards(self, orm):
        # Adding model 'Activity'
        db.create_table(u'gedeck_activity', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('name', self.gf('django.db.models.fields.CharField')(max_length=200)),
            ('required', self.gf('django.db.models.fields.BooleanField')(default=True)),
        ))
        db.send_create_signal(u'gedeck', ['Activity'])

        # Adding model 'GuestActivityRsvp'
        db.create_table(u'gedeck_guestactivityrsvp', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('created', self.gf('django.db.models.fields.DateTimeField')(auto_now_add=True, blank=True)),
            ('modified', self.gf('django.db.models.fields.DateTimeField')(auto_now=True, blank=True)),
            ('guest', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['gedeck.Guest'])),
            ('activity', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['gedeck.Activity'])),
        ))
        db.send_create_signal(u'gedeck', ['GuestActivityRsvp'])

        # Adding M2M table for field activities on 'Event'
        m2m_table_name = db.shorten_name(u'gedeck_event_activities')
        db.create_table(m2m_table_name, (
            ('id', models.AutoField(verbose_name='ID', primary_key=True, auto_created=True)),
            ('event', models.ForeignKey(orm[u'gedeck.event'], null=False)),
            ('activity', models.ForeignKey(orm[u'gedeck.activity'], null=False))
        ))
        db.create_unique(m2m_table_name, ['event_id', 'activity_id'])

        # Adding field 'Invitation.lead'
        db.add_column(u'gedeck_invitation', 'lead',
                      self.gf('django.db.models.fields.TextField')(default='', blank=True, null=True),
                      keep_default=False)

        # Adding field 'Invitation.lead_on_complete'
        db.add_column(u'gedeck_invitation', 'lead_on_complete',
                      self.gf('django.db.models.fields.TextField')(default='', blank=True, null=True),
                      keep_default=False)

        # Adding field 'GuestSelection.event'
        db.add_column(u'gedeck_guestselection', 'event',
                      self.gf('django.db.models.fields.related.ForeignKey')(default=1, to=orm['gedeck.Event']),
                      keep_default=False)

        # Adding field 'GuestPreference.event'
        db.add_column(u'gedeck_guestpreference', 'event',
                      self.gf('django.db.models.fields.related.ForeignKey')(default=1, to=orm['gedeck.Event']),
                      keep_default=False)

        # Adding field 'Preference.required'
        db.add_column(u'gedeck_preference', 'required',
                      self.gf('django.db.models.fields.BooleanField')(default=True),
                      keep_default=False)


    def backwards(self, orm):
        # Deleting model 'Activity'
        db.delete_table(u'gedeck_activity')

        # Deleting model 'GuestActivityRsvp'
        db.delete_table(u'gedeck_guestactivityrsvp')

        # Removing M2M table for field activities on 'Event'
        db.delete_table(db.shorten_name(u'gedeck_event_activities'))

        # Deleting field 'Invitation.lead'
        db.delete_column(u'gedeck_invitation', 'lead')

        # Deleting field 'Invitation.lead_on_complete'
        db.delete_column(u'gedeck_invitation', 'lead_on_complete')

        # Deleting field 'GuestSelection.event'
        db.delete_column(u'gedeck_guestselection', 'event_id')

        # Deleting field 'GuestPreference.event'
        db.delete_column(u'gedeck_guestpreference', 'event_id')

        # Deleting field 'Preference.required'
        db.delete_column(u'gedeck_preference', 'required')


    models = {
        u'gedeck.activity': {
            'Meta': {'object_name': 'Activity'},
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '200'}),
            'required': ('django.db.models.fields.BooleanField', [], {'default': 'True'})
        },
        u'gedeck.event': {
            'Meta': {'object_name': 'Event'},
            'active': ('django.db.models.fields.BooleanField', [], {'default': 'True'}),
            'activities': ('django.db.models.fields.related.ManyToManyField', [], {'to': u"orm['gedeck.Activity']", 'symmetrical': 'False'}),
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
        u'gedeck.guestactivityrsvp': {
            'Meta': {'object_name': 'GuestActivityRsvp'},
            'activity': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['gedeck.Activity']"}),
            'created': ('django.db.models.fields.DateTimeField', [], {'auto_now_add': 'True', 'blank': 'True'}),
            'guest': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['gedeck.Guest']"}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'modified': ('django.db.models.fields.DateTimeField', [], {'auto_now': 'True', 'blank': 'True'})
        },
        u'gedeck.guestpreference': {
            'Meta': {'object_name': 'GuestPreference'},
            'created': ('django.db.models.fields.DateTimeField', [], {'auto_now_add': 'True', 'blank': 'True'}),
            'event': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['gedeck.Event']"}),
            'guest': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['gedeck.Guest']"}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'modified': ('django.db.models.fields.DateTimeField', [], {'auto_now': 'True', 'blank': 'True'}),
            'preference': ('django.db.models.fields.TextField', [], {})
        },
        u'gedeck.guestselection': {
            'Meta': {'object_name': 'GuestSelection'},
            'created': ('django.db.models.fields.DateTimeField', [], {'auto_now_add': 'True', 'blank': 'True'}),
            'event': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['gedeck.Event']"}),
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
            'lead': ('django.db.models.fields.TextField', [], {'blank': 'True'}),
            'lead_on_complete': ('django.db.models.fields.TextField', [], {'blank': 'True'}),
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
            'required': ('django.db.models.fields.BooleanField', [], {'default': 'True'}),
            'title': ('django.db.models.fields.CharField', [], {'max_length': '200'})
        }
    }

    complete_apps = ['gedeck']