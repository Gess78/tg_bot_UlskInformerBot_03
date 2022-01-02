import aiohttp
import imgkit
from PIL import Image
from loguru import logger


# def wind_deg_to_str(deg):
#     arr = ['NNE', 'NE', 'ENE', 'E', 'ESE', 'SE', 'SSE', 'S', 'SSW', 'SW', 'WSW', 'W', 'WNW', 'NW', 'NNW', 'N']
#     return arr[int(abs((deg - 11.25) % 360) / 22.5)]

def wind_deg_to_str2(deg):
    # arr = ['NE', 'E', 'SE', 'S', 'SW', 'W', 'NW', 'N']
    arr = [
        'северо-восточный',
        'восточный',
        'юго-восточный',
        'южный',
        'юго-западный',
        'западный',
        'северо-западный',
        'северный'
    ]
    return arr[int(abs((deg - 22.5) % 360) / 45)]


weather_data: dict = {}


@logger.catch
async def get_weather_data():
    url_ = "https://api.openweathermap.org/data/2.5/weather?id=479123&appid=40212b3b1dcb8ccb9e860c0e494537f4&lang=ru&units=metric"
    async with aiohttp.ClientSession() as session:
        async with session.get(url_) as resp:
            json_data = await resp.json()
            global weather_data
            weather_data = {'description': json_data.get('weather')[0].get('description'),
                            'temp': int(json_data.get('main').get('temp')),
                            'temp_feels_like': int(json_data.get('main').get('feels_like')),
                            'pressure': int(json_data.get('main').get('pressure') * 0.750064),
                            'humidity': int(json_data.get('main').get('humidity')),
                            'wind_speed': int(json_data.get('wind').get('speed')),
                            'wind_direction': wind_deg_to_str2(json_data.get('wind').get('deg')),
                            }
            logger.info("ПОГОДА ПОЛУЧЕНА :)")


async def get_weather_pic():  # TODO СДЕЛАТЬ АСИНХРОННЫМ
    sss = """
        <link type="text/css" rel="stylesheet" href="https://www.meteoprog.ua/css/winformer.min.css?id=100">

    <div class="meteoprog-informer" style="width: 258px"
         data-params='{"city_ids":"14366","domain":"https://www.meteoprog.com/ru/","id":"61d11d782bac9295798b482e","lang":"ru"}'>


        <a title="Погода в городе Ульяновск" target="_blank" href="https://www.meteoprog.com/ru/weather/Ulyanovsk/">
            <img style="margin: 0 auto; display: block" src="https://www.meteoprog.ua/images/preloader.gif"
                 alt="Loading...">
        </a>
        <a target="_blank" class="constructor__met2wlink" href="https://www.meteoprog.com/ru/review/Ulyanovsk/">Погода на 2
            недели</a>


        <a class="constructor__metlink" target="_blank" href="https://www.meteoprog.com/ru/">
            <img style="display: block; margin: 0 auto;" alt="Meteoprog"
                 src="https://www.meteoprog.ua/images/meteoprog-inf.png">
        </a>
    </div>
    <script type="text/javascript" src="https://www.meteoprog.ua/js/winformer.min.js?id=100"></script>
        """
    imgkit.from_string(sss, 'data/weather.jpg')

    im = Image.open('data/weather.jpg')
    im_crop = im.crop((9, 9, 267, 217))
    im_crop.save('data/weather.jpg', quality=95)
    logger.info("ПОГОДА КАРТИНКОЙ ПОЛУЧЕНА :)")
