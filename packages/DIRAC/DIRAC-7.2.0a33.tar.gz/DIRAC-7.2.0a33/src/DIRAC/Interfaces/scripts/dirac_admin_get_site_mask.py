#!/usr/bin/env python
########################################################################
# File :    dirac-admin-get-site-mask
# Author :  Stuart Paterson
########################################################################

from __future__ import print_function
from __future__ import absolute_import
from __future__ import division
__RCSID__ = "$Id$"


from DIRAC.Core.Base import Script
from DIRAC.Core.Utilities.DIRACScript import DIRACScript


@DIRACScript()
def main():
  Script.setUsageMessage("""
  Get the list of sites enabled in the mask for job submission

  Usage:
    %s [options]
  """ % Script.scriptName)

  Script.parseCommandLine(ignoreErrors=True)

  from DIRAC import exit as DIRACExit, gLogger
  from DIRAC.Interfaces.API.DiracAdmin import DiracAdmin

  diracAdmin = DiracAdmin()

  gLogger.setLevel('ALWAYS')

  result = diracAdmin.getSiteMask(printOutput=True, status="Active")
  if result['OK']:
    DIRACExit(0)
  else:
    print(result['Message'])
    DIRACExit(2)


if __name__ == "__main__":
  main()
