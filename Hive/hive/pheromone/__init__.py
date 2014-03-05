#!/usr/bin/env python
from ..common.base import Base
from routes import Routes


class Pheromone(Base):

    def __init__(self):
        Base.__init__(self, "pheromone")


def main():
    pheromone = Pheromone()
    pheromone.start(Routes)
