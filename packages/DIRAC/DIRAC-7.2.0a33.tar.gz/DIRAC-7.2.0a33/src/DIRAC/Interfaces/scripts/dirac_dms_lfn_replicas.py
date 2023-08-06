#!/usr/bin/env python
########################################################################
# File :    dirac-admin-lfn-replicas
# Author :  Stuart Paterson
########################################################################
"""
  Obtain replica information from file catalogue client.
"""
from __future__ import print_function
from __future__ import absolute_import
from __future__ import division

__RCSID__ = "$Id$"

import DIRAC
from DIRAC.Core.Base import Script
from DIRAC.Core.Utilities.DIRACScript import DIRACScript


@DIRACScript()
def main():
  Script.registerSwitch('a', "All", "  Also show inactive replicas")
  Script.setUsageMessage('\n'.join([__doc__.split('\n')[1],
                                    'Usage:',
                                    '  %s [option|cfgfile] ... LFN ...' % Script.scriptName,
                                    'Arguments:',
                                    '  LFN:      Logical File Name or file containing LFNs']))
  Script.parseCommandLine(ignoreErrors=True)
  lfns = Script.getPositionalArgs()
  switches = Script.getUnprocessedSwitches()

  active = True
  for switch in switches:
    opt = switch[0].lower()
    if opt in ("a", "all"):
      active = False
  if len(lfns) < 1:
    Script.showHelp(exitCode=1)

  from DIRAC.Interfaces.API.Dirac import Dirac
  dirac = Dirac()
  exitCode = 0

  if len(lfns) == 1:
    try:
      with open(lfns[0], 'r') as f:
        lfns = f.read().splitlines()
    except BaseException:
      pass

  result = dirac.getReplicas(lfns, active=active, printOutput=True)
  if not result['OK']:
    print('ERROR: ', result['Message'])
    exitCode = 2

  DIRAC.exit(exitCode)


if __name__ == "__main__":
  main()
