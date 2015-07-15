
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.popup import Popup

from kivy.properties import ObjectProperty, StringProperty

from datepicker import DatePicker

from devslib.scrollbox import ScrollBox


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
        tarea.PUser = app.root.user
        tarea.save()
        
        
        taskitem = BattlePlanItem()
        taskitem.tasktext.text = self.tasktext.text
        taskitem.taskID = tarea.objectId
        self.tasks.add_widget(taskitem, index=len(self.tasks.layout.children))

        #clean controls
        self.tasktext.text = ""
        #self.tasktext.focus = True
        
    def updateList(self):
        tareas = Tareas.Query.filter(PUser__in=[app.root.user]).order_by("-createdAt")

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

class Main(BoxLayout):
    pass
    

class Orgboat(BoxLayout):

    menu = ObjectProperty()
    profile = ObjectProperty()
    workSpace = ObjectProperty()

        
    def changeTab(self, tabToShow):
        self.main.workSpace.remove_widget(self.currentTab)
        
        self.currentTab = tabToShow
        self.main.workSpace.add_widget(self.currentTab)

    def do_login(self, login):
        print login
        
        try:
            self.user = User.login(login.txt_email.text, login.txt_password.text)
        except:
            self.user = User.signup(login.txt_email.text, login.txt_password.text)
        
        self.remove_widget(login)
        
        self.main = Main()
        self.main.txt_information.text = self.user.username
        self.add_widget(self.main)

        #create the sections of the user interface
        
        self.battleplan = BattlePlan()
        self.reports = Reports()
        self.commendations = Commendations()
        self.stats = Stats()
        
        self.profile = self.main.profile
        
        #add profile section as visible
        #self.main.workSpace.add_widget(self.profile)
        
        #save the active section for successfull section change
        self.currentTab = self.main.profile
        
        #inicializar interfaz de usuario
        self.battleplan.updateList()

#parse stuff
try:
    Tareas = Object.factory("Tareas")
except:
    from parse_rest.connection import register, ParseBatcher
    from parse_rest.datatypes import Object
    from parse_rest.user import User

    #parse initialization
    register("hwKXR17rbtIP6ER9QL5AvQ5IM7ll17b1Iy3x4uTf", "1TifCFsTXIpUqlcZ0frTyCDHqW5HrCGtW10kqtpS")

    Tareas = Object.factory("Tareas")
    
    

if __name__ == "__main__":

    from kivy.app import App

    class OrgboatApp(App):
        def build(self):
            self.orgboat = Orgboat()
            return self.orgboat
            #return MyProfile()
        
    app = OrgboatApp()
    app.run()
