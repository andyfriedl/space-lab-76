#!/usr/bin/python
# -*- coding: utf-8 -*-

try:

    # import modules used here -- sys is a very standard one

    import sys
    import random
    import math
    import os
    import getopt
    import pygame
    import pickle
    import copy
    from collections import *
    from socket import *
    from pygame.locals import *
except ImportError, err:

    # from vector import *
    # import yaml
    # import pygame.mixer
    #    import ConfigParser

    print "couldn't load module. %s" % err
    sys.exit(2)


# Gather our code in a main() function

def main():
    print 'Hello there'
    print 'here'


# Command line args are in sys.argv[1], sys.argv[2] ...
# sys.argv[0] is the script name itself and can be ignored
# cool
# Standard boilerplate to call the main() function to begin
# the program.

if __name__ == '__main__':
    main()

