#vision/__init__.py
#A part of NonVisual Desktop Access (NVDA)
#This file is covered by the GNU General Public License.
#See the file COPYING for more details.
#Copyright (C) 2018-2019 NV Access Limited, Babbage B.V.

"""Framework to facilitate changes in how content is displayed on screen.
One or more assistant functions can be implemented in vision enhancement providers.
Add-ons can provide their own provider
using modules in the visionEnhancementProviders package containing a L{VisionEnhancementProvider} class.
"""

from .constants import *
from .providerBase import VisionEnhancementProvider
from .visionHandler import VisionHandler, getProviderClass
import pkgutil
import visionEnhancementProviders
import config
from logHandler import log

def initialize():
	global handler
	config.addConfigDirsToPythonPackagePath(visionEnhancementProviders)
	handler = VisionHandler()

def pumpAll():
	"""Runs tasks at the end of each core cycle."""
	# Note that a pending review update has to be executed before a pending caret update.
	if handler and handler.extensionPoints:
		handler.extensionPoints.post_coreCycle.notify()

def terminate():
	global handler
	handler.terminate()
	handler = None

def getProviderList(excludeNegativeChecks=True):
	"""Gets a list of available vision enhancement names with their descriptions as well as supported roles.
	@param excludeNegativeChecks: excludes all providers for which the check method returns C{False}.
	@type excludeNegativeChecks: bool
	@return: list of tuples with provider names, descriptions, and supported roles.
	@rtype: [(str,str,[ROLE_*])]
	"""
	providerList = []
	for loader, name, isPkg in pkgutil.iter_modules(visionEnhancementProviders.__path__):
		if name.startswith('_'):
			continue
		try:
			provider = getProviderClass(name)
		except:
			# Purposely catch everything.
			# A provider can raise whatever exception it likes,
			# therefore it is unknown what to expect.
			log.error(
				"Error while importing vision enhancement provider %s" % name,
				exc_info=True
			)
			continue
		try:
			if not excludeNegativeChecks or provider.check():
				providerList.append((
					provider.name,
					provider.description,
					list(provider.supportedRoles)
				))
			else:
				log.debugWarning("Vision enhancement provider %s reports as unavailable, excluding" % provider.name)
		except:
			# Purposely catch everything else as we don't want one failing provider
			# make it impossible to list all the others.
			log.error("", exc_info=True)
	providerList.sort(key=lambda d: d[1].lower())
	return providerList

def _isDebug():
	return config.conf["debugLog"]["vision"]
