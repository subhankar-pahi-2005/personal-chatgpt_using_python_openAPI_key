import sys
import openai
from PyQt5.QtWidgets import QApplication, QMainWindow, QTextEdit, QPushButton, QVBoxLayout, QHBoxLayout, QWidget, QSpacerItem, QSizePolicy
from PyQt5.QtCore import Qt, pyqtSignal
from PyQt5.QtGui import QKeyEvent, QIcon, QTextCursor, QColor

# Set your OpenAI API key
openai.api_key = "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"  #put your won openai API key here

class CustomTextEdit(QTextEdit):
    enterPressed = pyqtSignal()

    def keyPressEvent(self, event: QKeyEvent):
        if event.key() == Qt.Key_Return or event.key() == Qt.Key_Enter:
            self.enterPressed.emit()
        else:
            super().keyPressEvent(event)

class ChatbotGUI(QMainWindow):
    def __init__(self):
        super().__init__()

        self.init_ui()

    def init_ui(self):
        self.setWindowTitle("chatbot AI GPT")
        self.setGeometry(100, 100, 800, 400)

        self.output_text = QTextEdit(self)
        self.output_text.setReadOnly(True)
        self.output_text.setStyleSheet("background-color: #282c34; color: white; border: none;")
        self.output_text.setFontPointSize(14)

        self.input_text = CustomTextEdit(self)
        self.input_text.setStyleSheet("background-color: #454b54; color: white; border: none;")
        self.input_text.setFontPointSize(16)
        self.input_text.setFixedHeight(200)
        self.input_text.setPlaceholderText("Send a message...")

        self.send_button = QPushButton("Send", self)
        self.send_button.setFixedSize(80, 40)
        self.send_button.setStyleSheet("""
            background: qlineargradient(x1:0, y1:0, x2:0, y2:1, stop:0 #4CAF50, stop:1 #45A049);
            color: white;
            border: none;
            border-radius: 0px;
            font-size: 14px;
            font-weight: bold;
            padding: 5px;
        """)
        self.send_button.setCursor(Qt.PointingHandCursor)

        self.clear_button = QPushButton("Clear", self)
        self.clear_button.setFixedSize(80, 40)
        self.clear_button.setStyleSheet("""
            background: qlineargradient(x1:0, y1:0, x2:0, y2:1, stop:0 #f44336, stop:1 #d32f2f);
            color: white;
            border: none;
            border-radius: 0px;
            font-size: 14px;
            font-weight: bold;
            padding: 5px;
        """)
        self.clear_button.setCursor(Qt.PointingHandCursor)

        layout = QVBoxLayout()
        layout.addWidget(self.output_text)
        layout.addSpacerItem(QSpacerItem(0, 20, QSizePolicy.Expanding, QSizePolicy.Fixed))

        input_layout = QHBoxLayout()
        input_layout.addWidget(self.input_text)
        input_layout.addWidget(self.send_button)
        input_layout.addWidget(self.clear_button)
        layout.addLayout(input_layout)

        container = QWidget()
        container.setLayout(layout)
        self.setCentralWidget(container)

        self.send_button.clicked.connect(self.submit_input)
        self.clear_button.clicked.connect(self.clear_input)
        self.input_text.enterPressed.connect(self.submit_input)

    def submit_input(self):
        user_input = self.input_text.toPlainText()
        if user_input:
            response = generate_response(user_input)
            self.output_text.setTextColor(Qt.green)  # Set the text color to green
            self.output_text.append(f"You:  {user_input}\nbot: {response}")
            self.output_text.setTextColor(Qt.white)  # Reset the text color to white
            self.input_text.clear()

    def clear_input(self):
        self.input_text.clear()
        self.output_text.clear()

def generate_response(prompt):
    response = openai.Completion.create(
        engine="text-davinci-003",
        prompt=prompt,
        max_tokens=4000,
        n=1,
        stop=None,
        temperature=0.5,
    )
    return response["choices"][0]["text"]

def main():
    app = QApplication(sys.argv)
    window = ChatbotGUI()
    window.show()
    sys.exit(app.exec_())

if __name__ == "__main__":
    main()
