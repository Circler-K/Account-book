import sqlite3
import tkinter.ttk #콤보박스
from tkinter import*
from tkinter import messagebox
import time


##클래스선언
class appGUI:
	@staticmethod
	def combine_funcs(*funcs):
		def combined_func(*args, **kwargs):
			for f in funcs:
				f(*args, **kwargs)
		return combined_func

##개발자정보함수
	def onAbout(self):
	    messagebox.showinfo("About","개발자이름: 김한솔\n학번:30212\n학과:정보통신과")

##조회기능함수
	def selectData(self):
		combo_select=combobox.get()
		if combo_select is '':
			messagebox.showerror('오류', '조회할 행을 선택하시오')
			return

		strData1, strData2, strData3, strData4, strData5, strData6, strData7=[],[],[],[],[],[],[]
		con=sqlite3.connect("db.db")
		cur=con.cursor()
		sql='''SELECT Orders.OrderID
		,Orders.OrderDate
		,OrderDetails.ProductID
		,Products.ProductName
		,OrderDetails.Quantity
		,OrderDetails.UnitPrice
		,OrderDetails.Quantity*OrderDetails.UnitPrice AS Amount
		FROM Orders 
		INNER JOIN Customers ON Orders.CustomerID=Customers.CustomerID
		INNER JOIN OrderDetails ON Orders.OrderID=OrderDetails.OrderID
		INNER JOIN Products ON OrderDetails.ProductID=Products.ProductID
		WHERE 1=1 AND OrderDetails.Quantity*OrderDetails.UnitPrice>=1000 AND Products.ProductID %10 <>0 
		AND Customers.CompanyName="{}" ORDER BY Orders.OrderDate DESC, Products.ProductID ASC'''.format(combo_select) 
		

		print(combo_select)
		print(sql)
		cur.execute(sql)
		while(True):
			row=cur.fetchone()
			if row==None:
				break;
			strData1.append(row[0]);strData2.append(row[1])
			strData3.append(row[2]);strData4.append(row[3])
			strData5.append(row[4]);strData6.append(row[5])
			strData7.append(row[6])
		
		tree.delete(*tree.get_children())
		for item1, item2, item3, item4, item5, item6, item7 in zip(strData1, strData2, strData3, strData4, strData5, strData6,strData7):
			tree.insert("", "end", values=(item1, item2, item3, item4, item5, item6, item7))
			
		self.countCompany() #조회버튼을누를때 주문현황의 조회건수새로고침
		con.close()  

##주문현황의 조회건수함수(새로고침)
	def countCompany(self): 
		con = sqlite3.connect("db.db")
		cur = con.cursor()
		cur.execute("SELECT COUNT(A.OrderID) FROM Orders A INNER JOIN OrderDetails B ON A.OrderID = B.OrderID  INNER JOIN Products C ON B.ProductID = C.ProductID INNER JOIN Customers D ON A.CustomerID=D.CustomerID WHERE 1 = 1 AND B.Quantity * B.UnitPrice >= 1000 AND B.ProductID % 10 != 0 AND D.CompanyName=(?) ORDER BY A.OrderDate DESC, B.ProductID ASC",(combobox.get(),)) 
		numorder = cur.fetchone()
		testlist = list(numorder)
		num = testlist[0]
		self.label7.config(text=num)
		con.close()

##추가레이아웃 함수
	def insertData(self):
		global edt1,edt2,edt3,edt4,edt5,edt6
		top = Toplevel()
		top.title("항목 추가")
		top.geometry("400x300")
		label1=Label(top,text="거래처코드")
		label1.pack()
		edt1= Entry(top)
		edt1.pack()
		label2=Label(top,text="거래처명")
		label2.pack()
		edt2= Entry(top)
		edt2.pack()
		label3=Label(top,text="주문일자\n(다음과같은형식으로 입력하시오 ex)2019-06-13)")
		label3.pack()
		edt3= Entry(top)
		edt3.pack()
		label4=Label(top,text="품목명")
		label4.pack()
		edt4= Entry(top)
		edt4.pack()
		label5=Label(top,text="수량")
		label5.pack()
		edt5= Entry(top)
		edt5.pack()
		label6=Label(top,text="단가")
		label6.pack()
		edt6= Entry(top)
		edt6.pack()
		
		
		button=Button(top,text="적용",bg='#B7F0B1',fg='black',command=self.combine_funcs(lambda: self.insertDB(),top.destroy))
		button.pack(padx=10,pady=10)

##추가기능 함수
	def insertDB(self):
		strData1,strData2,strData3,strData4,strData5,strData6=[],[],[],[],[],[]
		array_list=[]
		array_list.append(edt1.get())
		array_list.append(edt2.get())
		array_list.append(edt3.get())
		array_list.append(edt4.get())
		array_list.append(edt5.get())
		array_list.append(edt6.get())
		for i in array_list:
			if len(i)==0:
				messagebox.showinfo("오류","빈칸이 있습니다.")
				return
		data1=edt1.get() #거래처코드입력
		data2=edt2.get() #거래처명입력
		data3=edt3.get() #주문일자입력
		data4= edt4.get() #품목명입력
		data5=edt5.get() #수량입력
		data6=edt6.get() #단가입력
		
		con=sqlite3.connect("db.db")
		cur=con.cursor()
		#거래처코드, 거래처명입력
		cur.execute("SELECT CustomerID, CompanyName FROM Customers")
		while(True):
			row=cur.fetchone()
			if row==None:
				break;
			strData1.append(row[0]); strData2.append(row[1])
		

			
		##둘다 DB에존재하지않는경우, ##CustomerID는없고 CompanyName DB에존재하는경우
		if data1 not in strData1 and data2 not in strData2:
			cur.execute("INSERT INTO Customers(CustomerID,CompanyName) VALUES((?), (?))",(data1,data2))

		##거래처코드가존재하는경우->DB데이터그대로
		elif data1 in strData1 :
			pass

		
		####주문일자 입력(Order)####
		if len(data3)==10 and data3[4]=='-'and data3[7]=='-'and ((int(data3[5])==0 and int(data3[6])>=1 and int(data3[6])<=9) or(int(data3[5])==1 and int(data3[6])>=0 and int(data3[6])<=2)) and ((int(data3[8])==0 and int(data3[9])>=1 and int(data3[9])<=9) or (int(data3[8])>=1 and int(data3[8])<=2 and int(data3[9])>=0 and int(data3[9])<=9) or (int(data3[8])==3 and int(data3[9])>=0 and int(data3[9])<=1)):
    		
			cur.execute("INSERT INTO Orders(CustomerID,OrderDate) VALUES((?),(?))",(data1,data3))
		else:
			messagebox.showinfo("오류","주문일자형식아닙니다.")
			return

		####품목명 입력(Products)####
		cur.execute("SELECT ProductName FROM Products")
		while(True):
			row=cur.fetchone()
			if row==None:
				break;
			strData4.append(row[0])
		#입력한 품목명이 테이블에있는경우
		if data4 in strData4:
			pass
		elif data4 not in strData4:
			cur.execute("INSERT INTO Products(ProductName) VALUES((?))",(data4,))
		
		#수량,단가입력(OrderDetails)
		cur.execute("SELECT MAX(OrderID) FROM Orders")
		OrderID=cur.fetchone()
		cur.execute("SELECT MAX(ProductID) FROM Products")
		ProductID=cur.fetchone()

		cur.execute("INSERT INTO OrderDetails(OrderID,ProductID,Quantity,UnitPrice) VALUES((?),(?),(?),(?))",(OrderID[0],ProductID[0],data5,data6,))

		con.commit()
		con.close()
		



##종료기능함수
	def Exit(self):
		result = tkinter.messagebox.askquestion("종료","프로그램을 종료하시겠습니까?")
		if result=='yes':
			self.master.destroy()
		else:
			pass
##수정레이아웃 함수	    
	def alterLayout(self): #변경기능 레이아웃

		global entry_list1, entry_list2, entry_list3, entry_list4 #주문일자, 품목명, 수량, 단가
		global entry_list_for_sql1, entry_list_for_sql2, entry_list_for_sql3, entry_list_for_sql4, entry_list_for_sql5, entry_list_for_sql6
		curItem = tree.focus()
		tree_value = tree.item(curItem)['values']
		if tree_value is '':
			messagebox.showerror('오류', '수정할 행을 선택하시오')
			return
		top = Toplevel()
		top.title("항목 수정")
		top.geometry("300x250")
		label1=Label(top,text="주문일자\n(다음과같은형식으로 입력하시오 ex)2019-06-13) ")
		label1.pack()
		entry_list1= Entry(top)
		entry_list1.insert(END,tree_value[1])
		entry_list1.pack()
		label2=Label(top,text="품목명")
		label2.pack()
		entry_list2= Entry(top)
		entry_list2.insert(END,tree_value[3])
		entry_list2.pack()
		label3=Label(top,text="수량")
		label3.pack()
		entry_list3= Entry(top)
		entry_list3.insert(END,tree_value[4])
		entry_list3.pack()
		label4=Label(top,text="단가")
		label4.pack()
		entry_list4= Entry(top)
		entry_list4.insert(END,tree_value[5])
		entry_list4.pack()


		entry_list_for_sql1= tree_value[0] #주문번호
		entry_list_for_sql2= tree_value[1] #주문일자
		entry_list_for_sql3= tree_value[2] #품목코드
		entry_list_for_sql4= tree_value[3] #품목명
		entry_list_for_sql5= tree_value[4] #수량
		entry_list_for_sql6= tree_value[5] #단가
		entry_list_for_sql7= tree_value[6] #금액

		AddButton = Button(top,bg='#B7F0B1',fg='black',text="수정",command=self.combine_funcs(lambda: self.alter(entry_list1,entry_list2,entry_list3,entry_list4),top.destroy))
		AddButton.pack(padx = 10, pady = 10, ipadx=5,ipady=5)

##변경기능 함수
	def alter(self,a1,a2,a3,a4): 
		checklist=[]
		tmp_alter_data1 = a1.get() #주문일자
		tmp_alter_data2 = a2.get() #품목명
		tmp_alter_data3 = a3.get() #수량
		tmp_alter_data4 = a4.get() #단가
		array_list=[]
		array_list.append(a1.get())
		array_list.append(a2.get())
		array_list.append(a3.get())
		array_list.append(a4.get())
		
		for i in array_list:
			if len(i)==0:
				messagebox.showinfo("오류","빈칸이 있습니다.")
				return
		# use selcom in SQL
		con = sqlite3.connect("db.db")
		# update
		cur = con.cursor()
		try :
			#주문일자수정
			cur.execute("UPDATE Orders SET  OrderDate=?  WHERE OrderID=? AND OrderDate=?",(tmp_alter_data1,entry_list_for_sql1,entry_list_for_sql2))
			print(con.commit())
			#수량,단가수정
			cur.execute("UPDATE OrderDetails SET Quantity=?,UnitPrice=? WHERE OrderID=? AND ProductID=? AND Quantity=? AND UnitPrice=?",(tmp_alter_data3,tmp_alter_data4,entry_list_for_sql1,entry_list_for_sql3,entry_list_for_sql5,entry_list_for_sql6))
			print(con.commit())
			#품목명수정
			cur.execute("SELECT ProductName FROM Products")
			while(True):
				productName_Check=cur.fetchone()
				if productName_Check==None:
					break;
				checklist.append(productName_Check[0])
			if tmp_alter_data2 not in checklist:
				messagebox.showerror('오류','수정하고자 하는 품목명이 DB에없습니다.(테이블에있는 품목명을입력하시오)')
			else:
				cur.execute("SELECT ProductID FROM Products WHERE ProductName=?",(tmp_alter_data2,))
				productID_Check=cur.fetchone()
				data=productID_Check[0]
				cur.execute("UPDATE Products SET ProductID=?, ProductName=? WHERE ProductID=? ",(data,tmp_alter_data2,entry_list_for_sql3))
				print(con.commit())
		except :
		    messagebox.showerror('오류', '데이터 수정 오류가 발생함')
		con.close()
		self.selectData()

##삭제기능 함수
	def remove(self): 
		check_OrderID=[]
		curItem = tree.focus()
		tree_value = tree.item(curItem)['values']
		if tree_value is '':
			messagebox.showerror('오류', '삭제할 행을 선택하시오')
			return
        

	    # sql용 변수선언
		tmp_remove_data1 = tree_value[0] #주문번호
		tmp_remove_data2 = tree_value[1] #주문일자
		tmp_remove_data3 = tree_value[2] #품목코드
		tmp_remove_data4 = tree_value[3] #품목명
		tmp_remove_data5 = tree_value[4] #수량
		tmp_remove_data6 = tree_value[5] #단가
		tmp_remove_data7 = tree_value[6] #금액
		con = sqlite3.connect("db.db")
		cur = con.cursor()
		try :
			cur.execute("DELETE FROM OrderDetails WHERE OrderID=? AND ProductID=? AND Quantity=? AND UnitPrice=?",(tmp_remove_data1,tmp_remove_data3,tmp_remove_data5,tmp_remove_data6))
			print(con.commit())
			cur.execute("SELECT OrderID FROM OrderDetails WHERE OrderID=?",(tmp_remove_data1,))
			while(True):
				check=cur.fetchone()
				if check==None: 
					break;
				check_OrderID.append(check[0])
				
			#OrderDetail에 OrderID가없다면 OrderS테이블의 OrderID삭제
			if not check_OrderID:
				cur.execute("DELETE FROM Orders WHERE OrderID=?",(tmp_remove_data1,))
				print(con.commit())
			
		except :
			messagebox.showerror('오류', '데이터 삭제 오류가 발생함')
		con.close()
		self.selectData()

##클래스의생성자
	def __init__(self, master):
		self.master = master #master=window
		global tree,combobox,combo_select
		con, cur= None, None 
		btnList=[None]*4 #버튼5개 
		master.geometry("900x600")
		master.title("프로그램")

		mainMenu=Menu(master)
		master.config(menu=mainMenu)

		style=ttk.Style(master)
		style.configure('TCombobox', font=('궁서체', 10,'bold'), background ='orange',fieldbackground='orange',foreground='orange')
		style.configure("Treeview", background="orange",fieldbackground="orange", foreground="black")
		style.element_create("Custom.Treeheading.border", "from", "default")
		style.layout("Custom.Treeview.Heading", [
			("Custom.Treeheading.cell", {'sticky': 'nswe'}),
			("Custom.Treeheading.border", {'sticky':'nswe', 'children': [
				("Custom.Treeheading.padding", {'sticky':'nswe', 'children': [
					("Custom.Treeheading.image", {'side':'right', 'sticky':''}),
					("Custom.Treeheading.text", {'sticky':'we'})
				]})
			]}),
		])
		style.configure("Custom.Treeview.Heading",  background="black", foreground="white", relief="flat")
		style.map("Custom.Treeview.Heading",relief=[('active','groove'),('pressed','sunken')])

		#파일메뉴
		fileMenu=Menu(mainMenu)
		mainMenu.add_cascade(label="파일",menu=fileMenu)
		fileMenu.add_command(label="조회",command=self.selectData)
		fileMenu.add_separator()
		fileMenu.add_command(label="추가",command=self.insertData)
		fileMenu.add_separator()
		fileMenu.add_command(label="수정",command=self.alterLayout)
		fileMenu.add_separator()
		fileMenu.add_command(label="삭제",command=self.remove)
		fileMenu.add_separator()
		fileMenu.add_command(label="종료",command=self.Exit)
		fileMenu=Menu(mainMenu)
		mainMenu.add_cascade(label="About",menu=fileMenu)
		fileMenu.add_command(label="개발자정보",command=self.onAbout)


		#####메인코드#####
		strData=[]
		listFrame=Frame(master)
		listFrame2=Frame(master) 
		OrdernumFrame = Frame(master)
		DateinfoFrame = Frame(master)
		#(콤보박스리스트)
		con=sqlite3.connect("db.db")
		cur=con.cursor()
		sql='''SELECT DISTINCT Customers.CompanyName
		
		FROM Orders 
		INNER JOIN Customers ON Orders.CustomerID=Customers.CustomerID
		INNER JOIN OrderDetails ON Orders.OrderID=OrderDetails.OrderID
		INNER JOIN Products ON OrderDetails.ProductID=Products.ProductID

		WHERE OrderDetails.Quantity*OrderDetails.UnitPrice>=1000 AND Products.ProductID %10 <>0 ORDER BY Orders.OrderDate DESC, Products.ProductID ASC
		'''
		cur.execute(sql)
		while(True):
			row=cur.fetchone()
			if row ==None:
				break;
			strData.append(row[0])
		combobox=tkinter.ttk.Combobox(listFrame,width=116,height=13,values=(strData))
		tree = ttk.Treeview(listFrame2,style="Custom.Treeview",columns=7,show=["headings"])


		listFrame.pack(side=TOP,fill=BOTH,expand=1)
		button=Button(listFrame, bg='#ABF200',text="조회",command=self.selectData)
		button.pack(side=RIGHT,ipadx=10, ipady=10,padx=10)
		label=Label(listFrame,text="                                                     거래처 현황                                                     ",fg="white",bg="black",font=("궁서체",10))
		label.pack(anchor=NW)



		style.configure('TCombobox', font=('궁서체', 10), background ='orange',fieldbackground='orange')
		combobox.master.option_add( '*TCombobox*Listbox.background', 'orange')
		combobox.pack(side=TOP,anchor=NW)
		
		label2 = Label(listFrame, font=("bold",13), bg = '#F0F0F0', fg = 'black',text = '조회건수:')
		label2.pack(side=LEFT,anchor=NW)
		
		#콤보박스의 개수
		con = sqlite3.connect("db.db")
		cur = con.cursor()
		cur.execute("SELECT COUNT(DISTINCT A.CustomerID)as 조회건수 FROM Customers A INNER JOIN Orders B ON A.CustomerID = B.CustomerID INNER JOIN OrderDetails C ON B.OrderID = C.OrderID WHERE 1 = 1 AND C.Quantity * C.UnitPrice >= 1000 AND C.ProductID % 10 != 0")
		numcompany = cur.fetchone()
		con.close()
		
		lable3 = Label(listFrame,font=("bold",13),bg='#F0F0F0',fg='black',text=numcompany)
		lable3.pack(side=LEFT,anchor=NW)


		
		listFrame2.pack(side=TOP,  fill=BOTH,expand=1)
		label1=Label(listFrame2, text="                                                       주문현황                                                      ",fg="white",bg="black",font=("궁서체",10))
		label1.pack(anchor=NW,pady=1)
		# ============================
		
		tree_yscrollbar = Scrollbar(listFrame2, orient="vertical", command=tree.yview)
		tree.configure(yscroll=tree_yscrollbar.set)
		tree["columns"] = ("wnansqjsgh", "wnansdlfwk", "vnaahrzhem", "vnaahraud", "tnfid","eksrk","rmador") 
		tree.heading('wnansqjsgh', text="주문번호", anchor=W)
		tree.heading('wnansdlfwk', text="주문일자", anchor=W)
		tree.heading('vnaahrzhem', text="품목코드", anchor=W)
		tree.heading('vnaahraud', text="품목명", anchor=W)
		tree.heading('tnfid', text="수량", anchor=W)
		tree.heading('eksrk', text="단가", anchor=W)
		tree.heading('rmador', text="금액", anchor=W)
		tree.column("wnansqjsgh", width=50, stretch=True, minwidth=0) 
		tree.column("wnansdlfwk", width=50, stretch=True)
		tree.column("vnaahrzhem", width=50, stretch=True)
		tree.column("vnaahraud", width=50, stretch=True)
		tree.column("tnfid", width=50, stretch=True)
		tree.column("eksrk", width=50, stretch=True)
		tree.column("rmador", width=50, stretch=True)
		
		
		tree.pack(anchor=NW,side=LEFT,fill=BOTH, expand=1)
		tree_yscrollbar.pack(side=LEFT, fill=Y) 


		btnList[0]=Button(listFrame2,bg='#ABF200', text="추가",command=self.insertData)
		btnList[1]=Button(listFrame2,bg='#ABF200', text="수정",command=self.alterLayout)
		btnList[2]=Button(listFrame2,bg='#ABF200', text="삭제",command=self.remove)
		btnList[3]=Button(listFrame2,bg='#ABF200', text="종료",command=self.Exit)

		for btn in btnList:
			btn.pack(side=TOP,fill=BOTH,ipadx=10, ipady=10,padx=10,pady=30)
		
		
		OrdernumFrame.pack(side=TOP, fill=BOTH) #조회건수
		label6 = Label(OrdernumFrame, font=("bold",13), bg = '#F0F0F0', fg = 'black',text = '조회건수 :')
		label6.pack(side=LEFT)
		self.label7 = Label(OrdernumFrame, font=("bold",13), bg = '#F0F0F0', fg = 'black',text = "Null")
		self.label7.pack(side=LEFT)

		
		DateinfoFrame.pack(side=TOP, fill=BOTH) #현재일시
		label8 = Label(DateinfoFrame, font=("bold",13), bg = '#F0F0F0', fg = 'black',text = '현재일시 :')
		label8.pack(side=LEFT)
		now = time.localtime()
		s = "%04d-%02d-%02d %02d:%02d:%02d" % (now.tm_year, now.tm_mon, now.tm_mday, now.tm_hour, now.tm_min, now.tm_sec)
		label9 = Label(DateinfoFrame, font=("bold",13), bg = '#F0F0F0', fg = 'black',text= s)
		label9.pack(side=LEFT)




##메인함수
def main():
	##변수 선언 부분
	window=Tk()
	MyFirs = appGUI(window)
	window.mainloop()

if __name__ == '__main__':
	main()