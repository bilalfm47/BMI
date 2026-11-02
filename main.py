import os
import json
from datetime import datetime
from kivy.lang import Builder
from kivy.core.window import Window
from kivymd.app import MDApp
from kivymd.uix.screen import MDScreen
from kivymd.uix.button import MDRaisedButton, MDFlatButton
from kivymd.uix.dialog import MDDialog
from kivymd.uix.list import OneLineListItem
from kivy.utils import platform

# Android Permissions Request (Play Store Compliance)
if platform == 'android':
    from android.permissions import request_permissions, Permission
    request_permissions([
        Permission.READ_EXTERNAL_STORAGE,
        Permission.WRITE_EXTERNAL_STORAGE,
        Permission.INTERNET,
        Permission.POST_NOTIFICATIONS
    ])

# Localization Dictionary (English & Urdu)
LANG_DATA = {
    'en': {
        'title': "BMI Calculator Pro",
        'weight_hint': "Enter Weight (kg)",
        'height_hint': "Enter Height (cm)",
        'age_hint': "Enter Age",
        'btn_calc': "Calculate BMI",
        'btn_history': "View History",
        'btn_lang': "Urdu / اردو",
        'result_title': "Your BMI Result",
        'history_title': "Saved History",
        'insight_title': "Pro Health Insight",
        'underweight': "Underweight - Need to gain weight.",
        'normal': "Normal - Excellent! Keep it up.",
        'overweight': "Overweight - Consider healthy diet.",
        'obese': "Obese - Health risk! Consult a doctor.",
        'error': "Please enter valid numbers!",
        'close': "Close"
    },
    'ur': {
        'title': "بی ایم آئی کیلکولیٹر پرو",
        'weight_hint': "وزن لکھیں (کلوگرام)",
        'height_hint': "قد لکھیں (سینٹی میٹر)",
        'age_hint': "عمر لکھیں",
        'btn_calc': "بی ایم آئی معلوم کریں",
        'btn_history': "ہسٹری دیکھیں",
        'btn_lang': "English",
        'result_title': "آپ کا بی ایم آئی رزلٹ",
        'history_title': "محفوظ شدہ ہسٹری",
        'insight_title': "پرو ہیلتھ رپورٹ",
        'underweight': "کم وزن - آپ کو وزن بڑھانے کی ضرورت ہے۔",
        'normal': "نورمل - بہت بہترین! برقرار رکھیں۔",
        'overweight': "زیادہ وزن - صحت بخش غذا کا سوچیں۔",
        'obese': "شدید زیادہ وزن - ڈاکٹر سے رجوع کریں۔",
        'error': "برائے مہربانی درست معلومات درج کریں!",
        'close': "بند کریں"
    }
}

KV = '''
MDScreen:
    md_bg_color: 0.1, 0.1, 0.12, 1
    
    MDBoxLayout:
        orientation: 'vertical'
        padding: "20dp"
        spacing: "15dp"
        
        MDLabel:
            id: main_title
            text: "BMI Calculator Pro"
            font_style: "H4"
            halign: "center"
            theme_text_color: "Custom"
            text_color: 0.2, 0.6, 1, 1
            size_hint_y: None
            height: "60dp"
            
        MDRaisedButton:
            id: lang_btn
            text: "Urdu / اردو"
            pos_hint: {"center_x": .5}
            on_release: app.toggle_language()
            md_bg_color: 0.3, 0.3, 0.35, 1

        MDTextField:
            id: weight_input
            hint_text: "Enter Weight (kg)"
            mode: "rectangle"
            input_filter: "float"
            line_color_focus: 0.2, 0.6, 1, 1
            hint_text_color_focus: 0.2, 0.6, 1, 1
            
        MDTextField:
            id: height_input
            hint_text: "Enter Height (cm)"
            mode: "rectangle"
            input_filter: "float"
            line_color_focus: 0.2, 0.6, 1, 1
            hint_text_color_focus: 0.2, 0.6, 1, 1

        MDTextField:
            id: age_input
            hint_text: "Enter Age"
            mode: "rectangle"
            input_filter: "int"
            line_color_focus: 0.2, 0.6, 1, 1
            hint_text_color_focus: 0.2, 0.6, 1, 1

        MDRaisedButton:
            id: calc_btn
            text: "Calculate BMI"
            size_hint_x: 1
            height: "50dp"
            on_release: app.calculate_bmi()
            md_bg_color: 0.2, 0.6, 1, 1

        MDRaisedButton:
            id: history_btn
            text: "View History"
            size_hint_x: 1
            height: "50dp"
            on_release: app.show_history_dialog()
            md_bg_color: 0.2, 0.25, 0.35, 1
            
        Widget:
            size_hint_y: 1
'''

class BMICalculatorPro(MDApp):
    def build(self):
        self.theme_cls.theme_style = "Dark"
        self.theme_cls.primary_palette = "Blue"
        self.current_lang = 'en'
        self.db_file = "bmi_history.json"
        return Builder.load_string(KV)

    def toggle_language(self):
        # Switch language safely
        self.current_lang = 'ur' if self.current_lang == 'en' else 'en'
        lang = LANG_DATA[self.current_lang]
        
        # Update UI texts dynamically
        self.root.ids.main_title.text = lang['title']
        self.root.ids.weight_input.hint_text = lang['weight_hint']
        self.root.ids.height_input.hint_text = lang['height_hint']
        self.root.ids.age_input.hint_text = lang['age_hint']
        self.root.ids.calc_btn.text = lang['btn_calc']
        self.root.ids.history_btn.text = lang['btn_history']
        self.root.ids.lang_btn.text = lang['btn_lang']

    def calculate_bmi(self):
        lang = LANG_DATA[self.current_lang]
        try:
            weight = float(self.root.ids.weight_input.text)
            height = float(self.root.ids.height_input.text) / 100 # Convert to meters
            age = self.root.ids.age_input.text
            
            if weight <= 0 or height <= 0:
                raise ValueError
                
            bmi = round(weight / (height * height), 1)
            
            # Categories & Pro Insights Logic
            if bmi < 18.5:
                status = lang['underweight']
                color = "⚠️"
            elif 18.5 <= bmi < 24.9:
                status = lang['normal']
                color = "✅"
            elif 25 <= bmi < 29.9:
                status = lang['overweight']
                color = "⚠️"
            else:
                status = lang['obese']
                color = "🚨"
                
            result_text = f"BMI: {bmi}\nStatus: {status}"
            self.save_to_history(bmi, status)
            
            # Show Result Dialog
            self.show_dialog(lang['result_title'], result_text)
            
        except ValueError:
            self.show_dialog(lang['error'], "")

    def save_to_history(self, bmi, status):
        # Pro Feature: Local Database Logging
        data = []
        if os.path.exists(self.db_file):
            with open(self.db_file, 'r') as f:
                try:
                    data = json.load(f)
                except:
                    data = []
                    
        timestamp = datetime.now().strftime("%Y-%m-%d %H:%M")
        data.append({"date": timestamp, "bmi": bmi, "status": status})
        
        with open(self.db_file, 'w') as f:
            json.json.dump(data, f)

    def show_history_dialog(self):
        lang = LANG_DATA[self.current_lang]
        history_text = ""
        
        if os.path.exists(self.db_file):
            with open(self.db_file, 'r') as f:
                try:
                    data = json.load(f)
                    for item in data[-5:]: # Show last 5 logs
                        history_text += f"📅 {item['date']} -> BMI: {item['bmi']}\n"
                except:
                    pass
                    
        if not history_text:
            history_text = "No history found." if self.current_lang == 'en' else "کوئی ہسٹری موجود نہیں ہے۔"
            
        self.show_dialog(lang['history_title'], history_text)

    def show_dialog(self, title, text):
        close_text = LANG_DATA[self.current_lang]['close']
        dialog = MDDialog(
            title=title,
            text=text,
            buttons=[MDFlatButton(text=close_text, on_release=lambda x: dialog.dismiss())]
        )
        dialog.open()

if __name__ == '__main__':
    BMICalculatorPro().run()





































































































































































































































































