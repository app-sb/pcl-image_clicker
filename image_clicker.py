import pyautogui
import keyboard
import time
import os

# 获取当前脚本所在目录
script_dir = os.path.dirname(os.path.abspath(__file__))
# 构造start.png的完整路径
image_path = os.path.join(script_dir, 'start.png')

print("=== 快速移动全屏幕图像检测程序 ===")
print(f"要检测的图像: {image_path}")
print("程序将在全屏范围内持续查找start.png图像")
print("找到后会以最快速度移动鼠标并点击图像中心")
print("按下F7键结束程序")
print("或者按Ctrl+C强制终止")

# 检查图像文件是否存在
if not os.path.exists(image_path):
    print(f"\n❌ 错误：找不到图像文件 {image_path}")
    print("请确保start.png文件与脚本位于同一目录下")
    input("按Enter键退出...")
    exit()
else:
    print(f"\n✅ 成功找到图像文件")

# 获取屏幕信息
screen_width, screen_height = pyautogui.size()
print(f"屏幕分辨率: {screen_width}x{screen_height}")

# 设置pyautogui参数
pyautogui.FAILSAFE = False  # 关闭安全模式，允许鼠标移动到屏幕边缘
pyautogui.PAUSE = 0.01  # 最小化操作间的暂停时间

# 主循环：全屏幕检测图像
print("\n🔍 开始全屏幕快速检测...")
found_count = 0
loop_count = 0

while True:
    loop_count += 1
    
    try:
        # 检查是否按下了F7键
        if keyboard.is_pressed('f7'):
            print(f"\n🛑 检测到F7键，程序结束")
            print(f"总计循环次数: {loop_count}")
            print(f"成功找到图像次数: {found_count}")
            break
            
        # 显示搜索状态（减少频率以提高性能）
        if loop_count % 50 == 0:  # 每50次循环显示一次
            print(f"搜索中... (循环次数: {loop_count})")
            
        try:
            # 全屏幕快速查找start.png图像
            location = pyautogui.locateOnScreen(
                image_path,
                grayscale=True,  # 使用灰度模式提高速度
                confidence=0.7 if hasattr(pyautogui, 'locateOnScreen') else None  # 仅在支持时使用
            )
            
            if location is not None:
                found_count += 1
                # 计算图像中心坐标
                center_x, center_y = pyautogui.center(location)
                print(f"\n🎉 第 {found_count} 次找到图像！")
                print(f"   图像位置: {location}")
                print(f"   中心坐标: ({center_x}, {center_y})")
                
                # 快速移动鼠标到图像中心（duration=0表示瞬间移动）
                print(f"   🖱️  快速移动到 ({center_x}, {center_y})")
                pyautogui.moveTo(center_x, center_y, duration=0)  # 瞬间移动
                
                # 点击
                pyautogui.click()
                print(f"   ✅ 已点击！")
                
                # 点击后短暂暂停，避免重复点击
                time.sleep(0.5)
            else:
                # 未找到图像时，极短暂停后继续查找
                time.sleep(0.1)
                
        except pyautogui.ImageNotFoundException:
            # 图像未找到，继续查找
            time.sleep(0.1)
            continue
        except Exception as e:
            # 忽略大多数错误，保持程序运行
            if "confidence" in str(e):
                # 如果是confidence参数错误，尝试不使用该参数
                try:
                    location = pyautogui.locateOnScreen(
                        image_path,
                        grayscale=True
                    )
                    if location is not None:
                        found_count += 1
                        center_x, center_y = pyautogui.center(location)
                        pyautogui.moveTo(center_x, center_y, duration=0)
                        pyautogui.click()
                        print(f"\n🎉 快速点击成功！")
                        time.sleep(0.5)
                except:
                    pass
            time.sleep(0.5)
            
    except KeyboardInterrupt:
        # 处理用户按下Ctrl+C的情况
        print(f"\n🛑 程序被用户中断")
        print(f"总计循环次数: {loop_count}")
        print(f"成功找到图像次数: {found_count}")
        break
    except Exception as e:
        # 忽略大多数错误，保持程序运行
        time.sleep(1)