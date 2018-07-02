# A part of NonVisual Desktop Access (NVDA)
# Copyright (C) 2018 NV Access Limited
# This file may be used under the terms of the GNU General Public License, version 2 or later.
# For more details see: https://www.gnu.org/licenses/gpl-2.0.html

"""This file provides utility methods for NVDA system tests.
It is copied into the (system test specific) NVDA profile directory as part of a
package. This allows us to share utility methods between the global plugin and the nvdaRobotLib library.
"""

from timeit import default_timer as _timer


def _blockUntilConditionMet(
		getValue,
		giveUpAfterSeconds,
		shouldStopEvaluator=lambda value: bool(value),
		intervalBetweenSeconds=0.1,
		errorMessage=None):
	"""Repeatedly tries to get a value up until a time limit expires. Tries are separated by
	a time interval. The call will block until shouldStopEvaluator returns True when given the value,
	the default evaluator just returns the value converted to a boolean.
	@return A tuple, (True, value) if evaluator condition is met, otherwise (False, None)
	@raises RuntimeError if the time limit expires and an errorMessage is given.
	"""
	assert callable(getValue)
	assert callable(shouldStopEvaluator)
	startTime = _timer()
	lastRunTime = startTime
	firstRun = True  # ensure we start immediately
	while (_timer() - startTime) < giveUpAfterSeconds:
		if firstRun or (_timer() - lastRunTime) > intervalBetweenSeconds:
			firstRun = False
			lastRunTime = _timer()
			val = getValue()
			if shouldStopEvaluator(val):
				return True, val
	else:
		if errorMessage:
			raise AssertionError(errorMessage)
		return False, None
