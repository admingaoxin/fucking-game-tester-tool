import pyautogui
import time
import random
import unreal
while True:

    print(pyautogui.position())
    # 获取当前鼠标位置
    x, y = pyautogui.position()

    # 按下鼠标左键
    pyautogui.mouseDown(button='left', x=x, y=y)

    # 移动鼠标一定距离
    pyautogui.move(100, 100)

    #        松开鼠标左键
    pyautogui.mouseUp(button='left', x=x+100, y=y+100)
    time.sleep(1)
  

  
  
  
  
  
  
  
  
  
  
  
  
  
  
  
  
  
  
  
  
  
  
    # # 设置线条的颜色
    # pyautogui.PAUSE = 0.01  # 每个pyautogui函数的执行间隔为0.01秒，用于控制移动速度
    # pyautogui.FAILSAFE = True  # 启用pyautogui安全模式

    # # 将鼠标移动到起点
    # pyautogui.moveTo(100, 100)

    # # 按住左键开始拖动
    # pyautogui.mouseDown()

    #  #将鼠标移动到终点，形成线条
    # pyautogui.dragTo(500, 500, button='left')

    # # 松开左键
    # pyautogui.mouseUp()
    # time.sleep(1)
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    # # pyautogui.moveTo(x=1500, y=random.randint(100, 900))
    # time.sleep(0.5)
    # # pyautogui.moveTo(x=1500, y=random.randint(100, 900))
    # # pyautogui.dragTo(x=1500, y=random.randint(100, 900))
    # # 获取当前的Unreal引擎编辑器
    # editor = unreal.EditorLevelLibrary.get_editor_world()
    # # 获取当前的鼠标位置
    # mouse_position = unreal.InputEventStateLibrary.get_mouse_position()
    # # 将鼠标位置转换为世界坐标系中的坐标
    # world_mouse_position = unreal.InputEventStateLibrary.convert_mouse_location_to_world_location(editor, mouse_position)
    # # 将鼠标位置移动到新位置
    # new_mouse_position = unreal.Vector(world_mouse_position.x + 100, world_mouse_position.y + 100, world_mouse_position.z)
    # unreal.InputEventStateLibrary.set_mouse_position(new_mouse_position)