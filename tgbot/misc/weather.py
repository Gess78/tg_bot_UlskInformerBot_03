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


@logger.catch
async def get_weather_pic():  # TODO СДЕЛАТЬ АСИНХРОННЫМ
    s1 = """
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

    s2 = '''
    <link type="text/css" rel="stylesheet" href="https://www.meteoprog.ua/css/winformer.min.css?id=100">

    <div class="meteoprog-informer" style="width: 258px" data-params='{"city_ids":"1456","domain":"https://www.meteoprog.com/ru/","id":"61d14c8d2bac9206558b472c","lang":"ru"}'>

      
        <a title="Погода в городе Астрахань" target="_blank" href="https://www.meteoprog.com/ru/weather/Astrahan/">
          <img style="margin: 0 auto; display: block" src="https://www.meteoprog.ua/images/preloader.gif" alt="Loading...">
        </a>
        <a target="_blank" class="constructor__met2wlink" href="https://www.meteoprog.com/ru/review/Astrahan/">Погода на 2 недели</a>
      

      <a class="constructor__metlink" target="_blank" href="https://www.meteoprog.com/ru/">
        <img style="display: block; margin: 0 auto;" alt="Meteoprog" src="https://www.meteoprog.ua/images/meteoprog-inf.png">
      </a>
    </div>
    <script type="text/javascript" src="https://www.meteoprog.ua/js/winformer.min.js?id=100"></script>
    '''

    s3 = '''<!-- Gismeteo Informer (begin) -->
<div id="GMI_240x90-2_ru_5130" class="gm-info">
    <div style="position:relative;width:240px;height:90px;border:solid 1px;background:#F5F5F5;border-color:#EAEAEA #E4E4E4 #DDDDDD #E6E6E6;border-radius:4px;-webkit-box-sizing:border-box;-moz-box-sizing:border-box;box-sizing:border-box;">
        <a style="font:11px/13px Arial,Verdana,sans-serif;text-align:center;text-overflow:ellipsis;text-decoration:none;display:block;overflow:hidden;margin:2px 3px;color:#0678CD;" href="https://www.gismeteo.ru/weather-astrakhan-5130/">Астрахань</a>
        <a style="font:9px/11px Tahoma,Arial,sans-serif;letter-spacing:0.5px;text-align:center;text-decoration:none;position:absolute;bottom:3px;left:0;width:100%;color:#333;" href="https://www.gismeteo.ru"><span style="color:#0099FF;">Gis</span>meteo</a>
    </div>
</div>
<script type="text/javascript">
(function() {
    var
        d = this.document,
        o = this.navigator.userAgent.match(/MSIE (6|7|8)/) ? true : false,
        s = d.createElement('script');
 
    s.src  = 'https://www.gismeteo.ru/informers/simple/install/';
    s.type = 'text/javascript';
    s[(o ? 'defer' : 'async')] = true;
    s[(o ? 'onreadystatechange' : 'onload')] = function() {
        try {new GmI({
            slug : '93300ecf40078cd0046d36c0e7db5ce0',
            type : '240x90-2',
            city : '5130',
            lang : 'ru'
        })} catch (e) {}
    }
 
    d.body.appendChild(s);
})();
</script>
<!-- Gismeteo Informer (finish) -->
    '''

    s4 = """<!-- Gismeteo Informer (begin) -->
<div id="GMI_240x90-2_ru_4407" class="gm-info">
    <div style="position:relative;width:240px;height:90px;border:solid 1px;background:#F5F5F5;border-color:#EAEAEA #E4E4E4 #DDDDDD #E6E6E6;border-radius:4px;-webkit-box-sizing:border-box;-moz-box-sizing:border-box;box-sizing:border-box;">
        <a style="font:11px/13px Arial,Verdana,sans-serif;text-align:center;text-overflow:ellipsis;text-decoration:none;display:block;overflow:hidden;margin:2px 3px;color:#0678CD;" href="https://www.gismeteo.ru/weather-ulyanovsk-4407/">Ульяновск</a>
        <a style="font:9px/11px Tahoma,Arial,sans-serif;letter-spacing:0.5px;text-align:center;text-decoration:none;position:absolute;bottom:3px;left:0;width:100%;color:#333;" href="https://www.gismeteo.ru"><span style="color:#0099FF;">Gis</span>meteo</a>
    </div>
</div>
<script type="text/javascript">
(function() {
    var
        d = this.document,
        o = this.navigator.userAgent.match(/MSIE (6|7|8)/) ? true : false,
        s = d.createElement('script');
 
    s.src  = 'https://www.gismeteo.ru/informers/simple/install/';
    s.type = 'text/javascript';
    s[(o ? 'defer' : 'async')] = true;
    s[(o ? 'onreadystatechange' : 'onload')] = function() {
        try {new GmI({
            slug : '93300ecf40078cd0046d36c0e7db5ce0',
            type : '240x90-2',
            city : '4407',
            lang : 'ru'
        })} catch (e) {}
    }
 
    d.body.appendChild(s);
})();
</script>
<!-- Gismeteo Informer (finish) -->"""

    # pdfkit.from_string(html_string, "filename.pdf", options=options)
    #
    options = {"--log-level": "warn"}
    imgkit.from_string(s1, 'data/weather.jpg', options=options)

    # options = {'enable-local-file-access': None}
    # imgkit.from_url('127.0.0.1:8000', 'data/weather.jpg', options=options)

    im = Image.open('data/weather.jpg')
    im_crop = im.crop((9, 9, 267, 217))
    im_crop.save('data/weather.jpg', quality=95)
    logger.info("ПОГОДА КАРТИНКОЙ ПОЛУЧЕНА :)")
