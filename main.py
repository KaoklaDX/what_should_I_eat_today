from kivy.app import App
from kivy.uix.screenmanager import ScreenManager, Screen
from kivy.uix.label import Label
from kivy.uix.button import Button
from kivy.uix.floatlayout import FloatLayout
from kivy.uix.boxlayout import BoxLayout
from kivy.graphics import Color, Rectangle, RoundedRectangle
from kivy.graphics.texture import Texture
from kivy.uix.textinput import TextInput
from kivy.uix.spinner import Spinner
from kivy.uix.popup import Popup
from kivy.core.window import Window
from kivy.metrics import dp
from kivy.uix.image import Image
from kivy.uix.scrollview import ScrollView
from kivy.resources import resource_find
import random
import pickle

class Food():
    def __init__(self, name, country, spice):
        self.name = name
        self.country = country
        self.spice = spice

    def __repr__(self):
        return f'Name = {self.name} Country = {self.country} Spice = {self.spice}'

class GradientBackground(FloatLayout):
    def __init__(self, **kwargs):
        super(GradientBackground, self).__init__(**kwargs)
        with self.canvas.before:
            # Define the gradient colors
            Color(0.992, 0.988, 0.902)  # equivalent to #FDFCE6
            self.rect = Rectangle(pos=self.pos, size=self.size)
        self.bind(size=self._update_rect)

    def _update_rect(self, instance, value):
        self.rect.size = value

class MyPopup(Popup):
    def __init__(self, title, message, **kwargs):
        super(MyPopup, self).__init__(**kwargs)
        self.title = title
        self.content = Label(text=message)
        self.size_hint = (None, None)
        self.size = (400, 200)

        close_button = Button(text='Close')
        close_button.bind(on_release=self.dismiss)
        self.content.add_widget(close_button)

class RoundedButton(Button):
    def __init__(self, **kwargs):
        super(RoundedButton, self).__init__(**kwargs)
        self.background_color = (0.922, 0.075, 0.075, 1)  # Set the background color with alpha channel
        self.radius = [20]  # Set the radius for rounded corners
        self.background_normal = ''
        self.bind(size=self._update_graphics, pos=self._update_graphics)

    def _update_graphics(self, *args):
        self.canvas.before.clear()  # Clear previous instructions
        with self.canvas.before:
            # Set background color
            Color(*self.background_color)
            # Draw rounded rectangle background
            RoundedRectangle(pos=self.pos, size=self.size, radius=self.radius)


class Back_Button(Button):
    def __init__(self, **kwargs):
        super(Back_Button, self).__init__(**kwargs)
        self.background_normal = ''
        self.background_color = (0.663, 0.91, 0.667, 1)
        self.text = 'back'



class StartScreen(Screen):
    def __init__(self, **kwargs):
        super(StartScreen, self).__init__(**kwargs)
        layout = FloatLayout()
        gradient_background = GradientBackground()
        label = Label(text="What should I eat Today?", font_size='24sp', color=(0, 0, 0, 1), size_hint=(None, None), size=(400, 50), pos_hint={"center_x": 0.5, 'top': 0.9})
        next_page = RoundedButton(text='Start', size_hint={0.2,0.15}, pos_hint={"center_x": 0.5, 'top':0.4})
        next_page.bind(on_press=self.on_press)
        layout.add_widget(gradient_background)
        layout.add_widget(label)
        layout.add_widget(next_page)
        self.add_widget(layout)

    def on_press(self ,instance):
        self.manager.current = 'Home'


class HomeScreen(Screen):
    def __init__(self, **kwargs):
        super(HomeScreen, self).__init__(**kwargs)
        layout = FloatLayout()
        gradient_background = GradientBackground()
        label = Label(text="What do you want to do?", font_size='24sp', color=(0, 0, 0, 1), size_hint=(None, None), size=(400, 50), pos_hint={"center_x": 0.5, 'top': 0.9})
        Add_food = RoundedButton(text='Add food', size_hint=(0.4, 0.1), pos_hint={"center_x": 0.5, 'top': 0.85})
        Add_food.bind(on_press=self.go_to_Add_food)
        Delete_food = RoundedButton(text='Delete food', size_hint=(0.4, 0.1), pos_hint={"center_x": 0.5, 'top': 0.725})
        Delete_food.bind(on_press=self.go_to_Delete_food)
        Show_food = RoundedButton(text='Show all food', size_hint=(0.4, 0.1), pos_hint={"center_x": 0.5, 'top': 0.6})
        Show_food.bind(on_press=self.go_to_Show_food)
        Random_food = RoundedButton(text='Random food', size_hint=(0.4, 0.1), pos_hint={"center_x": 0.5, 'top': 0.475})
        Random_food.bind(on_press=self.go_to_Random_food)
        layout.add_widget(gradient_background)
        layout.add_widget(label)
        layout.add_widget(Add_food)
        layout.add_widget(Delete_food)
        layout.add_widget(Show_food)
        layout.add_widget(Random_food)
        self.add_widget(layout)

    def go_to_Add_food(self, instance):
        self.manager.current = 'Add_food'

    def go_to_Delete_food(self, instance):
        self.manager.current = 'Delete_food'

    def go_to_Show_food(self, instance):
        self.manager.current = 'Show_food'

    def go_to_Random_food(self, instance):
        self.manager.current = 'Random_food'
class Add_foodScreen(Screen):
    def __init__(self, **kwargs):
        super(Add_foodScreen, self).__init__(**kwargs)
        layout = FloatLayout()
        gradient_background = GradientBackground()
        label = Label(text="Enter your Data", font_size='24sp', color=(0, 0, 0, 1), size_hint=(None, None), size=(400, 50), pos_hint={"center_x": 0.5, 'top': 0.9})
        self.food_name = TextInput(hint_text="Enter food name", font_size='24sp', multiline=False, size_hint=(0.4, 0.1), pos_hint={'center_x': 0.5, 'top': 0.85})
        self.food_country = TextInput(hint_text="Enter country name", font_size='24sp',multiline=False, size_hint=(0.4, 0.1), pos_hint={'center_x': 0.5, 'top': 0.7})
        self.food_spice = Spinner(text='Is it Spicy', values=('True', 'False'), size_hint=(0.4, 0.1), pos_hint={'center_x': 0.5, 'top': 0.55})
        submit_button = RoundedButton(text='Submit', size_hint={0.4,0.1}, pos_hint={'center_x': 0.5, 'top': 0.4})
        submit_button.bind(on_press = self.submit_data)
        back = Back_Button(size_hint={0.2,0.1},pos_hint={'left': 1, 'top': 1})
        back.bind(on_press = self.go_back)
        layout.add_widget(gradient_background)
        layout.add_widget(label)
        layout.add_widget(self.food_name)
        layout.add_widget(self.food_country)
        layout.add_widget(self.food_spice)
        layout.add_widget(submit_button)
        layout.add_widget(back)
        self.add_widget(layout)
    def go_back(self, instance):
        self.manager.current = 'Home'

    def submit_data(self, instance):
        food_name = self.food_name.text
        food_country = self.food_country.text
        food_spice = self.food_spice.text
        new_food = Food(name=food_name, country=food_country, spice=(food_spice == 'True'))

        try:
            with open('data.pkl', 'rb') as file:
                data = pickle.load(file)
        except FileNotFoundError:
            data = []

        data.append(new_food)

        with open('data.pkl', 'wb') as file:
            pickle.dump(data, file)

        self.food_name.text = ""
        self.food_country.text = ""
        self.food_spice.text = 'Is it Spicy'

        # Get the instance of Show_foodScreen and call add_food_real_time
        show_food_screen = self.manager.get_screen('Show_food')
        show_food_screen.add_food_real_time(new_food)

        self.manager.current = 'Home'

class Delete_foodScreen(Screen):
    def __init__(self, **kwargs):
        super(Delete_foodScreen, self).__init__(**kwargs)
        layout = FloatLayout()
        gradient_background = GradientBackground()
        label = Label(text='Enter food name you want to delete',font_size='24sp', color=(0, 0, 0, 1), size_hint=(None, None), size=(400, 50), pos_hint={"center_x": 0.5, 'top': 0.9})
        self.food_name= TextInput(hint_text='Enter your food name',font_size='24sp', multiline=False, size_hint=(0.4, 0.1), pos_hint={'center_x': 0.5, 'top': 0.8})
        submit_button = RoundedButton(text='Submit', size_hint={0.4, 0.1}, pos_hint={'center_x': 0.5, 'top': 0.4})
        submit_button.bind(on_press=self.submit_data)
        back = Back_Button(size_hint={0.2, 0.1}, pos_hint={'left': 1, 'top': 1})
        back.bind(on_press=self.go_back)
        layout.add_widget(gradient_background)
        layout.add_widget(label)
        layout.add_widget(self.food_name)
        layout.add_widget(submit_button)
        layout.add_widget(back)
        self.add_widget(layout)
    def go_back(self, instance):
        self.manager.current = 'Home'
    def submit_data(self, instance):
        food_name = self.food_name.text
        try:
            with open('data.pkl', 'rb') as file:
                data = pickle.load(file)
        except FileNotFoundError:
            self.food_name.text = ""
            popup = MyPopup(title='Alert', message='No data in this File')
            popup.open()
            return

        have_data = False
        for food in data:
            if food_name != food.name:
                continue
            else:
                have_data = True

        if not have_data:
            self.food_name.text = ""
            popup = MyPopup(title='Alert', message='No Food name in this File')
            popup.open()
            return

        def result(food, food_name):
            return [food for food in data if food.name != food_name]

        New_Data = result(food_name, food_name)

        with open('data.pkl', 'wb') as file:
            pickle.dump(New_Data, file)

        self.food_name.text = ""

        # Get the instance of Show_foodScreen and call delete_food_real_time
        show_food_screen = self.manager.get_screen('Show_food')
        show_food_screen.delete_food_real_time(food_name)

        self.manager.current = 'Home'


class Show_foodScreen(Screen):
    def __init__(self, **kwargs):
        super(Show_foodScreen, self).__init__(**kwargs)
        self.layout = FloatLayout()
        self.gradient_background = GradientBackground()
        self.back = Back_Button(size_hint={0.2,0.1},pos_hint={'left': 1, 'top': 1})
        self.back.bind(on_press = self.go_back)
        self.label = Label(text="All Foods", font_size='24sp', color=(0, 0, 0, 1),
                           size_hint=(None, None), size=(400, 50),
                           pos_hint={"center_x": 0.5, 'top': 0.9})

        self.scroll_view = ScrollView(size_hint=(1, None), size=(Window.width, Window.height - self.label.height - 10))
        self.food_layout = BoxLayout(orientation='vertical', size_hint_y=None, spacing=10)
        self.food_layout.bind(minimum_height=self.food_layout.setter('height'))  # Allow the layout to expand as needed
        self.scroll_view.add_widget(self.food_layout)

        self.layout.add_widget(self.gradient_background)
        self.layout.add_widget(self.label)
        self.layout.add_widget(self.back)
        self.layout.add_widget(self.scroll_view)
        self.add_widget(self.layout)

        # Load data from file initially
        self.food_items = self.load_data()
        self.refresh_display()
    def go_back(self, instance):
        self.manager.current = 'Home'
    def refresh_display(self):
        # Clear existing food widgets
        self.food_layout.clear_widgets()

        # Populate the food layout with labels for each food item
        for food in self.food_items:
            food_label = Label(text=str(food), font_size='16sp', size_hint_y=None, height=dp(40), color=(0, 0, 0, 1))
            self.food_layout.add_widget(food_label)

        # Calculate the height of the scroll view based on the number of food items
        scroll_height = len(self.food_items) * dp(65)  # Assuming each label is 50dp in height
        self.scroll_view.height = max(scroll_height, Window.height - self.label.height - dp(10))

    def add_food_real_time(self, new_food):
        # Add new food item to data structure
        self.food_items.append(new_food)

        # Refresh display to reflect the addition
        self.refresh_display()

    def delete_food_real_time(self, food_to_delete):
        # Remove food item from data structure
        self.food_items = [food for food in self.food_items if food.name != food_to_delete]

        # Refresh display to reflect the deletion
        self.refresh_display()

    def load_data(self):
        try:
            with open("data.pkl", "rb") as f:
                return pickle.load(f)
        except FileNotFoundError:
            return []

class RandomFoodScreen(Screen):
    def __init__(self, **kwargs):
        super(RandomFoodScreen, self).__init__(**kwargs)
        layout = FloatLayout()
        gradient_background = GradientBackground()
        label = Label(text="Random Food", font_size='24sp', color=(0, 0, 0, 1), size_hint=(None, None),
                      size=(400, 50), pos_hint={"center_x": 0.5, 'top': 0.9})
        self.label2 = Label(text="Start random you food", font_size='24sp', color=(0, 0, 0, 1), size_hint=(None, None),
                      size=(400, 50), pos_hint={"center_x": 0.5, 'top': 0.7})
        submit_button = RoundedButton(text='Random', size_hint={0.4, 0.1}, pos_hint={'center_x': 0.5, 'top': 0.4})
        submit_button.bind(on_press=self.random_food_submit)
        back = Back_Button(size_hint={0.2, 0.1}, pos_hint={'left': 1, 'top': 1})
        back.bind(on_press=self.go_back)
        layout.add_widget(gradient_background)
        layout.add_widget(label)
        layout.add_widget(self.label2)
        layout.add_widget(submit_button)
        layout.add_widget(back)
        self.add_widget(layout)
    def go_back(self, instance):
        self.manager.current = 'Home'
    def random_food_submit(self, instance):
        try:
            with open('data.pkl', 'rb') as file:
                data = pickle.load(file)
        except FileNotFoundError:
            popup = MyPopup(title='Alert', message='No data in this File')
            popup.open()
            return
        data_2 = []
        for food in data:
            data_2.append(food.name)
        self.label2.text = random.choice(data_2)

class WhatshouldIeatTodayApp(App):
    def build(self):
        sm = ScreenManager()
        sm.add_widget(StartScreen(name='Start'))
        sm.add_widget(HomeScreen(name='Home'))
        sm.add_widget(Add_foodScreen(name='Add_food'))
        sm.add_widget(Delete_foodScreen(name='Delete_food'))
        sm.add_widget(RandomFoodScreen(name='Random_food'))
        sm.add_widget(Show_foodScreen(name='Show_food'))
        return sm

if __name__ == '__main__':
    WhatshouldIeatTodayApp().run()
