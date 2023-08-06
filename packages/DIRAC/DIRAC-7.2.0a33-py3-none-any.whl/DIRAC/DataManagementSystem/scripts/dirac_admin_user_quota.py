#!/usr/bin/env python

from __future__ import absolute_import
from __future__ import division
from __future__ import print_function

__RCSID__ = "$Id$"

import DIRAC
from DIRAC.Core.Base import Script
from DIRAC.Core.Utilities.DIRACScript import DIRACScript


@DIRACScript()
def main():
  Script.setUsageMessage("""
  Show storage quotas for specified users or for all registered users if nobody is specified

  Usage:
    %s [user1 ...]
  """ % Script.scriptName)

  Script.parseCommandLine()
  users = Script.getPositionalArgs()

  from DIRAC import gLogger, gConfig

  if not users:
    res = gConfig.getSections('/Registry/Users')
    if not res['OK']:
      gLogger.error("Failed to retrieve user list from CS", res['Message'])
      DIRAC.exit(2)
    users = res['Value']

  gLogger.notice("-" * 30)
  gLogger.notice("%s|%s" % ('Username'.ljust(15), 'Quota (GB)'.rjust(15)))
  gLogger.notice("-" * 30)
  for user in sorted(users):
    quota = gConfig.getValue('/Registry/Users/%s/Quota' % user, 0)
    if not quota:
      quota = gConfig.getValue('/Registry/DefaultStorageQuota')
    gLogger.notice("%s|%s" % (user.ljust(15), str(quota).rjust(15)))
  gLogger.notice("-" * 30)
  DIRAC.exit(0)


if __name__ == "__main__":
  main()
