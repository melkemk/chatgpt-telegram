# from googletrans import Translator
# translator = Translator()
# translated=translator.translate('안녕하세요.')
# print(translated.text)

from easygoogletranslate import EasyGoogleTranslate
translator = EasyGoogleTranslate(
    target_language='en',
    timeout=10
)
result = translator.translate('This is an example.')


print(result)