import os
import sys

from PyQt5 import QtCore
from PyQt5.QtCore import Qt, QRegExp
from PyQt5.QtGui import QKeySequence, QFont, QPixmap, QSyntaxHighlighter, QTextCharFormat, QColor
from PyQt5.QtWidgets import QMainWindow, QApplication, QWidget, QVBoxLayout, QShortcut, QFileDialog, \
    QMessageBox, QPlainTextEdit, QLabel

class FileInfo:
    def __init__(self):
        self.parent_file_path = None
        self.file_name = None
        self.encoding = 'utf-8'
        self.saved = True
        self.modified = False

    def get_absolute_file_path(self):
        if self.parent_file_path and self.file_name:
            return os.path.join(self.parent_file_path, self.file_name)
        else:
            return None

class Highlighter(QSyntaxHighlighter):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.highlighting_rules = []
    def highlightBlock(self, text):
        for pattern, fmt in self.highlighting_rules:
            expression = QRegExp(pattern)
            index = expression.indexIn(text)
            while index >= 0:
                length = expression.matchedLength()
                self.setFormat(index, length, fmt)
                index = expression.indexIn(text, index + length)

class PythonHighlighter(Highlighter):
    """Python 语法高亮"""

    def __init__(self, parent=None):
        super().__init__(parent)
        self.init_formats()

    def init_formats(self):
        """初始化高亮格式"""

        # 关键字格式
        keyword_format = QTextCharFormat()
        keyword_format.setForeground(QColor("#0077CC"))
        keyword_format.setFontWeight(QFont.Bold)

        python_keywords = [
            'and', 'as', 'assert', 'break', 'class', 'continue',
            'def', 'del', 'elif', 'else', 'except', 'False',
            'finally', 'for', 'from', 'global', 'if', 'import',
            'in', 'is', 'lambda', 'None', 'nonlocal', 'not',
            'or', 'pass', 'raise', 'return', 'True', 'try',
            'while', 'with', 'yield', 'self'
        ]

        # 添加关键字规则
        for word in python_keywords:
            pattern = r'\b' + word + r'\b'
            self.highlighting_rules.append((pattern, keyword_format))

        # 类名格式
        class_format = QTextCharFormat()
        class_format.setForeground(QColor("#9944CC"))
        class_format.setFontWeight(QFont.Bold)
        self.highlighting_rules.append((r'\b[A-Z][a-zA-Z0-9_]*\b', class_format))

        # 函数名格式
        function_format = QTextCharFormat()
        function_format.setForeground(QColor("#DD7700"))
        self.highlighting_rules.append((r'\b\w+(?=\()', function_format))

        # 字符串格式
        string_format = QTextCharFormat()
        string_format.setForeground(QColor("#22AA22"))
        self.highlighting_rules.extend([
            (r'".*?"', string_format),
            (r"'.*?'", string_format),
            (r'""".*?"""', string_format),
            (r"'''.*?'''", string_format)
        ])

        # 注释格式
        comment_format = QTextCharFormat()
        comment_format.setForeground(QColor("#888888"))
        comment_format.setFontItalic(True)
        self.highlighting_rules.append((r'#.*$', comment_format))

        # 数字格式
        number_format = QTextCharFormat()
        number_format.setForeground(QColor("#AA5500"))
        self.highlighting_rules.append((r'\b\d+(\.\d+)?\b', number_format))

        # 装饰器格式
        decorator_format = QTextCharFormat()
        decorator_format.setForeground(QColor("#AA00AA"))
        self.highlighting_rules.append((r'@\w+', decorator_format))

class JavaHighlighter(Highlighter):
    """Java 语法高亮"""

    def __init__(self, parent=None):
        super().__init__(parent)
        self.init_formats()

    def init_formats(self):
        """初始化高亮格式"""

        # 关键字格式
        keyword_format = QTextCharFormat()
        keyword_format.setForeground(QColor("#0077CC"))
        keyword_format.setFontWeight(QFont.Bold)

        java_keywords = [
            'abstract', 'assert', 'boolean', 'break', 'byte', 'case',
            'catch', 'char', 'class', 'const', 'continue', 'default',
            'do', 'double', 'else', 'enum', 'extends', 'final',
            'finally', 'float', 'for', 'goto', 'if', 'implements',
            'import', 'instanceof', 'int', 'interface', 'long', 'native',
            'new', 'package', 'private', 'protected', 'public', 'return',
            'short', 'static', 'strictfp', 'super', 'switch', 'synchronized',
            'this', 'throw', 'throws', 'transient', 'try', 'void',
            'volatile', 'while', 'true', 'false', 'null'
        ]

        for word in java_keywords:
            pattern = r'\b' + word + r'\b'
            self.highlighting_rules.append((pattern, keyword_format))

        # 类名格式
        class_format = QTextCharFormat()
        class_format.setForeground(QColor("#9944CC"))
        class_format.setFontWeight(QFont.Bold)
        self.highlighting_rules.append((r'\b[A-Z][a-zA-Z0-9_]*\b', class_format))

        # 字符串格式
        string_format = QTextCharFormat()
        string_format.setForeground(QColor("#22AA22"))
        self.highlighting_rules.extend([
            (r'".*?"', string_format),
            (r"'.'", string_format)
        ])

        # 注释格式
        comment_format = QTextCharFormat()
        comment_format.setForeground(QColor("#888888"))
        comment_format.setFontItalic(True)
        self.highlighting_rules.extend([
            (r'//.*$', comment_format),
            (r'/\*.*?\*/', comment_format)
        ])

        # 数字格式
        number_format = QTextCharFormat()
        number_format.setForeground(QColor("#AA5500"))
        self.highlighting_rules.append((r'\b\d+(\.\d+)?[fFlL]?\b', number_format))

class JavaScriptHighlighter(Highlighter):
    """JavaScript 语法高亮"""

    def __init__(self, parent=None):
        super().__init__(parent)
        self.init_formats()

    def init_formats(self):
        """初始化高亮格式"""

        # 关键字格式
        keyword_format = QTextCharFormat()
        keyword_format.setForeground(QColor("#0077CC"))
        keyword_format.setFontWeight(QFont.Bold)

        js_keywords = [
            'break', 'case', 'catch', 'class', 'const', 'continue',
            'debugger', 'default', 'delete', 'do', 'else', 'export',
            'extends', 'finally', 'for', 'function', 'if', 'import',
            'in', 'instanceof', 'let', 'new', 'return', 'super',
            'switch', 'this', 'throw', 'try', 'typeof', 'var',
            'void', 'while', 'with', 'yield', 'true', 'false',
            'null', 'undefined', 'NaN', 'Infinity'
        ]

        for word in js_keywords:
            pattern = r'\b' + word + r'\b'
            self.highlighting_rules.append((pattern, keyword_format))

        # 字符串格式
        string_format = QTextCharFormat()
        string_format.setForeground(QColor("#22AA22"))
        self.highlighting_rules.extend([
            (r'".*?"', string_format),
            (r"'.*?'", string_format),
            (r'`.*?`', string_format)
        ])

        # 注释格式
        comment_format = QTextCharFormat()
        comment_format.setForeground(QColor("#888888"))
        comment_format.setFontItalic(True)
        self.highlighting_rules.extend([
            (r'//.*$', comment_format),
            (r'/\*.*?\*/', comment_format)
        ])

        # 函数格式
        function_format = QTextCharFormat()
        function_format.setForeground(QColor("#DD7700"))
        self.highlighting_rules.append((r'\b\w+(?=\()', function_format))

class CppHighlighter(Highlighter):
    """C++ 语法高亮"""

    def __init__(self, parent=None):
        super().__init__(parent)
        self.init_formats()

    def init_formats(self):
        """初始化高亮格式"""

        # 关键字格式
        keyword_format = QTextCharFormat()
        keyword_format.setForeground(QColor("#0077CC"))
        keyword_format.setFontWeight(QFont.Bold)

        cpp_keywords = [
            'alignas', 'alignof', 'and', 'and_eq', 'asm', 'auto',
            'bitand', 'bitor', 'bool', 'break', 'case', 'catch',
            'char', 'char8_t', 'char16_t', 'char32_t', 'class',
            'compl', 'concept', 'const', 'consteval', 'constexpr',
            'const_cast', 'continue', 'co_await', 'co_return',
            'co_yield', 'decltype', 'default', 'delete', 'do',
            'double', 'dynamic_cast', 'else', 'enum', 'explicit',
            'export', 'extern', 'false', 'float', 'for', 'friend',
            'goto', 'if', 'inline', 'int', 'long', 'mutable',
            'namespace', 'new', 'noexcept', 'not', 'not_eq',
            'nullptr', 'operator', 'or', 'or_eq', 'private',
            'protected', 'public', 'register', 'reinterpret_cast',
            'requires', 'return', 'short', 'signed', 'sizeof',
            'static', 'static_assert', 'static_cast', 'struct',
            'switch', 'template', 'this', 'thread_local', 'throw',
            'true', 'try', 'typedef', 'typeid', 'typename',
            'union', 'unsigned', 'using', 'virtual', 'void',
            'volatile', 'wchar_t', 'while', 'xor', 'xor_eq'
        ]

        for word in cpp_keywords:
            pattern = r'\b' + word + r'\b'
            self.highlighting_rules.append((pattern, keyword_format))

        # 预处理器格式
        preprocessor_format = QTextCharFormat()
        preprocessor_format.setForeground(QColor("#AA00AA"))
        self.highlighting_rules.append((r'^#.*$', preprocessor_format))

        # 字符串格式
        string_format = QTextCharFormat()
        string_format.setForeground(QColor("#22AA22"))
        self.highlighting_rules.append((r'".*?"', string_format))

        # 注释格式
        comment_format = QTextCharFormat()
        comment_format.setForeground(QColor("#888888"))
        comment_format.setFontItalic(True)
        self.highlighting_rules.extend([
            (r'//.*$', comment_format),
            (r'/\*.*?\*/', comment_format)
        ])

class HtmlHighlighter(Highlighter):
    """HTML 语法高亮"""

    def __init__(self, parent=None):
        super().__init__(parent)
        self.init_formats()

    def init_formats(self):
        """初始化高亮格式"""

        # 标签格式
        tag_format = QTextCharFormat()
        tag_format.setForeground(QColor("#0077CC"))
        self.highlighting_rules.append((r'<\/?\w+[^>]*>', tag_format))

        # 属性名格式
        attr_name_format = QTextCharFormat()
        attr_name_format.setForeground(QColor("#9944CC"))
        self.highlighting_rules.append((r'\b(\w+)=', attr_name_format))

        # 属性值格式
        attr_value_format = QTextCharFormat()
        attr_value_format.setForeground(QColor("#22AA22"))
        self.highlighting_rules.append((r'"[^"]*"', attr_value_format))

        # 注释格式
        comment_format = QTextCharFormat()
        comment_format.setForeground(QColor("#888888"))
        comment_format.setFontItalic(True)
        self.highlighting_rules.append((r'<!--.*?-->', comment_format))

class MarkdownHighlighter(Highlighter):
    """Markdown 语法高亮"""

    def __init__(self, parent=None):
        super().__init__(parent)
        self.init_formats()

    def init_formats(self):
        """初始化高亮格式"""

        # 标题格式
        header_format = QTextCharFormat()
        header_format.setForeground(QColor("#0077CC"))
        header_format.setFontWeight(QFont.Bold)
        self.highlighting_rules.extend([
            (r'^#{1,6}\s.*$', header_format),
            (r'^=+$', header_format),
            (r'^-+$', header_format)
        ])

        # 粗体格式
        bold_format = QTextCharFormat()
        bold_format.setFontWeight(QFont.Bold)
        self.highlighting_rules.extend([
            (r'\*\*.*?\*\*', bold_format),
            (r'__.*?__', bold_format)
        ])

        # 斜体格式
        italic_format = QTextCharFormat()
        italic_format.setFontItalic(True)
        self.highlighting_rules.extend([
            (r'\*.*?\*', italic_format),
            (r'_.*?_', italic_format)
        ])

        # 代码块格式
        code_format = QTextCharFormat()
        code_format.setForeground(QColor("#22AA22"))
        code_format.setFontFamily("Consolas")
        self.highlighting_rules.extend([
            (r'`.*?`', code_format),
            (r'^    .*$', code_format),
            (r'^\t.*$', code_format)
        ])

        # 链接格式
        link_format = QTextCharFormat()
        link_format.setForeground(QColor("#AA5500"))
        self.highlighting_rules.extend([
            (r'\[.*?\]\(.*?\)', link_format),
            (r'\[.*?\]:.*$', link_format)
        ])

class MainGui(QMainWindow):
    def __init__(self):
        super().__init__()
        self.highlighter = None
        self.background_label = None
        self.text_edit = None
        self.background_pixmap = None
        self.file_info = FileInfo()
        self.language_map = {
            '.py': 'Python',
            '.pyw': 'Python',
            '.java': 'Java',
            '.js': 'JavaScript',
            '.jsx': 'JavaScript',
            '.cpp': 'C++',
            '.cc': 'C++',
            '.cxx': 'C++',
            '.h': 'C++',
            '.hpp': 'C++',
            '.html': 'HTML',
            '.htm': 'HTML',
            '.md': 'Markdown',
            '.markdown': 'Markdown',
            '.txt': 'None'
        }
        self.highlighters = {
            'Python': PythonHighlighter,
            'Java': JavaHighlighter,
            'JavaScript': JavaScriptHighlighter,
            'C++': CppHighlighter,
            'HTML': HtmlHighlighter,
            'Markdown': MarkdownHighlighter,
            'None': None
        }
        self.init_ui()

    def init_ui(self):
        self.size_position()
        self.del_title()
        self.setup_background()
        self.editor()
        self.setup_shortcuts()
        self.text_edit.textChanged.connect(self.on_text_changed)
        self.highlight()

    def del_title(self):
        self.setWindowFlag(QtCore.Qt.FramelessWindowHint)

    def size_position(self):
        self.setMinimumSize(600, 400)
        qr = self.frameGeometry()
        cp = QApplication.desktop().availableGeometry().center()
        qr.moveCenter(cp)
        self.move(qr.topLeft())

    def highlight(self):
        if self.highlighter:
            self.highlighter.setDocument(None)
            self.highlighter = None
        language = self.change_language()
        if language != "None" and language in self.highlighters:
            highlighter_class = self.highlighters[language]
            if highlighter_class:
                self.highlighter = highlighter_class(self.text_edit.document())

    def change_language(self):
        file_path = self.file_info.get_absolute_file_path()
        if not file_path:
            return "None"

        _, ext = os.path.splitext(file_path)  # 从完整文件路径获取扩展名
        language = self.language_map.get(ext.lower(), "None")
        return language

    def setup_background(self):
        self.background_label = QLabel(self)
        pixmap = QPixmap(r"./background.jpeg")
        if pixmap.isNull():
            self.background_label.setStyleSheet("background-color: #2c3e50;")
        else:
            self.background_label.setScaledContents(False)  # 重要：不要自动缩放
            self.background_label.setPixmap(pixmap)
        self.background_label.setGeometry(0, 0, self.width(), self.height())
        self.background_label.lower()

    def update_background(self):
        if not self.background_label or not self.background_label.pixmap():
            return
        window_size = self.size()
        if window_size.width() == 0 or window_size.height() == 0:
            return
        original_pixmap = self.background_label.pixmap()
        if original_pixmap.isNull():
            return
        scaled_pixmap = original_pixmap.scaled(
            window_size.width(),
            window_size.height(),
            Qt.KeepAspectRatioByExpanding,
            Qt.SmoothTransformation
        )

        if (scaled_pixmap.width() > window_size.width() or
                scaled_pixmap.height() > window_size.height()):
            x = (scaled_pixmap.width() - window_size.width()) // 2
            y = (scaled_pixmap.height() - window_size.height()) // 2
            scaled_pixmap = scaled_pixmap.copy(
                x, y, window_size.width(), window_size.height()
            )
        self.background_label.setPixmap(scaled_pixmap)

    def resizeEvent(self, event):
        super().resizeEvent(event)
        if self.background_label:
            self.background_label.setGeometry(0, 0, self.width(), self.height())
            self.update_background()

    def editor(self):
        central_widget = QWidget()
        self.setCentralWidget(central_widget)
        layout = QVBoxLayout(central_widget)
        layout.setContentsMargins(0, 0, 0, 0)
        self.text_edit = QPlainTextEdit()
        layout.addWidget(self.text_edit)
        self.text_edit.setVerticalScrollBarPolicy(Qt.ScrollBarAlwaysOff)
        self.text_edit.setHorizontalScrollBarPolicy(Qt.ScrollBarAlwaysOff)
        font = QFont("Consolas", 11)
        self.text_edit.setFont(font)
        self.text_edit.setStyleSheet("""
            QPlainTextEdit {
                background-color: rgba(255, 255, 255, 0.7);
                border: 1px solid rgba(255, 255, 255, 0.2);
            }
        """)

    def setup_shortcuts(self):
        quit_shortcut = QShortcut(QKeySequence("Ctrl+Q"), self)
        quit_shortcut.activated.connect(self.close)
        save_shortcut = QShortcut(QKeySequence("Ctrl+S"), self)
        save_shortcut.activated.connect(self.save)
        open_shortcut = QShortcut(QKeySequence("Ctrl+O"), self)
        open_shortcut.activated.connect(self.open)
        maximize_shortcut = QShortcut(QKeySequence("Ctrl+M"), self)
        maximize_shortcut.activated.connect(self.toggle_maximize)
        minimize_shortcut = QShortcut(QKeySequence("Ctrl+N"), self)
        minimize_shortcut.activated.connect(self.showMinimized)

    def toggle_maximize(self):
        if self.isMaximized():
            self.showNormal()
        else:
            self.showMaximized()

    def on_text_changed(self):
        if not self.file_info.modified:
            self.file_info.modified = True

    def save(self):
        file_path = self.file_info.get_absolute_file_path()
        if file_path and os.path.exists(file_path):
            try:
                with open(str(file_path), "w", encoding=self.file_info.encoding) as file:
                    file.write(self.text_edit.toPlainText())
                    self.file_info.saved = True
                    self.file_info.modified = False
                    return True
            except Exception as e:
                print(e)
                return False
        else:
            abs_file_path, _ = QFileDialog.getSaveFileName(
                self, "save", "", "all file (*.*)"
            )
            if abs_file_path:
                parent_file_path = os.path.dirname(abs_file_path)
                file_name = os.path.basename(abs_file_path)
                if not os.path.exists(parent_file_path):
                    os.makedirs(parent_file_path, exist_ok=True)
                try:
                    with open(abs_file_path, "w", encoding=self.file_info.encoding) as file:
                        file.write(self.text_edit.toPlainText())
                        self.file_info.parent_file_path = parent_file_path
                        self.file_info.file_name = file_name
                        self.file_info.saved = True
                        self.file_info.modified = False
                        self.highlight()
                        return True
                except Exception as e:
                    print(e)
                    return False
            return False

    def open(self):
        if self.file_info.modified:
            file_name = self.file_info.file_name or "untitled file"
            reply = QMessageBox.question(
                self,
                f"save {file_name}?",
                QMessageBox.Yes | QMessageBox.No | QMessageBox.Cancel,
                QMessageBox.Yes
            )
            if reply == QMessageBox.Yes:
                if not self.save():
                    return
            elif reply == QMessageBox.Cancel:
                return
        abs_file_path, _ = QFileDialog.getOpenFileName(
            self, "open", "", "all file (*.*)"
        )
        if abs_file_path:
            try:
                with open(str(abs_file_path), "r", encoding=self.file_info.encoding) as file:
                    content = file.read()
                    self.text_edit.setPlainText(content)
                    self.file_info.parent_file_path = os.path.dirname(abs_file_path)
                    self.file_info.file_name = os.path.basename(abs_file_path)
                    self.file_info.saved = True
                    self.file_info.modified = False
                    self.highlight()
            except Exception as e:
                print(e)

    def closeEvent(self, event):
        if self.file_info.modified:
            file_name = self.file_info.file_name or "untitled file"
            reply = QMessageBox.question(
                self,
                "Save changes?",
                f"Do you want to save changes to {file_name}?",
                QMessageBox.Save | QMessageBox.Discard | QMessageBox.Cancel,
                QMessageBox.Save
            )
            if reply == QMessageBox.Save:
                if self.save():
                    event.accept()
                else:
                    event.ignore()
            elif reply == QMessageBox.Discard:
                event.accept()
            else:
                event.ignore()
        else:
            event.accept()

if __name__ == '__main__':
    app = QApplication(sys.argv)
    window = MainGui()
    window.show()
    sys.exit(app.exec_())