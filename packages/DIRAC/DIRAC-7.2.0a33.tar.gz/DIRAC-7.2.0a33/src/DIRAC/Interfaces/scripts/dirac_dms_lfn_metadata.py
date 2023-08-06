#!/usr/bin/env python
########################################################################
# File :    dirac-admin-lfn-metadata
# Author :  Stuart Paterson
########################################################################
"""
  Obtain replica metadata from file catalogue client.
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
  Script.setUsageMessage('\n'.join([__doc__.split('\n')[1],
                                    'Usage:',
                                    '  %s [option|cfgfile] ... LFN ...' % Script.scriptName,
                                    'Arguments:',
                                    '  LFN:      Logical File Name or file containing LFNs']))
  Script.parseCommandLine(ignoreErrors=True)
  lfns = Script.getPositionalArgs()

  if len(lfns) < 1:
    Script.showHelp()

  from DIRAC.Interfaces.API.Dirac import Dirac
  dirac = Dirac()
  exitCode = 0
  errorList = []

  if len(lfns) == 1:
    try:
      with open(lfns[0], 'r') as f:
        lfns = f.read().splitlines()
    except BaseException:
      pass

  result = dirac.getLfnMetadata(lfns, printOutput=True)
  if not result['OK']:
    print('ERROR: ', result['Message'])
    exitCode = 2

  DIRAC.exit(exitCode)


if __name__ == "__main__":
  main()
