import sys
import random
import json
import os
import math
import requests
from PyQt5.QtWidgets import (QApplication, QMainWindow, QVBoxLayout, QWidget,
                             QTextEdit, QLineEdit, QPushButton, QLabel,
                             QRadioButton, QButtonGroup, QHBoxLayout, QScrollArea)
from PyQt5.QtCore import Qt, QTimer, QTranslator, QLocale, QRect, QSize
from PyQt5.QtGui import QFont, QPainter, QColor, QPixmap, QImage
import pygame
from pygame import gfxdraw

# Configuration setup
CONFIG_DIR = "config"
CONFIG_FILE = os.path.join(CONFIG_DIR, "settings.json")
os.makedirs(CONFIG_DIR, exist_ok=True)

# Textos traducibles
TRANSLATION_TEXTS = {
    "window_title": "CharlieCharlie MultiLingual",
    "ask_question": "Ask your question...",
    "btn_ask": "Ask",
    "btn_exit": "Exit",
    "select_language": "Select your language",
    "btn_once": "Just this time",
    "btn_always": "Always",
    "welcome_message": "Ask your question...",
    "exit_question": "Can I exit?",
    "phrases": [
        "The spirits say no",
        "The answer is unclear",
        "Try again later",
        "The wind whispers no",
        "Not at this time",
        "The demons forbid it",
        "The veil is too thick",
        "The answer lies elsewhere",
        "The chalk circle trembles",
        "The pencil moves against your will"
    ]
}

class GlitchEffect:
    def __init__(self, width, height):
        self.width = width
        self.height = height
        self.glitch_timer = 0
        self.glitch_intensity = 0

    def update(self):
        self.glitch_timer += 1
        if random.random() < 0.1:
            self.glitch_intensity = random.randint(1, 3)

        if self.glitch_intensity > 0:
            self.glitch_intensity -= 0.1
            return True
        return False

    def apply_glitch(self, pixmap):
        if self.glitch_intensity <= 0:
            return pixmap

        # Convert QPixmap to QImage
        image = pixmap.toImage()

        # Apply simple glitch effects without pygame
        for _ in range(int(10 * self.glitch_intensity)):
            # Random pixel manipulation
            x = random.randint(0, image.width()-1)
            y = random.randint(0, image.height()-1)
            color = QColor(image.pixel(x, y))

            # Random color distortion
            if random.random() < 0.5:
                r, g, b = color.red(), color.green(), color.blue()
                channel = random.randint(0, 2)
                if channel == 0:
                    r = max(0, min(255, r + random.randint(-50, 50)))
                elif channel == 1:
                    g = max(0, min(255, g + random.randint(-50, 50)))
                else:
                    b = max(0, min(255, b + random.randint(-50, 50)))
                color.setRgb(r, g, b)
                image.setPixelColor(x, y, color)

            # Random horizontal line shift
            if random.random() < 0.3 and self.glitch_intensity > 1.5:
                shift = random.randint(1, 5)
                y_start = random.randint(0, image.height()-10)
                height = random.randint(1, 10)
                for y_line in range(y_start, min(y_start+height, image.height())):
                    for x_line in range(image.width()):
                        new_x = (x_line + shift) % image.width()
                        color = QColor(image.pixel(new_x, y_line))
                        image.setPixelColor(x_line, y_line, color)

        return QPixmap.fromImage(image)

class GoogleTranslator:
    @staticmethod
    def translate(text, target_lang):
        try:
            if target_lang == "en":  # No need to translate English
                return text

            url = "https://translate.googleapis.com/translate_a/single"
            params = {
                'client': 'gtx',
                'sl': 'auto',
                'tl': target_lang,
                'dt': 't',
                'q': text
            }
            response = requests.get(url, params=params, timeout=3)
            if response.status_code == 200:
                result = response.json()
                return result[0][0][0]
            return text
        except Exception as e:
            print(f"Translation error: {e}")
            return text

class CharlieCharlieGame(QMainWindow):
    def __init__(self):
        super().__init__()
        self.translator = QTranslator()
        self.current_language = "en"
        self.translated_texts = TRANSLATION_TEXTS.copy()
        self.load_config()

        self.setWindowTitle(self.translated_texts["window_title"])
        self.setGeometry(100, 100, 500, 600)

        # Game state
        self.game_active = False
        self.exit_allowed = False
        self.close_attempts = 0
        self.glitch_effect = GlitchEffect(500, 600)

        # Initialize UI
        self.init_ui()

        # Show language selection if no config
        if not hasattr(self, 'saved_language'):
            self.show_language_selection()
        else:
            self.set_language(self.saved_language)
            self.start_game()

    def init_ui(self):
        # Central widget
        self.central_widget = QWidget()
        self.setCentralWidget(self.central_widget)

        # Main layout
        self.main_layout = QVBoxLayout()
        self.central_widget.setLayout(self.main_layout)

        # Game title
        self.title_label = QLabel("CharlieCharlie")
        self.title_label.setAlignment(Qt.AlignCenter)
        self.title_label.setStyleSheet("font-size: 32px; font-weight: bold; color: #8B0000;")
        self.main_layout.addWidget(self.title_label)

        # Response display
        self.response_display = QTextEdit()
        self.response_display.setReadOnly(True)
        self.response_display.setAlignment(Qt.AlignCenter)
        self.response_display.setStyleSheet("""
            QTextEdit {
                font-size: 28px;
                font-weight: bold;
                text-align: center;
                border: 3px solid #8B0000;
                border-radius: 15px;
                padding: 30px;
                background-color: black;
                color: #8B0000;
                min-height: 150px;
            }
        """)
        self.main_layout.addWidget(self.response_display)

        # Input field
        self.input_field = QLineEdit()
        self.input_field.setPlaceholderText(self.translated_texts["ask_question"])
        self.input_field.setStyleSheet("""
            QLineEdit {
                font-size: 16px;
                padding: 10px;
                border: 2px solid #8B0000;
                border-radius: 8px;
                background-color: black;
                color: white;
            }
        """)
        self.main_layout.addWidget(self.input_field)

        # Buttons layout
        buttons_layout = QHBoxLayout()

        # Send button
        self.send_button = QPushButton(self.translated_texts["btn_ask"])
        self.send_button.setStyleSheet("""
            QPushButton {
                font-size: 18px;
                padding: 12px;
                background-color: #8B0000;
                color: white;
                border: none;
                border-radius: 8px;
                min-width: 120px;
            }
            QPushButton:hover {
                background-color: #A52A2A;
            }
            QPushButton:pressed {
                background-color: #600000;
            }
        """)
        self.send_button.clicked.connect(self.process_input)
        buttons_layout.addWidget(self.send_button)

        # Exit button
        self.exit_button = QPushButton(self.translated_texts["btn_exit"])
        self.exit_button.setStyleSheet("""
            QPushButton {
                font-size: 18px;
                padding: 12px;
                background-color: #333;
                color: white;
                border: none;
                border-radius: 8px;
                min-width: 120px;
            }
            QPushButton:hover {
                background-color: #555;
            }
            QPushButton:pressed {
                background-color: #111;
            }
        """)
        self.exit_button.clicked.connect(self.request_exit)
        buttons_layout.addWidget(self.exit_button)

        self.main_layout.addLayout(buttons_layout)

        # Language selection widgets (hidden by default)
        self.language_group = QButtonGroup()
        self.language_layout = QVBoxLayout()

        self.lang_title = QLabel(self.translated_texts["select_language"])
        self.lang_title.setStyleSheet("font-size: 20px; color: #8B0000;")
        self.lang_title.setAlignment(Qt.AlignCenter)
        self.language_layout.addWidget(self.lang_title)

        # Scroll area for languages
        scroll = QScrollArea()
        scroll.setWidgetResizable(True)
        scroll.setStyleSheet("background: transparent; border: none;")

        languages_widget = QWidget()
        languages_layout = QVBoxLayout(languages_widget)

        languages = [
            ("English", "en"),
            ("Español", "es"),
            ("Français", "fr"),
            ("Deutsch", "de"),
            ("Italiano", "it"),
            ("Português", "pt"),
            ("日本語", "ja"),
            ("中文", "zh"),
            ("Русский", "ru"),
            ("العربية", "ar")
        ]

        for name, code in languages:
            rb = QRadioButton(name)
            rb.code = code
            rb.setStyleSheet("""
                QRadioButton {
                    color: white;
                    font-size: 16px;
                    padding: 8px;
                    margin: 2px;
                }
                QRadioButton::indicator {
                    width: 20px;
                    height: 20px;
                }
            """)
            self.language_group.addButton(rb)
            languages_layout.addWidget(rb)

        scroll.setWidget(languages_widget)
        self.language_layout.addWidget(scroll)

        self.lang_buttons_layout = QHBoxLayout()

        self.once_button = QPushButton(self.translated_texts["btn_once"])
        self.once_button.setStyleSheet(self.send_button.styleSheet())
        self.once_button.clicked.connect(lambda: self.save_language(False))
        self.lang_buttons_layout.addWidget(self.once_button)

        self.always_button = QPushButton(self.translated_texts["btn_always"])
        self.always_button.setStyleSheet(self.send_button.styleSheet())
        self.always_button.clicked.connect(lambda: self.save_language(True))
        self.lang_buttons_layout.addWidget(self.always_button)

        self.language_layout.addLayout(self.lang_buttons_layout)

        self.language_widget = QWidget()
        self.language_widget.setLayout(self.language_layout)
        self.main_layout.addWidget(self.language_widget)

        # Hide game widgets initially
        self.toggle_game_ui(False)

        # Set main stylesheet
        self.setStyleSheet("""
            QMainWindow {
                background-color: black;
            }
            QScrollArea > QWidget > QWidget {
                background: transparent;
            }
        """)

    def paintEvent(self, event):
        super().paintEvent(event)
        if self.glitch_effect.update():
            painter = QPainter(self)
            try:
                pixmap = self.central_widget.grab()
                glitched_pixmap = self.glitch_effect.apply_glitch(pixmap)
                painter.drawPixmap(0, 0, glitched_pixmap)
            finally:
                painter.end()

    def toggle_game_ui(self, show):
        self.title_label.setVisible(show)
        self.response_display.setVisible(show)
        self.input_field.setVisible(show)
        self.send_button.setVisible(show)
        self.exit_button.setVisible(show)
        self.language_widget.setVisible(not show)

    def show_language_selection(self):
        self.toggle_game_ui(False)
        self.language_widget.setVisible(True)

    def save_language(self, save_to_config):
        selected_button = self.language_group.checkedButton()
        if selected_button:
            lang_code = selected_button.code
            if save_to_config:
                self.save_config(lang_code)
            self.set_language(lang_code)
            self.start_game()

    def set_language(self, lang_code):
        self.current_language = lang_code
        self.translate_ui()

    def translate_ui(self):
        # Translate all UI texts
        for key in TRANSLATION_TEXTS:
            if isinstance(TRANSLATION_TEXTS[key], list):
                self.translated_texts[key] = [
                    GoogleTranslator.translate(text, self.current_language)
                    for text in TRANSLATION_TEXTS[key]
                ]
            else:
                self.translated_texts[key] = GoogleTranslator.translate(
                    TRANSLATION_TEXTS[key], self.current_language)

        # Update UI elements
        self.setWindowTitle(self.translated_texts["window_title"])
        self.input_field.setPlaceholderText(self.translated_texts["ask_question"])
        self.send_button.setText(self.translated_texts["btn_ask"])
        self.exit_button.setText(self.translated_texts["btn_exit"])
        self.lang_title.setText(self.translated_texts["select_language"])
        self.once_button.setText(self.translated_texts["btn_once"])
        self.always_button.setText(self.translated_texts["btn_always"])

    def start_game(self):
        self.toggle_game_ui(True)
        self.game_active = True
        self.response_display.setPlainText(self.translated_texts["welcome_message"])

    def process_input(self):
        if not self.game_active:
            return

        question = self.input_field.text().strip()
        self.input_field.clear()

        if not question:
            return

        # Check if asking to exit
        exit_phrases = [
            GoogleTranslator.translate("exit", self.current_language),
            GoogleTranslator.translate("leave", self.current_language),
            GoogleTranslator.translate("quit", self.current_language),
            GoogleTranslator.translate("stop", self.current_language),
            GoogleTranslator.translate("end", self.current_language),
            GoogleTranslator.translate("close", self.current_language)
        ]

        if any(phrase in question.lower() for phrase in exit_phrases):
            self.handle_exit_request()
        else:
            # Random response
            response = random.choice(["SÍ", "NO"]) if self.current_language == "es" else random.choice(["YES", "NO"])
            self.response_display.setPlainText(response)
            self.animate_response()

    def handle_exit_request(self):
        response = random.choice(["SÍ", "NO"]) if self.current_language == "es" else random.choice(["YES", "NO"])
        self.response_display.setPlainText(response)

        if response in ["SÍ", "YES"]:
            self.exit_allowed = True
            QTimer.singleShot(1000, self.close)
        else:
            self.animate_response()

    def request_exit(self):
        self.input_field.setText(self.translated_texts["exit_question"])
        self.process_input()

    def animate_response(self):
        # Flash animation
        for i in range(3):
            QTimer.singleShot(i * 100, lambda: self.response_display.setStyleSheet(
                self.response_display.styleSheet().replace("color: #8B0000", "color: white")
            ))
            QTimer.singleShot(i * 100 + 50, lambda: self.response_display.setStyleSheet(
                self.response_display.styleSheet().replace("color: white", "color: #8B0000")
            ))

    def closeEvent(self, event):
        if self.exit_allowed:
            event.accept()
            return

        event.ignore()
        self.close_attempts += 1

        if self.close_attempts >= 20:
            self.exit_allowed = True
            self.close()
            return

        # Show random phrase
        phrases = self.translated_texts["phrases"]
        self.response_display.setPlainText(random.choice(phrases))
        self.animate_response()

        # Schedule next attempt
        QTimer.singleShot(500, lambda: self.closeEvent(event))

    def load_config(self):
        try:
            if os.path.exists(CONFIG_FILE):
                with open(CONFIG_FILE, 'r') as f:
                    config = json.load(f)
                    self.saved_language = config.get('language', 'en')
        except:
            self.saved_language = 'en'

    def save_config(self, language):
        try:
            with open(CONFIG_FILE, 'w') as f:
                json.dump({'language': language}, f)
        except:
            pass

if __name__ == "__main__":
    app = QApplication(sys.argv)
    app.setFont(QFont("Arial", 12))

    # Set dark palette
    palette = app.palette()
    palette.setColor(palette.Window, Qt.black)
    palette.setColor(palette.WindowText, Qt.white)
    palette.setColor(palette.Base, Qt.black)
    palette.setColor(palette.Text, Qt.white)
    app.setPalette(palette)

    window = CharlieCharlieGame()
    window.show()
    sys.exit(app.exec_())
