# -*- coding: utf-8 -*-
import datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models


class Migration(SchemaMigration):

    def forwards(self, orm):
        # Adding model 'Menu'
        db.create_table(u'gedeck_menu', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('name', self.gf('django.db.models.fields.CharField')(max_length=150)),
        ))
        db.send_create_signal(u'gedeck', ['Menu'])

        # Adding model 'MenuItem'
        db.create_table(u'gedeck_menuitem', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('active', self.gf('django.db.models.fields.BooleanField')(default=True)),
            ('type', self.gf('django.db.models.fields.CharField')(max_length=10)),
            ('title', self.gf('django.db.models.fields.CharField')(max_length=200)),
            ('description', self.gf('django.db.models.fields.TextField')(blank=True)),
            ('order', self.gf('django.db.models.fields.IntegerField')(default=0)),
            ('menu', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['gedeck.Menu'])),
        ))
        db.send_create_signal(u'gedeck', ['MenuItem'])

        # Adding model 'Guest'
        db.create_table(u'gedeck_guest', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('name', self.gf('django.db.models.fields.CharField')(max_length=150)),
            ('email', self.gf('django.db.models.fields.EmailField')(max_length=75)),
            ('rsvp', self.gf('django.db.models.fields.BooleanField')(default=False)),
            ('notify', self.gf('django.db.models.fields.BooleanField')(default=True)),
        ))
        db.send_create_signal(u'gedeck', ['Guest'])

        # Adding model 'Invitation'
        db.create_table(u'gedeck_invitation', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('created', self.gf('django.db.models.fields.DateTimeField')(auto_now_add=True, blank=True)),
            ('modified', self.gf('django.db.models.fields.DateTimeField')(auto_now=True, blank=True)),
            ('active', self.gf('django.db.models.fields.BooleanField')(default=True)),
            ('name', self.gf('django.db.models.fields.CharField')(max_length=200)),
            ('ref', self.gf('django.db.models.fields.CharField')(max_length=100)),
            ('menu', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['gedeck.Menu'], null=True, blank=True)),
        ))
        db.send_create_signal(u'gedeck', ['Invitation'])

        # Adding M2M table for field guests on 'Invitation'
        m2m_table_name = db.shorten_name(u'gedeck_invitation_guests')
        db.create_table(m2m_table_name, (
            ('id', models.AutoField(verbose_name='ID', primary_key=True, auto_created=True)),
            ('invitation', models.ForeignKey(orm[u'gedeck.invitation'], null=False)),
            ('guest', models.ForeignKey(orm[u'gedeck.guest'], null=False))
        ))
        db.create_unique(m2m_table_name, ['invitation_id', 'guest_id'])

        # Adding model 'GuestSelection'
        db.create_table(u'gedeck_guestselection', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('created', self.gf('django.db.models.fields.DateTimeField')(auto_now_add=True, blank=True)),
            ('modified', self.gf('django.db.models.fields.DateTimeField')(auto_now=True, blank=True)),
            ('guest', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['gedeck.Guest'])),
        ))
        db.send_create_signal(u'gedeck', ['GuestSelection'])

        # Adding M2M table for field items on 'GuestSelection'
        m2m_table_name = db.shorten_name(u'gedeck_guestselection_items')
        db.create_table(m2m_table_name, (
            ('id', models.AutoField(verbose_name='ID', primary_key=True, auto_created=True)),
            ('guestselection', models.ForeignKey(orm[u'gedeck.guestselection'], null=False)),
            ('menuitem', models.ForeignKey(orm[u'gedeck.menuitem'], null=False))
        ))
        db.create_unique(m2m_table_name, ['guestselection_id', 'menuitem_id'])


    def backwards(self, orm):
        # Deleting model 'Menu'
        db.delete_table(u'gedeck_menu')

        # Deleting model 'MenuItem'
        db.delete_table(u'gedeck_menuitem')

        # Deleting model 'Guest'
        db.delete_table(u'gedeck_guest')

        # Deleting model 'Invitation'
        db.delete_table(u'gedeck_invitation')

        # Removing M2M table for field guests on 'Invitation'
        db.delete_table(db.shorten_name(u'gedeck_invitation_guests'))

        # Deleting model 'GuestSelection'
        db.delete_table(u'gedeck_guestselection')

        # Removing M2M table for field items on 'GuestSelection'
        db.delete_table(db.shorten_name(u'gedeck_guestselection_items'))


    models = {
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
            'guests': ('django.db.models.fields.related.ManyToManyField', [], {'to': u"orm['gedeck.Guest']", 'symmetrical': 'False'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'menu': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['gedeck.Menu']", 'null': 'True', 'blank': 'True'}),
            'modified': ('django.db.models.fields.DateTimeField', [], {'auto_now': 'True', 'blank': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '200'}),
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