#!/usr/bin/env python
"""Pheromone is a component of Apiary designed for firing alerts based on user
defined events.

It uses honeycomb and some extra logic to test for when to fire alerts
in real time.

"""

from ..common.base import Base
from routes import Routes


class Pheromone(Base):

    def __init__(self):
        Base.__init__(self, "pheromone")


def main():
    pheromone = Pheromone()
    pheromone.start(Routes)
