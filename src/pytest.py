from pp import parse_args
import pytest
import argparse
import unittest

class TestCli(unittest.TestCase):
    """ Test the cli.py module """

    def __init__(self, *args, **kwargs):
        """ Initialize Unit Test """
        super(TestCli, self).__init__(*args, **kwargs)

    def setup(self):
        """ Setup before each test case """
        setup_config(app)
#        setup_logging(app)

    def teardown(self):
        """ Tear down after each test case """
        pass

    def test_version(self):
        parser = parse_args()
        with pytest.raises(SystemExit):
            args = vars(parser.parse_args(['', '-v']))

        assert args.version =='%(prog)s 1.0.1'

    def test_seed(self):
        parser = parse_args()
        args = parser.parse_args(['-s'])

        assert args.seed

    def test_theta(self):
        parser = parse_args()
        args = parser.parse_args(['-t'])

        assert args.theta        

    def test_numsim(self):
        parser = parse_args()
        args = parser.parse_args(['-n'])

        assert args.num_sim
        
    def test_mutnode(self):
        parser = parse_args()
        args = parser.parse_args(['-m'])

        assert args.mutate_node
        
    def test_coverage(self):
        parser = parse_args()
        args = parser.parse_args(['-c'])

        assert args.coverage

    def test_error(self):
        parser = parse_args()
        args = parser.parse_args(['-e'])

        assert args.error_rate

    def test_allele(self):
        parser = parse_args()
        args = parser.parse_args(['-a'])

        assert args.mute_allele

    def test_output(self):
        parser = parse_args()
        args = parser.parse_args(['-0'])

        assert args.output

    def test_zygosity(self):
        parser = parse_args()
        args = parser.parse_args(['-z'])

        assert args.zygosity




       
