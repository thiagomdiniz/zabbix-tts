#!/usr/bin/env python3

from ibm_watson import TextToSpeechV1
from ibm_cloud_sdk_core.authenticators import IAMAuthenticator
from ibm_watson import ApiException
import os
from playsound import playsound
from flask import Flask, request
from flask_restful import Api, Resource, abort
import requests

app = Flask(__name__)
api = Api(app)

user = 'some-user'
passwd = 'some-pass'

service_url = 'https://stream.watsonplatform.net/text-to-speech/api'
endpoint_timeout = 5
api_key = 'your_ibm_key'
audio_file = '/tmp/audio.mp3'
static_audio_file = os.path.dirname(os.path.realpath(__file__)) + '/tts-pt-br-static.mp3'

def talk(audio):
    playsound(audio)
    #os.system("/usr/bin/mpg123 %s" % audio)
    return {'message': 'ok'}

def checkUser(req):
    try:
        username = req.authorization.username
        password = req.authorization.password
    except Exception as e:
        abort(401, message="Username and Password for Basic Auth is missing! " + str(e))

    if user == username and passwd == password:
        pass
    else:
        abort(401, message="Authentication failed!")

def checkHttpEndpoint(url, timeout=5):
    r = requests.head(url, timeout=timeout)
    if r.status_code not in [200, 401]:
        raise Exception('Bad HTTP status code: %s' % r.status_code)
    return r.status_code == 200


class TTS(Resource):
    def get(self, lang, zabbixtext):
        checkUser(request)

        try:
            checkHttpEndpoint(service_url, endpoint_timeout)
            authenticator = IAMAuthenticator(api_key)
            text_to_speech = TextToSpeechV1(
                authenticator=authenticator
            )
            text_to_speech.set_service_url(service_url)

            if lang == 'pt-br':
                voice = 'pt-BR_IsabelaV3Voice'
            else:
                voice = 'en-US_LisaV3Voice'

            with open(audio_file, 'wb') as audio_fil:
                audio_fil.write(
                    text_to_speech.synthesize(
                        zabbixtext,
                        voice=voice,
                        accept='audio/mp3'
                    ).get_result().content)

            return talk(audio_file)

        except ApiException as ex:
            print("Method failed with status code " + str(ex.code) + ": " + str(ex.message))
            talk(static_audio_file)
            return {'message': 'Method failed with status code ' + str(ex.code) + ': ' + str(ex.message)}

        except Exception as e:
            print("Method failed: ", str(e))
            talk(static_audio_file)
            return {'message': 'Method failed: ' + str(e)}


api.add_resource(TTS, '/<string:lang>/<string:zabbixtext>')

if __name__ == '__main__':
    app.run(host='0.0.0.0',debug=True)
