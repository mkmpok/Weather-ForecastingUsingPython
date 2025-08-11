# Weather-ForecastingUsingPython
A Flask-based Weather Forecasting Web Application that fetches real-time weather data from the OpenWeatherMap API.
Users can enter any city name, and the app displays the temperature, humidity, weather conditions, and more in a clean, responsive web UI.

Features:-
🌍 Search weather for any city worldwide

🌡 Displays temperature, humidity, pressure, and wind speed

☁ Shows weather conditions (clear, cloudy, rainy, etc.)

🖥 Simple and responsive web interface

🔄 Live weather updates from OpenWeatherMap API

Technologies Used:-
Python 3

Flask (web framework)

Requests (for API calls)

Bootstrap / HTML / CSS (frontend styling)

OpenWeatherMap API (data source)

nstallation & Setup:-
1)git clone https://github.com/mkmpok/Weather-ForecastingUsingPython.git
cd Weather-ForecastingUsingPython

2)Install dependencies=
pip install -r requirements.txt

3)Get your API key from OpenWeatherMap and replace it in the code:
OPENWEATHER_API_KEY = "YOUR_API_KEY"

4)get one more key as=
FLASK_SECRET_KEY="Your_key"
you will get this by typing this in your terminal
"python -c "import secrets; print(secrets.token_hex(16))""

5)Run the Program=
python app.py
