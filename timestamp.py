from bokeh.core.properties import String
from bokeh.models import LayoutDOM

class TimeStamp(LayoutDOM):
    __implementation__ = open("timestamp.coffee").read()
    text = String(default = "Testing")