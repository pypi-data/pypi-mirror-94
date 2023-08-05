import logging

from AnyQt.QtCore import QTimer, Qt
from AnyQt.QtWidgets import QApplication, QComboBox, QLabel, QStyledItemDelegate

from Orange.util import try_
from Orange.widgets.utils.itemmodels import PyListModel
from Orange.widgets import widget, gui, settings
from Orange.data import Table
from orangecontrib.educational.i18n_config import *


def __(key):
    return i18n.t('educational.owgooglesheets.' + key)


log = logging.getLogger(__name__)


class URLComboBox(QComboBox):
    class TitleShowingPopupDelegate(QStyledItemDelegate):
        TitleRole = Qt.UserRole + 1

        def displayText(self, url, _):
            i = self.parent().findText(url, Qt.MatchExactly)
            model = self.parent().model()
            title = model.data(model.index(i, 0), self.TitleRole)
            return ('{0} ({1})' if title else '{1}').format(title, url)

    def __init__(self, parent, model_list, **kwargs):
        super().__init__(parent, **kwargs)
        self.setModel(PyListModel(iterable=model_list,
                                  flags=Qt.ItemIsSelectable | Qt.ItemIsEnabled | Qt.ItemIsEditable,
                                  parent=self))
        self.view().setItemDelegate(self.TitleShowingPopupDelegate(self))

    def setTitleFor(self, i, title):
        self.model().setData(self.model().index(i, 0), title,
                             self.TitleShowingPopupDelegate.TitleRole)


VALID_URL_HELP = 'https://docs.google.com/spreadsheets/<DOCUMENT_ID>/'


class OWGoogleSheets(widget.OWWidget):
    name = __("name")
    description = __("desc")
    keywords = ["google sheets", "load google sheets", "sheets", "load data"]
    icon = "icons/GoogleSheets.svg"
    priority = 100
    outputs = [(i18n.t("educational.common.data"), Table)]

    want_main_area = False
    resizing_enabled = False

    recent = settings.Setting([])
    reload_idx = settings.Setting(0)
    autocommit = settings.Setting(True)

    def __init__(self):
        super().__init__()
        self.table = None

        vb = gui.vBox(self.controlArea, __("box_google_sheet"))
        hb = gui.hBox(vb)
        self.combo = combo = URLComboBox(
            hb, self.recent, editable=True, minimumWidth=400,
            insertPolicy=QComboBox.InsertAtTop,
            toolTip=__("tooltip_format") + VALID_URL_HELP,
            currentIndexChanged=lambda: QTimer.singleShot(1, self.load_url))
        hb.layout().addWidget(QLabel(__("row_url"), hb))
        hb.layout().addWidget(combo)
        hb.layout().setStretch(1, 2)

        RELOAD_TIMES = (
            (__("gbox.no_reload"),),
            (__("gbox.5s"), 5000),
            (__("gbox.10s"), 10000),
            (__("gbox.30s"), 30000),
            (__("gbox.1min"), 60 * 1000),
            (__("gbox.2min"), 2 * 60 * 1000),
            (__("gbox.5min"), 5 * 60 * 1000),
        )

        reload_timer = QTimer(self, timeout=lambda: self.load_url(from_reload=True))

        def _on_reload_changed():
            if self.reload_idx == 0:
                reload_timer.stop()
                return
            reload_timer.start(RELOAD_TIMES[self.reload_idx][1])

        gui.comboBox(vb, self, 'reload_idx', label=__("row_reload_every"),
                     orientation=Qt.Horizontal,
                     items=[i[0] for i in RELOAD_TIMES],
                     callback=_on_reload_changed)

        box = gui.widgetBox(self.controlArea, __("box_info"), addSpace=True)
        info = self.data_info = gui.widgetLabel(box, '')
        info.setWordWrap(True)
        self.controlArea.layout().addStretch(1)
        gui.auto_commit(self.controlArea, self, 'autocommit', label=__("btn_commit"))

        self.set_info()

    def set_combo_items(self):
        self.combo.clear()
        for sheet in self.recent:
            self.combo.addItem(sheet.name, sheet.url)

    def commit(self):
        self.send('Data', self.table)

    class Error(widget.OWWidget.Error):
        error = widget.Msg(__("msg_cannot_load_spreadsheet"))

    def load_url(self, from_reload=False):
        url = self.combo.currentText()
        if not url:
            return

        if url not in self.recent:
            self.recent.insert(0, url)

        prev_table = self.table
        try:
            with self.progressBar(3) as progress:
                progress.advance()
                table = Table.from_url(url)
                progress.advance()
        except Exception as e:
            log.exception(__("text.cannot_load_data"), url)
            self.Error.error(try_(lambda: e.args[0], ''))
            self.table = None
        else:
            self.Error.clear()
            self.table = table
            self.combo.setTitleFor(self.combo.currentIndex(), table.name)
        self.set_info()

        def _equal(data1, data2):
            NAN = float('nan')
            return (try_(lambda: data1.checksum(), NAN) ==
                    try_(lambda: data2.checksum(), NAN))

        if not (from_reload and _equal(prev_table, self.table)):
            self.commit()

    def set_info(self):
        data = self.table
        if data is None:
            self.data_info.setText(__("row_no_spreadsheet_load"))
            return
        text = __("text.data_instruction").format(
            data.name, len(data), len(data.domain.attributes), len(data.domain.metas))
        text += try_(lambda: __("text.data_entry").format(data[0, 'Timestamp'],
                                                          data[-1, 'Timestamp']), '')
        self.data_info.setText(text)


if __name__ == "__main__":
    a = QApplication([])
    ow = OWGoogleSheets()
    ow.show()
    a.exec_()
