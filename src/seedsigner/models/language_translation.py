import json
import os

class LanguageTranslation:
    def __init__(self, language_code):
        self.language_code = language_code
        self.translations = self.load_translations()

    def load_translations(self):
        file_path = os.path.join(os.path.dirname(__file__), '..', 'language', f'{self.language_code}.json')
        if not os.path.exists(file_path):
            raise FileNotFoundError(f"Translation file {self.language_code}.json not found.")
        
        with open(file_path, 'r', encoding='utf-8') as f:
            return json.load(f)

    def translate(self, text, **kwargs):
        # 먼저 번역을 수행
        translated = self.translations.get(text, text)

        # 번역된 텍스트에 변수 값을 대입
        if kwargs:
            try:
                translated = translated.format(**kwargs)
            except KeyError:
                # 변수 대입에 실패하면 원본 텍스트를 사용
                return text.format(**kwargs)

        return translated