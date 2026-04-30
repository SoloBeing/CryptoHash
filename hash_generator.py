import sys
import hashlib
import hmac
import binascii
import zlib
from PyQt5.QtWidgets import (
    QApplication, QMainWindow, QWidget, QVBoxLayout, QHBoxLayout,
    QLabel, QTextEdit, QLineEdit, QPushButton, QTabWidget,
    QTableWidget, QTableWidgetItem, QHeaderView, QComboBox,
    QCheckBox, QGroupBox, QGridLayout, QSplitter, QFrame,
    QScrollArea, QAction, QMenuBar, QFileDialog, QMessageBox,
    QStatusBar, QToolButton, QSizePolicy
)
from PyQt5.QtCore import Qt, QThread, pyqtSignal, QTimer, QSize
from PyQt5.QtGui import (
    QFont, QColor, QPalette, QIcon, QClipboard,
    QSyntaxHighlighter, QTextCharFormat, QFontMetrics
)


# ── Color palette ──────────────────────────────────────────────────────────
BG_DARK    = "#0d1117"
BG_PANEL   = "#161b22"
BG_INPUT   = "#1c2128"
BG_ROW_ALT = "#1a2030"
ACCENT     = "#58a6ff"
ACCENT2    = "#3fb950"
ACCENT3    = "#f78166"
BORDER     = "#30363d"
TEXT_MAIN  = "#e6edf3"
TEXT_DIM   = "#8b949e"
TEXT_HASH  = "#79c0ff"
HOVER_BG   = "#21262d"
COPY_COLOR = "#56d364"


STYLESHEET = f"""
QMainWindow, QWidget {{
    background-color: {BG_DARK};
    color: {TEXT_MAIN};
    font-family: 'Courier New', 'Consolas', monospace;
    font-size: 13px;
}}

QMenuBar {{
    background-color: {BG_PANEL};
    color: {TEXT_MAIN};
    border-bottom: 1px solid {BORDER};
    padding: 2px;
}}
QMenuBar::item:selected {{ background-color: {HOVER_BG}; }}
QMenu {{
    background-color: {BG_PANEL};
    color: {TEXT_MAIN};
    border: 1px solid {BORDER};
}}
QMenu::item:selected {{ background-color: {ACCENT}; color: #000; }}

QTabWidget::pane {{
    border: 1px solid {BORDER};
    border-top: none;
    background-color: {BG_PANEL};
}}
QTabBar::tab {{
    background-color: {BG_DARK};
    color: {TEXT_DIM};
    padding: 8px 20px;
    border: 1px solid {BORDER};
    border-bottom: none;
    margin-right: 2px;
    font-size: 12px;
    letter-spacing: 0.5px;
}}
QTabBar::tab:selected {{
    background-color: {BG_PANEL};
    color: {ACCENT};
    border-top: 2px solid {ACCENT};
}}
QTabBar::tab:hover:!selected {{ background-color: {HOVER_BG}; color: {TEXT_MAIN}; }}

QTextEdit, QLineEdit, QPlainTextEdit {{
    background-color: {BG_INPUT};
    color: {TEXT_MAIN};
    border: 1px solid {BORDER};
    border-radius: 4px;
    padding: 6px 10px;
    selection-background-color: {ACCENT};
    font-family: 'Courier New', monospace;
}}
QTextEdit:focus, QLineEdit:focus {{
    border: 1px solid {ACCENT};
}}

QPushButton {{
    background-color: {BG_INPUT};
    color: {TEXT_MAIN};
    border: 1px solid {BORDER};
    border-radius: 4px;
    padding: 6px 14px;
    font-size: 12px;
}}
QPushButton:hover {{ background-color: {HOVER_BG}; border-color: {ACCENT}; color: {ACCENT}; }}
QPushButton:pressed {{ background-color: {ACCENT}; color: #000; }}

QPushButton#primary {{
    background-color: {ACCENT};
    color: #0d1117;
    font-weight: bold;
    border: none;
}}
QPushButton#primary:hover {{ background-color: #79c0ff; }}
QPushButton#primary:pressed {{ background-color: #388bfd; }}

QPushButton#danger {{
    background-color: transparent;
    color: {ACCENT3};
    border: 1px solid {ACCENT3};
}}
QPushButton#danger:hover {{ background-color: {ACCENT3}; color: #000; }}

QPushButton#copy {{
    background-color: transparent;
    color: {TEXT_DIM};
    border: 1px solid transparent;
    padding: 2px 6px;
    font-size: 11px;
}}
QPushButton#copy:hover {{ color: {COPY_COLOR}; border-color: {COPY_COLOR}; }}

QTableWidget {{
    background-color: {BG_PANEL};
    alternate-background-color: {BG_ROW_ALT};
    gridline-color: {BORDER};
    color: {TEXT_MAIN};
    border: 1px solid {BORDER};
    border-radius: 4px;
    selection-background-color: #1f3a5f;
}}
QTableWidget::item {{ padding: 6px 10px; }}
QTableWidget::item:selected {{ background-color: #1f3a5f; color: {TEXT_MAIN}; }}
QHeaderView::section {{
    background-color: {BG_INPUT};
    color: {TEXT_DIM};
    padding: 8px 10px;
    border: none;
    border-right: 1px solid {BORDER};
    border-bottom: 1px solid {BORDER};
    font-size: 11px;
    letter-spacing: 0.8px;
    text-transform: uppercase;
}}

QGroupBox {{
    background-color: {BG_PANEL};
    border: 1px solid {BORDER};
    border-radius: 6px;
    margin-top: 10px;
    padding-top: 8px;
    font-size: 11px;
    color: {TEXT_DIM};
    letter-spacing: 0.5px;
}}
QGroupBox::title {{
    subcontrol-origin: margin;
    left: 10px;
    padding: 0 4px;
    color: {ACCENT};
    font-size: 11px;
    letter-spacing: 1px;
}}

QCheckBox {{ color: {TEXT_DIM}; spacing: 6px; }}
QCheckBox::indicator {{
    width: 14px; height: 14px;
    background-color: {BG_INPUT};
    border: 1px solid {BORDER};
    border-radius: 2px;
}}
QCheckBox::indicator:checked {{
    background-color: {ACCENT};
    border-color: {ACCENT};
}}
QCheckBox:hover {{ color: {TEXT_MAIN}; }}

QComboBox {{
    background-color: {BG_INPUT};
    color: {TEXT_MAIN};
    border: 1px solid {BORDER};
    border-radius: 4px;
    padding: 4px 8px;
}}
QComboBox::drop-down {{ border: none; width: 20px; }}
QComboBox QAbstractItemView {{
    background-color: {BG_PANEL};
    color: {TEXT_MAIN};
    border: 1px solid {BORDER};
    selection-background-color: {ACCENT};
}}

QScrollBar:vertical {{
    background-color: {BG_DARK};
    width: 8px;
    border-radius: 4px;
}}
QScrollBar::handle:vertical {{
    background-color: {BORDER};
    border-radius: 4px;
    min-height: 30px;
}}
QScrollBar::handle:vertical:hover {{ background-color: {TEXT_DIM}; }}
QScrollBar::add-line:vertical, QScrollBar::sub-line:vertical {{ height: 0; }}

QStatusBar {{
    background-color: {BG_PANEL};
    color: {TEXT_DIM};
    border-top: 1px solid {BORDER};
    font-size: 11px;
}}

QSplitter::handle {{
    background-color: {BORDER};
    width: 1px;
    height: 1px;
}}

QLabel#hash_label {{
    color: {TEXT_HASH};
    font-family: 'Courier New', monospace;
    font-size: 12px;
    word-wrap: break-word;
    padding: 4px;
}}
QLabel#algo_label {{
    color: {TEXT_DIM};
    font-size: 11px;
    font-weight: bold;
    letter-spacing: 1px;
    min-width: 90px;
}}
QFrame#hash_row {{
    background-color: {BG_INPUT};
    border: 1px solid {BORDER};
    border-radius: 4px;
    padding: 4px;
}}
QFrame#hash_row:hover {{
    border-color: {ACCENT};
}}
QFrame#separator {{
    background-color: {BORDER};
    max-height: 1px;
}}
"""


# ── Hash algorithms ────────────────────────────────────────────────────────
def compute_crc32(data: bytes) -> str:
    val = zlib.crc32(data) & 0xFFFFFFFF
    return format(val, '08x')

def compute_adler32(data: bytes) -> str:
    val = zlib.adler32(data) & 0xFFFFFFFF
    return format(val, '08x')

HASH_ALGORITHMS = [
    ("MD5",        lambda d: hashlib.md5(d).hexdigest()),
    ("SHA-1",      lambda d: hashlib.sha1(d).hexdigest()),
    ("SHA-224",    lambda d: hashlib.sha224(d).hexdigest()),
    ("SHA-256",    lambda d: hashlib.sha256(d).hexdigest()),
    ("SHA-384",    lambda d: hashlib.sha384(d).hexdigest()),
    ("SHA-512",    lambda d: hashlib.sha512(d).hexdigest()),
    ("SHA3-224",   lambda d: hashlib.sha3_224(d).hexdigest()),
    ("SHA3-256",   lambda d: hashlib.sha3_256(d).hexdigest()),
    ("SHA3-384",   lambda d: hashlib.sha3_384(d).hexdigest()),
    ("SHA3-512",   lambda d: hashlib.sha3_512(d).hexdigest()),
    ("BLAKE2b",    lambda d: hashlib.blake2b(d).hexdigest()),
    ("BLAKE2s",    lambda d: hashlib.blake2s(d).hexdigest()),
    ("CRC32",      compute_crc32),
    ("Adler-32",   compute_adler32),
]

HASH_BITS = {
    "MD5": 128, "SHA-1": 160, "SHA-224": 224, "SHA-256": 256,
    "SHA-384": 384, "SHA-512": 512, "SHA3-224": 224, "SHA3-256": 256,
    "SHA3-384": 384, "SHA3-512": 512, "BLAKE2b": 512, "BLAKE2s": 256,
    "CRC32": 32, "Adler-32": 32,
}


# ── Hash row widget ────────────────────────────────────────────────────────
class HashRow(QFrame):
    def __init__(self, algo: str, parent=None):
        super().__init__(parent)
        self.setObjectName("hash_row")
        self.algo = algo
        self._hash_value = ""

        layout = QHBoxLayout(self)
        layout.setContentsMargins(10, 6, 6, 6)
        layout.setSpacing(8)

        self.algo_lbl = QLabel(algo)
        self.algo_lbl.setObjectName("algo_label")
        self.algo_lbl.setFixedWidth(88)

        self.hash_lbl = QLabel("—")
        self.hash_lbl.setObjectName("hash_label")
        self.hash_lbl.setTextInteractionFlags(Qt.TextSelectableByMouse)
        self.hash_lbl.setWordWrap(False)
        self.hash_lbl.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Preferred)

        self.copy_btn = QPushButton("⎘ COPY")
        self.copy_btn.setObjectName("copy")
        self.copy_btn.setFixedWidth(68)
        self.copy_btn.setCursor(Qt.PointingHandCursor)
        self.copy_btn.clicked.connect(self._copy)

        layout.addWidget(self.algo_lbl)
        layout.addWidget(self.hash_lbl)
        layout.addWidget(self.copy_btn)

    def set_hash(self, value: str):
        self._hash_value = value
        if value:
            # truncate display but show full on tooltip
            display = value if len(value) <= 64 else value[:60] + "…"
            self.hash_lbl.setText(display)
            self.hash_lbl.setToolTip(value)
            self.hash_lbl.setStyleSheet(f"color: #79c0ff;")
        else:
            self.hash_lbl.setText("—")
            self.hash_lbl.setToolTip("")
            self.hash_lbl.setStyleSheet(f"color: #8b949e;")

    def _copy(self):
        if self._hash_value:
            QApplication.clipboard().setText(self._hash_value)
            self.copy_btn.setText("✓ OK")
            QTimer.singleShot(1200, lambda: self.copy_btn.setText("⎘ COPY"))


# ── Text hashing tab ───────────────────────────────────────────────────────
class TextHashTab(QWidget):
    def __init__(self, parent=None):
        super().__init__(parent)
        self._build_ui()

    def _build_ui(self):
        main = QVBoxLayout(self)
        main.setContentsMargins(14, 14, 14, 14)
        main.setSpacing(10)

        # ── Input area ──
        in_group = QGroupBox("INPUT")
        in_layout = QVBoxLayout(in_group)
        in_layout.setSpacing(8)

        self.input_edit = QTextEdit()
        self.input_edit.setPlaceholderText("Type or paste text here to hash…")
        self.input_edit.setFixedHeight(110)
        self.input_edit.textChanged.connect(self._on_text_changed)
        in_layout.addWidget(self.input_edit)

        btn_row = QHBoxLayout()
        btn_row.setSpacing(8)

        self.encoding_combo = QComboBox()
        self.encoding_combo.addItems(["UTF-8", "UTF-16", "ASCII", "Latin-1"])
        self.encoding_combo.setFixedWidth(100)
        self.encoding_combo.currentTextChanged.connect(self._on_text_changed)

        self.upper_check = QCheckBox("UPPERCASE")
        self.upper_check.stateChanged.connect(self._on_text_changed)

        clear_btn = QPushButton("✕ Clear")
        clear_btn.setObjectName("danger")
        clear_btn.setFixedWidth(80)
        clear_btn.clicked.connect(self.input_edit.clear)

        copy_all_btn = QPushButton("⎘ Copy All Hashes")
        copy_all_btn.clicked.connect(self._copy_all)

        self.char_lbl = QLabel("0 chars | 0 bytes")
        self.char_lbl.setStyleSheet(f"color: {TEXT_DIM}; font-size: 11px;")

        btn_row.addWidget(QLabel("Encoding:"))
        btn_row.addWidget(self.encoding_combo)
        btn_row.addWidget(self.upper_check)
        btn_row.addStretch()
        btn_row.addWidget(self.char_lbl)
        btn_row.addWidget(clear_btn)
        btn_row.addWidget(copy_all_btn)
        in_layout.addLayout(btn_row)

        main.addWidget(in_group)

        # ── Hash results ──
        out_group = QGroupBox("HASH RESULTS")
        out_layout = QVBoxLayout(out_group)
        out_layout.setSpacing(4)

        self._rows: dict[str, HashRow] = {}
        for algo, _ in HASH_ALGORITHMS:
            row = HashRow(algo)
            self._rows[algo] = row
            out_layout.addWidget(row)

        scroll = QScrollArea()
        scroll.setWidgetResizable(True)
        scroll_content = QWidget()
        scroll_content_layout = QVBoxLayout(scroll_content)
        scroll_content_layout.setContentsMargins(0, 0, 0, 0)
        scroll_content_layout.setSpacing(4)
        for row in self._rows.values():
            scroll_content_layout.addWidget(row)
        scroll_content_layout.addStretch()
        scroll.setWidget(scroll_content)
        scroll.setStyleSheet("QScrollArea { border: none; }")

        out_layout.addWidget(scroll)
        main.addWidget(out_group, 1)

    def _get_bytes(self) -> bytes:
        text = self.input_edit.toPlainText()
        enc = self.encoding_combo.currentText().lower().replace("-", "")
        enc_map = {"utf8": "utf-8", "utf16": "utf-16", "ascii": "ascii", "latin1": "latin-1"}
        encoding = enc_map.get(enc, "utf-8")
        try:
            return text.encode(encoding)
        except Exception:
            return text.encode("utf-8", errors="replace")

    def _on_text_changed(self):
        data = self._get_bytes()
        upper = self.upper_check.isChecked()
        char_count = len(self.input_edit.toPlainText())
        self.char_lbl.setText(f"{char_count:,} chars | {len(data):,} bytes")

        for algo, fn in HASH_ALGORITHMS:
            try:
                h = fn(data)
                if upper:
                    h = h.upper()
                self._rows[algo].set_hash(h)
            except Exception as e:
                self._rows[algo].set_hash(f"ERROR: {e}")

    def _copy_all(self):
        lines = []
        for algo, row in self._rows.items():
            if row._hash_value:
                lines.append(f"{algo:<12} {row._hash_value}")
        if lines:
            QApplication.clipboard().setText("\n".join(lines))


# ── File hashing tab ───────────────────────────────────────────────────────
class FileHashWorker(QThread):
    progress = pyqtSignal(int)
    result   = pyqtSignal(dict)
    error    = pyqtSignal(str)

    def __init__(self, path: str, algos: list):
        super().__init__()
        self.path  = path
        self.algos = algos

    def run(self):
        try:
            import os
            size = os.path.getsize(self.path)
            hashers = {name: hashlib.new(name.lower().replace("-", "").replace("3", "3_").replace("blake2b","blake2b").replace("blake2s","blake2s"))
                       for name, _ in self.algos if name not in ("CRC32", "Adler-32")}
            # Use raw hashlib for standard ones
            hashers = {}
            fns = {name: fn for name, fn in self.algos}
            chunk_hashes: dict[str, list[bytes]] = {name: [] for name in fns}

            crc_val   = 0
            adler_val = 1
            md5    = hashlib.md5()
            sha1   = hashlib.sha1()
            sha224 = hashlib.sha224()
            sha256 = hashlib.sha256()
            sha384 = hashlib.sha384()
            sha512 = hashlib.sha512()
            sha3_224 = hashlib.sha3_224()
            sha3_256 = hashlib.sha3_256()
            sha3_384 = hashlib.sha3_384()
            sha3_512 = hashlib.sha3_512()
            b2b = hashlib.blake2b()
            b2s = hashlib.blake2s()

            processed = 0
            CHUNK = 65536
            with open(self.path, "rb") as f:
                while True:
                    chunk = f.read(CHUNK)
                    if not chunk:
                        break
                    md5.update(chunk); sha1.update(chunk); sha224.update(chunk)
                    sha256.update(chunk); sha384.update(chunk); sha512.update(chunk)
                    sha3_224.update(chunk); sha3_256.update(chunk)
                    sha3_384.update(chunk); sha3_512.update(chunk)
                    b2b.update(chunk); b2s.update(chunk)
                    crc_val   = zlib.crc32(chunk, crc_val) & 0xFFFFFFFF
                    adler_val = zlib.adler32(chunk, adler_val) & 0xFFFFFFFF
                    processed += len(chunk)
                    if size > 0:
                        self.progress.emit(int(processed / size * 100))

            result = {
                "MD5": md5.hexdigest(), "SHA-1": sha1.hexdigest(),
                "SHA-224": sha224.hexdigest(), "SHA-256": sha256.hexdigest(),
                "SHA-384": sha384.hexdigest(), "SHA-512": sha512.hexdigest(),
                "SHA3-224": sha3_224.hexdigest(), "SHA3-256": sha3_256.hexdigest(),
                "SHA3-384": sha3_384.hexdigest(), "SHA3-512": sha3_512.hexdigest(),
                "BLAKE2b": b2b.hexdigest(), "BLAKE2s": b2s.hexdigest(),
                "CRC32": format(crc_val, '08x'),
                "Adler-32": format(adler_val, '08x'),
            }
            self.result.emit(result)
        except Exception as e:
            self.error.emit(str(e))


class FileHashTab(QWidget):
    def __init__(self, parent=None):
        super().__init__(parent)
        self._worker = None
        self._build_ui()

    def _build_ui(self):
        main = QVBoxLayout(self)
        main.setContentsMargins(14, 14, 14, 14)
        main.setSpacing(10)

        # File selector
        file_group = QGroupBox("FILE")
        file_layout = QVBoxLayout(file_group)

        file_row = QHBoxLayout()
        self.file_edit = QLineEdit()
        self.file_edit.setPlaceholderText("Select a file to hash…")
        self.file_edit.setReadOnly(True)
        browse_btn = QPushButton("📂 Browse")
        browse_btn.setObjectName("primary")
        browse_btn.setFixedWidth(110)
        browse_btn.clicked.connect(self._browse)
        file_row.addWidget(self.file_edit)
        file_row.addWidget(browse_btn)
        file_layout.addLayout(file_row)

        self.file_info_lbl = QLabel("")
        self.file_info_lbl.setStyleSheet(f"color: {TEXT_DIM}; font-size: 11px;")
        file_layout.addWidget(self.file_info_lbl)

        main.addWidget(file_group)

        # Progress / status
        self.status_lbl = QLabel("No file selected")
        self.status_lbl.setStyleSheet(f"color: {TEXT_DIM}; font-size: 11px;")
        main.addWidget(self.status_lbl)

        # Results table
        out_group = QGroupBox("HASH RESULTS")
        out_layout = QVBoxLayout(out_group)
        out_layout.setSpacing(4)

        self._rows: dict[str, HashRow] = {}
        scroll = QScrollArea()
        scroll.setWidgetResizable(True)
        scroll_content = QWidget()
        scroll_content_layout = QVBoxLayout(scroll_content)
        scroll_content_layout.setContentsMargins(0, 0, 0, 0)
        scroll_content_layout.setSpacing(4)
        for algo, _ in HASH_ALGORITHMS:
            row = HashRow(algo)
            self._rows[algo] = row
            scroll_content_layout.addWidget(row)
        scroll_content_layout.addStretch()
        scroll.setWidget(scroll_content)
        scroll.setStyleSheet("QScrollArea { border: none; }")
        out_layout.addWidget(scroll)
        main.addWidget(out_group, 1)

    def _browse(self):
        path, _ = QFileDialog.getOpenFileName(self, "Select File")
        if path:
            self._hash_file(path)

    def _hash_file(self, path: str):
        import os
        self.file_edit.setText(path)
        size = os.path.getsize(path)

        def fmt_size(n):
            for unit in ['B', 'KB', 'MB', 'GB', 'TB']:
                if n < 1024: return f"{n:.1f} {unit}"
                n /= 1024
            return f"{n:.1f} PB"

        name = os.path.basename(path)
        self.file_info_lbl.setText(f"  {name}  ·  {fmt_size(size)}")
        self.status_lbl.setText("⏳ Hashing…")

        for row in self._rows.values():
            row.set_hash("")

        self._worker = FileHashWorker(path, HASH_ALGORITHMS)
        self._worker.progress.connect(lambda p: self.status_lbl.setText(f"⏳ Hashing… {p}%"))
        self._worker.result.connect(self._on_result)
        self._worker.error.connect(lambda e: self.status_lbl.setText(f"❌ Error: {e}"))
        self._worker.start()

    def _on_result(self, result: dict):
        self.status_lbl.setText(f"✓ Done")
        for algo, h in result.items():
            if algo in self._rows:
                self._rows[algo].set_hash(h)


# ── Compare tab ────────────────────────────────────────────────────────────
class CompareTab(QWidget):
    def __init__(self, parent=None):
        super().__init__(parent)
        self._build_ui()

    def _build_ui(self):
        main = QVBoxLayout(self)
        main.setContentsMargins(14, 14, 14, 14)
        main.setSpacing(14)

        title = QLabel("HASH COMPARISON")
        title.setStyleSheet(f"color: {ACCENT}; font-size: 11px; letter-spacing: 2px; font-weight: bold;")
        main.addWidget(title)

        desc = QLabel("Compare two hash values to check if they match. Paste hashes below.")
        desc.setStyleSheet(f"color: {TEXT_DIM}; font-size: 12px;")
        main.addWidget(desc)

        # Hash A
        a_group = QGroupBox("HASH A")
        a_layout = QVBoxLayout(a_group)
        self.hash_a = QLineEdit()
        self.hash_a.setPlaceholderText("Paste first hash here…")
        self.hash_a.textChanged.connect(self._compare)
        a_layout.addWidget(self.hash_a)
        main.addWidget(a_group)

        # Hash B
        b_group = QGroupBox("HASH B")
        b_layout = QVBoxLayout(b_group)
        self.hash_b = QLineEdit()
        self.hash_b.setPlaceholderText("Paste second hash here…")
        self.hash_b.textChanged.connect(self._compare)
        b_layout.addWidget(self.hash_b)
        main.addWidget(b_group)

        # Result
        self.result_lbl = QLabel("")
        self.result_lbl.setAlignment(Qt.AlignCenter)
        self.result_lbl.setStyleSheet("font-size: 16px; padding: 20px;")
        main.addWidget(self.result_lbl)

        # Details
        self.detail_lbl = QLabel("")
        self.detail_lbl.setAlignment(Qt.AlignCenter)
        self.detail_lbl.setStyleSheet(f"color: {TEXT_DIM}; font-size: 11px;")
        main.addWidget(self.detail_lbl)

        main.addStretch()

    def _compare(self):
        a = self.hash_a.text().strip().lower()
        b = self.hash_b.text().strip().lower()

        if not a or not b:
            self.result_lbl.setText("")
            self.detail_lbl.setText("")
            return

        match = hmac.compare_digest(a, b)
        if match:
            self.result_lbl.setText(f"✓  MATCH")
            self.result_lbl.setStyleSheet(f"color: {ACCENT2}; font-size: 22px; font-weight: bold; padding: 20px;")
            self.detail_lbl.setText(f"Both hashes are identical  ({len(a)*4} bits)")
        else:
            self.result_lbl.setText(f"✗  MISMATCH")
            self.result_lbl.setStyleSheet(f"color: {ACCENT3}; font-size: 22px; font-weight: bold; padding: 20px;")
            # Show where they differ
            diffs = sum(1 for x, y in zip(a, b) if x != y)
            total = max(len(a), len(b))
            self.detail_lbl.setText(f"Hashes differ in {diffs} of {min(len(a), len(b))} comparable characters  (lengths: {len(a)} vs {len(b)})")


# ── HMAC tab ───────────────────────────────────────────────────────────────
class HmacTab(QWidget):
    def __init__(self, parent=None):
        super().__init__(parent)
        self._build_ui()

    def _build_ui(self):
        main = QVBoxLayout(self)
        main.setContentsMargins(14, 14, 14, 14)
        main.setSpacing(10)

        title = QLabel("HMAC — HASH-BASED MESSAGE AUTHENTICATION CODE")
        title.setStyleSheet(f"color: {ACCENT}; font-size: 11px; letter-spacing: 1.5px; font-weight: bold;")
        main.addWidget(title)

        # Message
        msg_group = QGroupBox("MESSAGE")
        msg_layout = QVBoxLayout(msg_group)
        self.msg_edit = QTextEdit()
        self.msg_edit.setPlaceholderText("Enter message…")
        self.msg_edit.setFixedHeight(80)
        self.msg_edit.textChanged.connect(self._compute)
        msg_layout.addWidget(self.msg_edit)
        main.addWidget(msg_group)

        # Key
        key_group = QGroupBox("SECRET KEY")
        key_layout = QHBoxLayout(key_group)
        self.key_edit = QLineEdit()
        self.key_edit.setPlaceholderText("Enter secret key…")
        self.key_edit.setEchoMode(QLineEdit.Password)
        self.key_edit.textChanged.connect(self._compute)
        self.show_key_btn = QPushButton("👁")
        self.show_key_btn.setFixedWidth(36)
        self.show_key_btn.setCheckable(True)
        self.show_key_btn.toggled.connect(lambda c: self.key_edit.setEchoMode(
            QLineEdit.Normal if c else QLineEdit.Password))
        key_layout.addWidget(self.key_edit)
        key_layout.addWidget(self.show_key_btn)
        main.addWidget(key_group)

        # Algorithm selector
        algo_row = QHBoxLayout()
        algo_row.addWidget(QLabel("Algorithm:"))
        self.algo_combo = QComboBox()
        self.algo_combo.addItems(["MD5", "SHA-1", "SHA-224", "SHA-256", "SHA-384", "SHA-512",
                                   "SHA3-256", "SHA3-512"])
        self.algo_combo.setCurrentText("SHA-256")
        self.algo_combo.currentTextChanged.connect(self._compute)
        self.algo_combo.setFixedWidth(130)
        algo_row.addWidget(self.algo_combo)
        algo_row.addStretch()
        main.addLayout(algo_row)

        # Result
        out_group = QGroupBox("HMAC RESULT")
        out_layout = QVBoxLayout(out_group)
        self.result_lbl = QLabel("—")
        self.result_lbl.setObjectName("hash_label")
        self.result_lbl.setTextInteractionFlags(Qt.TextSelectableByMouse)
        self.result_lbl.setWordWrap(True)
        self.result_lbl.setStyleSheet(f"color: {TEXT_HASH}; font-size: 13px; padding: 8px;")
        copy_btn = QPushButton("⎘ Copy HMAC")
        copy_btn.clicked.connect(self._copy)
        out_layout.addWidget(self.result_lbl)
        out_layout.addWidget(copy_btn)
        main.addWidget(out_group)
        main.addStretch()

    def _compute(self):
        msg = self.msg_edit.toPlainText().encode("utf-8")
        key = self.key_edit.text().encode("utf-8")
        algo = self.algo_combo.currentText().lower().replace("-", "")
        algo_map = {
            "md5": "md5", "sha1": "sha1", "sha224": "sha224",
            "sha256": "sha256", "sha384": "sha384", "sha512": "sha512",
            "sha3256": "sha3_256", "sha3512": "sha3_512",
        }
        try:
            h = hmac.new(key, msg, algo_map.get(algo, "sha256"))
            self.result_lbl.setText(h.hexdigest())
        except Exception as e:
            self.result_lbl.setText(f"Error: {e}")

    def _copy(self):
        text = self.result_lbl.text()
        if text and text != "—":
            QApplication.clipboard().setText(text)


# ── Main window ────────────────────────────────────────────────────────────
class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("CryptoHash — Cryptographic Hash Generator")
        self.resize(820, 750)
        self.setStyleSheet(STYLESHEET)
        self._build_menu()
        self._build_ui()
        self._build_status()

    def _build_menu(self):
        mb = self.menuBar()
        file_menu = mb.addMenu("File")
        open_act = QAction("Open File…", self)
        open_act.setShortcut("Ctrl+O")
        file_menu.addAction(open_act)
        file_menu.addSeparator()
        quit_act = QAction("Quit", self)
        quit_act.setShortcut("Ctrl+Q")
        quit_act.triggered.connect(self.close)
        file_menu.addAction(quit_act)

        help_menu = mb.addMenu("Help")
        about_act = QAction("About CryptoHash", self)
        about_act.triggered.connect(self._about)
        help_menu.addAction(about_act)

    def _build_ui(self):
        central = QWidget()
        self.setCentralWidget(central)
        layout = QVBoxLayout(central)
        layout.setContentsMargins(0, 0, 0, 0)
        layout.setSpacing(0)

        # Header banner
        header = QFrame()
        header.setStyleSheet(f"background-color: {BG_PANEL}; border-bottom: 1px solid {BORDER};")
        header.setFixedHeight(54)
        hlayout = QHBoxLayout(header)
        hlayout.setContentsMargins(16, 0, 16, 0)

        title = QLabel("⬡  CRYPTOHASH")
        title.setStyleSheet(f"color: {ACCENT}; font-size: 16px; font-weight: bold; letter-spacing: 3px;")
        subtitle = QLabel("Cryptographic Hash Generator")
        subtitle.setStyleSheet(f"color: {TEXT_DIM}; font-size: 11px; letter-spacing: 1px;")

        hlayout.addWidget(title)
        hlayout.addWidget(subtitle)
        hlayout.addStretch()

        algo_count = QLabel(f"{len(HASH_ALGORITHMS)} algorithms")
        algo_count.setStyleSheet(f"color: {TEXT_DIM}; font-size: 11px; background-color: {BG_INPUT}; "
                                  f"border: 1px solid {BORDER}; border-radius: 10px; padding: 2px 10px;")
        hlayout.addWidget(algo_count)
        layout.addWidget(header)

        # Tabs
        self.tabs = QTabWidget()
        self.tabs.setTabPosition(QTabWidget.North)

        self.text_tab = TextHashTab()
        self.file_tab = FileHashTab()
        self.compare_tab = CompareTab()
        self.hmac_tab = HmacTab()

        self.tabs.addTab(self.text_tab,    "  TEXT HASH  ")
        self.tabs.addTab(self.file_tab,    "  FILE HASH  ")
        self.tabs.addTab(self.compare_tab, "  COMPARE    ")
        self.tabs.addTab(self.hmac_tab,    "  HMAC       ")

        layout.addWidget(self.tabs)

    def _build_status(self):
        sb = self.statusBar()
        sb.showMessage(f"  CryptoHash v1.0  ·  {len(HASH_ALGORITHMS)} hash algorithms  ·  "
                       f"MD5 · SHA-1/256/512 · SHA3 · BLAKE2 · CRC32 · Adler-32  ·  HMAC")

    def _about(self):
        QMessageBox.about(self, "About CryptoHash",
            "<b style='color:#58a6ff;'>CryptoHash v1.0</b><br><br>"
            "A cryptographic hash generator supporting 14 algorithms.<br><br>"
            "<b>Algorithms:</b> MD5, SHA-1, SHA-224/256/384/512, "
            "SHA3-224/256/384/512, BLAKE2b/s, CRC32, Adler-32<br><br>"
            "<b>Features:</b> Text hashing, file hashing, hash comparison, HMAC generation")


def main():
    app = QApplication(sys.argv)
    app.setApplicationName("CryptoHash")
    app.setStyle("Fusion")

    # Dark palette baseline
    palette = QPalette()
    palette.setColor(QPalette.Window,          QColor(BG_DARK))
    palette.setColor(QPalette.WindowText,      QColor(TEXT_MAIN))
    palette.setColor(QPalette.Base,            QColor(BG_INPUT))
    palette.setColor(QPalette.AlternateBase,   QColor(BG_ROW_ALT))
    palette.setColor(QPalette.Text,            QColor(TEXT_MAIN))
    palette.setColor(QPalette.Button,          QColor(BG_PANEL))
    palette.setColor(QPalette.ButtonText,      QColor(TEXT_MAIN))
    palette.setColor(QPalette.Highlight,       QColor(ACCENT))
    palette.setColor(QPalette.HighlightedText, QColor("#000000"))
    app.setPalette(palette)

    win = MainWindow()
    win.show()
    sys.exit(app.exec_())


if __name__ == "__main__":
    main()
