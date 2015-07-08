
from kivy.uix.floatlayout import FloatLayout
from kivy.uix.boxlayout import BoxLayout


#parse stuff
from parse_rest.connection import register, ParseBatcher
from parse_rest.datatypes import Object
from parse_rest.user import User

import time

#parse initialization
register("xIYoHZ0xgLwWIMWzQWPFtxrsZhzmpIQCFCAEJZch", "dqm0KGlhpaK9E0QoGi4dAMWmKuYokiutLegKeRPk")
     
Clientes = Object.factory("Clientes")
Plays = Object.factory("Inventory")

class AddClient(BoxLayout):
    pass

class Pos(BoxLayout):
    pass

class DevsHub(FloatLayout):
    def saveClient(self, w):
        cliente = Clientes()
        cliente.Name = w.parent.txt_name.text
        cliente.Direccion = w.parent.txt_direccion.text
        cliente.Telefono = w.parent.txt_telefono.text
        cliente.IFE = w.parent.txt_ife.text
        cliente.Monedero = w.parent.txt_monedero.text
        cliente.save()

if __name__ == "__main__":
    
    from kivy.app import App
    
    class DevsHubApp(App):
        def build(self):
            return DevsHub()

    DevsHubApp().run()
