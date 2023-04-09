import openai
from kivy.app import App
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.button import Button
from kivy.uix.label import Label
from kivy.uix.textinput import TextInput
from kivy.core.clipboard import Clipboard

openai.api_key = "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"

class ChatBox(BoxLayout):
    MAX_LOGS = 4
    MAX_MESSAGE_LENGTH = 1000

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.orientation = 'vertical'

        self.chat_logs = Label(size_hint_y=0.9, text='', font_size='16sp')
        self.chat_input = TextInput(size_hint_y=0.1, font_size='16sp')
        self.chat_submit = Button(text='Отправить', size_hint_y=0.1)
        self.chat_submit.bind(on_press=self.send_message)

        self.add_widget(self.chat_logs)
        self.add_widget(self.chat_input)
        self.add_widget(self.chat_submit)

        self.logs = []

    def send_message(self, instance):
        txt = self.chat_input.text
        self.chat_input.text = ''
        if len(txt) > self.MAX_MESSAGE_LENGTH:
            txt = txt[:self.MAX_MESSAGE_LENGTH] + '...'
        response = openai.Completion.create(
            model="text-davinci-003",
            prompt=f"ChatGPT: {txt}",
            temperature=0.8,
            max_tokens=1000,
            top_p=1.0,
            frequency_penalty=0.5,
            presence_penalty=0.0,
        )
        answer = response["choices"][0]["text"]
        self.logs.append((txt, answer))

        if len(self.logs) > self.MAX_LOGS:
            self.logs.pop(0)

        self.chat_logs.text = ''
        for log in self.logs:
            self.chat_logs.text += f"\nYou: {log[0]}\nChatGPT: {log[1]}\n"


class ChatApp(App):
    def build(self):
        return ChatBox()

if __name__ == "__main__":
    ChatApp().run()
