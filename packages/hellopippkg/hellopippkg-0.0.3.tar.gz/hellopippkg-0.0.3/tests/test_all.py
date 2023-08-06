import pytest
from hellopip.hellopip import print_hellopip

def testall():
	try:
		assert print_hellopip() == 'SUCCESS'
		return "SUCCESS"
	except Exception as e:
		return e