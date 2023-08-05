#!/usr/bin/python3

# This file should be loaded during the register tests

from ..register import register_class


class AutoLoadTestCase():
    pass


__all__ = ['AutoLoadTestCase']
register_class(AutoLoadTestCase)
