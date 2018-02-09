import os
import sys
import json
import time
import boto3
import configparser

from datetime import date, datetime
from collections import namedtuple

EBS_conf    = namedtuple('EBS', 'iops size type')
RDS_conf    = namedtuple('RDS', 'name iops size iclass stype version')
Aurora_conf = namedtuple('Aurora', 'name iclass stype')
PgSQL_conf  = namedtuple('PgSQL', 'dsn')
Citus_conf  = namedtuple('Citus', 'dsn')

class Setup():
    def __init__(self, filename):
        conf = configparser.ConfigParser()
        conf.read(filename)

        self.region  = conf.get('aws', 'REGION')
        self.az      = conf.get('aws', 'AZ')
        self.vpc     = conf.get('aws', 'VPC')
        self.subnet  = conf.get('aws', 'SUBNET')
        self.sg      = conf.get('aws', 'SG')
        self.ami     = conf.get('aws', 'AMI')
        self.keyname = conf.get('aws', 'KeyName')

        self.itype   = conf.get('loader', 'instance')

        self.ebs = EBS_conf(
            iops = conf.getint('ebs', 'iops'),
            size = conf.getint('ebs', 'size'),
            type = conf.get('ebs', 'type')
        )

        self.rds = RDS_conf(
            name    = conf.get('rds', 'name'),
            iops    = conf.getint('rds', 'iops'),
            size    = conf.getint('rds', 'size'),
            iclass  = conf.get('rds', 'class'),
            stype   = conf.get('rds', 'stype'),
            version = conf.get('rds', 'pgversion')
        )

        self.aurora = Aurora_conf(
            name    = conf.get('rds', 'name'),
            iclass  = conf.get('rds', 'class'),
            stype   = conf.get('rds', 'stype')
        )

        self.pgsql = PgSQL_conf(dsn = conf.get('pgsql', 'dsn'))
        self.citus = Citus_conf(dsn = conf.get('citus', 'dsn'))