from kivy.app import App
from kivy.uix.boxlayout import BoxLayout
from kivy.lang import Builder
import jieba

KV = """
BoxLayout:
    orientation: 'vertical'
    spacing: 10
    padding: 10

    TextInput:
        id: item_input
        hint_text: '输入商品信息（格式：商品名|价格，每行一个）'
        size_hint_y: 0.4
        multiline: True
        background_color: (.1, .1, .1, 1)
        foreground_color: (1, 1, 1, 1)

    TextInput:
        id: min_price
        hint_text: '最低价格'
        input_filter: 'int'
        background_color: (.1, .1, .1, 1)
        foreground_color: (1, 1, 1, 1)

    TextInput:
        id: max_price
        hint_text: '最高价格'
        input_filter: 'int'
        background_color: (.1, .1, .1, 1)
        foreground_color: (1, 1, 1, 1)

    TextInput:
        id: keyword_filter
        hint_text: '关键词筛选（多个用英文逗号分隔）'
        background_color: (.1, .1, .1, 1)
        foreground_color: (1, 1, 1, 1)

    Button:
        text: '开始筛选'
        size_hint_y: 0.15
        on_press: app.filter_items()
        background_color: (.2, .2, .2, 1)
        color: (1, 1, 1, 1)

    ScrollView:
        Label:
            id: output_label
            text: ''
            size_hint_y: None
            height: self.texture_size[1]
            text_size: self.width, None
            halign: 'left'
            valign: 'top'
            color: (1, 1, 1, 1)
"""

class MainApp(App):
    def build(self):
        self.title = "咸鱼助手"
        return Builder.load_string(KV)

    def filter_items(self):
        raw_text = self.root.ids.item_input.text.strip()
        keyword_raw = self.root.ids.keyword_filter.text.strip()
        keywords = [k.strip().lower() for k in keyword_raw.split(',') if k.strip()]

        try:
            min_price = int(self.root.ids.min_price.text)
            max_price = int(self.root.ids.max_price.text)
        except ValueError:
            self.root.ids.output_label.text = '价格区间输入有误'
            return

        stop_words = {"支持", "验机", "全新", "二手", "正品", "成色", "国行", "黑色", "未拆封"}

        result_lines = []
        for line in raw_text.split('\\n'):
            if '|' in line:
                title, price_str = line.split('|', 1)
                try:
                    price = int(price_str)
                    if min_price <= price <= max_price:
                        if keywords and not any(k in title.lower() for k in keywords):
                            continue
                        words = jieba.lcut(title)
                        kw_out = [w for w in words if w not in stop_words and len(w.strip()) > 1]
                        result_lines.append(f"✔ {title} - ¥{price}｜关键词: {', '.join(kw_out)}")
                except:
                    continue

        self.root.ids.output_label.text = '\\n'.join(result_lines) if result_lines else '未找到符合条件的商品'

if __name__ == "__main__":
    MainApp().run()
