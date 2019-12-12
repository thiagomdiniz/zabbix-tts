# Zabbix-TTS

HTTP Flask endpoint that receives requests containing text and transforms it into audio to speak the text.

This allows Zabbix to send alert/trigger text to this endpoint and a TV(Raspberry pi) can speak the received text.

## Usage

There are two Python3 scripts:

1. Use the "tts-google.py" script to use gTTS, a Python library to interface with Google Translate’s text-to-speech API.

2. Use the "tts-watson.py" script to use the IBM Watson text to speech service.
   
   You will need an IBM cloud account to use this script. Your API key must be entered in the "api_key" variable of the Python script.

   [https://www.ibm.com/watson/services/text-to-speech/](https://www.ibm.com/watson/services/text-to-speech/)

   [https://cloud.ibm.com/catalog/services/text-to-speech](https://cloud.ibm.com/catalog/services/text-to-speech)

In both scripts you must edit the credentials for HTTP Basic Auth (variables "user" and "passwd").

In both scripts you can change the "endpoint_timeout" variable to increase or decrease the timeout in seconds to try to access the voice API over the internet. In this case a standard audio will be played.

Install Python requirements:

* For gTTS script:
```
pip3 install -r requirements-google.txt
```

* For Watson script:
```
pip3 install -r requirements-watson.txt
```

Run the script:

```
# for gTTS
python3 tts-google.py

or

chmod +x tts-google.py
./tts-google.py

# for Watson
python3 tts-watson.py

or

chmod +x tts-watson.py
./tts-watson.py
```

Make a request

```
curl -u "user:pass" http://<your-address>/<lang>/<text-to-speech>
```

For gTTS script, "\<lang\>" can be any language available through the command "gtts-cli --all".

For Watson script, "\<lang\>" can be "en" or "pt-br".

"\<text-to-speech\>" is the text that will be converted to speech. For example:

```
curl -u "user:pass" http://127.0.0.1:5000/pt-br/testando%20o%20script
```

## Zabbix configuration

The "text2speech.sh" script will be used by Zabbix as media type to apply URL encoding to the triggers text and make the HTTP request to the Python script endpoint.
Change the "user" and "pass" variables according to the HTTP Basic Auth credentials set in the Python script.

See an example configuration at [medium.com/@thiagomdiniz](https://medium.com/@thiagomdiniz/se-meu-zabbix-falasse-cd4388c90c0e?sk=08adc79742dc449bd62bf8ac7b92e23d).

### gTTS (Google Text-to-Speech) docs:

[https://gtts.readthedocs.io/en/latest/](https://gtts.readthedocs.io/en/latest/)

### Watson text-to-speech docs:

[https://cloud.ibm.com/apidocs/text-to-speech/text-to-speech?code=python](https://cloud.ibm.com/apidocs/text-to-speech/text-to-speech?code=python)
