import os
from datetime import datetime, timedelta, tzinfo

import spack.config

logfile = ''


import sys
import time


class JST(tzinfo):
    def utcoffset(self, dt):
        return timedelta(hours=9)
    def tzname(self, dt):
        return "JST"
    def dst(self, dt):
        return timedelta(0)


def init_logfile(logid=None):
    """Set up the logfile: {logdir}/YYYYMMDD/spack[_{logid}].log
       {logdir} is specified in config.yaml; otherwise no log is output."""
    
    global logfile

    logdir = spack.config.get('config:logdir')

    if logdir and os.path.isdir(logdir):

        d = datetime.now(JST())
        date_dir = '%s/%s' % (logdir, d.strftime('%Y%m%d'))
        if not(os.path.exists(date_dir)):
            try:
                os.makedirs(date_dir)
                os.chmod(date_dir, 0o777)
            except OSError as e:
                if e.errno != 17:
                    return
                pass

        target_dir = '%s/%s' % (date_dir, logid)
        if not(os.path.exists(target_dir)):
            try:
                os.makedirs(target_dir)
                os.chmod(target_dir, 0o777)
            except OSError as e:
                if e.errno != 17:
                    return
                pass

        logfile = target_dir + '/' + 'spack_' + logid + '.log'

def output_specs(specs):
    """Output the specs to the specified logfile."""

    global logfile
    
    if logfile:
        try:
            with open(logfile, mode='a') as f:
                for spec in specs:
                    f.write(str(spec) + '\n')
            os.chmod(logfile, 0o644)
        except:
            pass
