from seedsigner.views.view import View, Destination, BackStackView
from seedsigner.gui.components import FontAwesomeIconConstants, SeedSignerIconConstants
from seedsigner.gui.screens.screen import ButtonListScreen, RET_CODE__BACK_BUTTON
from seedsigner.views.tools_views import ToolsImageEntropyLivePreviewView, ToolsDiceEntropyMnemonicLengthView, ToolsRandomEntropyMnemonicLengthView
from seedsigner.views.language_views import translator

class GenerateSeedMenuView(View):
    def run(self):
        IMAGE = (translator("Image"), FontAwesomeIconConstants.CAMERA)
        DICE = (translator("Dice roll"), FontAwesomeIconConstants.DICE)
        RANDOM = (translator("Random function"), FontAwesomeIconConstants.RANDOM)
        
        button_data = [IMAGE, DICE, RANDOM]
        
        selected_menu_num = self.run_screen(
            ButtonListScreen,
            title=translator("New Seed"),
            is_button_text_centered=False,
            button_data=button_data,
        )
        
        if selected_menu_num == RET_CODE__BACK_BUTTON:
            return Destination(BackStackView)
        elif button_data[selected_menu_num] == IMAGE:
            return Destination(ToolsImageEntropyLivePreviewView)
        elif button_data[selected_menu_num] == DICE:
            return Destination(ToolsDiceEntropyMnemonicLengthView)
        elif button_data[selected_menu_num] == RANDOM:
            return Destination(ToolsRandomEntropyMnemonicLengthView)