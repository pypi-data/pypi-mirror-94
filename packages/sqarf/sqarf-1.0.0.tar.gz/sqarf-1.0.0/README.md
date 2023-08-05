[![Code style: black](https://img.shields.io/badge/code%20style-black-000000.svg)](https://github.com/psf/black)

[![Downloads](https://pepy.tech/badge/sqarf/month)](https://pepy.tech/project/sqarf)

# sqarf

Simple Quality Assurance Reports and Fixes

## Install
Activate your virtualenv and:

`pip install -U squarf`

## Test

Clone the git repository, activate your virtual env, cd to the repository root and:
```
pip install -e.[dev]
pytest -sv --cov=sqarf --color=yes --cov-report term-missing tests/
```

Our Ci coverage report can be visible here: https://kabaretstudio.gitlab.io/sqarf/

## Usage

You create a QA test by subclassing `squarf.QATest()` and implementing its `test()` method.
It must return `True` if the test passed and `False` otherwise, along with an message explaining why.

The method receives a `context` argument which is a dict-like object you can use to perform the test. 
It may contain the thing to test, or parameters of the test, it's up to you. The test can also modify 
the context content, and thus affect furter tests.

Each test can decide if it's relevant in a given context by returning `True` or `False` from its
`relevant_for()` method. When returning `False`, the test's `test()` will not be called.

If `test()` returned `False` (test has failed) and `can_fix()` returns `True`, the `fix()` method
will be called at an appropiate time. Each test can choose to disable auto-fix for its sub-tests and 
unperformed sibbling tests by calling the context's `set_allow_auto_fix()` method.

Your test may "contain" sub-test by returning a list of test **types** from its `get_sub_test_types()`
method. The result of a test is affected by its `test()` return value and by all its sub-tests results.
Note that sub-test are performed **after** the *parent* test.

By default, when a test fails, further test will still be perfomed. Each test can choose to cancel its
sub-tests and unperformed sibbling tests by calling the context's `set_stop_on_fail()` method.

Once you have your test types defined, you will use a `sqarf.Session()` to run them. Your tell
which test to perform using its `refister_test_types()` method, and you can prepare the test context using
the `context_set()` method. Once the session is configured, each call to `run()` will instanciate all the
tests and return a `QAResult` instance which evaluates to `True` if the no tests failed without being fixed.

The session can export details about each test performed by each `run()` with `to_lines()` (for prints), 
`to_dict_list()` (for inspection), `to_json()`/`to_json_file()` (for persistance), `to_html_tree` (for 
reporting), ...

The idea is to build a "main group" for *all your tests* with sub-groups using their `relevant_for()` method 
to activate or desactivate whole branches of tests. This strategy will let you manage a single test collection
and have consistant reports, and will prevent you from writing your test classe names all around you code !

You can read `tests\test_usage.py` for more usage details.

# Basic Example 

The `TestGroup` test is used to group `IsEnough` and `IsEven` tests.

The `TestGroup` configures the `IsEnough` test thru the `context`.

The `IsEnough` test may de-activate the `IsEven` test by setting a value in the `context`.

The session sets the value to test in the context.

```
import sqarf

class IsEnough(sqarf.QATest):

    def test(self, context):
        value = context['value']
        minimum = context['minimum']
        if value > 2*minimum:
            context['pass_iseven_test'] = True

        if value > minimum:
            return True, "Got more that {}.".format(
                minimum
            )
        else:
            return False, "{} is not enough !".format(
                value
            )

class IsEven(sqarf.QATest):

    def test(self, context):
        if context['pass_iseven_test']:
            return True, 'Test disabled by a previous test.'
        if context['value'] % 2:
            return False, "not even a little bit even"
        else:
            return True, "even in even"

class TestGroup(sqarf.QATest):

    def get_sub_test_types(self):
        return (IsEnough, IsEven)

    def test(self, context):
        context['minimum'] = 10

# perform tests in various conditions:

session = sqarf.Session()
session.register_test_types([TestGroup,])

session.context_set(value=15)
result = session.run()
assert result.passed()

session.context_set(value=5)
result = session.run()
assert result.failed()

# This run will skip the IsEven test:
session.context_set(value=30)
result = session.run()
assert result.failed()

```


