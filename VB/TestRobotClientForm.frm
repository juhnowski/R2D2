VERSION 5.00
Object = "*\ARobotClient.vbp"
Begin VB.Form frmTestRobotClient 
   Caption         =   "Симулятор"
   ClientHeight    =   4590
   ClientLeft      =   120
   ClientTop       =   450
   ClientWidth     =   4050
   LinkTopic       =   "Form1"
   MinButton       =   0   'False
   ScaleHeight     =   4590
   ScaleWidth      =   4050
   StartUpPosition =   3  'Windows Default
   Begin PrjRobotClient.RobotClientControl rcc 
      Height          =   4575
      Left            =   0
      TabIndex        =   0
      Top             =   0
      Width           =   4065
      _ExtentX        =   7170
      _ExtentY        =   8070
   End
End
Attribute VB_Name = "frmTestRobotClient"
Attribute VB_GlobalNameSpace = False
Attribute VB_Creatable = False
Attribute VB_PredeclaredId = True
Attribute VB_Exposed = False

Private Sub Form_Resize()
    If (frmTestRobotClient.Width < 4290) Then frmTestRobotClient.Width = 4290
    If (frmTestRobotClient.Height < 5160) Then frmTestRobotClient.Height = 5160

    rcc.Width = frmTestRobotClient.Width - 200
    rcc.Height = frmTestRobotClient.Height - 600
End Sub

