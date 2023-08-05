import os
from kabaret import flow
from kabaret.pyscript_flow import PyScriptValue


class ExtraTestFile(flow.Object):

    filename = flow.Param("")
    active = flow.BoolParam(True)


class AddExtraTestFile(flow.Action):

    _extra_test_files = flow.Parent()
    filename = flow.Param()

    def needs_dialog(self):
        return True

    def get_buttons(self):
        return ["Add Test File"]

    def run(self, button):
        if button != "Add Test File":
            return
        self._extra_test_files.get_or_add_test_file(self.filename.get())


class ExtraTestFiles(flow.Map):

    add_extra_test_file = flow.Child(AddExtraTestFile).ui(
        expanded=True,
    )

    @classmethod
    def mapped_type(cls):
        return ExtraTestFile

    def get_extra_test_file(self, filename):
        filename = os.path.normpath(filename)
        for xtf in self.mapped_items():
            if os.path.normpath(xtf.filename.get()) == filename:
                return xtf

    def get_or_add_test_file(self, filename):
        xtf = self.get_extra_test_file(filename)
        if xtf is not None:
            return xtf

        xtf = self.add("I{:03}".format(len(self) + 1))
        xtf.filename.set(filename)
        self.touch()
        return xtf

    def columns(self):
        return ["Name", "Active"]

    def _fill_row_cells(self, row, item):
        row["Name"] = os.path.basename(item.filename.get())
        row["Active"] = not item.active.get() and "X" or ""

    # def _fill_row_style(self, style, item, row):

    def get_filenames(self):
        return [
            item.filename.get() for item in self.mapped_items() if item.active.get()
        ]


default_extra_test_code = """
import sqarf

class MyTest(sqarf.QATest):
    '''
    Tu peux pas test !
    '''
    def test(self, context):
        with self.log.section("Context tunning") as log:
            log.info("Tunning...")
            context.set_stop_on_fail(False)
            context.set_allow_auto_fix(False)
            log.info("Changing...")
            context['asset_list'] = ['Riri', 'Fifi', 'Loulou']
            try:
                del context['something']
            except KeyError:
                pass

        with self.log.section("This is a section log") as log:
            log.info('Checking context')
            object = context.get('TESTED')
            if not object:
                log.error("Nothing to test !")
                return False, "Nothing being TESTED :/"
            else:
                log.warning("Don't eat the yellow snow...")
                return True, "TESTED="+context['TESTED'].oid()

def get_root_tests():
    return [MyTest]

"""


class ExtraTestsConfig(flow.Object):

    extra_test_files = flow.Child(ExtraTestFiles).ui(expanded=True)

    with flow.group("Custom Tests"):
        use_extra_test_code = flow.BoolParam(False)
        extra_test_code = flow.Param(default_extra_test_code, PyScriptValue)

    def get_extra_filenames(self):
        return self.extra_test_files.get_filenames()

    def get_extra_code(self):
        if not self.use_extra_test_code.get():
            return None
        code = str(self.extra_test_code.get() or "").strip()
        return code
