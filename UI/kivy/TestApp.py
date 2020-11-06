import kivy
from kivy.app import App
from kivy.uix.widget import Widget
from kivy.uix.label import Label
from kivy.uix.checkbox import CheckBox
from kivy.uix.gridlayout import GridLayout

class check_box(GridLayout):

    def __init__(self, **kwargs):
        super(check_box, self).__init__(**kwargs)

        self.options ={'option 1':0, 'option 2':0, 'option 3':0}

        self.cols = 2

        self.lbl_active = Label(text = 'Select your exercises')
        self.add_widget(self.lbl_active)
        self.lbl_active = Label(text = '')
        self.add_widget(self.lbl_active)

        self.add_widget(Label(text='Option 1'))
        self.active = CheckBox(active = False)
        self.add_widget(self.active)
        self.active.bind(active = self.on_checkbox_Active1)

        self.add_widget(Label(text='Option 2'))
        self.active = CheckBox(active = False)
        self.add_widget(self.active)
        self.active.bind(active = self.on_checkbox_Active2)

        self.add_widget(Label(text='Option 3'))
        self.active = CheckBox(active = False)
        self.add_widget(self.active)
        self.active.bind(active = self.on_checkbox_Active3)

    def on_checkbox_Active1(self, checkboxInstance, value):
        self.options['option 1'] = value
        print(self.options['option 1'])

    def on_checkbox_Active2(self, checkboxInstance, value):
        self.options['option 2'] = value
        print(self.options['option 2'])

    def on_checkbox_Active3(self, checkboxInstance, value):
        self.options['option 3'] = value
        print(self.options['option 3'])

class CheckBoxApp(App):
    def build(self):
        return check_box()

if __name__ == '__main__':
    CheckBoxApp().run()
