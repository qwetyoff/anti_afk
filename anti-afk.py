import os
import time
import msvcrt
import pydirectinput
import keyboard
import sys
import ctypes

def is_admin():
    try:
        return ctypes.windll.shell32.IsUserAnAdmin()
    except:
        return False

if not is_admin():
    ctypes.windll.shell32.ShellExecuteW(None, "runas", sys.executable, " ".join(sys.argv), None, 1)
    sys.exit()

username = os.getlogin()
bot_running = False

default_file = "default_macro.txt"
state_file = "current_macro.txt"

if not os.path.exists(default_file):
    with open(default_file, "w", encoding="utf-8") as f:
        f.write("w3,s3,~")
    print(f"[+] Default configuration file created on startup: {default_file}")

if not os.path.exists(state_file):
    with open(state_file, "w", encoding="utf-8") as f:
        f.write(default_file)

# Мгновенный сброс флага работы и чистый отжим кнопок
def stop_bot():
    global bot_running
    if bot_running:
        bot_running = False
        print("\n[!] Emergency stop! Releasing keys and returning to menu...")
        for key in ['w', 'a', 's', 'd', 'space']:
            pydirectinput.keyUp(key)

keyboard.add_hotkey('end', stop_bot)

def parse_macro_file(filename):
    if not os.path.exists(filename):
        return None, False
    try:
        with open(filename, 'r', encoding='utf-8') as f:
            content = f.read().strip()
        
        if not content:
            return None, False
            
        raw_commands = [c.strip().lower() for c in content.split(",") if c.strip()]
        steps = []
        has_loop_sign = False
        
        for cmd in raw_commands:
            if cmd == '~':
                has_loop_sign = True
                break
                
            keys_part = ""
            time_part = ""
            for char in cmd:
                if char.isalpha() or char == '+':
                    keys_part += char
                elif char.isdigit() or char == '.':
                    time_part += char
            
            keys_list = [k.strip() for k in keys_part.split('+') if k.strip()]
            duration = float(time_part) if time_part else 0.0
            
            if not keys_list:
                steps.append((["_pause_"], duration, True))
            elif duration > 0.0:
                steps.append((keys_list, duration, True))
            else:
                steps.append((keys_list, 0.1, False))
                    
        return steps, has_loop_sign
    except:
        return None, False

# Новая функция ожидания: проверяет кнопку END каждые 2 миллисекунды
def precise_sleep(duration):
    global bot_running
    start_time = time.time()
    while time.time() - start_time < duration:
        if not bot_running:
            return False
        time.sleep(0.002)
    return True

while True:
    with open(state_file, "r", encoding="utf-8") as f:
        current_active_macro = f.read().strip()

    print("\n===========================================")
    print(f"              Welcome, {username}.        ")
    print(f"Current active macro: [{current_active_macro}]")
    print("1 - Start active macro.")
    print("2 - Import macro.")
    print("3 - Reset macro to default.")
    print("4 - Exit.")
    print("Type your choise (1-4) and do NOT press enter")

    choice = None
    while choice is None:
        if msvcrt.kbhit():
            char = msvcrt.getch().decode('utf-8', errors='ignore')
            if char.isdigit():
                num = int(char)
                if 1 <= num <= 4:
                    choice = num

    print(f"Your choice: {choice}")

    if choice == 1:
        steps, has_loop_sign = parse_macro_file(current_active_macro)
        if not steps:
            print(f"[-] Error: Selected file '{current_active_macro}' cannot be loaded. Resetting to default.")
            with open(state_file, "w", encoding="utf-8") as f:
                f.write(default_file)
            continue

        print(f"\n[+] Executing macro from {current_active_macro}...")
        print("Press END anytime to stop and return to menu.")
        
        bot_running = True
        
        # Прерываемый отсчет перед стартом
        if not precise_sleep(5.0):
            continue
        
        main_loop_broken = False
        while bot_running:
            for keys, duration, is_hold in steps:
                if not bot_running: 
                    main_loop_broken = True
                    break
                
                if "_pause_" in keys:
                    print(f"-> Idle pause for {duration}s")
                    if not precise_sleep(duration): 
                        main_loop_broken = True
                        break
                elif is_hold:
                    print(f"-> Holding keys {keys} for {duration}s")
                    for key in keys:
                        pydirectinput.keyDown(key)
                        
                    if not precise_sleep(duration):
                        main_loop_broken = True
                        break
                        
                    for key in keys:
                        pydirectinput.keyUp(key)
                else:
                    print(f"-> Pressing keys {keys}")
                    for key in keys:
                        pydirectinput.press(key)
                        
            if main_loop_broken or not has_loop_sign or not bot_running:
                break
        
        # После выхода из цикла бот снова готов принимать команды меню
        print("[+] Returned to main menu.")

    elif choice == 2:
        filename = input("\nEnter the config filename (e.g., macro): ").strip()
        if not filename.endswith('.txt'):
            filename += '.txt'
            
        steps, has_loop_sign = parse_macro_file(filename)
        if not steps:
            print(f"[-] Error: File '{filename}' could not be imported.")
        else:
            with open(state_file, "w", encoding="utf-8") as f:
                f.write(filename)
            print(f"[+] Loaded {len(steps)} actions from {filename}.")
            print(f"[+] '{filename}' is now set as the active macro.")

    elif choice == 3:
        with open(state_file, "w", encoding="utf-8") as f:
            f.write(default_file)
        print(f"\n[+] Active macro reset to default: {default_file}")

    elif choice == 4:
        print("Exiting...")
        sys.exit()
