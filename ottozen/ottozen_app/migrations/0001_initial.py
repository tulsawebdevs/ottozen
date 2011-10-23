# encoding: utf-8
import datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models

class Migration(SchemaMigration):

    def forwards(self, orm):
        
        # Adding model 'Point'
        db.create_table('ottozen_app_point', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('name', self.gf('django.db.models.fields.CharField')(max_length=255, db_index=True)),
            ('user', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['auth.User'])),
            ('address', self.gf('django.db.models.fields.CharField')(max_length=255, blank=True)),
            ('latitude', self.gf('django.db.models.fields.DecimalField')(null=True, max_digits=13, decimal_places=8, blank=True)),
            ('longitude', self.gf('django.db.models.fields.DecimalField')(null=True, max_digits=13, decimal_places=8, blank=True)),
        ))
        db.send_create_signal('ottozen_app', ['Point'])

        # Adding model 'Route'
        db.create_table('ottozen_app_route', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('user', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['auth.User'])),
            ('start_time', self.gf('django.db.models.fields.TimeField')(null=True)),
        ))
        db.send_create_signal('ottozen_app', ['Route'])

        # Adding model 'RoutePoint'
        db.create_table('ottozen_app_routepoint', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('route', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['ottozen_app.Route'])),
            ('point', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['ottozen_app.Point'])),
            ('sequence', self.gf('django.db.models.fields.IntegerField')()),
        ))
        db.send_create_signal('ottozen_app', ['RoutePoint'])

        # Adding model 'Alert'
        db.create_table('ottozen_app_alert', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('user', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['auth.User'])),
            ('route', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['ottozen_app.Route'])),
            ('created', self.gf('django.db.models.fields.DateTimeField')(auto_now_add=True, blank=True)),
            ('text', self.gf('django.db.models.fields.CharField')(max_length=255)),
            ('sent', self.gf('django.db.models.fields.BooleanField')(default=False)),
        ))
        db.send_create_signal('ottozen_app', ['Alert'])

        # Adding model 'UserProfile'
        db.create_table('ottozen_app_userprofile', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('user', self.gf('django.db.models.fields.related.OneToOneField')(to=orm['auth.User'], unique=True)),
            ('mobile_num', self.gf('django.db.models.fields.CharField')(default='918.......', max_length=10)),
            ('email_confirmed', self.gf('django.db.models.fields.BooleanField')(default=False)),
            ('mobile_confirmed', self.gf('django.db.models.fields.BooleanField')(default=False)),
            ('ok_to_email', self.gf('django.db.models.fields.BooleanField')(default=False)),
        ))
        db.send_create_signal('ottozen_app', ['UserProfile'])


    def backwards(self, orm):
        
        # Deleting model 'Point'
        db.delete_table('ottozen_app_point')

        # Deleting model 'Route'
        db.delete_table('ottozen_app_route')

        # Deleting model 'RoutePoint'
        db.delete_table('ottozen_app_routepoint')

        # Deleting model 'Alert'
        db.delete_table('ottozen_app_alert')

        # Deleting model 'UserProfile'
        db.delete_table('ottozen_app_userprofile')


    models = {
        'auth.group': {
            'Meta': {'object_name': 'Group'},
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'unique': 'True', 'max_length': '80'}),
            'permissions': ('django.db.models.fields.related.ManyToManyField', [], {'to': "orm['auth.Permission']", 'symmetrical': 'False', 'blank': 'True'})
        },
        'auth.permission': {
            'Meta': {'ordering': "('content_type__app_label', 'content_type__model', 'codename')", 'unique_together': "(('content_type', 'codename'),)", 'object_name': 'Permission'},
            'codename': ('django.db.models.fields.CharField', [], {'max_length': '100'}),
            'content_type': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['contenttypes.ContentType']"}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '50'})
        },
        'auth.user': {
            'Meta': {'object_name': 'User'},
            'date_joined': ('django.db.models.fields.DateTimeField', [], {'default': 'datetime.datetime.now'}),
            'email': ('django.db.models.fields.EmailField', [], {'max_length': '75', 'blank': 'True'}),
            'first_name': ('django.db.models.fields.CharField', [], {'max_length': '30', 'blank': 'True'}),
            'groups': ('django.db.models.fields.related.ManyToManyField', [], {'to': "orm['auth.Group']", 'symmetrical': 'False', 'blank': 'True'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'is_active': ('django.db.models.fields.BooleanField', [], {'default': 'True'}),
            'is_staff': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'is_superuser': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'last_login': ('django.db.models.fields.DateTimeField', [], {'default': 'datetime.datetime.now'}),
            'last_name': ('django.db.models.fields.CharField', [], {'max_length': '30', 'blank': 'True'}),
            'password': ('django.db.models.fields.CharField', [], {'max_length': '128'}),
            'user_permissions': ('django.db.models.fields.related.ManyToManyField', [], {'to': "orm['auth.Permission']", 'symmetrical': 'False', 'blank': 'True'}),
            'username': ('django.db.models.fields.CharField', [], {'unique': 'True', 'max_length': '30'})
        },
        'contenttypes.contenttype': {
            'Meta': {'ordering': "('name',)", 'unique_together': "(('app_label', 'model'),)", 'object_name': 'ContentType', 'db_table': "'django_content_type'"},
            'app_label': ('django.db.models.fields.CharField', [], {'max_length': '100'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'model': ('django.db.models.fields.CharField', [], {'max_length': '100'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '100'})
        },
        'ottozen_app.alert': {
            'Meta': {'object_name': 'Alert'},
            'created': ('django.db.models.fields.DateTimeField', [], {'auto_now_add': 'True', 'blank': 'True'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'route': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['ottozen_app.Route']"}),
            'sent': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'text': ('django.db.models.fields.CharField', [], {'max_length': '255'}),
            'user': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['auth.User']"})
        },
        'ottozen_app.point': {
            'Meta': {'object_name': 'Point'},
            'address': ('django.db.models.fields.CharField', [], {'max_length': '255', 'blank': 'True'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'latitude': ('django.db.models.fields.DecimalField', [], {'null': 'True', 'max_digits': '13', 'decimal_places': '8', 'blank': 'True'}),
            'longitude': ('django.db.models.fields.DecimalField', [], {'null': 'True', 'max_digits': '13', 'decimal_places': '8', 'blank': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '255', 'db_index': 'True'}),
            'user': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['auth.User']"})
        },
        'ottozen_app.route': {
            'Meta': {'object_name': 'Route'},
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'start_time': ('django.db.models.fields.TimeField', [], {'null': 'True'}),
            'user': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['auth.User']"}),
            'waypoints': ('django.db.models.fields.related.ManyToManyField', [], {'to': "orm['ottozen_app.Point']", 'through': "orm['ottozen_app.RoutePoint']", 'symmetrical': 'False'})
        },
        'ottozen_app.routepoint': {
            'Meta': {'object_name': 'RoutePoint'},
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'point': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['ottozen_app.Point']"}),
            'route': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['ottozen_app.Route']"}),
            'sequence': ('django.db.models.fields.IntegerField', [], {})
        },
        'ottozen_app.userprofile': {
            'Meta': {'object_name': 'UserProfile'},
            'email_confirmed': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'mobile_confirmed': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'mobile_num': ('django.db.models.fields.CharField', [], {'default': "'918.......'", 'max_length': '10'}),
            'ok_to_email': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'user': ('django.db.models.fields.related.OneToOneField', [], {'to': "orm['auth.User']", 'unique': 'True'})
        }
    }

    complete_apps = ['ottozen_app']
