import sys
import random
from PyQt5.QtWidgets import (QApplication, QMainWindow, QTextEdit, QVBoxLayout, QWidget, QLineEdit)
from PyQt5.QtMultimedia import QSoundEffect
from PyQt5.QtCore import Qt, QTimer, QUrl
from PyQt5.QtGui import QFont, QColor, QTextCursor, QPainter, QPen, QPixmap, QTextBlockFormat

class CustomLineEdit(QLineEdit):
    def __init__(self, parent=None, click_sounds=None, *args, **kwargs):
        super(CustomLineEdit, self).__init__(parent, *args, **kwargs)
        self.cursor_visible = True
        self.cursor_timer = QTimer(self)
        self.cursor_timer.timeout.connect(self.blink_cursor)
        self.cursor_timer.start(500)
        self.setCursor(Qt.BlankCursor)  # Отключаем системный курсор
        self.setText("> ")  # Фиксируем символ ">" в начале строки
        self.block_position = 2  # Блокируем перемещение курсора левее позиции 2
        self.click_sounds = click_sounds

    def blink_cursor(self):
        self.cursor_visible = not self.cursor_visible
        self.update()

    def keyPressEvent(self, event):
        if event.key() == Qt.Key_Backspace and self.cursorPosition() <= self.block_position:
            return
        super().keyPressEvent(event)
        # Преобразование текста в верхний регистр
        self.setText(self.text().upper())
        self.setCursorPosition(len(self.text()))
        random_sound = random.choice(self.click_sounds)
        random_sound.play()


    def mousePressEvent(self, event):
        super().mousePressEvent(event)
        if self.cursorPosition() < self.block_position:
            self.setCursorPosition(self.block_position)

    def handle_cursor_position_changed(self, old, new):
        if new < self.block_position:
            self.setCursorPosition(self.block_position)

    def paintEvent(self, event):
        super().paintEvent(event)
        if self.cursor_visible:
            painter = QPainter(self)
            painter.setPen(Qt.NoPen)  # Убираем рамку
            painter.setPen(Qt.NoPen)
            painter.setBrush(QColor("green"))  # Устанавливаем цвет для заливки
            cursor_pos = self.cursorRect().topLeft()
            painter.drawRect(cursor_pos.x(), cursor_pos.y(), 10, self.fontMetrics().height())  # Рисуем полный квадрат


class TransparentLayer(QWidget):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setAttribute(Qt.WA_TranslucentBackground)  # Устанавливаем прозрачность фона
        self.setWindowFlags(Qt.Widget | Qt.FramelessWindowHint)
        self.setAttribute(Qt.WA_TransparentForMouseEvents)

    def paintEvent(self, event):
        painter = QPainter(self)
        painter.setOpacity(0.3) 
        pixmap = QPixmap("overlay.jpg")  # Загрузка изображения
        painter.drawPixmap(self.rect().adjusted(-10, -10, 10, 10), pixmap)
        painter.end()

class FalloutHackingTerminal(QMainWindow):
    def __init__(self):
        super().__init__()
        self.initUI()

    def initUI(self):
        self.setWindowTitle("Fallout Hacking Terminal")
        self.setGeometry(100, 100, 800, 600)

        self.terminal_font = QFont("AcPlus IBM VGA 9x8", 40, QFont.Monospace)
        self.input_font = QFont("AcPlus IBM VGA 9x8", 30, QFont.Monospace)

        self.central_widget = QWidget()
        self.setCentralWidget(self.central_widget)
        self.layout = QVBoxLayout(self.central_widget)
        self.layout.setContentsMargins(0, 0, 0, 0)
        self.layout.setSpacing(0)

        self.terminal_output = QTextEdit(self)
        self.terminal_output.setFont(self.terminal_font)
        self.terminal_output.setStyleSheet("""
            background-color: black; 
            color: green; 
            padding: 10px;
        """)
        self.terminal_output.setReadOnly(True)
        self.terminal_output.setCursor(Qt.BlankCursor)
        self.layout.addWidget(self.terminal_output)

        cursor = self.terminal_output.textCursor()
        block_format = QTextBlockFormat()
        block_format.setLineHeight(120, QTextBlockFormat.ProportionalHeight)  # Устанавливаем 150% от высоты строки
        cursor.setBlockFormat(block_format)
        self.terminal_output.setTextCursor(cursor)

        self.startup_sound = QSoundEffect()
        self.startup_sound.setSource(QUrl.fromLocalFile("sounds_poweron.wav"))  # Укажи путь к звуку старта
        self.startup_sound.setVolume(0.5)
        
        self.shutdown_sound = QSoundEffect()
        self.shutdown_sound.setSource(QUrl.fromLocalFile("sounds_poweroff.wav"))  # Укажи путь к звуку выключения
        self.shutdown_sound.setVolume(0.5)

        self.typing_sounds = []
        for i in range(1, 9):  # Предположим, у тебя есть 6 звуков печати
            sound = QSoundEffect()
            sound.setSource(QUrl.fromLocalFile(f"sounds_ui_hacking_charsingle_0{i}.wav"))
            sound.setVolume(0.2)
            self.typing_sounds.append(sound)

        self.input_line = CustomLineEdit(self, self.typing_sounds)
        self.input_line.setFont(self.input_font)
        self.input_line.setStyleSheet("""
            background-color: black; 
            color: green; 
            border: none; 
            margin: 0px; 
            padding: 5px 10px; 
        """)
        self.input_line.cursorPositionChanged.connect(self.input_line.handle_cursor_position_changed)
        self.input_line.returnPressed.connect(self.process_input)
        self.layout.addWidget(self.input_line)

        self.overlay = TransparentLayer(self)
        self.overlay.resize(self.size())

        self.possible_words = []
        self.entered_words = []
        self.state = "enter_words"
        self.current_word = ""

        self.print_timer = QTimer(self)

        self.start_animation()

    def keyPressEvent(self, event):
        self.input_line.setFocus()  # Переключаем фокус на строку ввода

    def start_animation(self):
        self.startup_sound.play()
        hacked_text = (
            "!! WARNING: SYSTEM OVERRIDE !!\n"
            "Accessing RobCo Industries (TM) Termlink [UNAUTHORIZED]\n"
            "--------------------------------------------\n"
            ">>> SECURITY PROTOCOL BREACHED <<<\n"
            "Initializing system lockdown...\n\n"
            "*** ATTEMPTING OVERRIDE ***\n"
            "......\n"
            "SYSTEM ERROR: ACCESS GRANTED\n"
            "--------------------------------------------\n\n"
            "Terminal: RobCo Industries (TM)\n"
            "Status: COMPROMISED\n"
            "--------------------------------------------\n"
            "Type commands to proceed...\n"
        )
        QTimer.singleShot(1500, lambda: self.append_terminal(hacked_text, interval=5))


    def enable_input(self):
        self.input_line.setDisabled(False)
        self.input_line.setFocus()
        self.print_timer.timeout.disconnect(self.enable_input)

    def resizeEvent(self, event):
        self.overlay.resize(self.size())
        super().resizeEvent(event)



    def generate_random_bits(self, length=4):
        return f"0x{random.randint(0, 16**length - 1):0{length}X}"


    def append_terminal(self, text, color="green", interval=50):
        self.terminal_output.moveCursor(QTextCursor.End)
        self.terminal_output.setTextColor(QColor(color))
        
        self.current_text = text
        self.current_char_index = 0
        self.print_timer = QTimer(self)
        self.print_timer.timeout.connect(lambda: self.print_character(interval))
        self.print_timer.start(interval)

    def print_character(self, interval):
        if self.current_char_index < len(self.current_text):
            char = self.current_text[self.current_char_index]
            self.terminal_output.insertPlainText(char)
            self.current_char_index += 1

            # Воспроизводим случайный звук
            typing_sound = random.choice(self.typing_sounds)
            typing_sound.play()

            # Останавливаем таймер и перезапускаем его через заданный интервал
            self.print_timer.stop()
            QTimer.singleShot(interval, self.print_timer.start)
        else:
            self.print_timer.stop()

    def display_words_and_suggest(self):
        # Очищаем текстовое поле и выводим заголовок
        self.terminal_output.clear()
        self.terminal_output.moveCursor(QTextCursor.End)
        self.terminal_output.setTextColor(QColor("green"))
        self.terminal_output.insertPlainText("Welcome to RobCo Industries (TM) Termlink\n\n")

        # Выводим слова в две колонки без анимации
        col1, col2 = "", ""
        for i, word in enumerate(self.entered_words):
            # Определяем цвет слова на основе того, подходит оно или нет
            if word in self.possible_words:
                color = "green"  # Слово подходит
                display_word = word
            else:
                color = "green"  
                display_word = '.' * len(word)

            random_bits = self.generate_random_bits()  # Генерация случайных битов в формате Fallout
            if i % 2 == 0:
                col1 = f"{random_bits} {display_word:<15}"
            else:
                col2 = f"{random_bits} {display_word:<15}"
                self.terminal_output.setTextColor(QColor(color))
                self.terminal_output.insertPlainText(f"{col1} {col2}\n\n")

        if len(self.entered_words) % 2 != 0:
            self.terminal_output.setTextColor(QColor("green" if self.entered_words[-1] in self.possible_words else "gray"))
            self.terminal_output.insertPlainText(f"{col1}\n\n")

        # Логика для предложения слова с анимацией
        letter_coverage = {word: len(set(word)) for word in self.possible_words}
        self.current_word = max(letter_coverage, key=letter_coverage.get)

        # Выводим предложенное слово с анимацией
        self.append_terminal(f"\nSuggested word: {self.current_word}\n")

    def process_input(self):
        self.input_line.setText(self.input_line.text().rstrip("█"))
        user_input = self.input_line.text()[2:].strip().upper()
        self.input_line.clear()
        self.input_line.setText("> ")

        if user_input.upper() == "N":
            self.reset_terminal()
            return
        
        if user_input.upper() == "EXIT":
            self.terminal_output.clear()
            self.append_terminal("Exiting the system...\n\nShutting down...", interval=30)
            QTimer.singleShot(1500, lambda: self.shutdown_sound.play())
            QTimer.singleShot(2000, QApplication.quit)
            return

        if self.state == "enter_words":
            self.entered_words = user_input.split()
            if self.entered_words:
                self.possible_words = self.entered_words[:]
                self.display_words_and_suggest()
                self.state = "enter_matches"
        elif self.state == "enter_matches":
            if user_input.isdigit():
                match_count = int(user_input)
                self.possible_words = [word for word in self.possible_words if self.match(self.current_word, word) == match_count]
                if not self.possible_words:
                    self.append_terminal("\nNo words left! You've failed.\n", interval=0)
                else:
                    self.display_words_and_suggest()
            else:
                self.append_terminal("\nInvalid input. Please enter a number.\n", interval=0)

    def match(self, word1, word2):
        # Логика проверки совпадений символов двух слов
        return sum(1 for a, b in zip(word1, word2) if a == b)

    def reset_terminal(self):
        self.append_terminal("\nResetting...\n")
        self.possible_words = []
        self.entered_words = []
        self.state = "enter_words"

        # Создаем таймер для задержки
        self.reset_timer = QTimer(self)
        self.reset_timer.setSingleShot(True)  # Таймер срабатывает только один раз
        self.reset_timer.timeout.connect(self.clear_terminal_after_reset)
        self.reset_timer.start(1000)  # Задержка 2 секунды (2000 миллисекунд)

    def clear_terminal_after_reset(self):
        self.terminal_output.clear()
        self.append_terminal("Welcome to RobCo Industries (TM) Termlink\n\n")

    def match(self, word1, word2):
        return sum(1 for a, b in zip(word1, word2) if a == b)

def main():
    app = QApplication(sys.argv)
    app.setOverrideCursor(Qt.BlankCursor)
    terminal = FalloutHackingTerminal()
    terminal.showFullScreen()
    sys.exit(app.exec_())

if __name__ == '__main__':
    main()
