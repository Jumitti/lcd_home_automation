import tkinter as tk
from re import match
from time import sleep

custom_chars = {}  # Storage CustomCharacters


class LcdSimulator:
    def __init__(self):  # Initialise the Tkinter window
        self.LCD_BACKGROUND = "green"
        self.LCD_FOREGROUND = "black"
        self.SESSION_STATE_BACKLIGHT = ''
        self.columns = 16
        self.rows = 2
        self.char_width = 75
        self.char_height = 120
        self.rectangles = []

        self.rects = []
        self.texts = []

        self.root = tk.Tk()
        self.root.title("LCD 16x2 Simulator")

        self.canvas = tk.Canvas(self.root, width=self.columns * self.char_width, height=self.rows * self.char_height,
                                bg=self.LCD_BACKGROUND)
        self.canvas.pack()

        self.chars = []
        for row in range(self.rows):
            for col in range(self.columns):
                rect = self.canvas.create_rectangle(
                    col * self.char_width,
                    row * self.char_height,
                    (col + 1) * self.char_width,
                    (row + 1) * self.char_height,
                    outline=self.LCD_FOREGROUND,
                    width=5
                )
                text = self.canvas.create_text(
                    col * self.char_width + self.char_width // 2,
                    row * self.char_height + self.char_height // 2,
                    text="",
                    font=("Courier", 115),
                    fill=self.LCD_FOREGROUND
                )
                self.rects.append(rect)
                self.texts.append(text)
                self.chars.append(text)

        self.custom_characters = CustomCharactersSimulator(self)

    # put string function
    def lcd_display_string(self, text, line=0):
        line = line - 1
        start_index = line * self.columns
        for i, char in enumerate(text):
            if start_index + i < len(self.chars):
                self.canvas.itemconfig(self.chars[start_index + i], text=char)

        self.lcd_update()

    # put extended string function. Extended string may contain placeholder like {0xFF} for
    # displaying the particular symbol from the symbol table
    def lcd_display_extended_string(self, text, line=0):
        line = line - 1
        i = 0
        x_offset = 0
        while i < len(text):
            match_result = match(r'\{0[xX][0-9a-fA-F]{2}}', text[i:])
            if match_result:
                char_code = match_result.group(0)
                custom_char_bitmap = self.custom_characters.get_custom_char(char_code)
                self.custom_characters.draw_custom_char(custom_char_bitmap,
                                                        x_offset * self.char_width,
                                                        line * self.char_height, self.LCD_FOREGROUND)
                x_offset += 1
                i += 6
            else:
                self.canvas.itemconfig(self.chars[line * self.columns + x_offset], text=text[i])
                x_offset += 1
                i += 1
        self.lcd_update()

    # clear lcd
    def lcd_clear(self):
        self.root.update_idletasks()
        self.root.update()
        for i in range(2):
            self.lcd_display_string("                ", i)
        for rect_id in self.rectangles:
            self.canvas.delete(rect_id)
        self.rectangles.clear()

    def lcd_update(self):
        self.root.update_idletasks()
        self.root.update()

    # backlight control (on/off)
    # options: lcd_backlight(1) = ON, lcd_backlight(0) = OFF
    def lcd_backlight(self, state):
        if state == 1:
            self.LCD_BACKGROUND = "green"
            self.LCD_FOREGROUND = "black"
        elif state == 0:
            self.LCD_BACKGROUND = "black"
            self.LCD_FOREGROUND = "green"

        self.canvas.configure(bg=self.LCD_BACKGROUND)

        for rect in self.rects:
            self.canvas.itemconfig(rect, outline=self.LCD_FOREGROUND)
        for text in self.texts:
            self.canvas.itemconfig(text, fill=self.LCD_FOREGROUND)

        self.SESSION_STATE_BACKLIGHT = state


class CustomCharactersSimulator:
    def __init__(self, lcd):
        self.lcd = lcd
        # Data for custom character #1. Code {0x00}
        self.char_1_data = ["11111",
                            "10001",
                            "10001",
                            "10001",
                            "10001",
                            "10001",
                            "10001",
                            "11111"]
        # Data for custom character #2. Code {0x01}
        self.char_2_data = ["11111",
                            "10001",
                            "10001",
                            "10001",
                            "10001",
                            "10001",
                            "10001",
                            "11111"]
        # Data for custom character #3. Code {0x02}
        self.char_3_data = ["11111",
                            "10001",
                            "10001",
                            "10001",
                            "10001",
                            "10001",
                            "10001",
                            "11111"]
        # Data for custom character #4. Code {0x03}
        self.char_4_data = ["11111",
                            "10001",
                            "10001",
                            "10001",
                            "10001",
                            "10001",
                            "10001",
                            "11111"]
        # Data for custom character #5. Code {0x04}
        self.char_5_data = ["11111",
                            "10001",
                            "10001",
                            "10001",
                            "10001",
                            "10001",
                            "10001",
                            "11111"]
        # Data for custom character #6. Code {0x05}
        self.char_6_data = ["11111",
                            "10001",
                            "10001",
                            "10001",
                            "10001",
                            "10001",
                            "10001",
                            "11111"]
        # Data for custom character #7. Code {0x06}
        self.char_7_data = ["11111",
                            "10001",
                            "10001",
                            "10001",
                            "10001",
                            "10001",
                            "10001",
                            "11111"]
        # Data for custom character #8. Code {0x07}
        self.char_8_data = ["11111",
                            "10001",
                            "10001",
                            "10001",
                            "10001",
                            "10001",
                            "10001",
                            "11111"]

    # load custom character data to CG RAM for later use in extended string. Data for
    # characters is hold in file custom_characters.txt in the same folder as i2c_dev.py
    # file. These custom characters can be used in printing of extended string with a
    # placeholder with desired character codes: 1st - {0x00}, 2nd - {0x01}, 3rd - {0x02},
    # 4th - {0x03}, 5th - {0x04}, 6th - {0x05}, 7th - {0x06} and 8th - {0x07}.
    def load_custom_characters_data(self):
        char_data_list = [
            (f"{{0x00}}", self.char_1_data),
            (f"{{0x01}}", self.char_2_data),
            (f"{{0x02}}", self.char_3_data),
            (f"{{0x03}}", self.char_4_data),
            (f"{{0x04}}", self.char_5_data),
            (f"{{0x05}}", self.char_6_data),
            (f"{{0x06}}", self.char_7_data),
            (f"{{0x07}}", self.char_8_data)
        ]

        for char_name, bitmap in char_data_list:
            if len(bitmap) != 8 or any(len(row) != 5 for row in bitmap):
                continue
            custom_chars[char_name] = bitmap

    def get_custom_char(self, char_name):
        return custom_chars.get(char_name, ["00000"] * 8)

    # Draw CustomCharacters
    def draw_custom_char(self, bitmap, x, y, color):
        pixel_size = 15
        for row, line in enumerate(bitmap):
            for col, bit in enumerate(line):
                if bit == '1':
                    rect_id = self.lcd.canvas.create_rectangle(
                        x + (col * pixel_size),
                        y + (row * pixel_size),
                        x + ((col + 1) * pixel_size),
                        y + ((row + 1) * pixel_size),
                        fill=color,
                        outline=color
                    )
                    self.lcd.rectangles.append(rect_id)
