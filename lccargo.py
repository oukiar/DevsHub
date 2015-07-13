
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.popup import Popup

from kivy.properties import ObjectProperty, StringProperty


class TaskMenu(Popup):
    
    taskItem = ObjectProperty()
    
    def selfDelete(self):
        print self.taskItem.taskID
                
        #delete from the database
        tarea = Tareas.Query.get(objectId=self.taskItem.taskID)
        tarea.delete()
        
        
        #update gui
        self.taskItem.parent.parent.parent.parent.updateList()
        
        #close this dialog
        self.dismiss()
        
    def selfSave(self):
        
        tarea = Tareas.Query.get(objectId=self.taskItem.taskID)
        tarea.Task = self.txt_tarea.text
        tarea.Status = self.lst_status.text
        tarea.save()
        
        self.taskItem.parent.parent.parent.parent.updateList()
        
        self.dismiss()

class BattlePlanItem(BoxLayout):
    taskID = StringProperty()
    
    def open_menu(self):
        tm = TaskMenu(taskItem=self)
        tm.txt_tarea.text = self.tasktext.text
        
        #obtener tarea
        tarea = Tareas.Query.get(objectId=self.taskID)
        #inicializar valores en GUI
        tm.lst_status.text = tarea.Status
        
        tm.open()
    
class NewReceipt(BoxLayout):
    tasks = ObjectProperty()
    tasktext = ObjectProperty()
    
    def __init__(self, **kwargs):
        super(NewReceipt, self).__init__(**kwargs)
        

class Reports(BoxLayout):
	pass

class Commendations(BoxLayout):
	pass
	
class Stats(BoxLayout):
	pass

class Orgboat(BoxLayout):
	
	menu = ObjectProperty()
	receipts = ObjectProperty()
	workSpace = ObjectProperty()
	
	def __init__(self, **kwargs):
		super(Orgboat, self).__init__(**kwargs)
		
		self.newreceipt = NewReceipt()
		self.reports = Reports()
		self.commendations = Commendations()
		self.stats = Stats()
		
		self.currentTab = self.receipts
		
	def changeTab(self, tabToShow):
		self.workSpace.remove_widget(self.currentTab)
		
		self.currentTab = tabToShow
		self.workSpace.add_widget(self.currentTab)
		

if __name__ == "__main__":
	from kivy.app import App
	
	class LCCargoApp(App):
		def build(self):
			self.orgboat = Orgboat()
			return self.orgboat
		
	LCCargoApp().run()
