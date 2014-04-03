from ..common.base import Base
from routes import Routes

__author__ = "John Davidge"
__credits__ = ["Sam Betts", "John Davidge", "Jack Fletcher", "Bradley Jones"]
__license__ = "Apache v2.0"
__version__ = "1.0"


class Sting(Base):

    def __init__(self):
        Base.__init__(self, "sting")


def main():
    sting = Sting()
    sting.start(Routes)
