"""
python 2.7
"""
import wx
from matplotlib.figure import Figure
from matplotlib.backends.backend_wxagg import FigureCanvasWxAgg as FigureCanvas
import wx.xrc
import numpy as np
import wx.grid as gridlib
import shelve
from accDispConvert import *
from spectraCalculation import *
####################################

####################################
class MySheet(wx.grid.Grid):
    def __init__(self,parent,colName1,nRow,nCol,data):
        super(MySheet,self).__init__(parent)
        self.nRow=nRow
        self.nCol=nCol
        self.data=data
        self.colName1 = colName1
        self.InitUI()
        self.Bind(wx.grid.EVT_GRID_LABEL_RIGHT_CLICK, self.on_label_right_click)


    def InitUI(self):
        nOfRows = self.nRow
        nOfCols = self.nCol
        self.CreateGrid(nOfRows, nOfCols)
        self.SetRowLabelSize(0)
        self.SetLabelFont(wx.Font(12,wx.DEFAULT,wx.NORMAL,wx.NORMAL,False))
        self.SetColLabelValue(0,"times (s)")
        self.SetLabelBackgroundColour((180,247,166))
        self.SetColLabelValue(1,self.colName1)
        [self.SetCellValue(i1, 0, str(format(self.data[i1,0], '.3f')))\
         for i1 in range(len(self.data[:,0]))]
        [self.SetCellValue(i2, 1, str(format(self.data[i2,1], '.6f'))) \
         for i2 in range(len(self.data[:,1]))]
        self.EnableEditing( False )

    def on_label_right_click(self, event):
        menus = [(wx.NewId(), "Copy", self.copy)]
        popup_menu = wx.Menu()
        for menu in menus:
            popup_menu.Append(menu[0], menu[1])
            self.Bind(wx.EVT_MENU, menu[2], id=menu[0])
        self.PopupMenu(popup_menu, event.GetPosition())
        popup_menu.Destroy()
        return

    def copy(self, event):
        """
        Copies range of selected cells to clipboard.
        """
        selection = self.get_selection()
        if not selection:
            return []
        start_row, start_col, end_row, end_col = selection
        data = u''
        rows = range(start_row, end_row + 1)
        for row in rows:
            columns = range(start_col, end_col + 1)
            for idx, column in enumerate(columns, 1):
                if idx == len(columns):
                    # if we are at the last cell of the row, add new line instead
                    data += self.GetCellValue(row, column) + "\n"
                else:
                    data += self.GetCellValue(row, column) + "\t"
        text_data_object = wx.TextDataObject()
        text_data_object.SetText(data)
        if wx.TheClipboard.Open():
            wx.TheClipboard.SetData(text_data_object)
            wx.TheClipboard.Close()
        else:
            wx.MessageBox("Can't open the clipboard", "Warning")

    def get_selection(self):
        """
        Returns selected range's start_row, start_col, end_row, end_col
        If there is no selection, returns selected cell's start_row=end_row, start_col=end_col
        """
        if not len(self.GetSelectionBlockTopLeft()):
            selected_columns = self.GetSelectedCols()
            selected_rows = self.GetSelectedRows()
            if selected_columns:
                start_col = selected_columns[0]
                end_col = selected_columns[-1]
                start_row = 0
                end_row = self.GetNumberRows() - 1
            elif selected_rows:
                start_row = selected_rows[0]
                end_row = selected_rows[-1]
                start_col = 0
                end_col = self.GetNumberCols() - 1
            else:
                start_row = end_row = self.GetGridCursorRow()
                start_col = end_col = self.GetGridCursorCol()
        elif len(self.GetSelectionBlockTopLeft()) > 1:
            wx.MessageBox("Multiple selections are not supported", "Warning")
            return []
        else:
            start_row, start_col = self.GetSelectionBlockTopLeft()[0]
            end_row, end_col = self.GetSelectionBlockBottomRight()[0]
        return [start_row, start_col, end_row, end_col]


####################################
class MyPlot(wx.Panel):
    def __init__(self,parent,X,Y,xTitle,yTitle):
        wx.Panel.__init__(self,parent)
        self.figure = Figure()
        self.figure.subplots_adjust(top =0.95, bottom = 0.25,right=0.99,left=0.1)
        self.axes = self.figure.add_subplot(111)
        self.y_max = 1.0
        self.axes.plot(X,Y)
        self.axes.grid()
        self.axes.set_xlabel(xTitle)
        self.axes.set_ylabel(yTitle)
        self.axes.set_xlim(min(X), max(X))
        yValue=max(np.abs(Y))
        self.axes.set_ylim(-1.2*yValue,1.2*yValue)
        self.canvas = FigureCanvas(self, -1, self.figure)
        sizer = wx.BoxSizer(wx.VERTICAL)
        sizer.Add(self.canvas,1,wx.EXPAND)
        self.SetSizer(sizer)
####################################
class TimeHistoryPage(wx.Panel):
    def __init__(self,parent):
        wx.Panel.__init__(self,parent)
        self.ui()
        self.myPlot()
        self.mySheet()
    def ui(self):
        sizerbase=wx.BoxSizer(wx.HORIZONTAL)
        self.panelH1=wx.Panel(self,style=wx.SUNKEN_BORDER)
        self.panelH2=wx.Panel(self,style=wx.SUNKEN_BORDER)
        sizerbase.Add(self.panelH1,13, wx.EXPAND)
        sizerbase.Add(self.panelH2,2, wx.EXPAND)
        self.SetSizer(sizerbase)

    def mySheet(self):
        sizerH2= wx.GridSizer(3, 1, 5, 5)
        accData=np.hstack((np.mat(self.X).T,np.mat(self.Y).T))
        velData = np.hstack((np.mat(self.X).T, np.mat(self.vel).T))
        dispData = np.hstack((np.mat(self.X).T, np.mat(self.disp).T))
        nrow=len(self.X)
        ncol=2
        sheet1=MySheet(self.panelH2,"acc(g)",nrow,ncol,accData)
        sheet2=MySheet(self.panelH2,"vel(cm/s)",nrow,ncol,velData)
        sheet3= MySheet(self.panelH2,"disp(cm)",nrow,ncol,dispData)
        sizerH2.Add(sheet1,0,wx.EXPAND)
        sizerH2.Add(sheet2,0,wx.EXPAND)
        sizerH2.Add(sheet3,0,wx.EXPAND)
        self.panelH2.SetSizer(sizerH2)

    def myPlot(self):
        sizerH1 = wx.GridSizer(3,1,5,5)
        loadDB = shelve.open('dataStore.db')
        acc= loadDB.get("inputAcc")
        self.X= acc[:,0]
        self.Y= acc[:,1]
        self.dt=self.X[1]-self.X[0]
        self.vel=AccToVelocity(self.dt,self.Y)
        self.disp=VelToDisplacement (self.dt,self.vel)
        plot1 = MyPlot(self.panelH1,self.X,self.Y,"time (s)","acceleration (g)")
        plot2= MyPlot(self.panelH1,self.X,self.vel,"time (s)","velocity (cm/s)")
        plot3 = MyPlot(self.panelH1,self.X,self.disp,"time (s)","displacement (cm)")
        sizerH1.Add(plot1,1,wx.EXPAND)
        sizerH1.Add(plot2,1,wx.EXPAND)
        sizerH1.Add(plot3,1,wx.EXPAND)
        self.panelH1.SetSizerAndFit(sizerH1)


    ####################################
class spectraPage(wx.Panel):
    def __init__(self,parent):
        wx.Panel.__init__(self, parent)
        self.timeAcc=self.loadData()
        self.ui()
        self.responseParaPanel()
        # self.myPlot()
        self.mySheet()

    def loadData(self):
        loadDB = shelve.open('dataStore.db')
        acc = loadDB.get("inputAcc")
        return acc

    def ui(self):
        sizerbase = wx.BoxSizer(wx.HORIZONTAL)
        self.panelH1 = wx.Panel(self, style=wx.SUNKEN_BORDER)
        self.panelH2 = wx.Panel(self, style=wx.SUNKEN_BORDER)
        sizerbase.Add(self.panelH1, 10, wx.EXPAND)
        sizerbase.Add(self.panelH2, 2, wx.EXPAND)
        self.SetSizer(sizerbase)

        sizerH1=wx.BoxSizer(wx.VERTICAL)
        self.panelH1Up=wx.Panel(self.panelH1)
        self.panelH1Down= wx.Panel(self.panelH1)
        sizerH1.Add(self.panelH1Up,1,wx.EXPAND)
        sizerH1.Add(self.panelH1Down,1,wx.EXPAND)
        self.panelH1.SetSizerAndFit(sizerH1)

        sizerH1Up=wx.BoxSizer(wx.HORIZONTAL)
        self.panelH1Up1=wx.Panel(self.panelH1Up)
        self.panelH1Up2 = wx.Panel(self.panelH1Up)
        sizerH1Up.Add(self.panelH1Up1,1,wx.EXPAND)
        sizerH1Up.Add(self.panelH1Up2,1,wx.EXPAND)
        self.panelH1Up.SetSizerAndFit(sizerH1Up)

        sizerH1Down=wx.BoxSizer(wx.HORIZONTAL)
        self.panelH1Down1=wx.Panel(self.panelH1Down)
        self.panelH1Down2=wx.Panel(self.panelH1Down)
        self.panelH1Down3=wx.Panel(self.panelH1Down)
        sizerH1Down.Add(self.panelH1Down1,1,wx.EXPAND)
        sizerH1Down.Add(self.panelH1Down2,1,wx.EXPAND)
        sizerH1Down.Add(self.panelH1Down3,1,wx.EXPAND)
        self.panelH1Down.SetSizerAndFit(sizerH1Down)

        sizerH2=wx.BoxSizer(wx.VERTICAL)
        self.panelH2Up=wx.Panel(self.panelH2)
        self.panelH2Middle=wx.Panel(self.panelH2,style=wx.SUNKEN_BORDER)
        self.panelH2Down=wx.Panel(self.panelH2)
        sizerH2.Add(self.panelH2Up,5,wx.EXPAND)
        sizerH2.Add(self.panelH2Middle,2,wx.EXPAND)
        sizerH2.Add(self.panelH2Down, 5, wx.EXPAND)
        self.panelH2.SetSizerAndFit(sizerH2)

    def responseParaPanel(self):

        sizerH2_1=wx.BoxSizer(wx.VERTICAL)
        panelUp=wx.Panel(self.panelH2Middle)
        panelMiddle=wx.Panel(self.panelH2Middle)
        panelDown=wx.Panel(self.panelH2Middle)
        sizerH2_1.Add(panelUp)
        sizerH2_1.Add(panelMiddle)
        sizerH2_1.Add(panelDown)


        sizerH2H1=wx.BoxSizer(wx.HORIZONTAL)
        sText1 = wx.StaticText(panelUp, label='damping ratio:',style=wx.ALIGN_RIGHT)
        textCtrl1 = wx.TextCtrl(panelUp, -1, style=wx.ALIGN_LEFT)
        sizerH2H1.Add(sText1,1,wx.ALL|wx.CENTER,5)
        sizerH2H1.Add(textCtrl1,1,wx.ALL|wx.RIGHT,5)


        sizerH2H2=wx.BoxSizer(wx.HORIZONTAL)
        sText2= wx.StaticText(panelMiddle, label='period (s):',style=wx.ALIGN_RIGHT)
        textCtrl2= wx.TextCtrl(panelMiddle, -1, style=wx.ALIGN_LEFT)
        sizerH2H2.Add(sText2,wx.ALL|wx.CENTER,5)
        sizerH2H2.Add(textCtrl2,1,wx.ALL|wx.RIGHT,5)



        sizerH2H3=wx.BoxSizer(wx.HORIZONTAL)
        panel3_1=wx.Panel(panelDown)
        panel3_2=wx.Panel(panelDown)
        panel3_3=wx.Panel(panelDown)
        sizerH2H3.Add(panel3_1,3,wx.EXPAND)
        sizerH2H3.Add(panel3_2, 1, wx.EXPAND)
        sizerH2H3.Add(panel3_3, 3, wx.EXPAND)


        sizerH2H3_1=wx.BoxSizer(wx.HORIZONTAL)
        button1 = wx.Button(panel3_2, -1, 'Run',style=wx.BU_EXACTFIT)
        button1.SetOwnBackgroundColour("#E0EEE0")
        sizerH2H3_1.Add(button1, 0, wx.ALIGN_CENTER)
        panel3_2.SetSizerAndFit(sizerH2H3_1)

        panelUp.SetSizerAndFit(sizerH2H1)
        panelMiddle.SetSizerAndFit(sizerH2H2)
        panelDown.SetSizerAndFit(sizerH2H3)
        self.panelH2Middle.SetSizerAndFit(sizerH2_1)






    def mySheet(self):
        X=[1,2,3]
        Y=[3,4,5]
        accData = np.hstack((np.mat(X).T, np.mat(Y).T))
        nrow = len(X)
        ncol = 2
        sizerSheet1=wx.BoxSizer(wx.VERTICAL)
        sheet1 = MySheet(self.panelH2Up, "acc(g)", nrow, ncol, accData)
        sizerSheet1.Add(sheet1,1,wx.EXPAND)
        self.panelH2Up.SetSizer(sizerSheet1)






####################################
class baseView(wx.Frame):
    def __init__(self):
        self.screenSize = wx.DisplaySize()
        title = "Wave Analysis"
        sizeScreen = (self.screenSize[0], self.screenSize[1])
        wx.Frame.__init__(self, None, -1, title, size=sizeScreen)
        self.notebook = wx.Notebook(self)
        menubar = wx.MenuBar()
        fileMenu = wx.Menu()
        fileItem = fileMenu.Append(wx.ID_OPEN, 'Open','Open ground motion')
        self.Bind(wx.EVT_MENU, self.fileOpen, fileItem)
        menubar.Append(fileMenu, '&File')
        self.SetMenuBar(menubar)
        self.statusBar()#set status bar


    def statusBar(self):
        #set status bar
        statusBar = self.CreateStatusBar(number=3)
        statusBar.SetStatusText("Version: 0.0.1", 0)
        statusBar.SetStatusText("Author: Junjun Guo", 1)
        statusBar.SetStatusText("Email: guojj_ce@163.com", 2)

    def fileOpen(self,e):
        wildcard = "Text Files (*.txt)|*.txt"
        dlg = wx.FileDialog(self, "Choose a file", os.getcwd(), "", wildcard, style=wx.FD_OPEN)
        if dlg.ShowModal() == wx.ID_OK:
            openFilePath = dlg.GetPath()
            timeAccValues=np.loadtxt(openFilePath)
            loadDB = shelve.open('dataStore.db', flag='n')
            loadDB["inputAcc"] = timeAccValues
            loadDB.close()
            self.notebook.AddPage(TimeHistoryPage(self.notebook), "Time History")
            self.notebook.AddPage(spectraPage(self.notebook), "spectra")
        dlg.Destroy()

if __name__=="__main__":
    app=wx.App()
    frame=baseView()
    frame.Show(True)
    app.MainLoop()



