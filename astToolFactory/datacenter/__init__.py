"""IDK.

This is something like a unified interface for 'datacenter' activities.

I know I can use it to define the 'public' API.

AFAIK, however, I cannot use it to simplify the definition of the 'private' API used within the 'datacenter'.
"""

# isort: split
from astToolFactory.datacenter._dataServer import (
	getElementsBe as getElementsBe, getElementsDocstringGrab as getElementsDocstringGrab, getElementsDOT as getElementsDOT,
	getElementsGrab as getElementsGrab, getElementsMake as getElementsMake, getElementsTypeAlias as getElementsTypeAlias)

