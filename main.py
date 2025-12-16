import sys
import requests
import PyQt5.QtWidgets as qw
from PyQt5.QtCore import Qt
from PyQt5.QtGui import QIcon

class WeatherApp(qw.QWidget):
    def __init__(self):
        super().__init__()
        self.city_label = qw.QLabel("Enter city name: ",self)
        self.city_input = qw.QLineEdit(self)
        self.get_weather_button = qw.QPushButton("Get Weather",self)
        self.temp_label = qw.QLabel(self)
        self.emoji_label = qw.QLabel(self)
        self.description_label = qw.QLabel(self)
        self.initUI()

    def initUI(self):
        self.setWindowTitle("Weather App")
        self.setWindowIcon(QIcon("weather.png))
        vbox = qw.QVBoxLayout()
        vbox.addWidget(self.city_label)
        vbox.addWidget(self.city_input)
        vbox.addWidget(self.get_weather_button)
        vbox.addWidget(self.temp_label)
        vbox.addWidget(self.emoji_label)
        vbox.addWidget(self.description_label)

        self.setLayout(vbox)
        self.city_label.setAlignment(Qt.AlignCenter)
        self.city_input.setAlignment(Qt.AlignCenter)
        self.temp_label.setAlignment(Qt.AlignCenter)
        self.emoji_label.setAlignment(Qt.AlignCenter)
        self.description_label.setAlignment(Qt.AlignCenter)

        self.city_label.setObjectName('city_label')
        self.city_input.setObjectName('city_input')
        self.get_weather_button.setObjectName('get_weather_button')
        self.temp_label.setObjectName('temp_label')
        self.emoji_label.setObjectName('emoji_label')
        self.description_label.setObjectName('description_label')

        self.setStyleSheet("""
            QLabel, QPushButton{
                font-family: calibri;
            }
            QLabel#city_label{
                font-size: 40px;
                font-style: italic;
                font-weight: bold;
            }
            QLineEdit#city_input{
                font-size: 40px;
            }
            QPushButton#get_weather_button{
                font-size: 30px;
                font-weight: bold;
            }
            QLabel#temp_label{
                font-size: 80px;
            }
            QLabel#emoji_label{
                font-size: 90px;
                font-family: Segoe UI emoji;
            }
            QLabel#description_label{
                font-size: 60px;
            }
            
        """)


        self.city_input.returnPressed.connect(self.get_weather)
        self.get_weather_button.clicked.connect(self.get_weather)

    def get_weather(self):
        api_key = "b72cc574d2499729425dac3d94b61c6f"
        city = self.city_input.text()
        url = f"https://api.openweathermap.org/data/2.5/weather?q={city}&appid={api_key}"

        try:

            response =  requests.get(url)
            response.raise_for_status()
            data = response.json()

            if data["cod"] == 200:
                self.display_weather(data)
        except requests.exceptions.HTTPError as http_error:
            match response.status_code:
                case 400:
                    self.display_error("Bad request:\nplease check your input")
                case 401:
                    self.display_error("Unauthorized:\nInvalid API Key")
                case 403:
                    self.display_error("Forbidden:\nAccess Denied")
                case 404:
                    self.display_error("Not Found:\nCity not found")
                case 500:
                    self.display_error("Internal Server Error:\n please try again later")
                case 502:
                    self.display_error("Bad Gateway:\nInvalid response from the server")
                case 503:
                    self.display_error("Service Unavailable:\n Server is down")
                case 504:
                    self.display_error("Gateway Timeout:\nNo response from the server")
                case _:
                    self.display_error(f"http error occurred:\n {http_error}")
        except requests.exceptions.ConnectionError:
            self.display_error("Connection error:\nPlease check your internet connection")
        except requests.exceptions.Timeout:
            self.display_error("Timeout error:\nThe request took too long")
        except requests.exceptions.TooManyRedirects:
            self.display_error("Too many redirects error:\nCheck the URL")
        except requests.exceptions.RequestException as req_error:
            self.display_error(f"Request error occurred:\n{req_error}")

    def display_error(self,message):
        self.temp_label.setStyleSheet("font-size: 30px;")
        self.temp_label.setText(message)
        self.emoji_label.clear()
        self.description_label.clear()

    def display_weather(self,data):
        self.temp_label.setStyleSheet("font-size: 80px;")
        temperature_k = data["main"]["temp"]
        temperature_c = temperature_k - 273.15
        temperature_f = (temperature_k * 9/5) - 459.67
        weather_id = data["weather"][0]["id"]
        weather_description = data["weather"][0]["description"]

        self.temp_label.setText(f"{temperature_c:.0f}°C ➡️ {temperature_f:.0f}°F")
        self.emoji_label.setText(self.get_weather_emoji(weather_id))
        self.description_label.setText(weather_description)

    @staticmethod
    def get_weather_emoji(weather_id):
        if 200<= weather_id <= 232:
            return "⛈️"
        elif 300<= weather_id <= 321:
            return "⛅"
        elif 500<= weather_id <= 531:
            return "🌧️"
        elif 600<= weather_id <= 622:
            return "❄️"
        elif 701<= weather_id <= 741:
            return "🌫️"
        elif weather_id == 762:
            return "🌋"
        elif weather_id==771:
            return "💨"
        elif weather_id==781:
            return "🌪️"
        elif weather_id==800:
            return "☀️"
        elif 801<= weather_id <= 804:
            return "☁️"
        else:
            return ""

if __name__ == "__main__":
    app = qw.QApplication(sys.argv)
    w = WeatherApp()
    w.show()

    sys.exit(app.exec_())
