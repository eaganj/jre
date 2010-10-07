from Quartz import *
from Quartz.QuartzCore import *
import objc

if 'setGeometryFlipped_' not in CALayer.__dict__:
    class CALayer(objc.Category(CALayer)):
        def setGeometryFlipped_(self, flipped):
            pass # TODO: FIXME
