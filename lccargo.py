
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
    
class BattlePlan(BoxLayout):
    tasks = ObjectProperty()
    tasktext = ObjectProperty()
    
    def __init__(self, **kwargs):
        super(BattlePlan, self).__init__(**kwargs)
        #self.updateList()
    
    def addTask(self):
        tarea = Tareas()
        tarea.Task = self.tasktext.text
        tarea.Status = "Pending"
        tarea.PUser = devshub.root.user
        tarea.save()
        
        
        taskitem = BattlePlanItem()
        taskitem.tasktext.text = self.tasktext.text
        taskitem.taskID = tarea.objectId
        self.tasks.add_widget(taskitem, index=len(self.tasks.layout.children))

        #clean controls
        self.tasktext.text = ""
        #self.tasktext.focus = True
        
    def updateList(self):
        tareas = Tareas.Query.filter(PUser__in=[devshub.root.user]).order_by("-createdAt")

        self.tasks.clear()

        for tarea in tareas:
            taskitem = BattlePlanItem()
            taskitem.tasktext.text = tarea.Task
            taskitem.taskID = tarea.objectId
            
            if tarea.Status == "Pending":
                taskitem.img_menu.source = "menu_pending.png"
            elif tarea.Status == "In progress":
                taskitem.img_menu.source = "menu_inprogress.png"
            elif tarea.Status == "Done":
                taskitem.img_menu.source = "menu_done.png"
            elif tarea.Status == "Expired":
                taskitem.img_menu.source = "menu_expired.png"
            
            self.tasks.add_widget(taskitem)

class Reports(BoxLayout):
	pass

class Commendations(BoxLayout):
	pass
	
class Stats(BoxLayout):
	pass

class Orgboat(BoxLayout):
	
	menu = ObjectProperty()
	profile = ObjectProperty()
	workSpace = ObjectProperty()
	
	def __init__(self, **kwargs):
		super(Orgboat, self).__init__(**kwargs)
		
		self.battleplan = BattlePlan()
		self.reports = Reports()
		self.commendations = Commendations()
		self.stats = Stats()
		
		self.currentTab = self.profile
		
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
