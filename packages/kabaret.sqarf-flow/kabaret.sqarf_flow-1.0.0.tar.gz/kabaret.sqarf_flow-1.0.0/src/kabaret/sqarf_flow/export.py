from kabaret import flow

import sqarf


class ExportStyleChoice(flow.values.ChoiceValue):

    CHOICES = sqarf.Session.get_exporter_names()

    @classmethod
    def default(cls):
        return cls.CHOICES[0]


class ExportOptionsChoices(flow.values.MultiChoiceValue):

    _config = flow.Parent()

    def get_exporter_defaults(self):
        export_style = self._config.export_style.get()
        return sqarf.Session.get_exporter_defaults(export_style)

    def choices(self):
        return [i[0] for i in self.get_exporter_defaults()]

    def update(self):
        old_selected = self.get()
        new_defaults = self.get_exporter_defaults()
        new_selected = []
        for option, checked in new_defaults:
            if option in old_selected or checked:
                new_selected.append(option)
        self.set(new_selected)

    def to_dict(self):
        keys = self.choices()
        selected = self.get()
        if not selected:
            # Nothing selected (which is our default)
            # means use default options. So we need to:
            selected = [i[0] for i in self.get_exporter_defaults() if i[1]]
        d = {}
        for k in keys:
            d[k] = k in selected
        return d


class ExportConfig(flow.Object):

    export_style = flow.Param(ExportStyleChoice.default(), ExportStyleChoice).watched()
    export_options = flow.Param([], ExportOptionsChoices)
    filename = flow.Param("")
    allow_overwrite = flow.BoolParam(True)

    def load(self, other_export_config):
        self.export_style.set(other_export_config.export_style.get())
        self.export_options.set(other_export_config.export_options.get())
        self.filename.set(other_export_config.filename.get())
        self.allow_overwrite.set(other_export_config.allow_overwrite.get())

    def child_value_changed(self, value):
        if value is self.export_style:
            self.export_options.update()

    def get_config_dict(self):
        config = self.export_options.to_dict()
        return config


class ExportReportAction(flow.Action):

    also_open_in_browser = flow.BoolParam(True)

    config = flow.Child(ExportConfig).ui(expanded=True)

    def get_report(self):
        raise NotImplementedError()

    def needs_dialog(self):
        return True

    def get_buttons(self):
        return ["Export"]

    def run(self, button):
        report = self.get_report()
        try:
            filename = self.export(report)
        except Exception as err:
            import traceback

            msg = "There was an error:\n'{}'\n{}".format(
                str(err),
                traceback.format_exc(),
            )
            print(msg)
            self.message.set(
                "<font color=red><b>ERROR:</b></font><pre>{}</pre>".format(msg)
            )
            return self.get_result(close=False)

        self.message.set('Exported to "{}"'.format(filename))
        return

    def export(self, report, config=None):
        """
        Exports the given `report`.
        If `config` is given, it must be a ExportConfig
        instance.
        If no `config` is given, self.config is used.
        """
        config = config or self.config
        return report.export_report(
            self.config.export_style.get(),
            self.config.get_config_dict(),
            self.config.filename.get(),
            self.config.allow_overwrite.get(),
            self.also_open_in_browser.get(),
        )
