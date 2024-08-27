from seedsigner.views.view import View, Destination, MainMenuView
from seedsigner.gui.screens.language_selection_screen import LanguageSelectionScreen
from seedsigner.models.language_translation import LanguageTranslation
from seedsigner.gui.components import GUIConstants
import seedsigner.views.view as view
import seedsigner.gui.screens.screen as screen
import seedsigner.models.settings_definition as settings_definition
import seedsigner.gui.components as components
# 전역 변수 선언
current_selected_language = "EN"
translator = LanguageTranslation("EN").translate
view.view_current_selected_language="EN"
screen.screen_current_selected_language="EN"
components.components_current_selected_language="EN"
settings_definition.SettingsDefinition.set_language("EN")
class LanguageSelectionView(View):
    def __init__(self):
        super().__init__()

    def run(self):
        global current_selected_language, translator  # 전역 변수 사용 선언
        selected_language = "English"

        # 언어 선택에 따라 언어 코드를 설정합니다.
        language_code_map = {
            "English": "EN",
            "한국어": "KR",
            "Español": "ES",
            "Français": "FR",
            "Deutsch": "DE",
            "中文": "SC",
            "日本語": "JP",
            "Italiano": "IT"
        }

        # selected_language를 적절한 언어 코드로 변환하여 설정합니다.
        current_selected_language = language_code_map.get(selected_language, "EN")  # 기본값은 'en'으로 설정
        view.view_current_selected_language="EN"
        screen.screen_current_selected_language=current_selected_language
        components.components_current_selected_language=current_selected_language

        translator = LanguageTranslation(current_selected_language).translate
        font_current_selected_language= current_selected_language if current_selected_language in ("KR", "SC", "JP") else "EN"
        GUIConstants.TOP_NAV_TITLE_FONT_NAME = f'NotoSans{font_current_selected_language}-SemiBold'
        GUIConstants.BODY_FONT_NAME = f'NotoSans{font_current_selected_language}-SemiBold'
        GUIConstants.BUTTON_FONT_NAME = f'NotoSans{font_current_selected_language}-SemiBold'
        GUIConstants.REGULAR_FONT_NAME = f'NotoSans{font_current_selected_language}-Regular'

        settings_definition.SettingsDefinition.set_language(current_selected_language)
        
        # 언어 선택 후 메인 메뉴로 이동
        return Destination(MainMenuView)
