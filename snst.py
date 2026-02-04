import sys
from PyQt5.QtWidgets import QApplication, QWidget, QVBoxLayout, QPushButton, QLineEdit, QComboBox, QLabel
import numpy as np
import sounddevice as sd

def generate_white_noise(duration, sample_rate=44100, amplitude=0.5):
    noise = amplitude * np.random.uniform(-1, 1, int(sample_rate * duration))
    return noise

def generate_sine_wave(frequency, duration, sample_rate=44100, amplitude=0.5):
    t = np.linspace(0, duration, int(sample_rate * duration), endpoint=False)
    signal = amplitude * np.sin(2 * np.pi * frequency * t)
    return signal

def play_sound(signal, sample_rate=44100):
    sd.play(signal, samplerate=sample_rate)
    sd.wait()

class CustomWindow(QWidget):
    def __init__(self):
        super().__init__()
        self.initUI()

    def initUI(self):
        layout = QVBoxLayout()

        self.comboBox = QComboBox(self)
        self.comboBox.addItems(["Синус - оба канала", "Белый шум", "Синус - правый канал", "Синус - левый канал"])

        self.textInput = QLineEdit(self)
        self.textInput2 = QLineEdit(self)

        self.button = QPushButton('Старт', self)
        self.button.clicked.connect(self.on_button_click)

        self.label1 = QLabel('', self)
        self.label2 = QLabel('', self)
        self.label3 = QLabel('', self)

        layout.addWidget(self.label1)
        layout.addWidget(self.comboBox)
        layout.addWidget(self.label2)
        layout.addWidget(self.textInput)
        layout.addWidget(self.label3)
        layout.addWidget(self.textInput2)
        layout.addWidget(self.button)

        self.setLayout(layout)
        self.setWindowTitle('SineNoiseStereoTest')
        self.setGeometry(100, 100, 200, 200)

        self.label1.setText(f'Тест')
        self.label3.setText(f'Частота (для синусов)')
        self.label2.setText(f'Длительность')
    def on_button_click(self):

        selection = self.comboBox.currentText()
        duration = int(self.textInput.text())

        if selection == "Синус - оба канала":
            frequency = int(self.textInput2.text())
            sine_wave = generate_sine_wave(frequency, duration)
            play_sound(sine_wave)

        elif selection == "Белый шум":
            noise = generate_white_noise(duration)
            play_sound(noise)

        elif selection == "Синус - правый канал":
            frequency = int(self.textInput2.text())
            t = np.linspace(0, duration, int(44100 * duration), endpoint=False)
            signal = 0.5 * np.sin(2 * np.pi * frequency * t)
            audio_data = np.zeros((len(signal), 2))
            audio_data[:, 1] = signal
            sd.play(audio_data, samplerate=44100)
            sd.wait()

        elif selection == "Синус - левый канал":
            frequency = int(self.textInput2.text())
            t = np.linspace(0, duration, int(44100 * duration), endpoint=False)
            signal = 0.5 * np.sin(2 * np.pi * frequency * t)
            audio_data = np.zeros((len(signal), 2))
            audio_data[:, 0] = signal
            sd.play(audio_data, samplerate=44100)
            sd.wait()

if __name__ == '__main__':
    app = QApplication(sys.argv)
    window = CustomWindow()
    window.show()
    sys.exit(app.exec_())
