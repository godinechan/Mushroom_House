#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Tue Mar 20 00:09:22 2018

@author: godinechan
"""
class Board:
    """
    <Doc string>
    """
    def __init__(self, height, width):
        self.height = height
        self.width = width
        self.size = self.height * self.width
        self.slots = {(i, j): None for i in range(height) for j in range(width)}