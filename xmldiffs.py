#!/usr/bin/env python
import click
import xmltodict
from filecmp import dircmp
from loguru import logger

q1 = xmltodict.parse("""<?xml version="1.0" encoding="UTF-8"?>
  <mydocument has="an attribute">
    <and>
      <many>elements哈哈</many>
      <many>more elements</many>
    </and>
    <plus a="complex">
      element as well
    </plus>
  </mydocument>
  """)

q2 = xmltodict.parse("""<?xml version="1.0" encoding="UTF-8"?>
  <mydocument has="an attribute">
    <and>
      <many>elements哈哈</many>
      <many>more elements</many>
    </and>
    <plus a="complex">
      element as well
    </plus>
  </mydocument>
  """)

print(q1)
print(q2)

if q1 == q2:
    print('equal')
else:
    print('not equal')


class Diff(object):
    """
    Iff two variables are all Path or are all File, compare them relate.
    """
    def __init__(self):
        pass

    def compare(self):
        pass


class Report(object):
    """
    If two folders are not equals, just report folders not equals;
    Iff folders are equal, compare files under folders.
    """
    def __init__(self):
        self.is_equal = False
        self.not_equal_list = []
        pass

    def set_equal(self, equal: bool):
        self.is_equal = equal

    def __str__(self):

        return 'result'


if __name__ == '__main__':
    print('hello, world!')
    r = Report()

    print(r)
