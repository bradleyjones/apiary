#!/usr/bin/env python
from ..common.base import Base
import controller
import routes

class Intelligence(Base):
    
    def __init__(self):
        Base.__init__(self, "intelligence")

def main():
    intelligence = Intelligence()
    intelligence.startServer(routes, controller)
