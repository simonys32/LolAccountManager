import sys
import customtkinter
import os
import LeagueAcc
import json
import os
import endpoints
from pathlib import Path
from tkinter import END, Tk
from PIL import Image
from pydantic import BaseModel 
from dotenv import load_dotenv
from CTkMessagebox import CTkMessagebox
customtkinter.set_appearance_mode("dark")  # Modes: system (default), light, dark
customtkinter.set_default_color_theme("blue")  # Themes: blue (default), dark-blue, green


def resource_path(relative_path):
    if hasattr(sys, "_MEIPASS"):
        return os.path.join(sys._MEIPASS, relative_path)
    else:
        return (relative_path)

accounts = []
greyMain = '#2B2B2B'

dir_path = '%s\\AccountManager\\' %  os.environ['APPDATA'] 
offsetButtonEntry = 0.05
widthButtonEntry = 160
font2=('Agency FB', 25, 'bold')
font3=('Arial', 16)
font4=('Arial', 16, 'bold')
class LeagueAcc2(BaseModel):
    elo: str
    id: str
    loginname: str
    puuid: str
    pw: str
    summoner: str
    tagline: str

class MyHeaderFrame(customtkinter.CTkFrame):
    def __init__(self, master, **kwargs):
        super().__init__(master, **kwargs)

        self.place(relx=0.19, rely=0.05)
        self.grid_propagate(0)
        self.label = customtkinter.CTkLabel(self, text="SummonerName",font=font2)
        self.label2 = customtkinter.CTkLabel(self, text="Rank",font=font2)
        self.label3 = customtkinter.CTkLabel(self, text="Loginname",font=font2)
        self.label4 = customtkinter.CTkLabel(self, text="Password",font=font2)

        self.columnconfigure(1, weight=25)
        self.columnconfigure(2, weight=25)
        self.columnconfigure(3, weight=25)
        self.columnconfigure(4, weight=25)

        self.label.grid(row=0, column=1, pady=9)
        self.label2.grid(row=0, column=2, pady=9)
        self.label3.grid(row=0, column=3, pady=9)
        self.label4.grid(row=0, column=4, pady=9)


class MyFrame(customtkinter.CTkScrollableFrame):
    def __init__(self, master, **kwargs):
        super().__init__(master, **kwargs)

        self.columnconfigure(1, weight=30)
        self.columnconfigure(2, weight=15)
        
        self.columnconfigure(3, weight=5)
        self.columnconfigure(4, weight=25)
        self.columnconfigure(5, weight=25)

    def start(self):
        self.place(relx=0.19, rely=0.10)
        x = 1
        for account in accounts:
            self.label = customtkinter.CTkEntry(self, placeholder_text=account.loginname, font=font3, border_color=greyMain, border_width=0, fg_color=greyMain,justify='center')
            self.label.insert(0, account.summoner+'#'+account.tagline)
            self.label.configure(state='readonly')
            self.label2 = customtkinter.CTkEntry(self, placeholder_text=account.loginname, font=font4, border_color=greyMain, border_width=0, fg_color=greyMain,justify='center')
            self.label2.insert(0, account.elo)
            self.label2.configure(state='readonly')
            self.label3 = customtkinter.CTkEntry(self, placeholder_text=account.loginname, font=font3, border_color=greyMain, border_width=0, fg_color=greyMain,justify='center')
            self.label3.insert(0, account.loginname)
            self.label3.configure(state='readonly')
            self.label4 = customtkinter.CTkEntry(self, placeholder_text=account.loginname, font=font3, border_color=greyMain, border_width=0, fg_color=greyMain, justify='center')
            self.label4.insert(0,account.pw)
            self.label4.configure(state='readonly')
            self.label4.pack_propagate(0)

            elocheck = account.elo.split()

            imgPath = '../img/'
            match elocheck[0]:
                case 'MASTER':
                    imgPath+='master'
                case 'GRANDMASTER':
                     imgPath+='grandmaster'
                case 'DIAMOND':
                     imgPath+='diamond'
                case 'IRON':
                     imgPath+='iron'
                case 'CHALLENGER':
                     imgPath+='challenger'
                case 'BRONZE':
                     imgPath+='bronze'
                case 'PLATINUM':
                     imgPath+='platinum'
                case 'GOLD':
                     imgPath+='gold'
                case 'EMERALD':
                     imgPath+='emerald'
                case _:
                    imgPath+='unranked'
            imgPath+='.png'    
            rank_img = customtkinter.CTkImage(Image.open(resource_path(imgPath)), size=(55, 55))

            self.labelElo = customtkinter.CTkLabel(self, image=rank_img , text="", font=font3,)

            self.labelElo.grid(row=x, column=3, pady=9)
            self.label.grid(row=x, column=1, pady=9)
            self.label2.grid(row=x, column=2, pady=9)
            self.label3.grid(row=x, column=4, pady=9)
            self.label4.grid(row=x, column=5, pady=9)
            x += 1
    
    def clip(self, input):
        r = Tk()
        print(input)
        r.withdraw()
        r.clipboard_clear()
        r.clipboard_append(input)
        r.update() #

        
class App(customtkinter.CTk):
    def __init__(self):
        
       
        load_dotenv()
        super().__init__()
        if not os.path.exists(dir_path):
            os.makedirs(dir_path)
        
        self.loadData()
        self.winfo_exists

        self.geometry("1650x800")
        self.title("League Account Manager")
        self.wm_iconbitmap(resource_path('../img/dab.ico'))
        pingu_img = customtkinter.CTkImage(Image.open(resource_path('../img/dab.png')), size=(100, 100))

        self.pingu = customtkinter.CTkLabel(self, image=pingu_img , text="")
        self.pingu.place(relx=offsetButtonEntry+0.018, rely=0.15, anchor=customtkinter.NW)

        self.grid_rowconfigure(0, weight=1)  # configure grid system
        self.grid_columnconfigure(0, weight=1)

        self.resizable(False, False)

        self.entry = customtkinter.CTkEntry(self,width=widthButtonEntry, placeholder_text="Loginname")
        self.entry.place(relx=offsetButtonEntry, rely=0.3,anchor=customtkinter.W)

        self.entry2 = customtkinter.CTkEntry(self,width=widthButtonEntry, placeholder_text="Password")
        self.entry2.place(relx=offsetButtonEntry, rely=0.35,anchor=customtkinter.W)

        self.entry3 = customtkinter.CTkEntry(self,width=widthButtonEntry, placeholder_text="Summonername")
        self.entry3.place(relx=offsetButtonEntry, rely=0.4,anchor=customtkinter.W)

        self.entry4 = customtkinter.CTkEntry(self, width=widthButtonEntry, placeholder_text="Tagline")
        self.entry4.place(relx=offsetButtonEntry, rely=0.45,anchor=customtkinter.W)

        #remove buttons
        self.entry6 = customtkinter.CTkEntry(self,width=widthButtonEntry, placeholder_text="Summonername")
        self.entry6.place(relx=offsetButtonEntry, rely=0.70,anchor=customtkinter.W)

        self.entry5 = customtkinter.CTkEntry(self,width=widthButtonEntry, placeholder_text="Tagline")
        self.entry5.place(relx=offsetButtonEntry, rely=0.75,anchor=customtkinter.W)

        

        self.button3 = customtkinter.CTkButton(self, width=widthButtonEntry, height=60,text="Remove Account", command=self.removeAccount, font=font2)
        self.button3.place(relx=offsetButtonEntry, rely=0.80, anchor=customtkinter.NW)

        self.dataFrame = MyFrame(master=self, width=1200,height=650)
       
        self.headerFrame = MyHeaderFrame(master=self, width=1221, height=50, border_color="darkgray", border_width=4, fg_color="#3f3f3f")

        self.button = customtkinter.CTkButton(self, width=widthButtonEntry, height=60,text="Reload Elo", command=self.button_refresh, font=font2)
        self.button.place(relx=offsetButtonEntry, rely=0.05, anchor=customtkinter.NW)

        
        self.button2 = customtkinter.CTkButton(self, width=widthButtonEntry, height=60,text="Add Account", command=self.button_addaccount, font=font2)
        self.button2.place(relx=offsetButtonEntry, rely=0.5, anchor=customtkinter.NW)
        
        self.labelResult =customtkinter.CTkLabel(self, text= "")
        self.labelResult.place(relx=0.06,rely=0.45)
        self.dataFrame.start()

        
    

    def saveAccounts(self):
        outputJson = '{\n "LeagueAcc": [\n \t'
        for idx, account in enumerate(accounts):
            if(idx==0):
                outputJson += account.toJSON()+'\n'
            else:
                outputJson += ',\n' + account.toJSON()
        outputJson+='\n]\n }'
        with open(dir_path+"dataprint.json", "w") as outfile:
            outfile.write(outputJson)


    def button_refresh(self):
        for account in accounts:
            account.reloadElo()
        self.saveAccounts()
        self.dataFrame.start()

    

    def button_addaccount(self):
        newacc = LeagueAcc.LeagueAcc(self.entry.get(), self.entry2.get(), self.entry3.get(), self.entry4.get())
        newAccountResult = newacc.loadData()

        if newAccountResult:
             accounts.append(newacc)
             self.button_refresh()
             CTkMessagebox(title="Success",message="Account added successfully",icon="check", option_1="Thanks")
             self.entry.delete(0,END)
             self.entry2.delete(0,END)
             self.entry3.delete(0,END)
             self.entry4.delete(0,END)
        else:
            CTkMessagebox(title="Error", message="Failed to add account, try again",icon="warning", option_1="Try again")
        

        #Validate data
        self.saveAccounts()
    
    
    def loadData(self):
        
        dataprintCheck = Path(dir_path+'dataprint.json')
        if dataprintCheck.is_file() == True:
           with open(dir_path+'dataprint.json', 'r') as openfile:
            json_object = json.load(openfile)
            
            league_accs = [LeagueAcc2.model_validate(item) for item in json_object["LeagueAcc"]]
            
            for leagueacc in league_accs:
                currAcc = LeagueAcc.LeagueAcc(leagueacc.loginname,leagueacc.pw, leagueacc.summoner, leagueacc.tagline)
                currAcc.setPuuid(leagueacc.puuid)
                currAcc.setid(leagueacc.id)
                currAcc.setElo(leagueacc.elo)
                currAcc.reloadName()
                accounts.append(currAcc)

    
            
    def clearFrame(self):
    # destroy all widgets from frame
        for widget in self.dataFrame.winfo_children():
            widget.destroy()
        self.dataFrame.place_forget()
    
    def removeAccount(self):
        answer = True
        dataprintCheck = Path(dir_path+'dataprint.json')
        if dataprintCheck.is_file() == True:
            deleteName = self.entry6.get()
            deleteTag = self.entry5.get()
           
            
            with open(dir_path+'dataprint.json', 'r') as openfile:
                accounts.clear()
                json_object = json.load(openfile)
                
                league_accs = [LeagueAcc2.model_validate(item) for item in json_object["LeagueAcc"]]
            
                for leagueacc in league_accs:
                    
                    if(leagueacc.summoner==deleteName and leagueacc.tagline==deleteTag):
                        answer = False
                        continue
                        
                    else:
                        currAcc = LeagueAcc.LeagueAcc(leagueacc.loginname,leagueacc.pw, leagueacc.summoner, leagueacc.tagline)
                        currAcc.setPuuid(leagueacc.puuid)
                        currAcc.setid(leagueacc.id)
                        currAcc.setElo(leagueacc.elo)
                        accounts.append(currAcc)
                self.saveAccounts()
                self.clearFrame()
                self.dataFrame.start()
                self.entry5.delete(0,END)
                self.entry6.delete(0,END)

        if(answer):
            CTkMessagebox(title="Error", message="No matching account found",icon="warning", option_1="Retry")
        else:
            CTkMessagebox(title="Success", message="Removed account successfully",icon="check", option_1="Thanks") 
        
app = App()
app.mainloop()


