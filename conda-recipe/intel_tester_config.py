import sys

IS_WIN = True if sys.platform.startswith('win') else False

CONFIG = {
    'framework' : 'other',
    'arg' : 'PYCMD -c "from numpy import test; test(label={label}, verbose=2, extra_argv={extra_argv})"'.format(
          label="'fast'" if IS_WIN else "'full'", # skip slow tests on Windows
	  # see https://github.com/numpy/numpy/issues/13387
	  extra_argv=["--deselect", "numpy\\distutils\\tests\\test_system_info.py"] if IS_WIN else []
       ),
    'env' : None,
    'expect_except' : None,
    'need_sources' : False,
    'location' : None,
    'use_re' : False,
    'parser' : 'pytest',
    'errors' : {
        '2.7' : {
            'Win' : set(),
            'Lin' : set(),
            'Mac' : set()
        },
        '3.5' : {
            'Win' : set(),
            'Lin' : set(),
            'Mac' : set()
        },
        '3.6' : {
            'Win' : set(),
            'Lin' : set(),
            'Mac' : set()
        }
    },
    'failures' : {
        '2.7' : {
            'Win' : set(),
            'Lin' : {'TestKind.test_all'},
            'Mac' : {'TestKind.test_all',
                     #'test_special (test_umath.TestLog1p)',
                     #'test_special (test_umath.TestExpm1)',
                    },
        },
        '3.5' : {
            'Win' : set(),
            'Lin' : {'TestKind.test_all'},
            'Mac' : {'TestKind.test_all'},
        },
        '3.6' : {
            'Win' : {
                     # 'test_special (test_umath.TestLog1p)',
                     # 'test_special (test_umath.TestExpm1)',
                    },
            'Lin' : {'TestKind.test_all'},
            'Mac' : {'TestKind.test_all',
                     # 'test_special (test_umath.TestLog1p)',
                     # 'test_special (test_umath.TestExpm1)',
                     },
        },
    },
    'validation' : {
        'errors' : {
            '3.6' : {
                'Win' : { 'test_astype_largearray (test_regression.TestRegression)', #SAT-1381
                          'test_format.test_large_archive',                          #SAT-1381
                          'test_big_arrays (test_io.TestSavezLoad)',                 #SAT-1381
                          'numpy.core.tests.test_memmap.TestMemmap.test_path',       #SAT-1381
                },
                'Lin' : { 'test_astype_largearray (test_regression.TestRegression)', #SAT-1381
                          'test_format.test_large_archive',                          #SAT-1381
                          'test_big_arrays (test_io.TestSavezLoad)',                 #SAT-1381
                },
                'Mac' : { 'test_astype_largearray (test_regression.TestRegression)', #SAT-1381
                          'test_format.test_large_archive',                          #SAT-1381
                          'test_big_arrays (test_io.TestSavezLoad)',                 #SAT-1381
                },
            },
        },
        'failures' : {
            '2.7' : {
                'Win' : set(),
                'Lin' : { 'numpy.tests.test_scripts.test_f2py', },                   #SAT-1381
                'Mac' : { 'numpy.tests.test_scripts.test_f2py', },                   #SAT-1381
            },
            '3.6' : {
                'Win' : { 'numpy.core.tests.test_memmap.TestMemmap.test_path', },    #SAT-1381
                'Lin' : { 'numpy.tests.test_scripts.test_f2py', },                   #SAT-1381
                'Mac' : { 'numpy.tests.test_scripts.test_f2py', },                   #SAT-1381
            },
        },
    },
}

def fetch_config(pyver):
    return CONFIG
