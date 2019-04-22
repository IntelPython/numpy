CONFIG = {
    'framework' : 'other',
    'arg' : 'PYCMD -c "from numpy import test; test({}, verbose=2)"'.format("'full'"),
    'env' : None,
    'expect_except' : None,
    'need_sources' : False,
    'location' : None,
    'use_re' : False,
    'parser' : 'pytest',
    'errors' : {
        '2.7' : {
            'Win' : {'test_astype_largearray (test_regression.TestRegression)', # SAT-1168
                     'test_poly (test_polynomial.TestDocs)'},
            'Lin' : set(),
            'Mac' : set()
        },
        '3.5' : {
            'Win' : {'test_astype_largearray (test_regression.TestRegression)'},  # SAT-1168
            'Lin' : set(),
            'Mac' : set()
        },
        '3.6' : {
            'Win' : set(),
            'Lin' : set(),
            'Mac' : {'numpy.f2py.tests.test_return_real.TestCReturnReal.test_all'}
        }
    },
    'failures' : {
        '2.7' : {
            'Win' : {'test_inplace_division_array_type (test_core.TestMaskedArrayInPlaceArithmetics)',
                     'test_mem_overlap.TestUFunc.test_unary_ufunc_1d_manual',
                     'test_special (test_umath.TestLog1p)',
                     'test_special (test_umath.TestExpm1)',
                     },
            'Lin' : {'TestKind.test_all'},
            'Mac' : {'TestKind.test_all',
                     'test_special (test_umath.TestLog1p)',
                     'test_special (test_umath.TestExpm1)',
                    },
        },
        '3.5' : {
            'Win' : set(),
            'Lin' : {'TestKind.test_all'},
            'Mac' : {'TestKind.test_all'},
        },
        '3.6' : {
            'Win' : {
                     'test_special (test_umath.TestLog1p)',
                     'test_special (test_umath.TestExpm1)',
                    },
            'Lin' : {'TestKind.test_all'},
            'Mac' : {'TestKind.test_all',
                     'test_special (test_umath.TestLog1p)',
                     'test_special (test_umath.TestExpm1)',
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
