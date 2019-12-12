import speech_recognition as sr
import time

#%%
'''
   // Voice Recognition (Speech-to-Text) - Google Speech Recognition API
   -> This API converts spoken text (microphone) into written text (Python strings)
   -> Personal or testing purposes only
   -> Generic key is given by default (it may be revoked by Google at any time)
   -> If using API key, quota for your own key is 50 requests per day
'''

#%%

def recognize_speech_from_mic(recognizer, microphone,lang,duration):

    # check that recognizer and microphone arguments are appropriate type
    if not isinstance(recognizer, sr.Recognizer):
        raise TypeError("`recognizer` must be `Recognizer` instance")

    if not isinstance(microphone, sr.Microphone):
        raise TypeError("`microphone` must be `Microphone` instance")

    # adjust the recognizer sensitivity to ambient noise and record audio
    # from the microphone
    timeout=time.time() + duration
    f = open("text.txt", "w")
    with microphone as source:
        recognizer.adjust_for_ambient_noise(source,duration=5) # #  analyze the audio source for 1 second

        print('Speak now')

        recognizer.pause_threshold=0.5


        while True:
            response = {
                "success": True,
                "error": None,
                "transcription": None
            }

            text = None

            try:
                audio = recognizer.listen(source)
            except:
                pass

            try:
                text = recognizer.recognize_google(audio, language=lang)
                if text is not None:
                    f.write(text + '\n' )

                if text =="stop recording" or time.time()>timeout:
                     break

            except sr.RequestError:
                # API was unreachable or unresponsive
                response["success"] = False
                response["error"] = "API unavailable/unresponsive"
            except sr.UnknownValueError:
                # speech was unintelligible
                response["error"] = "Unable to recognize speech"

            # print('\nSuccess : {}\nError   : {}\n\nText from Speech\n{}\n\n{}' \
            #       .format(response['success'],
            #               response['error'],
            #               '-' * 17,
            #               response['transcription']))
            print (text)
    f.close()




#%%
if __name__ == "__main__":
    recognizer = sr.Recognizer()
    mic = sr.Microphone(device_index=1,chunk_size=20480)
    recognize_speech_from_mic(recognizer, mic,"en-US",120)

    # while True:
    #       response = recognize_speech_from_mic(recognizer, mic)
    #       print('\nSuccess : {}\nError   : {}\n\nText from Speech\n{}\n\n{}' \
    #        .format(response['success'],
    #               response['error'],
    #               '-'*17,
    #               response['transcription']))

'''Afrikaans	af-za
Arabic	ar-ww
Arabic (Jordanian)	ar-jo
Assamese	as-in
Basque	eu-es
Bengali	bn-bd
Bengali (Indian)	bn-in
Bhojpuri	bh-in
Bulgarian	bg-bg
Cantonese	cn-hk
Catalan	ca-es
Czech	cs-cz
Danish	da-dk
Dutch	nl-nl
Dutch (Belgian)	nl-be
English (Australian)	en-au
English (Indian)	en-in
English (Singaporean)	en-sg
English (South African)	en-za
English (UK)	en-gb
English (US)	en-us (Default)
Finnish	fi-fi
French	fr-fr
French (Belgian)	fr-be
French (Canadian)	fr-ca
Galician	gl-es
German	de-de
German (Austrian)	de-at
German (Swiss)	de-ch
Greek	el-gr
Gujarati	gu-in
Hebrew	he-il
Hindi	hi-in
Hungarian	hu-hu
Icelandic	is-is
Indonesian	id-id
Italian	it-it
Japanese	ja-jp
Kannada	kn-in
Korean	ko-kr
Malay	ms-my
Malayalam	ml-in
Mandarin	zh-cn
Mandarin (Taiwanese)	zh-tw
Marathi	mr-in
Nepali	ne-np
Norwegian	no-no
Oriya	or-in
Polish	pl-pl
Portuguese	pt-pt
Portuguese (Brazilian)	pt-br
Punjabi	pa-in
Romanian	ro-ro
Russian	ru-ru
Serbian	sr-rs
Slovak	sk-sk
Slovenian	sl-si
Spanish	es-es
Spanish (Argentinian)	es-ar
Spanish (Colombian)	es-co
Spanish (US & Mexican)	es-us
Swedish	sv-se
Tamil	ta-in
Telugu	te-in
Thai	th-th
Turkish	tr-tr
Ukrainian	uk-ua
Urdu (Indian)	ur-in
Urdu (Pakistani)	ur-pk
Valencian	va-es
Vietnamese	vi-vn
Welsh	cy-gb'''