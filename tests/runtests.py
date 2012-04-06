#!/usr/bin/env python
'''
Discover all instances of unittest.TestCase in this directory.
'''
# Import python libs
import os
import optparse
# Import salt libs
import saltunittest
from integration import TestDaemon

TEST_DIR = os.path.dirname(os.path.normpath(os.path.abspath(__file__)))

PNUM = 50


def run_integration_tests(opts=None):
    '''
    Execute the integration tests suite
    '''
    if not opts:
        opts = {}
    print '~' * PNUM
    print 'Setting up Salt daemons to execute tests'
    print '~' * PNUM
    with TestDaemon():
        if opts.get('module', True):
            moduleloader = saltunittest.TestLoader()
            moduletests = moduleloader.discover(
                    os.path.join(TEST_DIR, 'integration', 'modules'),
                    '*.py'
                    )
            print '~' * PNUM
            print 'Starting Module Tests'
            print '~' * PNUM
            saltunittest.TextTestRunner(verbosity=1).run(moduletests)
        if opts.get('client', True):
            clientloader = saltunittest.TestLoader()
            clienttests = clientloader.discover(os.path.join(TEST_DIR, 'integration', 'client'), '*.py')
            print '~' * PNUM
            print 'Starting Client Tests'
            print '~' * PNUM
            saltunittest.TextTestRunner(verbosity=1).run(clienttests)


def run_unit_tests(opts=None):
    '''
    Execute the unit tests
    '''
    if not opts:
        opts = {}
    if not opts.get('unit', True):
        return
    loader = saltunittest.TestLoader()
    tests = loader.discover(os.path.join(TEST_DIR, 'unit', 'templates'), '*.py')
    print '~' * PNUM
    print 'Starting Unit Tests'
    print '~' * PNUM
    saltunittest.TextTestRunner(verbosity=1).run(tests)


def parse_opts():
    '''
    Parse command line options for running specific tests
    '''
    parser = optparse.OptionParser()
    parser.add_option('-m',
            '--module',
            '--module-tests',
            dest='module',
            default=False,
            action='store_true',
            help='Run tests for modules')
    parser.add_option('-c',
            '--client',
            '--client-tests',
            dest='client',
            default=False,
            action='store_true',
            help='Run tests for client')
    parser.add_option('-u',
            '--unit',
            '--unit-tests',
            dest='unit',
            default=False,
            action='store_true',
            help='Run unit tests')

    options, args = parser.parse_args()

    reverse = False

    opts = {}

    for key, val in options.__dict__.items():
        if val:
            reverse = True
        opts[key] = not val

    if reverse:
        for key, val in opts.items():
            opts[key] = not opts[key]

    return opts


if __name__ == "__main__":
    opts = parse_opts()
    run_integration_tests(opts)
    run_unit_tests(opts)
