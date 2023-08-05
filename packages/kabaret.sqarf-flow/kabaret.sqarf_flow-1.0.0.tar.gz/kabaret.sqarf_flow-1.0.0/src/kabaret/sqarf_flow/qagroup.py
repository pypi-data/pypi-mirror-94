import sqarf

from kabaret import flow

from .qareport import QAReportCollection
from .extra_tests import ExtraTestsConfig
from .export import ExportConfig


class RunQATestsAction(flow.Action):

    ICON = ("icons.gui", "sqarf")

    _qa_group = flow.Parent()

    also_export_report = flow.BoolParam(True)
    also_open_report_in_browser = flow.BoolParam(True)
    goto_report_page = flow.BoolParam(False)

    def needs_dialog(self):
        return True

    def get_buttons(self):
        return ["Run Tests"]

    def run(self, button):
        report = self._qa_group.do_run_tests(
            self.also_export_report.get(),
            self.also_open_report_in_browser.get(),
            self.message.set,
        )
        if self.goto_report_page.get():
            return self.get_result(goto=report.oid())


class GotoLastReportAction(flow.Action):

    ICON = ("icons.gui", "chevron-sign-to-right")

    _qa_group = flow.Parent()

    def needs_dialog(self):
        last_report = self._qa_group.get_last_report()
        if last_report is None:
            return True
        return False

    def get_buttons(self):
        last_report = self._qa_group.get_last_report()
        if last_report is None:
            self.message.set(
                "No report available yet.\n" "Please Run Tests at least once..."
            )
            return ["Run Tests"]
        else:
            return ["Run Tests", "Show Last Report"]

    def run(self, button):
        if button == "Run Tests":
            return self._qa_group.run_tests.run("Go")

        last_report = self._qa_group.get_last_report()
        return self.get_result(goto=last_report.oid())


class ShowLastReportAction(GotoLastReportAction):

    ICON = ("icons.gui", "text-file")

    def run(self, button):
        if button == "Run Tests":
            return self._qa_group.run_tests.run("Go")

        last_report = self._qa_group.get_last_report()
        return last_report.show.run(None)


class QAGroup(flow.Object):
    """
    In order to use this class, you need to implement `get_scarf_test_types()`
    in its parent to return a list of QATest subclasses.

    If you want to allow usage with only extra tests (form file or
    inline code), you can override `get_test_types()` here to return
    an empty list instead of calling parent's `get_scarf_test_types()`

    You can fine tune the `sqarf.Session` by overriding `_configure_session()`.
    For example, to set a custom title...

    The Test will receive a context with a "TESTED" key containing the
    result of the `get_tested()` method. Default implementation
    returns the parent.

    You can programmatically run the tests using `do_run_tests()`.
    You can export the last tests report easily using:
        `get_last_report().export_report(filename)`
    or
        `get_last_report().show_report()`

    See `kabaret.sqarf_flow.qareport.QAReport()` for more details.

    """

    ICON = ("icons.gui", "sqarf")

    _parent = flow.Parent()

    run_tests = flow.Child(RunQATestsAction)
    show_last_report = flow.Child(ShowLastReportAction)
    goto_last_report = flow.Child(GotoLastReportAction)

    with flow.group("Config"):
        custom_tests = flow.Child(ExtraTestsConfig)
        export_config = flow.Child(ExportConfig)

    reports = flow.Child(QAReportCollection).ui(expanded=True)

    def get_tested(self):
        return self._parent

    def get_test_types(self):
        try:
            return self._parent.get_scarf_test_types()
        except AttributeError:
            raise AttributeError(
                "Could not find `get_test_type` in {}._parent".format(self.oid())
            )

    def _configure_session(self, session):
        """
        Override this to add extra configuration to
        the sqarf.Session right before its `run()` is called.

        The 'TESTED' key is already set in the context.

        (Default implementation does nothing.)
        """
        return

    def get_last_report(self):
        names = self.reports.mapped_names()
        if not names:
            return None
        last_report_name = names[0]
        return self.reports.get_mapped(last_report_name)

    def do_run_tests(self, also_export, also_open_in_browser, messager=None):
        """
        Run all the test types returned by `get_test_types()`,
        store the report in `self.reports` and return the
        report object.
        """
        messager = messager or (lambda msg: print("[SQARF Run] {}".format(msg)))

        messager("Starting test session")
        session = sqarf.Session()
        session.register_test_types(self.get_test_types())

        messager("Loading extra test files")
        for filename in self.custom_tests.get_extra_filenames():
            messager("   " + filename)
            session.register_tests_from_file(filename)
            messager("   Ok.")

        code = self.custom_tests.get_extra_code()
        if code:
            messager("Loading extra test code")
            session.register_tests_from_string(code, "flow_custom_tests")
            messager("   Ok.")

        key = "TESTED"
        tested_object = self.get_tested()
        messager("Adding context {}=<{}>".format(key, tested_object.oid()))
        session.context_set(TESTED=tested_object)
        if tested_object is not None:
            session.set_title(tested_object.oid())

        messager("Adding extra session config")
        self._configure_session(session)

        messager("Running Tests")
        session.run()

        messager("Saving Report")
        json_report = session.to_json()
        report = self.reports.store_report(json_report)

        if also_export:
            report.export_report(also_open_in_browser=also_open_in_browser)

        return report
