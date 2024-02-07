import os
from typing import Callable, Iterable, Literal, Union

from PyQt6.QtWidgets import (
    QComboBox,
    QFileDialog,
    QHBoxLayout,
    QLabel,
    QLineEdit,
    QMainWindow,
    QMessageBox,
    QPushButton,
    QVBoxLayout,
    QWidget,
)


class MainWindow(QMainWindow):
    def __init__(
        self,
        start_tvo: Callable,
        supported_languages: Iterable[str],
        device: Literal["cuda", "cpu"],
    ):
        self.whisper_sizes = ["tiny", "base", "small", "medium", "large"]
        self.device = device
        self.supported_languages = set(supported_languages)
        super().__init__()
        self.setWindowTitle(f"Video Translation and Voiceover ({device})")

        layout = QVBoxLayout()
        centralWidget = QWidget()
        centralWidget.setLayout(layout)
        self.setCentralWidget(centralWidget)

        self.input_directory_button = QPushButton("Input Directory")
        self.input_directory_button.clicked.connect(
            lambda: self.choose_directory("input")
        )
        self.output_directory_button = QPushButton("Output Directory")
        self.output_directory_button.clicked.connect(
            lambda: self.choose_directory("output")
        )

        self.subdirs_to_skip_layout = QVBoxLayout()
        self.subdirs_to_skip_input = QLineEdit()
        self.subdirs_to_skip_input.setPlaceholderText("Enter subdirectories to skip")
        self.subdirs_to_skip_input.returnPressed.connect(
            lambda: self.add_subdirectory_to_skip()
        )
        self.subdirs_to_skip_label = "Subdirectories to skip:"
        self.subdirs_to_skip_layout.addWidget(QLabel(self.subdirs_to_skip_label))
        self.subdirs_to_skip_layout.addWidget(self.subdirs_to_skip_input)

        self.tts_speed_layout = QHBoxLayout()
        self.tts_speed_input = QLineEdit()
        self.tts_speed_input.setPlaceholderText("1.0")
        self.tts_speed_input.returnPressed.connect(lambda: self.set_tts_speed())
        self.tts_speed_layout.addWidget(QLabel("TTS speed"))
        self.tts_speed_layout.addWidget(self.tts_speed_input)

        self.whisper_size_layout = QHBoxLayout()
        self.whisper_size_input = QComboBox()
        self.whisper_size_input.addItems([""] + self.whisper_sizes)
        self.whisper_size_input.currentIndexChanged.connect(
            lambda: self.select_whisper_size()
        )
        self.whisper_size_layout.addWidget(QLabel("Whisper size"))
        self.whisper_size_layout.addWidget(self.whisper_size_input)

        self.source_language_layout = QHBoxLayout()
        self.source_language_input = QLineEdit()
        self.source_language_input.setPlaceholderText("Enter source language")
        self.source_language_input.returnPressed.connect(
            lambda: self.select_source_language()
        )
        self.source_language_layout.addWidget(QLabel("Source language"))
        self.source_language_layout.addWidget(self.source_language_input)

        self.input_language_indicator_layout = QHBoxLayout()
        self.input_language_indicator_input = QLineEdit()
        self.input_language_indicator_input.setPlaceholderText(
            "Enter input language indicator"
        )
        self.input_language_indicator_input.returnPressed.connect(
            self.set_input_language_indicator
        )
        self.input_language_indicator_layout.addWidget(
            QLabel("Input language indicator")
        )
        self.input_language_indicator_layout.addWidget(
            self.input_language_indicator_input
        )

        self.output_language_indicator_layout = QHBoxLayout()
        self.output_language_indicator_input = QLineEdit()
        self.output_language_indicator_input.setPlaceholderText(
            "Enter output language indicator"
        )
        self.output_language_indicator_input.returnPressed.connect(
            self.set_output_language_indicator
        )
        self.output_language_indicator_layout.addWidget(
            QLabel("Output language indicator")
        )
        self.output_language_indicator_layout.addWidget(
            self.output_language_indicator_input
        )

        self.start_button = QPushButton()
        self.start_button.setText("START TRANSLATION AND VOICEOVER")
        self.start_button.clicked.connect(lambda: self.start(start_tvo))

        layout.addWidget(self.input_directory_button)
        layout.addWidget(self.output_directory_button)
        layout.addLayout(self.subdirs_to_skip_layout)
        layout.addLayout(self.tts_speed_layout)
        layout.addLayout(self.whisper_size_layout)
        layout.addLayout(self.source_language_layout)
        layout.addLayout(self.input_language_indicator_layout)
        layout.addLayout(self.output_language_indicator_layout)
        layout.addWidget(self.start_button)

        self.align_label_sizes(centralWidget)

        self.input_directory: str = ""
        self.output_directory: str = ""
        self.subdirs_to_skip: list[str] = list()
        self.tts_speed: float = 1.0
        self.whisper_size: str = ""
        self.source_language: str = ""
        self.input_language_indicator: str = ""
        self.output_language_indicator: str = ""

    def start(self, start_tvo: Callable):
        errors: list[str] = list()
        if not os.path.isdir(self.input_directory):
            errors.append("Selected input directory is not a valid directory!")
        if not os.path.isdir(self.output_directory):
            errors.append("Selected output directory is not a valid directory!")
        if self.whisper_size not in self.whisper_sizes:
            errors.append("Selected whisper size is not valid!")
        if self.source_language not in self.supported_languages:
            errors.append("Selected language is not supported!")

        if not errors:
            start_tvo(
                self.input_directory,
                self.output_directory,
                self.subdirs_to_skip,
                self.tts_speed,
                self.whisper_size,
                self.source_language,
                self.input_language_indicator,
                self.output_language_indicator,
                self.device,
            )
        else:
            self.show_error_dialog("Error", "Please select all parameters:", errors)

    def align_label_sizes(self, centralWidget: QWidget):
        labels: list[QLabel] = list()
        max_width = 0
        for widget in centralWidget.children():
            if isinstance(widget, QLabel):
                if widget.text() != self.subdirs_to_skip_label:
                    width = widget.fontMetrics().boundingRect(widget.text()).width()
                    max_width = max(max_width, width)
                    labels.append(widget)
        for label in labels:
            label.setMinimumWidth(max_width)

    def choose_directory(self, directory: Literal["input", "output"]):
        dir_path = QFileDialog.getExistingDirectory(
            self, f"Select {directory} directory "
        )
        if dir_path:
            if directory == "input":
                self.input_directory = dir_path
                self.input_directory_button.setText(dir_path)
            elif directory == "output":
                self.output_directory = dir_path
                self.output_directory_button.setText(dir_path)

    def add_subdirectory_to_skip(self):
        subdir_to_skip = self.subdirs_to_skip_input.text()
        if subdir_to_skip:
            self.subdirs_to_skip.append(subdir_to_skip)
            self.subdirs_to_skip_input.setPlaceholderText(
                ",".join(self.subdirs_to_skip).lstrip(",")
            )
            self.subdirs_to_skip_input.clear()

    def set_tts_speed(self):
        try:
            self.tts_speed = float(self.tts_speed_input.text())
            self.tts_speed_input.clear()
        except ValueError:
            self.show_error_dialog("Error", "Invalid tts speed")

    def select_whisper_size(self):
        self.whisper_size = self.whisper_size_input.currentText()

    def select_source_language(self):
        language = self.source_language_input.text().strip()
        if language in self.supported_languages:
            self.source_language = language
            self.source_language_input.setPlaceholderText(language)
            self.source_language_input.clear()
        else:
            self.show_error_dialog(
                "Error",
                "Language not supported!",
                "You can see all of the supported languages at "
                + "<a href='https://github.com/openai/whisper/blob/main/whisper/tokenizer.py'>Whispers GitHub page</a>.",
            )

    def show_error_dialog(
        self,
        window_title: str,
        error_message: str,
        error_details: Union[str, list[str]] = "",
    ):
        if isinstance(error_details, list):
            error_details = "\n".join(error_details).strip()
        msgBox = QMessageBox()
        msgBox.setIcon(QMessageBox.Icon.Critical)
        msgBox.setWindowTitle(window_title)
        msgBox.setText(error_message)
        msgBox.setInformativeText(error_details)
        msgBox.setStandardButtons(QMessageBox.StandardButton.Ok)
        msgBox.setDefaultButton(QMessageBox.StandardButton.Ok)
        msgBox.exec()

    def set_input_language_indicator(self):
        language_indicator = self.input_language_indicator_input.text().strip()
        self.input_language_indicator = language_indicator
        self.input_language_indicator_input.setPlaceholderText(language_indicator)
        self.input_language_indicator_input.clear()

    def set_output_language_indicator(self):
        language_indicator = self.output_language_indicator_input.text().strip()
        self.output_language_indicator = language_indicator
        self.output_language_indicator_input.setPlaceholderText(language_indicator)
        self.output_language_indicator_input.clear()
