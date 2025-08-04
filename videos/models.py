# This is an auto-generated Django model module.
# You'll have to do the following manually to clean this up:
#   * Rearrange models' order
#   * Make sure each model has one field with primary_key=True
#   * Make sure each ForeignKey and OneToOneField has `on_delete` set to the desired behavior
#   * Remove `managed = False` lines if you wish to allow Django to create, modify, and delete the table
# Feel free to rename the models, but don't rename db_table values or field names.
from django.db import models

class Rols(models.Model):
    id_rol = models.AutoField(primary_key=True)
    roles = models.CharField(max_length=50, unique=True)

    class Meta:
        db_table = 'rols'

class Person(models.Model):
    id_persona = models.AutoField(primary_key=True)
    nombre = models.CharField(max_length=50)
    apellido = models.CharField(max_length=50)
    cedula = models.CharField(max_length=20)
    cargo = models.CharField(max_length=50)
    gerencia = models.CharField(max_length=50)
    
    
    class Meta:
        
        db_table = 'person'


class Users(models.Model):
    id = models.AutoField(primary_key=True)
    username = models.CharField(max_length=50, unique=True)
    password = models.CharField(max_length=100)
    person_id = models.ForeignKey('Person', models.DO_NOTHING, db_column='person_id')
    rol_id = models.ForeignKey(Rols, models.DO_NOTHING, db_column='rol_id')

    class Meta:
        
        db_table = 'users'



class Videos(models.Model):
    
    video_id = models.AutoField(db_column='video_id', primary_key=True)
    video_name = models.CharField(max_length=100)
    location = models.FileField(upload_to='video/') # This is the corrected line
    fecha = models.CharField(max_length=50) # Consider models.DateField or models.DateTimeField

    class Meta:
        db_table = 'video'