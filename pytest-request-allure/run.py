import sys
import pytest
from util import glb


def main(argv):


    glb.xls_path = argv[1]
    glb.xls_report_path = argv[2]
    pytest.main(["-s","--reruns", "1", "--reruns-delay",
                 "2", "--alluredir", "result"])


    ##"-runxfail",


if __name__ == '__main__':
    main(sys.argv)
