def checkpassword(self):
        for i in self.password_Entry.get():
            a = self.password_Entry.get()
            if a[0].isalpha()!=True:
                return 12
            else:
                j =  True
                if j:
                    for i in self.password_Entry.get() :
                        if i.isnumeric():
                            k = True
                            if k :
                                for i in self.password_Entry.get() :
                                    if i in string.punctuation:
                                        return True
            

    def check_email(self):
        if self.email_Entry.get =="":
            messagebox.showerror("Error","please enter Email")
        
        lower = ["a","b","c","d","e","f","g","h","i","j","k","l","m","n","o","p","q","r","s","t","u","v","w","x","y","z",
                 "A","B","C","D","E","F","G","H","I","J","K","L","M","N","O","P","Q","R","S","T","U","V","W","X","Y","Z"]
        number = [ "1","2","3","4","5","6","7","8","9","0"]
        Special = ["." ,"-","_"]
        other = ["!","#","$","%","^","&","*","(",")","[","]","{","}","|","/",":",";","'",'"',"?","<",">","=","+","`","~"]
        email = str(self.email_Entry.get())
        sb =str(self.email_Entry.get())
        if len(email)>=63:
            return False
        if sb.count("@")!=1:
            return False
        s = email.split("@")
        s1 = s[0]
        s2 = s[1]
        if len(s1)<=3:
            return False
        elif s2.count(".")!=1:
            return False
        elif s1.isnumeric():
            return False
        for i in s1:
            if i in other:
                return False
        
        
        
        domain = s2.split(".")
        d1 = domain[0]
        d2 = domain[1]
        for i in d1:
            if i in Special or i in other:
                return False
        for i in d2 :
            if i in Special and i in other:
                return False


        if len(d1)<3:
            return False
        
        elif len(d2)<2:
            return False
        elif ".." in s1 or "__" in s1 or "--" in s1 :
            return False
        elif ".-" in s1 or "._" in s1 or "-_" in s1:
            return False
        elif "-." in s1 or "_." in s1 or "_-" in s1 :
            return False    

        for i in s1:
            if i in lower:
                a= True
                if a:
                    for i in s1:
                        if i in number:
                            b= True
                        else:
                            b = True
                            for i in s1:
                                if i in Special:
                                    return True
                                else:
                                    return True
            else:
                return False    
        else:
            return TRUE         
                                    




    def add(self):
        con = sqlite3.connect(database=r"Billing_System.db")
        cur = con.cursor()
        try:
                if self.Emp_Entry.get() =="":
                    messagebox.showerror("Error", "Employee ID must be required" , parent = self.root)


                elif self.name_Entry.get() =="":
                    messagebox.showerror("Error","Name must be required please enter the name")

                elif self.name_Entry.get().isalpha()!=True:
                    messagebox.showerror("Error","Plese Don't use integers and special letters in name")
                elif self.gender_entry.get() == "Select":
                    messagebox.showerror("Error","Please select the gender")
                elif self.contact_Entry.get() == "":
                    messagebox.showerror("Error","Please enter contact number")       
                elif self.contact_Entry.get().isnumeric()!=True:
                    messagebox.showerror("Error","Plese Don't use Strings and Special letters in Contact")
                elif len(str(self.contact_Entry.get()))!=10:
                    print(len(str(self.contact_Entry.get())))
                    messagebox.showerror("Error", "Invalid Contact Number pleaseenter correct ontact number")
                elif self.check_email()!=True:
                    messagebox.showerror("Error","Invalid email please enter valid email")
                elif self.dob_Entry.get() =="":
                    messagebox.showerror("Error","please enter date of birth")
                elif self.doj_Entry.get() =="":
                    messagebox.showerror("Error","please enter date of Joining")
                elif self.password_Entry.get()=="":
                    messagebox.showerror("Error","Please generate password using mixture of numbers and strings")    
                elif self.checkpassword()==False: 
                    messagebox.showerror("Error","password must be mixture of numbers ,alphabates and special characters please create a strong password")
                elif len(self.password_Entry.get())<6 or len(self.password_Entry.get())>11:
                    messagebox.showerror("Error","the size of password must be greater than 6 and shorter than 11")
                elif self.checkpassword()==12: 
                    messagebox.showerror("Error","Eror first letter must be alphabate in password")
                elif self.Salary_Entry.get()=="":
                    messagebox.showerror("Error","please enter salary")
                elif self.Salary_Entry.get().isnumeric()!=True:
                    messagebox.showerror("Error","please don't strings and special characters in salary")
                elif self.Address_Entry.get("0.1", END).strip()=="":
                    messagebox.showerror("Error","please enter address ")

                else:
                    cur.execute("select * from Employee where eid = ?",(self.Emp_Entry.get(),))
                    row = cur.fetchone()
                    cur.execute("select * from Employee where email = ?",(self.email_Entry.get(),))
                    row2 = cur.fetchone()
                    cur.execute("select * from Employee where utype = 'Admin'")
                    row3 = cur.fetchone()
                    if (row!= None):
                        messagebox.showerror("Error" , "This Employee id already exists , try diffrent", parent = self.root)
                    elif (row2!= None):
                        messagebox.showerror("Error" , "This Emain ID already exists , try diffrent", parent = self.root)
                    elif (row3!= None or row3==None):
                        if self.usert_type_cmb.get() =="Admin" and row3!=None:
                            messagebox.showerror("Error" , "User Type Admin already exists , try diffrent", parent = self.root)
                        elif self.usert_type_cmb.get() == "Employee" or row3==None:
                            cur.execute("insert into Employee (eid,name,email,gender,contact,dob,doj,pass,utype,address,salary) values(?,?,?,?,?,?,?,?,?,?,?)",(
                                    self.Emp_Entry.get(),
                                    self.name_Entry.get(),
                                    self.email_Entry.get(),
                                    self.gender_entry.get(),
                                    self.contact_Entry.get(),
                                    self.dob_Entry.get(),
                                    self.doj_Entry.get(),
                                    self.password_Entry.get(),
                                    self.usert_type_cmb.get(),
                                    self.Address_Entry.get("1.0",END),
                                    self.Salary_Entry.get()                    
                                ))
                            con.commit()
                            messagebox.showinfo("success" , "Employee added sucessfully",parent = self.root)
                            con.close()
                            self.clear()
                    self.show()
        except Exception as ex:
               messagebox.showerror("Error", f"Error due to {str(ex)}",parent = self.root)


    def show(self):
        con = sqlite3.connect(database=r"Billing_System.db")
        cur = con.cursor()
        try:
            cur.execute("select * from Employee")
            rows = cur.fetchall()
            self.frameTreaview.delete(*self.frameTreaview.get_children())
            for row in rows:
                self.frameTreaview.insert("",END,values=row)
            con.close()
        except Exception as ex:
            messagebox.showerror("Error", f"Error due to : {str(ex)}",parent=self.root)



    def get_data(self,ev):
        self.clear()
        try:
            f=self.frameTreaview.focus()
            content = (self.frameTreaview.item(f))
            row=content['values']
            self.Emp_Entry.config(state=WRITABLE)
            self.dob_Entry.config(state=WRITABLE)
            self.doj_Entry.config(state=WRITABLE)
            self.Emp_Entry.delete(0,END)
            self.Emp_Entry.insert(0,row[0]) 
            self.name_Entry.insert(0,row[1]) 
            self.email_Entry.insert(0,row[2]) 
            self.gender_entry.set(row[3]) 
            self.contact_Entry.insert(0,row[4]) 
            self.dob_Entry.insert(0,row[5]) 
            self.doj_Entry.insert(0,row[6]) 
            self.password_Entry.insert(0,row[7]) 
            self.usert_type_cmb.set(row[8]) 
            self.Address_Entry.delete("1.0", END) 
            self.Address_Entry.insert(END ,row[9]) 
            self.Salary_Entry.insert(0,row[10])
            self.Emp_Entry.config(state="readonly")
            self.dob_Entry.config(state="readonly")
            self.doj_Entry.config(state="readonly")



        except Exception as ex:
            messagebox.showerror("Error", f"Error due to {str(ex)}",parent = self.root)


    def update(self):
        con = sqlite3.connect(database=r"Billing_System.db")
        cur = con.cursor()
        try:
                if self.Emp_Entry.get() =="":
                    messagebox.showerror("Error", "Employee ID must be required" , parent = self.root)
                elif self.name_Entry.get() =="":
                    messagebox.showerror("Error","Name must be required please enter the name")
                elif self.name_Entry.get().isalpha()!=True:
                    messagebox.showerror("Error","Plese Don't use integers and special letters in name")
                elif self.gender_entry.get() == "Select":
                    messagebox.showerror("Error","Please select the gender")
                elif self.contact_Entry.get() == "":
                    messagebox.showerror("Error","Please enter contact number")       
                elif self.contact_Entry.get().isnumeric()!=True:
                    messagebox.showerror("Error","Plese Don't use Strings and Special letters in Contact")
                elif len(str(self.contact_Entry.get()))!=10:
                    print(len(str(self.contact_Entry.get())))
                    messagebox.showerror("Error", "Invalid Contact Number pleaseenter correct ontact number")
                elif self.check_email()!=True:
                    messagebox.showerror("Error","Invalid email please enter valid email")
                elif self.dob_Entry.get() =="":
                    messagebox.showerror("Error","please enter date of birth")
                elif self.doj_Entry.get() =="":
                    messagebox.showerror("Error","please enter date of Joining")
                elif self.password_Entry.get()=="":
                    messagebox.showerror("Error","Please generate password using mixture of numbers and strings")    
                elif self.checkpassword()==False: 
                    messagebox.showerror("Error","password must be mixture of numbers ,alphabates and special characters please create a strong password")
                elif len(self.password_Entry.get())<6 or len(self.password_Entry.get())>11:
                    messagebox.showerror("Error","the size of password must be greater than 6 and shorter than 11")
                elif self.checkpassword()==12: 
                    messagebox.showerror("Error","Eror first letter must be alphabate in password")
                elif self.Salary_Entry.get()=="":
                    messagebox.showerror("Error","please enter salary")
                elif self.Salary_Entry.get().isnumeric()!=True:
                    messagebox.showerror("Error","please don't strings and special characters in salary")
                elif self.Address_Entry.get("0.1", END).strip()=="":
                    messagebox.showerror("Error","please enter address ")

                else:
                    cur.execute("select * from Employee where eid = ?",(self.Emp_Entry.get(),))
                    row = cur.fetchone()
                    if row == None:
                        messagebox.showerror("Error" , "Invalid Employee ID", parent = self.root)
                    else:
                        cur.execute("update Employee set name=?,email=?,gender=?,contact=?,dob=?,doj=?,pass=?,utype=?,address=?,salary=? where eid=?",(
                            self.name_Entry.get(),
                            self.email_Entry.get(),
                            self.gender_entry.get(),
                            self.contact_Entry.get(),
                            self.dob_Entry.get(),
                            self.doj_Entry.get(),
                            self.password_Entry.get(),
                            self.usert_type_cmb.get(),
                            self.Address_Entry.get("1.0",END),
                            self.Salary_Entry.get() ,   
                            self.Emp_Entry.get()
                        ))
                        con.commit()
                        messagebox.showinfo("success" , "Employee Updated sucessfully",parent = self.root)
                        con.close()
                        self.show()
                        self.clear()

        except Exception as ex:
            messagebox.showerror("Error", f"Error due to {str(ex)}",parent = self.root)



    def delete(self):
        con = sqlite3.connect(database=r"Billing_System.db")
        cur = con.cursor()
        try:
                if self.Emp_Entry.get() =="":
                    messagebox.showerror("Error", "Employee ID must be required" , parent = self.root)
                else:
                    cur.execute("select * from Employee where eid = ?",(self.Emp_Entry.get(),))
                    row = cur.fetchone()
                    if row == None:
                        messagebox.showerror("Error" , "Invalid Employee ID", parent = self.root)
                    else:
                        op= messagebox.askyesno("conform", "Doyou really want to delete the Employee ?",parent = self.root)
                        if op == True:
                            cur.execute("delete from Employee where eid=?" ,(self.Emp_Entry.get(),))
                            con.commit()
                            messagebox.showinfo("Delete" , "Employee deleted successfully",parent=self.root)
                            con.close()
                            self.show()
                            self.clear()
        except Exception as ex:
            messagebox.showerror("Error", f"Error due to {str(ex)}",parent = self.root)





    def clear(self):
        try:
            self.Emp_Entry.config(state=WRITABLE)
            self.dob_Entry.config(state=WRITABLE)
            self.doj_Entry.config(state=WRITABLE)
            self.Emp_Entry.delete(0, END)  
            self.name_Entry.delete(0, END)  
            self.email_Entry.delete(0, END)  
            self.gender_entry.set("Select")  
            self.gender_entry.insert(0,"Select") 
            self.contact_Entry.delete(0, END)  
            self.dob_Entry.delete(0, END)  
            self.doj_Entry.delete(0, END)  
            self.password_Entry.delete(0, END)
            self.usert_type_cmb.set("Admin")  
            self.usert_type_cmb.insert(0,"Admin") 
            self.Address_Entry.delete(1.0, END)  
            self.Salary_Entry.delete(0, END)  
            self.generateeid()
            self.Emp_Entry.config(state="readonly")
            self.dob_Entry.config(state="readonly")
            self.doj_Entry.config(state="readonly")


        except Exception as ex:
            messagebox.showerror("Error", f"Error due to {str(ex)}",parent = self.root)


    def search(self):
        con = sqlite3.connect(database="Billing_System.db")
        cur = con.cursor()
        try:
            if self.searchby.get()=="Select":
                messagebox.showerror("Error","Select the Search by option" , parent = self.root)

            elif self.searchby.get() == "":
                messagebox.showerror("Error","Search input should be required" , parent=self.root)
            else:
                cur.execute("select * from Employee where "+ self.searchby.get()+" like '%"+self.search1.get()+"%'")
                rows = cur.fetchall()
                if len(rows)!=0:
                    self.frameTreaview.delete(*self.frameTreaview.get_children())
                    for row in rows:
                        self.frameTreaview.insert("",END,values=row)
                else:
                    messagebox.showerror("Error","No record found",parent = self.root)
            con.close()

        except Exception as ex:
            messagebox.showerror("Error",f"Error due to {str(ex)}",parent = self.root)




    def show_calendar(self, event):
        self.lbl = Label(self.root,bg="white" )
        self.lbl.place(x=585,y=260,width=260,height=230 )
        max_date =datetime.now()
        cal = Calendar(self.lbl, selectmode="day", date_pattern = "dd-mm-yyyy",maxdate = max_date,year=2024,day=31 ,month=12)
        cal.pack()
        s = 0
        def get_date():
            date = cal.get_date()
            self.dob_Entry.config(state=WRITABLE)
            self.dob_Entry.delete(0, 'end')
            self.dob_Entry.insert(0, date)
            self.lbl.destroy()
        def cal_state():
            get_date()
            self.dob_Entry.config(state="readonly")
            

        btn_date = Button(self.lbl , text="Slect date" ,relief="solid",border=0,padx=20,pady=10, bg="black",fg="white",command=cal_state,font=("times new roman"  , 20 ,"bold" ),justify="center",cursor="hand2").place(x=80 , y=190 , height=35 , width=120)
        

    def show_calendar_doj(self, event):
        self.lbl1 = Label(self.root,bg="white" )
        self.lbl1.place(x=1040,y=250,width=260,height=230 )
        max_date =datetime.now()
        cal = Calendar(self.lbl1, selectmode="day", date_pattern = "dd-mm-yyyy",maxdate = max_date,year=2024,day=29 ,month=9)
        cal.pack()
        s = 0
        def get_date():
            date = cal.get_date()
            self.doj_Entry.config(state=WRITABLE)
            self.doj_Entry.delete(0, 'end')
            self.doj_Entry.insert(0, date)
            self.lbl1.destroy()
        def cal_state():
            get_date()
            self.doj_Entry.config(state="readonly")
            self.lbl1.destroy()
            

        btn_date = Button(self.lbl1 , text="Slect date" ,relief="solid",border=0,padx=20,pady=10, bg="black",fg="white",command=cal_state,font=("times new roman"  , 20 ,"bold" ),justify="center",cursor="hand2").place(x=80 , y=190 , height=35 , width=120)
        

    def generateeid(self):
        con = sqlite3.connect(database="Billing_System.db")
        cur = con.cursor()
        cur.execute("Select * from Employee")
        row = cur.fetchone()
        if row !=None: 
            self.Emp_Entry.config(state=WRITABLE)
            con = sqlite3.connect(database="Billing_System.db")
            cur = con.cursor()
            cur.execute("SELECT MAX(eid) FROM Employee")
            result = cur.fetchone()
            c = result[0]  # Extracting the integer value from the tuple
            con.commit()
            c = int(c) + 1
            self.Emp_Entry.delete(0, END)
            billno = c
            self.Emp_Entry.insert(0, billno)
            self.Emp_Entry.config(state="readonly")

        else:
            self.Emp_Entry.config(state=WRITABLE)
            billno = 1001
            self.Emp_Entry.delete(0,END)
            self.Emp_Entry.insert(0, billno)
            self.Emp_Entry.config(state="readonly")
