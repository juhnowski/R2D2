VERSION 5.00
Object = "{248DD890-BB45-11CF-9ABC-0080C7E7B78D}#1.0#0"; "MSWINSCK.OCX"
Begin VB.UserControl RobotClientControl 
   ClientHeight    =   1905
   ClientLeft      =   0
   ClientTop       =   0
   ClientWidth     =   4065
   ScaleHeight     =   1905
   ScaleWidth      =   4065
   Begin VB.CheckBox cbSocketState 
      Caption         =   "���������� ��������� ������"
      Height          =   255
      Left            =   120
      TabIndex        =   11
      Top             =   1560
      Width           =   2655
   End
   Begin VB.CommandButton btnClean 
      Caption         =   "��������"
      Height          =   315
      Left            =   2880
      TabIndex        =   10
      Top             =   1550
      Width           =   1095
   End
   Begin VB.CheckBox cbAutomaticReconnect 
      Height          =   315
      Left            =   2600
      TabIndex        =   9
      Top             =   480
      Value           =   1  'Checked
      Width           =   200
   End
   Begin VB.CommandButton btnConnect 
      Caption         =   "����������"
      Height          =   315
      Left            =   2850
      TabIndex        =   8
      Top             =   480
      Width           =   1150
   End
   Begin VB.TextBox txtPort 
      Height          =   315
      Left            =   2050
      TabIndex        =   7
      Text            =   "9001"
      Top             =   480
      Width           =   495
   End
   Begin VB.TextBox txtHost 
      Height          =   315
      Left            =   1000
      TabIndex        =   5
      Text            =   "127.0.0.1"
      Top             =   480
      Width           =   1000
   End
   Begin MSWinsockLib.Winsock socket 
      Left            =   3360
      Top             =   960
      _ExtentX        =   741
      _ExtentY        =   741
      RemoteHost      =   "127.0.0.1"
      RemotePort      =   9001
   End
   Begin VB.ListBox lstLog 
      Height          =   645
      ItemData        =   "RobotClientCtrl.ctx":0000
      Left            =   120
      List            =   "RobotClientCtrl.ctx":0002
      TabIndex        =   2
      Top             =   840
      Width           =   3855
   End
   Begin VB.TextBox txtCmd 
      Height          =   285
      Left            =   960
      TabIndex        =   1
      Text            =   "i"
      Top             =   120
      Width           =   1815
   End
   Begin VB.CommandButton btnSend 
      Caption         =   "���������"
      Height          =   315
      Left            =   2800
      TabIndex        =   0
      Top             =   120
      Width           =   1215
   End
   Begin VB.Label Label3 
      Caption         =   ":"
      Height          =   255
      Left            =   2000
      TabIndex        =   6
      Top             =   480
      Width           =   135
   End
   Begin VB.Label Label2 
      Caption         =   "�������:"
      Height          =   255
      Left            =   120
      TabIndex        =   4
      Top             =   120
      Width           =   735
   End
   Begin VB.Label Label1 
      Caption         =   "���������:"
      Height          =   255
      Left            =   120
      TabIndex        =   3
      Top             =   480
      Width           =   975
   End
End
Attribute VB_Name = "RobotClientControl"
Attribute VB_GlobalNameSpace = False
Attribute VB_Creatable = True
Attribute VB_PredeclaredId = False
Attribute VB_Exposed = True
Private Declare Sub Sleep Lib "kernel32" (ByVal dwMilliseconds As Long)

Dim isUrlChanged As Boolean


Private Sub btnClean_Click()
    '������ ����
    lstLog.Clear
End Sub

Private Sub btnConnect_Click()
On Error GoTo e
    '��������� ��������� ����������
    SimHost = txtHost.Text
    SimPort = txtPort.Text
    
    If (Len(SimHost) = 0) Then
        MsgBox "������:" & "�� ������ ���� ����������", vbCritical
        Exit Sub
    End If
    
    If (Len(SimPort) = 0) Then
        MsgBox "������:" & "�� ������ ���� ����������", vbCritical
        Exit Sub
    End If
    
    '������ ��������� ����� ����� �����������
    socket.Close
    
    socket.LocalPort = 0
    
    '������������� ��������� ����������
    socket.RemoteHost = SimHost
    socket.RemotePort = SimPort
    
    '������������� ����������
    socket.Connect
    
    If (isUrlChanged) Then
        lstLog.AddItem ("���������:" + txtHost.Text + ":" + txtPort.Text)
        lstLog.ListIndex = lstLog.ListCount - 1
        isUrlChanged = False
    End If

    btnSend.SetFocus
    
    Exit Sub
    
e:
    MsgBox "������:" & Err.Description, vbCritical
    
End Sub

Private Sub btnSend_Click()
On Error GoTo e
    '������� ������������ ����������
    msg = txtCmd.Text
    
    '��������� �� ������� ������
    If (Len(msg) > 0) Then
            
            '���������� ���������
            socket.SendData (msg)
    End If
    
    Exit Sub
e:
    MsgBox "������:" & Err.Description, vbCritical
    
    '��������� ����������
    socket_Close
End Sub

Private Sub socket_Close()

    '������� ��������� � ��� � �������� ������
    If (cbSocketState.Value) Then lstLog.AddItem ("����� ������")
    
    '��������� ������������� � ������ ����������
    btnConnect.Enabled = True
    
    '� ������ ��������� ����� ���� �������� ����� ��������������� ����������
    If (cbAutomaticReconnect.Value) Then btnConnect_Click
    
End Sub

Private Sub socket_Connect()
    '������� ��������� � ��� �� �������� ����������
    If (cbSocketState.Value) Then
        lstLog.AddItem ("���������� � " + socket.RemoteHostIP + " �����������")
        lstLog.ListIndex = lstLog.ListCount - 1
    End If
    
    '�� �����������, ������ ���������� �� �����
    btnConnect.Enabled = False
    
End Sub

Private Sub socket_DataArrival(ByVal bytesTotal As Long)
    '�������� ���������
    Dim data As String
    
    '��������� ��������� ���������
    socket.GetData data, vbString
    
    '������� ��������� � ���
    lstLog.AddItem ("���������:" + data)
    lstLog.ListIndex = lstLog.ListCount - 1
    
End Sub

Private Sub socket_Error(ByVal Number As Integer, Description As String, ByVal Scode As Long, ByVal Source As String, ByVal HelpFile As String, ByVal HelpContext As Long, CancelDisplay As Boolean)
'��������� ������ ������
    '������� ������ � ���
    lstLog.AddItem ("������:" + Description)
    
    '��������� ����������
    socket_Close
End Sub

Private Sub txtCmd_KeyPress(KeyAscii As Integer)
    If (KeyAscii = 13) Then
        If (socket.State = sckClosed) Then
            btnConnect.SetFocus
        Else
            btnSend.SetFocus
        End If
        
    End If
End Sub

Private Sub txtHost_Change()
'���� �������� ����� ����������, �� ����� ���������
    socket.Close
    isUrlChanged = True
End Sub

Private Sub txtPort_Change()
'���� �������� ����� ����������, �� ����� ���������
    socket.Close
    isUrlChanged = True
End Sub


Private Sub UserControl_Initialize()
    isUrlChanged = True
End Sub

Private Sub UserControl_Resize()
    '������ �� ��������� ����
    If (UserControl.Width < 4065) Then UserControl.Width = 4065
    If (UserControl.Height < 1905) Then UserControl.Height = 1905

    '������ �� ����������� �������� ��������
    lstLog.Width = UserControl.Width - 200
    lstLog.Height = UserControl.Height - 1125
    cbSocketState.Top = UserControl.Height - 350
    btnClean.Top = UserControl.Height - 350
    
End Sub

Private Sub UserControl_Show()
    '������ ����� �� ������ ����������
    btnConnect.SetFocus
End Sub
