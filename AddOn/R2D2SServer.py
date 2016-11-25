############################################### Revision history #####################################################################################
# 2.7.3 - Add vesion label into panel
# 2.7.4 - Bugfix radian instead gr.
# 2.7.13 - Add error codes to response
# 2.7.18 - Bugfixing Plecho rotation constraint
# 2.8.6 - Change constraints value
# 2.8.14 - Dobavleny comandy po uglam i Lokot - f3
# 2.10.4 - Rorrectirovka pod novuyu model
######################################################################################################################################################
bl_info = {
    'name': 'R2D2 Socket Server',
    'author': 'Ilya Juhnowski',
    'version': (2, 10, 4),
    "blender": (2, 6, 1),
    "api": 12345,
    'location': 'Properties > Render',
    'description': 'Socket Server for communication with VB client with R2D2 command parser',
    'warning': 'It doesnt work without R2D2 blender model. You need change parser implementation to fix it.',
    'wiki_url': 'none',
    'tracker_url': 'none',
    'category': 'Render'}
   

import bpy
import socket
import threading
import socketserver
import bgl

global ss
global server

class ThreadedTCPRequestHandler(socketserver.BaseRequestHandler):
    f1_min = -2.434734266 # = -139.5
    f1_max = 2.434734266  # = 139.5 grad
    x_1 = 90*3.1415926/180
    
    f2_min = -3.438298568 # = -197 grad
    f2_max = 0.52359877   # = 30 grad
    x_2 = 90*3.1415926/180
    
    f3_min = 0 # = 0 grad
    f3_max = 1.082104118   # = +62 grad
    x_3 = 90*3.1415926/180
    y_3 = 220.5*3.1415926/180

    f1_step = 0.00872638  # =0.5 grad
    f2_step = 0.0174527   # = 1 grad

    def handle(self):

        data = self.request.recv(1024).decode("utf-8")

        #set response
        response = "400 Internal Error"

        cmd = data[0:3]
        
        if (cmd=="-f1"):
            f1 = bpy.data.objects['Bashnya'].rotation_euler[2]
            if (f1>self.f1_min):
                bpy.data.objects['Bashnya'].rotation_euler = (self.x_1, 0, f1 - self.f1_step)
                response = "200 Ok"
            else :
                    response = "311 pos:"+str(f1*180/3.1415926)
        
        elif (cmd=="+f1"):
            f1 = bpy.data.objects['Bashnya'].rotation_euler[2]            
            if (f1 < self.f1_max):
                bpy.data.objects['Bashnya'].rotation_euler = (self.x_1, 0, f1 + self.f1_step)
                response = "200 Ok"
            else :
                    response = "312 pos:"+str(f1*180/3.1415926)

        elif (cmd=="-f2"):
            f2 = bpy.data.objects['Plecho'].rotation_euler[1]
            if (f2 > self.f2_min):
                bpy.data.objects['Plecho'].rotation_euler = (self.x_2, f2 - self.f2_step, 0)
                response = "200 Ok"
            else :
                response = "321 pos:"+str(f2*180/3.1415926) 
       
        elif (cmd=="+f2"):
            f2 = bpy.data.objects['Plecho'].rotation_euler[1]
            if (f2 < self.f2_max):
                bpy.data.objects['Plecho'].rotation_euler = (self.x_2, f2 + self.f2_step , 0)
                response = "200 Ok"
            else :
                response = "322 pos:"+str(f2*180/3.1415926) 		

        elif (cmd=="i"):
            bpy.data.objects['Plecho'].rotation_euler = (self.x_1, 0, 0)            
            bpy.data.objects['Bashnya'].rotation_euler = (self.x_2, 0, 0)
            bpy.data.objects['Lokot'].rotation_euler = (self.x_3, 220.5, 0)
            response = "200 Ok"
            
        elif (cmd=="stop"):
            server.shutdown()
            response = "900 Server Shutdown"
            print("server shutdown")

        elif (cmd=="f1="):
            f_tmp = float(data[3:1024])*3.1415926/180
            print("f1=", data[3:1024], " grad -> ", f_tmp, " radian")
            f1 = bpy.data.objects['Bashnya'].rotation_euler[2]
            
            if (f_tmp < self.f1_min):
                response = "311 pos:"+str(f1*180/3.1415926)
            elif (f_tmp > self.f1_max):
                response = "312 pos:"+str(f1*180/3.1415926)
            else:
                bpy.data.objects['Bashnya'].rotation_euler = (self.x_1, 0, f_tmp)
                response = "200 Ok"

        elif (cmd=="f2="):
            f_tmp = float(data[3:1024])*3.1415926/180
            print("f2=", data[3:1024], " grad -> ", str(f_tmp), " radian")
            f2 = bpy.data.objects['Plecho'].rotation_euler[1]

            if (f_tmp < self.f2_min):
                response = "321 pos:"+str(f2*180/3.1415926)
            elif (f_tmp > self.f2_max):
                response = "322 pos:"+str(f2*180/3.1415926)
            else:
                bpy.data.objects['Plecho'].rotation_euler = (self.x_2, f_tmp , 0)
                response = "200 Ok"

        elif (cmd=="f3="):
            f_tmp = float(data[3:1024])*3.1415926/180
            print("f3=", data[3:1024], "grad -> ", f_tmp, " radian")
            f3 = bpy.data.objects['Lokot'].rotation_euler[1]

            if (f_tmp < self.f3_min):
                response = "331 pos:"+str(f3*180/3.1415926)
            elif (f_tmp > self.f3_max):
                response = "332 pos:"+str(f3*180/3.1415926)
            else:
                bpy.data.objects['Lokot'].rotation_euler = (self.x_3, self.y_3 + f_tmp , 0)
                response = "200 Ok"
        else :
            response = "401 Unknown command"

        self.request.send(str.encode(response))

class ThreadedTCPServer(socketserver.ThreadingMixIn, socketserver.TCPServer):
    allow_reuse_address = True
    
class SServer():
    
    def __init__(self,host="127.0.0.1",port=9001):
        self.host = host
        self.port = port
        self.started = False
        print("SServer initialized")
        
    def __start__(self):
        print("Server start: start")
        global server
        server = ThreadedTCPServer((self.host, self.port), ThreadedTCPRequestHandler)
        server_thread = threading.Thread(target=server.serve_forever)
        server_thread.daemon = True
        server_thread.start()
        self.started = True
        print ("Server loop running in thread:" + str(server_thread.name))
        print("Server start: done")
        
    def __stop__(self):
        global server
        print("Server shutdown: start")
        server.shutdown()    
        self.started = False
        print("Server shutdown: done")
    
    def __setHost__(self, host):
        if self.started:
            self.stop()
        self.host = host

    def __setPort__(self, port):
        if self.started:
            self.stop()
        self.port = port

ss = SServer()
print(ss)

class SServerStart(bpy.types.Operator):
    '''Socket Server Start'''
    bl_idname = "object.sserver_start"
    bl_label = "Socket Server Controller"
    global ss
    
    def execute(self, context):
        print("SServer start")
        print(ss)
        ss.__start__()
        return {'FINISHED'}

class SServerStop(bpy.types.Operator):
    '''Socket Server Stop'''
    bl_idname = "object.sserver_stop"
    bl_label = "Socket Server Stop"
    global ss
    def execute(self, context):
        print("SServer stop")
        print(ss)
        ss.__stop__()
        return {'FINISHED'}

class SSPanel(bpy.types.Panel):
    bl_label = "Socket Server"
    bl_idname = "OBJECT_SS_controller"
    bl_space_type = "PROPERTIES"
    bl_region_type = "WINDOW"
    bl_context = "render"
            
    def draw(self, context):
        layout = self.layout
        scene = context.scene
        obj = context.object
        rd = scene.render
        row = layout.row()
        global ss #= SServer()
    
        row.operator("object.sserver_start", text="start", icon='WORLD_DATA')
        row.operator("object.sserver_stop", text="stop", icon='WORLD_DATA')
        
        split = layout.split()
        col = split.column()
        row = col.row()
        row.label(text=str("Host: "+ss.host))
        
        split = layout.split()
        col = split.column()
        row = col.row()
        row.label(text=str("Port: "+str(ss.port)))

        split = layout.split()
        col = split.column()
        row = col.row()
        row.label(text=str("Is Started: "+str(ss.started)))
        
        split = layout.split()
        col = split.column()
        row = col.row()
        row.label(text=str("Version: "+str(bl_info['version'])))

def register():
    #bpy.context.object["SS_Host"] = "127.0.0.1"
    #bpy.context.object["SS_Port"] = 9001
    bpy.utils.register_class(SServerStart)
    bpy.utils.register_class(SServerStop)
    bpy.utils.register_class(SSPanel)


def unregister():
    bpy.utils.unregister_class(SSPanel)
    bpy.utils.unregister_class(SServerStart)
    bpy.utils.unregister_class(SServerStop)

if __name__ == "__main__":
    register()
