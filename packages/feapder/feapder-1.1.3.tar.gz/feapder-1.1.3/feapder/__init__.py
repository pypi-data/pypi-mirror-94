# -*- coding: utf-8 -*-
"""
Created on 2020/4/21 10:41 PM
---------
@summary:
---------
@author: Boris
@email: boris@bzkj.tech
"""
import os, sys
import re

from feapder.core.spiders import Spider, BatchSpider, SingleSpider
from feapder.core.base_parser import BaseParse, BatchParser
from feapder.network.request import Request
from feapder.network.response import Response
from feapder.network.item import Item, UpdateItem
from feapder.utils.custom_argparse import ArgumentParser

sys.path.insert(0, re.sub(r"([\\/]items)|([\\/]spiders)", "", os.getcwd()))

__all__ = [
    "SingleSpider",
    "Spider",
    "BatchSpider",
    "BaseParse",
    "BatchParser",
    "Request",
    "Response",
    "Item",
    "UpdateItem",
    "ArgumentParser",
]
