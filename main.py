
from kivy.uix.floatlayout import FloatLayout
from kivy.uix.boxlayout import BoxLayout
from kivy.properties import ObjectProperty

#parse stuff
from parse_rest.connection import register, ParseBatcher
from parse_rest.datatypes import Object
from parse_rest.user import User

import time

#parse initialization
register("xIYoHZ0xgLwWIMWzQWPFtxrsZhzmpIQCFCAEJZch", "dqm0KGlhpaK9E0QoGi4dAMWmKuYokiutLegKeRPk")
     
Clientes = Object.factory("Clientes")
Inventories = Object.factory("Inventories")

class AddClient(BoxLayout):
    pass

class Pos(BoxLayout):
    pass

class InventoryItem(BoxLayout):

    def addInventoryItem(self, w):
        inventoryitem = Inventories()
        inventoryitem.Clave = w.parent.txt_clave.text
        inventoryitem.Producto = w.parent.txt_producto.text
        inventoryitem.Existencias = w.parent.txt_existencias.text
        inventoryitem.Minimo = w.parent.txt_minimo.text
        inventoryitem.Maximo = w.parent.txt_maximo.text
        inventoryitem.Precio = w.parent.txt_precio.text
        inventoryitem.save()

        newitem = InventoryItem()
        self.parent.parent.parent.parent.lst_inventory.layout.add_widget(newitem)

class Inventory(BoxLayout):
    lst_inventory = ObjectProperty()


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
