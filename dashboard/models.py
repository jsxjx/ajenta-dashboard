from __future__ import unicode_literals

from django.db import models


class Call(models.Model):
    callid = models.AutoField(db_column='CallID', primary_key=True)
    uniquecallid = models.CharField(db_column='UniqueCallID', max_length=20)
    conferencename = models.CharField(db_column='ConferenceName', max_length=200)
    tenantname = models.CharField(db_column='TenantName', max_length=128)
    conferencetype = models.CharField(db_column='ConferenceType', max_length=2)
    endpointtype = models.CharField(db_column='EndpointType', max_length=1)
    callerid = models.CharField(db_column='CallerID', max_length=200)
    callername = models.CharField(db_column='CallerName', max_length=200, blank=True, null=True)
    jointime = models.DateTimeField(db_column='JoinTime')
    leavetime = models.DateTimeField(db_column='LeaveTime', blank=True, null=True)
    callstate = models.CharField(db_column='CallState', max_length=80)
    direction = models.CharField(db_column='Direction', max_length=1)
    routerid = models.CharField(db_column='RouterID', max_length=128, blank=True, null=True)
    gwid = models.CharField(db_column='GWID', max_length=40, blank=True, null=True)
    gwprefix = models.CharField(db_column='GWPrefix', max_length=20, blank=True, null=True)
    referencenumber = models.CharField(db_column='ReferenceNumber', max_length=64, blank=True, null=True)
    applicationname = models.CharField(db_column='ApplicationName', max_length=24, blank=True, null=True)
    applicationversion = models.CharField(db_column='ApplicationVersion', max_length=32, blank=True, null=True)
    applicationos = models.CharField(db_column='ApplicationOs', max_length=24, blank=True, null=True)
    devicemodel = models.CharField(db_column='DeviceModel', max_length=50, blank=True, null=True)
    endpointpublicipaddress = models.CharField(db_column='EndpointPublicIPAddress', max_length=48)
    callcompletioncode = models.CharField(db_column='CallCompletionCode', max_length=1)
    extension = models.CharField(db_column='Extension', max_length=64, blank=True, null=True)
    endpointguid = models.CharField(db_column='EndpointGUID', max_length=64)
    accesstype = models.CharField(db_column='AccessType', max_length=1)
    roomtype = models.CharField(db_column='RoomType', max_length=1)
    roomowner = models.CharField(db_column='RoomOwner', max_length=40)

    class Meta:
        managed = True
        db_table = 'ConferenceCall2'
