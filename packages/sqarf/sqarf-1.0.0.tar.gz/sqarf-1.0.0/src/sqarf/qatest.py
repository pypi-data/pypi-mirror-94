"""



"""
import time
import traceback
import inspect
import getpass

from .context import QAContext
from .log import Log


class QAResult(object):
    class STATUS:
        ERROR = "ERROR"
        NOT_RAN = "NOT RAN"
        SKIPPED = "SKIPPED"
        IRRELEVANT = "IRRELEVANT"
        PASSED = "PASSED"
        FAILED = "FAILED"
        FIXED = "FIXED"
        FIX_FAILED = "FIX FAILED"

    @classmethod
    def ERROR(cls, why, err, trace):
        return cls(cls.STATUS.ERROR, why, err, trace)

    @classmethod
    def NOT_RAN(cls):
        return cls(cls.STATUS.NOT_RAN, "Not yet ran.")

    @classmethod
    def SKIPPED(cls, why):
        return cls(cls.STATUS.SKIPPED, why)

    @classmethod
    def IRRELEVANT(cls, why):
        return cls(cls.STATUS.IRRELEVANT, why)

    @classmethod
    def PASSED(cls, why):
        return cls(cls.STATUS.PASSED, why)

    @classmethod
    def FAILED(cls, why):
        return cls(cls.STATUS.FAILED, why)

    @classmethod
    def FIXED(cls, why):
        return cls(cls.STATUS.FIXED, why)

    @classmethod
    def FIX_FAILED(cls, why, previous_result):
        result = cls(cls.STATUS.FIX_FAILED, why)
        result._before_fix_result = previous_result
        return result

    def __init__(self, status, summary, err=None, trace=None):
        super(QAResult, self).__init__()
        self._status = status
        self._summary = summary
        self._error = err
        self._trace = trace
        self._before_fix_result = None
        self._timestamp = time.time()

    @classmethod
    def failed_statuses(cls):
        return (
            cls.STATUS.FAILED,
            cls.STATUS.FIX_FAILED,
            cls.STATUS.ERROR,
        )

    def failed(self):
        return self._status in self.failed_statuses()

    @classmethod
    def passed_statuses(cls):
        return (
            cls.STATUS.SKIPPED,
            cls.STATUS.PASSED,
            cls.STATUS.FIXED,
            cls.STATUS.IRRELEVANT,
        )

    def passed(self):
        return self._status in self.passed_statuses()

    @classmethod
    def not_applicable_statuses(cls):
        return (
            cls.STATUS.SKIPPED,
            cls.STATUS.NOT_RAN,
            cls.STATUS.IRRELEVANT,
        )

    def not_applicable(self):
        return self._status in self.not_applicable_statuses()

    def to_dict(self):
        before_fix = None
        if self._before_fix_result is not None:
            before_fix = self._before_fix_result.to_dict()
        return dict(
            timestamp=self._timestamp,
            status=self._status,
            summary=str(self._summary),
            error=self._error and str(self._error) or None,
            trace=self._trace,
            before_fix=before_fix,
        )

    def __bool__(self):
        return self.passed()

    def __str__(self):
        s = "{} ({})".format(self._status, self._summary)
        if self._error is not None:
            s += ': "{!s}"'.format(self._error)
            s += "\n" + self._trace
        return s

    def __add__(self, other):
        if not isinstance(other, self.__class__):
            raise TypeError()

        summary = self._summary
        status = self._status

        if not other.not_applicable():
            if self.failed():
                status = self._status
            elif other.failed():
                status = other._status
                summary = "Sub Test Failed"
        return self.__class__(status, summary)


class QATest(object):

    _forced_filename = None

    @classmethod
    def test_filename(cls):
        if cls._forced_filename is not None:
            return cls._forced_filename
        else:
            return inspect.getfile(cls)

    @classmethod
    def test_name(cls):
        """
        Returns the name for this QATest.
        May be overridden to return any string.

        Default is to use the class name.
        """
        return cls.__name__

    @classmethod
    def test_description(cls):
        """
        Returns short and long description for this QATest.
        May be overridden to return two strings.

        The short description should not contain "\\n".
        The long description may be an empty string.

        Default is to use the class docstring:
        first line is short description and the remaining is
        the long description.
        """
        doc = (cls.__doc__ or "").strip()
        if not doc:
            return None, None
        try:
            short, long = doc.split("\n", 1)
        except ValueError:
            return doc, None
        else:
            nice_long = ""
            for line in long.split("\n\n"):
                for wrapped in line.split("\n"):
                    nice_long += wrapped.strip() + " "
                nice_long += "\n"

        return short.strip(), nice_long.strip()

    @classmethod
    def get_sub_test_types(cls):
        return []

    def __init__(self):
        super(QATest, self).__init__()
        self._timestamp = time.time()

        # will be filled in test(), fix(), but also
        # by the parent test if any:
        self._log = Log()

        self._context = None
        self._result = None
        self._sub_tests = []  # QATest instances, filled at run()

    @property
    def log(self):
        """Read only attribute `self.log`"""
        return self._log

    def relevant_for(self, context):
        """
        Returns bool, str: relevant for this context, detail message
        `context` may be modified.
        """
        return True, "Default Relevance"

    def can_fix(self, context):
        return False, "No Fix for this."

    def fix(self, context):
        """
        Must return bool, str:
            boo: True if fix succeeded, False if not.
            str: summary (describes why it succeeded or not)
        """
        raise NotImplementedError(self)

    def test(self, context):
        """
        Must return bool, str:
            boo: True if test passed, False if test failed.
            str: summary (tells why it failed or passed)

        Default is to return True with empty summary

        Do not attempt to use `self.fix()` here, it will be called
        as needed later on.
        """
        return True, ""

    def _store_sub_test(self, test):
        self._sub_tests.append(test)

    def _results_sum(self, result):
        """
        Return the sum of `result` and all sub-tests results.
        """
        sub_results = [t._result for t in self._sub_tests]
        return sum(sub_results, result)

    def _run_sub_tests(self, context):
        """
        Build sub-test instances, run them and store
        results.
        """
        stop_subs = False
        for TestType in self.get_sub_test_types():
            # Build Test
            self.log.debug("Instanciating test type", TestType)
            try:
                test = TestType()
            except Exception as err:
                self.log.debug(
                    "Error while instanciating test type", TestType, ":", err
                )
                trace = traceback.format_exc()
                result = QAResult.ERROR(
                    "Error creating sub-test {}. Aborting.".format(TestType), err, trace
                )
                self._result = result
                self.log.debug("Stop _run_sub_test(context) with result", result)
                return

            self._store_sub_test(test)

            if stop_subs:
                self.log.debug("Stop subs requested, skiping run for", test)
                test.log.debug("Test aborted by parent test", self)
                test.log.debug("Result set to", self._result)
                test._result = QAResult.SKIPPED("Test stopped after fail.")
                test.log.debug("Result set to", test._result)
                continue

            # Check Relevance
            test.log.debug("=> calling relevant_for(contex)")
            try:
                relevant, why = test.relevant_for(context)
            except Exception as err:
                self.log.debug("Error checking relevance for", test)
                test.log.debug("Error checking relevance:", err)
                trace = traceback.format_exc()
                result = QAResult.ERROR("Error checking relevance.", err, trace)
                test._result = result
                test.log.debug("Result set to", test._result)
                continue
            else:
                test.log.debug("relevant_for(contex) returned", (relevant, why))
                if not relevant:
                    result = QAResult.IRRELEVANT(why)
                    test._result = result
                    test.log.debug("setting result to", test._result)
                    test.log.debug("End of test branch.")
                    continue

            # Run Test and its Sub-Tests
            self.log.debug("=> calling test.run(context) on", test)
            result = test.run(context)
            if result.failed() and context.stop_on_fail():
                self.log.debug(": test.run(context) failed for", test)
                self.log.debug(": context.stop_on_fail() == True")
                self.log.debug("Skipping all sub-tests from now on.")
                stop_subs = True
                continue

    def run(self, base_context):
        """
        Runs this test and all its sub-tests.
        Returns self._result (a QAResult)
        """
        if self._context is not None:
            raise Exception("Test already performed.")

        # Create a context stage based on the "parent" one:
        self._context = QAContext(base_context)

        # run this test
        self.log.debug("=> calling self.test(context)")
        try:
            passed, why = self.test(self._context)
        except Exception as err:
            self.log.debug("self.test() raised", err)
            trace = traceback.format_exc()
            result = QAResult.ERROR("Could not run test.", err, trace)
            self.log.debug("storing result", result)
            self._result = result
            self.log.debug("Ending run() with result", result)
            return result
        else:
            self.log.debug("self.test() returned", (passed, why))
            if passed:
                result = QAResult.PASSED(why)
            else:
                result = QAResult.FAILED(why)
        self.log.debug("storing result", result)
        self._result = result

        # fix if needed, possible and allowed:
        try:
            can_fix, why = self.can_fix(self._context)
        except Exception as err:
            self.log.debug("self.can_fix(context) raised", err)
            trace = traceback.format_exc()
            result = QAResult.ERROR("Error while asking if can fix.", err, trace)
            self.log.debug("Ending run() with result", result)
            self._result = result
            return result

        if result.failed() and self._context.allow_auto_fix() and can_fix:
            self.log.debug(": result.failed() == True")
            self.log.debug(": context.allow_auto_fix() == True")
            self.log.debug(": self.can_fix(context) == True")
            self.log.debug("=> calling self.fix(context)")
            try:
                fixed, why = self.fix(self._context)
            except Exception as err:
                self.log.debug("self.fix(context) raised", err)
                trace = traceback.format_exc()
                result = QAResult.ERROR("Error while fixing.", err, trace)
            else:
                self.log.debug("self.fix(context) returned", (fixed, why))
                if fixed:
                    result = QAResult.FIXED(why)
                else:
                    result = QAResult.FIX_FAILED(why, self._result)
            self.log.debug("updating result", result)
            self._result = result

        # cancel sub-tests if needed:
        if result.failed() and self._context.stop_on_fail():
            self.log.debug(": result.failed() == True")
            self.log.debug(": context.stop_on_fail() == True")
            self.log.debug("Ending run() with result", result)
            self._result = result
            return result

        # run all sub-tests
        self.log.debug("=> self._run_sub_tests(context)")
        self._run_sub_tests(self._context)
        self.log.debug("<= self._run_sub_tests(context)")

        # Update our result with sub-result:
        self.log.debug("summing sub-test results with current result")
        self._result = self._results_sum(result)
        self.log.debug("result updated to", self._result)

        # Return our result for convenience
        self.log.debug("run() completed with result", self._result)
        return self._result

    def to_lines(self, indent=0):
        indent_str = indent * "  "
        lines = ["{}{}:{}".format(indent_str, self.test_name(), self._result)]
        for test in self._sub_tests:
            lines.extend(test.to_lines(indent + 1))
        return lines

    def to_dict(self):
        """Returns a dict containing info for this test and all sub tests"""
        short_description, long_description = self.test_description()

        context_dict = {}
        context_edits = None
        if self._context is not None:
            context_dict = self._context.to_dict()
            context_edits = self._context.edits()

        log_lines = None
        log_text = ""
        if self.log is not None:
            log_lines = self.log.to_lines(0)
            log_text = self.log.pformat()

        qualname = "{}.{}".format(
            self.__class__.__module__,
            self.__class__.__name__,
        )
        return dict(
            test_type=qualname,
            test_filename=self.test_filename(),
            test_name=self.test_name(),
            short_description=short_description,
            long_description=long_description,
            timestamp=self._timestamp,
            username=getpass.getuser(),
            sub_tests=[t.to_dict() for t in self._sub_tests],
            context_edits=context_edits,
            context=context_dict,
            result=self._result.to_dict(),
            log_lines=log_lines,
            log_text=log_text,
        )
