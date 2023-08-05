import os
import json
import webbrowser
import time
import tempfile

try:
    json_parse_exception = json.decoder.JSONDecodeError
except AttributeError:  # Python 2
    json_parse_exception = ValueError

try:
    import maya
except ImportError:
    slang_time = time.ctime
else:
    try:
        maya.MayaDT
    except AttributeError:
        slang_time = time.ctime
    else:

        def _maya_slang_time(ts):
            return maya.MayaDT(ts).slang_time()

        slang_time = _maya_slang_time

import sqarf
import sqarf.qatest
import sqarf.html_table_export
import sqarf.html_tree_export

from kabaret import flow

from .export import ExportReportAction


class SaveDefaultExportConfigAction(flow.Action):

    _export_action = flow.Parent()

    def allow_context(self, context):
        return "details" in context

    def needs_dialog(self):
        return True

    def get_buttons(self):
        self.message.set(
            "Save export config to {} ?".format(self.get_dst_export_config().oid())
        )
        return ["Save Default Config"]

    def get_dst_export_config(self):
        return self._export_action._report.get_qa_group_export_config()

    def run(self, button):
        if button != "Save Default Config":
            return

        dst_config = self.get_dst_export_config()
        dst_config.load(self._export_action.config)
        self.message.set("")


class LoadDefaultExportConfigAction(flow.Action):

    _export_action = flow.Parent()

    def allow_context(self, context):
        return "details" in context

    def needs_dialog(self):
        return True

    def get_buttons(self):
        self.message.set(
            "Load export config from {} ?".format(self.get_source_export_config().oid())
        )
        return ["Load Default Config"]

    def get_source_export_config(self):
        return self._export_action._report.get_qa_group_export_config()

    def run(self, button):
        if button != "Load Default Config":
            return

        src_config = self.get_source_export_config()
        self._export_action.config.load(src_config)
        self.message.set("")


class ExportAsReportAction(ExportReportAction):

    _report = flow.Parent()

    load_defaults = flow.Child(LoadDefaultExportConfigAction)
    store_defaults = flow.Child(SaveDefaultExportConfigAction)

    def get_report(self):
        return self._report


class DefaultExportReportAction(ExportReportAction):

    _report = flow.Parent()

    def needs_dialog(self):
        return False

    def run(self, button):
        # Will use config from
        # QAGroup:
        exported_filename = self._report.export_report()
        print("{} exported to {}".format(self.oid(), exported_filename))


class ShowReportAction(flow.Action):

    _report = flow.Parent()

    def needs_dialog(self):
        return False

    def run(self, button):
        # Will use config from
        # QAGroup:
        self._report.show_report()


class QAReport(flow.Object):

    _as_json = flow.Param().watched()

    ran_by = flow.Computed()
    ran_on = flow.Computed()
    result = flow.Computed()
    summary = flow.Computed()

    show = flow.Child(ShowReportAction)
    export = flow.Child(DefaultExportReportAction)
    export_as = flow.Child(ExportAsReportAction).ui(label="Export as...")

    def _get_data(self):
        try:
            data = self._data
        except AttributeError:
            data = None
        if data is not None:
            return data

        try:
            self._data = json.loads(self._as_json.get())
        except json_parse_exception:
            self._data = []
        return self._data

    def child_value_changed(self, value):
        if value is self._as_json:
            self._data = None
            self.ran_by.touch()
            self.ran_on.touch()
            self.result.touch()
            self.summary.touch()
            # self.display.touch()

    def compute_child_value(self, value):
        if value is self.ran_by:
            data = self._get_data()
            username = data and data[0].get("username", "???")
            self.ran_by.set(username)
            return

        if value is self.ran_on:
            data = self._get_data()
            timestamp = data and data[0]["result"]["timestamp"] or 0
            self.ran_on.set(timestamp)
            return

        if value is self.result:
            data = self._get_data()
            result = data and data[0]["result"]["status"] or "???"
            self.result.set(result)
            return

        if value is self.summary:
            data = self._get_data()
            summary = data and data[0]["result"]["summary"]
            self.summary.set(summary)

    def get_qa_group_export_config(self):
        report_map = self._mng.parent
        if report_map is None:
            return None
        qa_group = report_map._mng.parent
        if qa_group is None:
            return None
        try:
            return qa_group.export_config
        except AttributeError:
            return None

    def get_export_defaults(
        self, export_style, export_options, filename, allow_overwrite
    ):
        if None not in (export_style, export_options, filename, allow_overwrite):
            return export_style, export_options, filename, allow_overwrite

        config = self.get_qa_group_export_config()
        if config is None:
            raise Exception(
                "Could not get default export config "
                "for report {}: QAGroup.export_config not found".format(self.oid())
            )

        if export_style is None:
            export_style = config.export_style.get()
        if export_options is None:
            export_options = config.export_options.to_dict()
        if filename is None:
            filename = config.filename.get()
        if allow_overwrite is None:
            allow_overwrite = config.allow_overwrite.get()
        return export_style, export_options, filename, allow_overwrite

    def show_report(self, export_style=None, export_options=None):
        """
        Show the report in a webbrowser.
        If export_style or export_options is None,
        the report must be inside a QAGroup which will be
        used to fine default values.
        """
        # Using None would resolve to default, keep it ""
        # so that export_report() set it to a tmp name:
        filename = ""

        self.export_report(
            export_style,
            export_options,
            filename,
            True,
            True,
        )

    def export_report(
        self,
        export_style=None,
        export_options=None,
        filename=None,
        allow_overwrite=None,
        also_open_in_browser=False,
    ):
        """
        Exports the report in a webbrowser.
        If export_style, export_options, filename or
        allow_overwrite is None, the report must be inside
        a QAGroup which will be used to find default values.

        If filename is None and no default is set, a temp filename
        will be used.

        Returns the exported filename.
        """

        (
            export_style,
            export_options,
            filename,
            allow_overwrite,
        ) = self.get_export_defaults(
            export_style, export_options, filename, allow_overwrite
        )

        if not filename:
            filename = os.path.join(
                tempfile.gettempdir(), "sqarf_report_{}.html".format(time.time())
            )

        session_dict_list = self._get_data()
        exporter = sqarf.Session.get_exporter(export_style, export_options)
        exporter.export(
            session_dict_list,
            filename,
            allow_overwrite,
            also_open_in_browser,
        )

        return filename


class QAReportCollection(flow.Map):
    @classmethod
    def mapped_type(cls):
        return QAReport

    def mapped_names(self, page_num=0, page_size=None):
        # We need to bake to a list, generators dont have __len__:
        return list(
            reversed(super(QAReportCollection, self).mapped_names(page_num, page_size))
        )

    def columns(self):
        return ["By", "On", "Result", "Summary"]

    def _fill_row_cells(self, row, item):
        row["By"] = item.ran_by.get()
        row["On"] = slang_time(item.ran_on.get() or 0)
        row["Result"] = item.result.get()
        row["Summary"] = item.summary.get()

    def _fill_row_style(self, style, item, row):
        if row["Result"] != "PASSED":
            style["Result_background-color"] = "#440000"
        else:
            style["Result_background-color"] = "#004400"

    def store_report(self, json_report):
        report_name = "R{:03}".format(len(self) + 1)
        report = self.add(report_name)
        report._as_json.set(json_report)
        self.touch()
        return report


class QAReports(flow.Object):

    reports = flow.Child(QAReportCollection).ui(expanded=True)

    def store_report(self, json_report):
        return self.reports.store_report(json_report)
