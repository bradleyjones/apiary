from ..common.base import Base
from routes import Routes

class Sting(Base):

    def __init__(self):
        Base.__init__(self, "sting")


def main():
    sting = Sting()
    sting.start(Routes)
