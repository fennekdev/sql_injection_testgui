"""
version: production
author: fennekdev
github: https://github.com/fennekdev/sql_injection_testgui
"""
import tkinter as tk
import customtkinter as ctk
import tkinter.messagebox as tkmb
import sqlite3
import os
import db_management as dbm

class App(ctk.CTk,dbm.Query):
	def __init__(self):
		super().__init__()

		self.db_name = "standart_db.db"
		self.current_table="users" # pls use that as standart
		dbm.standart_db_init("standart_db.db")
        
		self.geometry("900x700")

		ctk.set_appearance_mode("dark")
		ctk.set_default_color_theme("dark-blue")

		self.title("Sql-injection test")

		self.resizable(True, True)

		self.pagetitel=ctk.StringVar()
		self.pagetitel.set("Low security login")

		self.query_lvl=1
		self.query_dict ={}
		self.quot_in_query=False
		self.count_to_quot=0
		self.exec_text=ctk.StringVar()
		self.exec_text.set("Executet Query:\nSELECT password\nFROM users\nWHERE username = input_username")
		self.exec_query_prefix="Executet Query:\n"
		self.frame_init()

	def frame_init(self):
		self.mainframe = ctk.CTkFrame(master=self)
		self.mainframe.pack(expand = True)

		self.login_frame_init()
		self.output_frame_init()
		self.query_frame_init()
		self.table_frame_init()

		titel = ctk.CTkLabel(master = self.mainframe,textvariable=self.pagetitel,font=("Arial",15))
		titel.grid(row= 0,pady=10,sticky="W",padx = 20)

		reset_loginframe_but = ctk.CTkButton(master = self.mainframe,text="Reset all",command=self.reset_all,font=("Arial",20))
		reset_loginframe_but.grid(row = 0 ,pady = 10,sticky = "E",padx=10)

		self.table_view_but = ctk.CTkButton(master = self.mainframe, text="Show Tabels", font=("Arial",20),command=self.show_table)
		self.table_view_but.grid(row=0,column=3,padx=10)

		change_query_but=ctk.CTkButton(master=self.mainframe,text="Change Query", command=self.change_query,font=("Arial",20))
		change_query_but.grid(row=0,column=1,columnspan=2)

		self.mainframe.update()

	def show_table(self): # maby use CTkTable for table View
		def on_close():
			print("destoyed")# test
			table_view.destroy()
			self.table_view_but.configure(state="normal")

		table_view = ctk.CTkToplevel(master=self)
		table_view.geometry("400x600")
		table_view.title("Table content")

		self.table_view_but.configure(state="disabled")
		
		table_view.protocol("WM_DELETE_WINDOW", on_close)

		database_label=ctk.CTkLabel(master = table_view,
							  text=dbm.print_db_formated(self.db_name,self.current_table),
							  font=("Arial",17))
		database_label.pack()

	def change_query(self):
		pass

	def reset_all(self):
		self.mainframe.destroy()
		self.frame_init()

	def clear_output(self):
		self.output_textbox.delete("1.0","end")

	def output_frame_init(self):
		self.output_frame = ctk.CTkFrame(master=self.mainframe)
		self.output_frame.grid(row =2,column=0,padx = 10,pady =10,sticky ="nesw",columnspan=2)

		titel = ctk.CTkLabel(master = self.output_frame,text="Output: ",font=("Arial",15))
		titel.grid(sticky = "W",pady=5,padx=20)

		self.output_textbox=ctk.CTkTextbox(master = self.output_frame,fg_color="transparent",font=("Arial",12),border_width=2,wrap="word",text_color=("gray10", "#DCE4EE"),width=600)
		self.output_textbox.grid(row=1,column=0,pady=10,padx=20)
		
	def count_chars_until_index(self,string,index):
		count = 0
		for char in string:
			if count == index:
				break
			count +=1

		return count
	
	def update_query(self):
		self.textbox.configure(state="normal")

		query = self.user_pass.get()
		if len(query) <1:
			pass
			# aktion on empty entry
			self.exec_text.set("Executet Query:\nSELECT password\nFROM users\nWHERE username = input_username")

		updated_query = f"SELECT password\nFROM users\nWHERE username = \"{query}\""
		self.textbox.delete("1.0","end")
		self.textbox.insert(ctk.END,updated_query)

		self.textbox.tag_add("blau",1.0,1.6)
		self.textbox.tag_add("blau",2.0,2.4)
		self.textbox.tag_add("blau",3.0,3.6)

		if query.endswith("--"):
			self.textbox.tag_add("outmark","end -4 chars","end -1 chars")
			self.exec_text.set(self.exec_query_prefix+updated_query[:-3])

		else:
			self.exec_text.set(self.exec_query_prefix+updated_query)


		if query.find("\"") > -1:
			self.quot_in_query = True
			self.count_to_quot+=1

			n = self.count_chars_until_index(updated_query,updated_query.find("\""))
			N = self.count_chars_until_index(query,query.find("\""))
			
			self.textbox.tag_add("rot",f"1.0 + {n+N+1} chars","end -2 chars")

		else:
			self.quot_index = None
			self.quot_in_query = False

		if self.quot_in_query == False:
			self.textbox.tag_add("green","3.18","end -2 chars")

		else:
			n = self.count_chars_until_index(updated_query,updated_query.find("\""))
			N = self.count_chars_until_index(query,query.find("\""))


			self.textbox.tag_add("green",f"1.0 + {n+1} chars",f"1.0 + {n+N+1} chars")

		self.exec_query.update()
		self.textbox.update()
		self.textbox.configure(state="disabled")


	def query_frame_init(self):
		self.query_frame = ctk.CTkFrame(master=self.mainframe,width=300)
		self.query_frame.grid(row =1,column=1,padx = 10,pady =10,sticky="wens")

		label = ctk.CTkLabel(master=self.query_frame,text='SQL Query',font=("Arial",20))
		label.grid(row = 0,sticky = "nw",pady=10)

		querey_pre = "SELECT password\nFROM users\nWHERE username = \"here username\""

		self.textbox = ctk.CTkTextbox(self.query_frame,fg_color="transparent",font=("Arial",17),border_width=2,wrap="word",width=300,height=150)
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

	def table_frame_init(self):  # sql operator legende
		self.table_frame = ctk.CTkFrame(master=self.mainframe)
		self.table_frame.grid(row =1,column=3,padx = 10,pady =10,sticky ="NSE",rowspan = 2)

	def login_frame_init(self):
		self.logframe = ctk.CTkFrame(master=self.mainframe)
		self.logframe.grid(row = 1,padx = 10,pady=10,sticky ="nsew")

		label = ctk.CTkLabel(master=self.logframe,text='Enter Username and Password',font=("Arial",20))
		label.grid(row = 0,pady = 30,padx = 10)

		user_entry= ctk.CTkEntry(master=self.logframe,placeholder_text="Username",font=("Arial",20),width=200)
		user_entry.grid(row = 1,pady = 15)

		self.user_pass= ctk.CTkEntry(master=self.logframe,placeholder_text="Password",font=("Arial",20),width=200)
		self.user_pass.bind("<KeyRelease>", lambda event: self.update_query())
		self.user_pass.grid(row = 2,pady = 20)

		button = ctk.CTkButton(master=self.logframe,text='Login',command=lambda: self.login(user_entry,self.user_pass),font=("Arial",25))
		button.grid(row = 3,pady = 20)


	def login(self,user,passw):

		pass
		
		username=user.get()
		username=str(username)

		password=passw.get()
		password=str(password)

		# basic login should return True
		# should be able to login as admin with injection
		# show to clear out psw databasre
		

if __name__ == "__main__":
	
	app = App()
	#app.test()

	app.mainloop()
