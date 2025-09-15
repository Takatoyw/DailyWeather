import sys
from PyQt6.QtWidgets import QApplication, QWidget, QVBoxLayout, QLabel, QPushButton, QLineEdit
from PyQt6.QtGui import QPixmap, QFont, QIcon
from PyQt6.QtCore import Qt
import requests
import json

api_key = "a7678a760cd54014043d22b515f1e540"

class WeatherApp(QWidget):
    def __init__(self):
        super().__init__()
        self.initUI()

    def initUI(self):
        self.setWindowTitle('Daily Weather | ahmetcakir-dev')
        self.setWindowIcon(QIcon('İmages/cloud_weather.ico'))
        self.setStyleSheet("""
            QWidget {
                background: qlineargradient(x1:0, y1:0, x2:0, y2:1,
                    stop:0 #e0f7fa, stop:1 #b2ebf2);
                font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif;
            }
        """)
        self.layout = QVBoxLayout()

        self.city_input = QLineEdit(self)
        self.city_input.setPlaceholderText('Enter city name')
        self.city_input.setStyleSheet("font-size: 14px; padding: 5px; border: 1px solid #ccc; border-radius: 5px;")
        self.city_input.returnPressed.connect(self.get_weather)
        self.layout.addWidget(self.city_input)

        self.button = QPushButton('Get Weather', self)
        self.button.setStyleSheet("background-color: #4CAF50; color: white; border-radius: 5px; padding: 10px; font-size: 14px;")
        self.button.clicked.connect(self.get_weather)
        self.layout.addWidget(self.button)

        self.icon_label = QLabel(self)
        self.icon_label.setFixedSize(100, 100)
        self.icon_label.setStyleSheet("border: none;")
        self.layout.addWidget(self.icon_label, alignment=Qt.AlignmentFlag.AlignCenter)

        self.label = QLabel('Weather info will appear here', self)
        self.label.setStyleSheet("font-size: 19px; color: #333; padding: 10px;")
        self.label.setFont(QFont('Dubai', 18))
        self.label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.layout.addWidget(self.label)

        self.setLayout(self.layout)
        self.setFixedSize(320, 400)
        self.show()

    def get_weather(self):
        city = self.city_input.text()
        if not city:
            self.label.setText('Please enter a city name')
            return
        url = f"https://api.openweathermap.org/data/2.5/weather?q={city}&appid={api_key}&units=metric"
        
        try:
            response = requests.get(url)
            data = response.json()

            if data["cod"] != 200:
                if data["cod"] == "404":
                    self.label.setFont(QFont('Dubai', 16,))
                    self.label.setStyleSheet("color: red;")
                    self.label.setAlignment(Qt.AlignmentFlag.AlignCenter)
                    self.label.setText("City not found. Check name.")
                else:
                    self.label.setFont(QFont('Dubai', 16,))
                    self.label.setStyleSheet("color: red;")
                    self.label.setAlignment(Qt.AlignmentFlag.AlignCenter)
                    self.label.setText(f"Error: {data['message']}")
                return

            weather_description = data["weather"][0]["description"]
            temperature = data["main"]["temp"]
            humidity = data["main"]["humidity"]
            wind_speed = data["wind"]["speed"]
            pressure = data["main"]["pressure"]
            icon_code = data["weather"][0]["icon"]
            lat = data["coord"]["lat"]
            lon = data["coord"]["lon"]

            # Load icon
            icon_url = f"https://openweathermap.org/img/wn/{icon_code}@2x.png"
            icon_response = requests.get(icon_url)
            pixmap = QPixmap()
            pixmap.loadFromData(icon_response.content)
            self.icon_label.setPixmap(pixmap)

            # Get UV Index
            uv_url = f"https://api.openweathermap.org/data/2.5/uvi?lat={lat}&lon={lon}&appid={api_key}"
            uv_response = requests.get(uv_url)
            uv_data = uv_response.json()
            uvi = uv_data.get("value", "N/A")

            # Get Air Quality
            air_url = f"https://api.openweathermap.org/data/2.5/air_pollution?lat={lat}&lon={lon}&appid={api_key}"
            air_response = requests.get(air_url)
            air_data = air_response.json()
            aqi = air_data["list"][0]["main"]["aqi"] if air_data["list"] else "N/A"

            weather_info = (f"City: {city}\n"
                            f"Weather: {weather_description}\n"
                            f"Temperature: {temperature}°C\n"
                            f"Humidity: {humidity}%\n"
                            f"Wind Speed: {wind_speed} m/s\n"
                            f"Pressure: {pressure} hPa\n"
                            f"UV Index: {uvi}\n"
                            f"Air Quality Index: {aqi}")
            self.label.setWordWrap(True)
            self.label.setStyleSheet("color: #333; padding: 10px; font-weight: bold;")
            self.label.setAlignment(Qt.AlignmentFlag.AlignLeft)
            self.label.setText(weather_info)
            self.label.setFont(QFont('Dubai', 12,))

        except Exception as e:
            self.label.setStyleSheet("color: red;")
            self.label.setText(f"An error occurred: {e}")

if __name__ == '__main__':
    app = QApplication(sys.argv)
    window = WeatherApp()
    sys.exit(app.exec())
