# Roblox Keyboard Macro Bot

A specialized Python-based automation tool designed for gameplay loop automation and repetitive task execution in Roblox via low-level hardware keyboard emulation.

## Project Overview

This bot is a console application built specifically for the Windows operating system. Unlike generic software clickers, this solution utilizes low-level **Scan Codes** instead of standard Virtual Key Codes. This approach ensures that input signals are correctly intercepted and processed by DirectX-driven 3D game engines like Roblox, eliminating the common issue where character movements fail to register inside the game world.

## Key Features

*   **Low-Level Emulation:** Built on top of the `pydirectinput` library to guarantee precise execution of key states (`W`, `A`, `S`, `D`, `Space`, etc.) within 3D game environments.
*   **Asynchronous Global Hook:** Registers a system-wide keyboard hook for the `END` key. Pressing it triggers an immediate break in execution, releases all active keys, and transfers control back to the main console menu safely.
*   **Diagonal Movement Support:** Supports simultaneous key combinations using the plus sign operator (e.g., `w+d`) for diagonal travel patterns or joint action execution.
*   **Flexible Config Parsing:** Automatically processes both continuous hold intervals (e.g., `w3`) and single instantaneous click events (e.g., `space`) within the same configuration sequence.
*   **Persistent Session States:** Remembers the last imported configuration profile by storing it in a local state tracking file, ensuring it remains active upon successive application launches.

## Architecture and Execution Logic

The application leverages a non-blocking precise timing loop that yields every 2 milliseconds. This architecture prevents thread lock issues typically associated with standard synchronous delay mechanisms (`time.sleep`) and maintains a flag polling frequency of up to 500 checks per second. Upon receiving an abort command from the operating system, the running task halts instantly without waiting for the current step timer to expire.

## System Requirements

*   **Operating System:** Windows 10 or Windows 11
*   **Runtime Environment:** Python version 3.8 or higher
*   **Access Privileges:** Administrative rights (required to establish the low-level global keyboard hook over the Roblox application interface)

## Dependencies Installation

Before running the application script, you must install the external packages required for hardware input simulation and hook registrations:

```bash
pip install pydirectinput keyboard
```

## Configuration Syntax

Macro sequences are structured inside plain text files using the `.txt` extension. Commands must be separated by commas in a single continuous line, containing no spaces or carriage returns.

*   `w3` – Holds down the `W` key for exactly 3 seconds.
*   `w+d5` – Holds down both `W` and `D` keys simultaneously for 5 seconds.
*   `space` – Simulates a single quick click of the Spacebar key.
*   `2.5` or `.5` – Commands the bot to idle in place (no keys pressed) for the specified duration.
*   `~` – The infinite loop marker. Must be placed strictly at the very end of the line. If omitted, the macro runs exactly once and halts.

### Configuration String Examples

*   **Basic Forward and Backward Movement Loop:**
    ```text
    w3,s3,~
    ```
*   **Complex Trajectory with Jumps and Idles:**
    ```text
    w+d4,1.5,space,w2,s4,~
    ```

## Usage Instructions

1. Place the main Python script file and your custom configuration text files (e.g., `macro.txt`) inside the exact same folder directory.
2. Execute the Python script. The application will prompt for User Account Control (UAC) elevation to obtain Administrative privileges.
3. Interact with the console menu by pressing the corresponding number on your keyboard (the terminal uses immediate character reading, so pressing `Enter` after the number is not required):
    *   `1` – Execute the current active macro profile.
    *   `2` – Import and switch to a new configuration file.
    *   `3` – Reset the current profile back to the default factory layout (`w3,s3,~`).
    *   `4` – Exit the application safely.
4. After selecting option `1`, a 5-second countdown will begin, allowing you sufficient time to click into and focus the Roblox game window.
5. To stop the automation routine at any point, press the `END` key on your keyboard.
