#!/usr/bin/env python

import sys
import scraperwiki

def main():
    scraperwiki.sqlite.save_var('category', sys.argv[1])
    print 'Saved'

if __name__ == '__main__':
    main()
