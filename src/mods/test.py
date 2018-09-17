from pp import parse_args
from unittest import TestCase

class CommandLineTestCase(TestCase):
    """
    Base TestCase class, sets up a CLI parser
    """
@classmethod
def setUpClass(cls):
    parser = parse_args()
    cls.parser = parser

class PingTestCase(CommandLineTestCase):

#class TestCli(TestCase):
    """ Test the cli.py module """

    def __init__(self, *args, **kwargs):
        """ Initialize Unit Test """
        super(PingTestCase, self).__init__(*args, **kwargs)


    def teardown(self):
        """ Tear down after each test case """
        pass

    def test_version(self):
        parser = parse_args()
        with self.assertRaises(SystemExit):
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

