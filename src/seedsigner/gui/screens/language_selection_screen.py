from dataclasses import dataclass
from PIL import ImageFont, ImageDraw
import os
from seedsigner.gui.components import TextArea, Button, GUIConstants
from seedsigner.gui.screens.screen import BaseScreen
from seedsigner.hardware.buttons import HardwareButtonsConstants

@dataclass
class LanguageSelectionScreen(BaseScreen):
    def __post_init__(self):
        super().__post_init__()

        # Create a TextArea for instructions
        self.title = TextArea(
            screen_x=0,
            screen_y=0,
            height=GUIConstants.TOP_NAV_HEIGHT,
            text="Select Language",
            is_text_centered=True,
            font_name=GUIConstants.TOP_NAV_TITLE_FONT_NAME,
            font_size=GUIConstants.TOP_NAV_TITLE_FONT_SIZE,
        )
        self.components.append(self.title)

        # 폰트 경로 설정
        current_dir = os.path.dirname(os.path.abspath(__file__))
        font_dir = os.path.join(current_dir, '..', '..', 'resources', 'fonts')

        # 폰트 파일명과 크기 설정
        self.fonts = {
            '한국어': ImageFont.truetype(os.path.join(font_dir, 'NotoSansKR-SemiBold.ttf'), GUIConstants.BODY_FONT_MAX_SIZE),
            'English': ImageFont.truetype(os.path.join(font_dir, 'NotoSansEN-SemiBold.ttf'), GUIConstants.BODY_FONT_MAX_SIZE),
            '日本語': ImageFont.truetype(os.path.join(font_dir, 'NotoSansJP-SemiBold.ttf'), GUIConstants.BODY_FONT_MAX_SIZE),
            '中文': ImageFont.truetype(os.path.join(font_dir, 'NotoSansSC-SemiBold.ttf'), GUIConstants.BODY_FONT_MAX_SIZE),
            'Hongkong': ImageFont.truetype(os.path.join(font_dir, 'NotoSansHK-SemiBold.ttf'), GUIConstants.BODY_FONT_MAX_SIZE),
        }
        self.language_list = [
            "English", "한국어", "Español", "Français", 
            "Deutsch", "中文", "日本語", "Italiano"
        ]
        # Create a list of languages with appropriate fonts
        self.languages = [
            {"text": lang, "font": self.fonts.get(lang, self.fonts['English'])}
            for lang in self.language_list
        ]

        self.is_dropdown_open = False
        self.selected_index = 0
        self.dropdown_items = []

        # Create dropdown button
        self.dropdown_button = self.create_dropdown_button()
        self.components.append(self.dropdown_button)

        # Create confirm button
        self.confirm_button = self.create_confirm_button()
        self.components.append(self.confirm_button)

        # Set initial focus on dropdown button
        self.focused_component = self.dropdown_button

        self.visible_items_count = 3
        self.scroll_offset = 0
        self.dropdown_padding = 5
        self.focused_dropdown_index = 0 
    def create_dropdown_button(self):
        button_width = 200
        button_height = 40
        button_x = (self.canvas_width - button_width) // 2
        button_y = self.title.screen_y + self.title.height + 20

        return Button(
            text=self.languages[self.selected_index]["text"],
            screen_x=button_x,
            screen_y=button_y,
            width=button_width,
            height=button_height,
            font_name=GUIConstants.BUTTON_FONT_NAME,
            font_size=GUIConstants.BUTTON_FONT_SIZE,
        )

    def create_confirm_button(self):
        button_width = 120
        button_height = 40
        button_x = (self.canvas_width - button_width) // 2
        button_y = self.canvas_height - button_height - 20

        return Button(
            text="Confirm",
            screen_x=button_x,
            screen_y=button_y,
            width=button_width,
            height=button_height,
        )

    def draw_dropdown(self):
        dropdown_width = 200
        dropdown_item_height = 40
        dropdown_x = (self.canvas_width - dropdown_width) // 2
        dropdown_y = self.dropdown_button.screen_y + self.dropdown_button.height

        self.dropdown_items = []
        for i, lang in enumerate(self.languages):
            item_y = dropdown_y + i * dropdown_item_height
            item = Button(
                text=lang["text"],
                screen_x=dropdown_x,
                screen_y=item_y,
                width=dropdown_width,
                height=dropdown_item_height,
                font_name=GUIConstants.BUTTON_FONT_NAME,
                font_size=GUIConstants.BUTTON_FONT_SIZE,
            )
            if i == self.selected_index:
                item.is_selected = True
            self.dropdown_items.append(item)
        self.components.extend(self.dropdown_items)

    def clear_dropdown(self):
        for item in self.dropdown_items:
            self.components.remove(item)
        self.dropdown_items = []

    def render(self):
        # Clear the canvas
        self.renderer.draw.rectangle((0, 0, self.canvas_width, self.canvas_height), fill=GUIConstants.BACKGROUND_COLOR)
        
        # Render the title
        self.title.render()

        # Render the dropdown button
        self.dropdown_button.render()

        # Render the confirm button
        self.confirm_button.render()

        # Highlight focused component
        if self.focused_component == self.dropdown_button:
            self.renderer.draw.rectangle([
                self.dropdown_button.screen_x - 2, self.dropdown_button.screen_y - 2, 
                self.dropdown_button.screen_x + self.dropdown_button.width + 2, 
                self.dropdown_button.screen_y + self.dropdown_button.height + 2
            ], outline=GUIConstants.ACCENT_COLOR, width=2)
        elif self.focused_component == self.confirm_button:
            self.renderer.draw.rectangle([
                self.confirm_button.screen_x - 2, self.confirm_button.screen_y - 2, 
                self.confirm_button.screen_x + self.confirm_button.width + 2, 
                self.confirm_button.screen_y + self.confirm_button.height + 2
            ], outline=GUIConstants.ACCENT_COLOR, width=2)
        
        # Draw dropdown arrow
        if not self.is_dropdown_open:
            arrow_size = 10
            arrow_x = self.dropdown_button.screen_x + self.dropdown_button.width - 20
            arrow_y = self.dropdown_button.screen_y + (self.dropdown_button.height - arrow_size) // 2
            self.renderer.draw.polygon([
                (arrow_x, arrow_y), 
                (arrow_x + arrow_size, arrow_y), 
                (arrow_x + arrow_size // 2, arrow_y + arrow_size)
            ], fill=GUIConstants.BODY_FONT_COLOR)

        # Draw dropdown items
        if self.is_dropdown_open:
            dropdown_height = self.visible_items_count * self.dropdown_items[0].height
            dropdown_y = self.dropdown_button.screen_y + self.dropdown_button.height + self.dropdown_padding

            # Draw dropdown background
            self.renderer.draw.rectangle([
                self.dropdown_button.screen_x, dropdown_y,
                self.dropdown_button.screen_x + self.dropdown_button.width, dropdown_y + dropdown_height
            ], fill=GUIConstants.BACKGROUND_COLOR)

            # Draw dropdown border (excluding right side)
            self.renderer.draw.line([
                (self.dropdown_button.screen_x, dropdown_y),
                (self.dropdown_button.screen_x, dropdown_y + dropdown_height),
                (self.dropdown_button.screen_x + self.dropdown_button.width, dropdown_y + dropdown_height),
                (self.dropdown_button.screen_x, dropdown_y)
            ], fill=GUIConstants.BODY_FONT_COLOR, width=1)

            for i, item in enumerate(self.dropdown_items[self.scroll_offset:self.scroll_offset + self.visible_items_count]):
                item_y = dropdown_y + i * item.height
                
                # 각 언어에 맞는 폰트로 텍스트 그리기
                lang_font = next(lang["font"] for lang in self.languages if lang["text"] == item.text)
                text_color = GUIConstants.BUTTON_SELECTED_FONT_COLOR if i == self.focused_dropdown_index else GUIConstants.BUTTON_FONT_COLOR
                background_color = GUIConstants.ACCENT_COLOR if i == self.focused_dropdown_index else GUIConstants.BACKGROUND_COLOR
                
                # 모든 버튼에 테두리 추가
                self.renderer.draw.rectangle([
                    item.screen_x, item_y, 
                    item.screen_x + item.width - 1, 
                    item_y + item.height - 1
                ], fill=background_color, outline=GUIConstants.INACTIVE_COLOR, width=2)
                
                self.renderer.draw.text(
                    (item.screen_x + item.width // 2, item_y + item.height // 2),
                    item.text,
                    font=lang_font,
                    fill=text_color,
                    anchor="mm"
                )

                if i == self.focused_dropdown_index:
                    self.renderer.draw.rectangle([
                        item.screen_x, item_y, 
                        item.screen_x + item.width - 1, 
                        item_y + item.height - 1
                    ], outline=GUIConstants.BODY_FONT_COLOR, width=2)
                    # 코너 픽셀을 채워 테두리를 더 굵고 일관되게 만듭니다
                    self.renderer.draw.point([item.screen_x, item_y], fill=GUIConstants.BODY_FONT_COLOR)
                    self.renderer.draw.point([item.screen_x + item.width - 1, item_y], fill=GUIConstants.BODY_FONT_COLOR)
                    self.renderer.draw.point([item.screen_x, item_y + item.height - 1], fill=GUIConstants.BODY_FONT_COLOR)
                    self.renderer.draw.point([item.screen_x + item.width - 1, item_y + item.height - 1], fill=GUIConstants.BODY_FONT_COLOR)

            # Draw scrollbar
            scrollbar_width = 10
            scrollbar_height = dropdown_height
            scrollbar_x = self.dropdown_button.screen_x + self.dropdown_button.width - scrollbar_width
            scrollbar_y = dropdown_y

            # Draw scrollbar background
            self.renderer.draw.rectangle([
                scrollbar_x, scrollbar_y,
                scrollbar_x + scrollbar_width, scrollbar_y + scrollbar_height
            ], fill=GUIConstants.BUTTON_BACKGROUND_COLOR, outline=GUIConstants.BODY_FONT_COLOR, width=1)

            # Calculate and draw scrollbar handle
            total_items = len(self.languages)
            handle_height = max(scrollbar_height * self.visible_items_count // total_items, 20)
            handle_y = scrollbar_y + (scrollbar_height - handle_height) * self.scroll_offset // (total_items - self.visible_items_count)
            self.renderer.draw.rectangle([
                scrollbar_x + 2, handle_y,
                scrollbar_x + scrollbar_width - 2, handle_y + handle_height
            ], fill=GUIConstants.ACCENT_COLOR)

        self.renderer.show_image()

    def _run(self):
        while True:
            self.render()

            input = self.hw_inputs.wait_for(HardwareButtonsConstants.ALL_KEYS)
            
            if input == HardwareButtonsConstants.KEY_PRESS:
                if self.focused_component == self.dropdown_button:
                    if not self.is_dropdown_open:
                        self.is_dropdown_open = True
                        self.draw_dropdown()
                        self.scroll_offset = max(0, min(self.selected_index - 1, len(self.languages) - self.visible_items_count))
                        self.focused_dropdown_index = self.selected_index - self.scroll_offset
                    else:
                        self.is_dropdown_open = False
                        self.clear_dropdown()
                elif self.focused_component == self.confirm_button:
                    selected_language = self.languages[self.selected_index]["text"]
                    return selected_language  # 선택된 언어 반환
                elif self.is_dropdown_open:
                    self.selected_index = self.scroll_offset + self.focused_dropdown_index
                    self.dropdown_button.text = self.languages[self.selected_index]["text"]
                    self.dropdown_button.font = self.languages[self.selected_index]["font"]
                    self.is_dropdown_open = False
                    self.clear_dropdown()

            elif input in [HardwareButtonsConstants.KEY_UP, HardwareButtonsConstants.KEY_DOWN]:
                if self.is_dropdown_open:
                    if input == HardwareButtonsConstants.KEY_UP:
                        if self.focused_dropdown_index > 0:
                            self.focused_dropdown_index -= 1
                        elif self.scroll_offset > 0:
                            self.scroll_offset -= 1
                        elif self.scroll_offset == 0 and self.focused_dropdown_index == 0:
                            self.focused_component = self.dropdown_button
                            self.is_dropdown_open = False
                            self.clear_dropdown()
                    else:  # KEY_DOWN
                        if self.focused_dropdown_index < self.visible_items_count - 1 and self.scroll_offset + self.focused_dropdown_index < len(self.languages) - 1:
                            self.focused_dropdown_index += 1
                        elif self.scroll_offset + self.visible_items_count < len(self.languages):
                            self.scroll_offset += 1
                    
                    # Update selected_index based on current scroll_offset and focused_dropdown_index
                    self.selected_index = self.scroll_offset + self.focused_dropdown_index
                    
                    # Update dropdown button text and font
                    self.dropdown_button.text = self.languages[self.selected_index]["text"]
                    self.dropdown_button.font = self.languages[self.selected_index]["font"]
                else:
                    if self.focused_component == self.dropdown_button:
                        self.focused_component = self.confirm_button
                    else:
                        self.focused_component = self.dropdown_button

            self.renderer.show_image()