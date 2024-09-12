"""
version: production
author: fennekdev
github: https://github.com/fennekdev/sql_injection_testgui
tutorial: https://youtu.be/xvFZjo5PgG0?si=bFdqQvvSoPK7LpwR

Injections 
Query lvl 1: password: " Or 1=1--
Query lvl 2: password: admin" as Text) and password = "false" or 1=1--
	
"""
import tkinter as tk
import customtkinter as ctk
from CTkMessagebox import CTkMessagebox
import sqlite3
import os
import db_management as dbm

class App(ctk.CTk,dbm.Query):
	def __init__(self):
		super().__init__()

		self.db_name = "standart_db.db"
		self.current_table="users" # pls use that as standart
		dbm.standart_db_init("standart_db.db")
        
		self.geometry("1300x700")

		ctk.set_appearance_mode("dark")
		ctk.set_default_color_theme("dark-blue")

		self.title("Sql-injection test")

		self.resizable(True, True)

		self.pagetitel=ctk.StringVar()
		self.pagetitel.set("Low security login")

		self.query_lvl=1

		self.exec_text=ctk.StringVar()
		self.exec_text.set("Executet Query:\nSELECT password\nFROM users\nWHERE username = input_username and password = input_password")
		self.exec_query_prefix="Executet Query:\n"
		
		self.user_qouted = False
		self.psw_qouted = False
		
		self.frame_init()

	def frame_init(self):
		self.mainframe = ctk.CTkFrame(master=self)
		self.mainframe.pack(expand = True)

		self.login_frame_init()
		self.output_frame_init()
		self.query_frame_init()
		self.legende_frame_init()

		titel = ctk.CTkLabel(master = self.mainframe,textvariable=self.pagetitel,font=("Arial",15))
		titel.grid(row= 0,pady=10,sticky="W",padx = 10)

		reset_loginframe_but = ctk.CTkButton(master = self.mainframe,text="Reset all",command=self.reset_all,font=("Arial",20))
		reset_loginframe_but.grid(row = 0 ,pady = 10,sticky = "E",padx=10)

		self.table_view_but = ctk.CTkButton(master = self.mainframe, text="Show Tabels", font=("Arial",20),command=self.show_table)
		self.table_view_but.grid(row=0,column=3,padx=10)

		self.change_query_but=ctk.CTkButton(master=self.mainframe,text="Change Query: 1", command=self.change_query,font=("Arial",20))
		self.change_query_but.grid(row=0,column=1,columnspan=2)

		self.mainframe.update()

	def show_table(self): # maby use CTkTable for table View
		def on_close():
			table_view.destroy()
			self.table_view_but.configure(state="normal")

		table_view = ctk.CTkToplevel(master=self)
		table_view.geometry("400x600")
		table_view.wm_attributes("-topmost",True)
		table_view.title("Table content")

		self.table_view_but.configure(state="disabled")
		
		table_view.protocol("WM_DELETE_WINDOW", on_close)

		database_label=ctk.CTkLabel(master = table_view,
							  text=dbm.print_db_formated(self.db_name,self.current_table),
							  font=("Arial",17))
		database_label.pack()

	def change_query(self):
		if self.query_lvl == 1:
			self.query_lvl = 2
			self.change_query_but.configure(text="Change Query: 2")
			self.textbox.configure(state="normal")

			updated_query = "SELECT password\nFROM users\nWHERE username = CAST(\"username\" as TEXT) and password = CAST(\"password\" as TEXT)"
			self.textbox.delete("1.0","end")
			self.textbox.insert(ctk.END,updated_query)
			
			self.textbox.tag_add("blau",1.0,1.6)
			self.textbox.tag_add("blau",2.0,2.4)
			self.textbox.tag_add("blau",3.0,3.6)

		
			self.exec_query.update()
			self.textbox.update()
			self.textbox.configure(state="disabled")
		
		elif self.query_lvl == 2:
			self.query_lvl =3
			self.change_query_but.configure(text="Change Query: 3")

		elif self.query_lvl == 3:
			self.query_lvl =1
			self.change_query_but.configure(text="Change Query: 1")

			querey_pre = "SELECT password\nFROM users\nWHERE username = \"here username\" and password = \"here password\""
			
			self.textbox.configure(state="normal")
			self.textbox.delete("1.0","end")

			self.textbox.insert("1.0", querey_pre)

			self.textbox.tag_add("blau",1.0,1.6)
			self.textbox.tag_add("blau",2.0,2.4)
			self.textbox.tag_add("blau",3.0,3.6)

			self.textbox.tag_config("blau",foreground="cyan")
			self.textbox.tag_config("rot", foreground="indian red")
			self.textbox.tag_config("outmark",background="light grey",foreground ="black")
			self.textbox.tag_config("green",foreground="green")

			self.textbox.configure(state="disabled")



	def reset_all(self):
		self.mainframe.destroy()
		self.frame_init()

	def output_frame_init(self):
		def clear_output():
			self.output_textbox.delete("1.0","end")

		self.output_frame = ctk.CTkFrame(master=self.mainframe)
		self.output_frame.grid(row =2,column=0,padx = 10,pady =10,sticky ="nesw",columnspan=2)

		titel = ctk.CTkLabel(master = self.output_frame,text="Output: ",font=("Arial",15))
		titel.grid(sticky = "W",pady=5,padx=20)

		self.output_textbox=ctk.CTkTextbox(master = self.output_frame,fg_color="transparent",font=("Arial",20),border_width=2,wrap="word",text_color=("gray10", "#DCE4EE"),width=600)
		self.output_textbox.grid(row=1,column=0,pady=10,padx=20)

		clear_button = ctk.CTkButton(master=self.output_frame,text="Clear Output",command=clear_output)
		clear_button.grid(row=1,column=1)
		
	def count_chars_until_index(self,string,index):
		count = 0
		for char in string:
			if count == index:
				break
			count +=1

		return count
	
	def update_query(self):
		self.textbox.configure(state="normal")

		psw = self.user_pass.get()
		user = self.user_entry.get()
		if self.query_lvl == 1:
			if len(psw) <1:
				pass
				# action on empty entry
				self.exec_text.set("Executet Query:\nSELECT password\nFROM users\nWHERE username = input_username")

			updated_query = f"SELECT password\nFROM users\nWHERE username = \"{user}\" and password = \"{psw}\""
			self.textbox.delete("1.0","end")
			self.textbox.insert(ctk.END,updated_query)

			self.textbox.tag_add("blau",1.0,1.6)
			self.textbox.tag_add("blau",2.0,2.4)
			self.textbox.tag_add("blau",3.0,3.6)

			# green taging
			begin_user = self.count_chars_until_index(updated_query,updated_query.find("\""))+1
			end_user = self.count_chars_until_index(updated_query,updated_query.find("\"",begin_user))
			self.textbox.tag_add("green",
						f"1.0 + {begin_user} chars",
						f"1.0 +{end_user} chars")
			
					
			begin_psw = self.count_chars_until_index(updated_query,updated_query.find("\"",begin_user+len(user)+1))
			end_psw = self.count_chars_until_index(updated_query,updated_query.find("\"",begin_psw+1))
			if len(psw):
				self.textbox.tag_add("green",
							f"1.0 + {begin_psw+1} chars",
							f"1.0 +{end_psw} chars")

			# quot detection
			
			if user.find("\"") > -1:
				self.user_qouted = True

				n = self.count_chars_until_index(updated_query,updated_query.find("\"")) # maby here begin on begin_user
				N = self.count_chars_until_index(user,user.find("\""))
				
				self.textbox.tag_add("rot",f"1.0 + {n+N+1} chars",f"end -{len(psw)+20} chars") # end should be last char of user

			else:
				self.user_qouted = False	

			if psw.find("\"") > -1:
				self.psw_qouted = True
				n = self.count_chars_until_index(updated_query,updated_query.find("\"",begin_psw))
				self.textbox.tag_add("rot",f"1.0 + {n+1} chars","end -2 chars")

			else:
				self.psw_qouted = False

			# outcommend detection
			skip = 0
			if updated_query.find("--") != -1:
				if user.find("--") !=-1:
					if self.user_qouted == False:
						skip = updated_query.find("--")+2

					elif self.user_qouted == True:
						# check index from quot
						if user.find("--")>user.find("\""):
							n = self.count_chars_until_index(updated_query,updated_query.find("--"))
							self.textbox.tag_add("outmark",f"1.0 + {n} chars","end -1 chars")
						else:
							# skip index
							skip = updated_query.find("--")+2
				else:
					pass

				if psw.find("--") !=-1:
					if self.psw_qouted == False:
						pass

					elif self.psw_qouted == True:
						if skip == 0:
							if psw.find("--")>psw.find("\""):
								n = self.count_chars_until_index(updated_query,updated_query.find("--"))
								self.textbox.tag_add("outmark",f"1.0 + {n} chars","end -1 chars")

						elif skip != 0:
							if psw.find("--")>psw.find("\""):
								n = self.count_chars_until_index(updated_query,updated_query.find("--",skip+1))
								self.textbox.tag_add("outmark",f"1.0 + {n} chars","end -1 chars")

				else:
					pass
		elif self.query_lvl == 2:
			updated_query = f"SELECT password\nFROM users\nWHERE username = CAST(\"{user}\" as TEXT) and password = CAST(\"{psw}\" as TEXT)"
			self.textbox.delete("1.0","end")
			self.textbox.insert(ctk.END,updated_query)

			self.textbox.tag_add("blau",1.0,1.6)
			self.textbox.tag_add("blau",2.0,2.4)
			self.textbox.tag_add("blau",3.0,3.6)

		elif self.query_lvl == 3:
			updated_query = f"SELECT password\nFROM users\nWHERE username = %s AND password = %s\"\"\"\ncursor.execute(query,({user},{psw}))"
		
			self.textbox.delete("1.0","end")
			self.textbox.insert(ctk.END,updated_query)

			self.textbox.tag_add("blau",1.0,1.6)
			self.textbox.tag_add("blau",2.0,2.4)
			self.textbox.tag_add("blau",3.0,3.6)

		self.exec_query.update()
		self.textbox.update()
		self.textbox.configure(state="disabled")


	def query_frame_init(self):
		self.query_frame = ctk.CTkFrame(master=self.mainframe,width=500)
		self.query_frame.grid(row =1,column=1,padx = 10,pady =10,sticky="wens")

		label = ctk.CTkLabel(master=self.query_frame,text='SQL Query',font=("Arial",20))
		label.grid(row = 0,sticky = "nw",pady=10,padx=5)

		querey_pre = "SELECT password\nFROM users\nWHERE username = \"here username\" and password = \"here password\""

		self.textbox = ctk.CTkTextbox(self.query_frame,fg_color="transparent",font=("Arial",17),border_width=2,wrap="word",width=500,height=150)
		self.textbox.configure(state="normal")
		self.textbox.insert("1.0", querey_pre)

		self.textbox.tag_add("blau",1.0,1.6)
		self.textbox.tag_add("blau",2.0,2.4)
		self.textbox.tag_add("blau",3.0,3.6)

		self.textbox.tag_config("blau",foreground="cyan")
		self.textbox.tag_config("rot", foreground="indian red")
		self.textbox.tag_config("outmark",background="light grey",foreground ="black")
		self.textbox.tag_config("green",foreground="green")

		self.textbox.configure(state="disabled")

		self.textbox.grid(row=1,sticky = "nswe",padx=5)
		
		self.exec_query = ctk.CTkLabel(master = self.query_frame,textvariable=self.exec_text,justify="left",font=("Arial",15))
		self.exec_query.grid(row=2,pady = 10,sticky = "w",padx=5)

	def legende_frame_init(self):  # sql operator legende
		self.legende_frame = ctk.CTkFrame(master=self.mainframe)
		self.legende_frame.grid(row =1,column=3,padx = 10,pady =10,sticky ="NSE",rowspan = 2)

		query_legend_title=ctk.CTkLabel(master=self.legende_frame,text="query cheat-sheet",font=("Arial",15))
		query_legend_title.grid(row = 0)

		query_cheat_sheat = ctk.CTkLabel(master=query_legend_title,font=("Arial",15),text="--\nmakes the code ignore the query comming after it\n\n \"\nwhen used you are allowed to inject query code after\n\n")
		query_cheat_sheat.grid(row = 1,padx = 5)

	def login_frame_init(self):
		self.logframe = ctk.CTkFrame(master=self.mainframe)
		self.logframe.grid(row = 1,padx = 10,pady=10,sticky ="nsew")

		label = ctk.CTkLabel(master=self.logframe,text='Enter Username and Password',font=("Arial",20))
		label.grid(row = 0,pady = 30,padx = 10)

		self.user_entry= ctk.CTkEntry(master=self.logframe,placeholder_text="Username",font=("Arial",20),width=270)
		self.user_entry.grid(row = 1,pady = 15)
		self.user_entry.bind("<KeyRelease>", lambda event: self.update_query())

		self.user_pass= ctk.CTkEntry(master=self.logframe,placeholder_text="Password",font=("Arial",20),width=270)
		self.user_pass.bind("<KeyRelease>", lambda event: self.update_query())
		# later for ohter usage
		self.user_pass.grid(row = 2,pady = 20)

		button = ctk.CTkButton(master=self.logframe,text='Login',command=lambda: self.login(self.user_entry,self.user_pass),font=("Arial",25))
		button.grid(row = 3,pady = 20)


	def login(self,user,passw):
		
		username=user.get()
		#username=str(username) harder lvl

		password=passw.get()
		#password=str(password) harder lvl

		return_value=dbm.exec_query(self.query_lvl,self.db_name,self.current_table,username,password)

		self.output_textbox.insert("1.0",return_value)

		if return_value =="True\n":
			CTkMessagebox(message=f"Login succesfully as {username}",icon="check", option_1="continue")

		elif return_value =="False\n":
			CTkMessagebox(message="Login not succesfully",icon="cancel", option_1="shit")


if __name__ == "__main__":
	
	app = App()
	app.mainloop()
