import tkinter as tk
from tkinter import filedialog
from tkinter import ttk
import ElGamalCipher.encryption as encrypt

# Constant colors and fonts using in this GUI
HEADER_FONT = ('Open Sans', 17)
BUTTON_FONT_LIGHT = ('Open Sans light', 13)
LABEL_FONT = ('Open Sans', 13)
LABEL_FONT_INFO = ('Open Sans light', 13)
LABEL_FONT_SMALL = ('Open Sans', 11)
ENTRY_FONT = ('Open Sans', 10)
STATUS_FONT = ('Open Sans Bold', 20)

BACKGROUND_COLOR_GRAY = '#434343'
BACKGROUND_COLOR_GRAY_DARKER = '#333333'
BUTTON_COLOR_GRAY = '#373739'
BUTTON_COLOR_GRAY_ACTIVE = '#353535'
BUTTON_COLOR_GRAY_PRESSED = '#313131'
BUTTON_COLOR_LIGHT = '#F4F4F4'
SUCCESS_COLOR = '#55C621'
WARNING_COLOR = '#EFC61C'
ERROR_COLOR = '#FC5753'


# Other settings
DEBUG = True
SIZE_OF_BITS = 1024

encryption = encrypt.ElGamal()


class CryptApp(tk.Tk):
    """
        Main class for initializing multiple windows and handle it.
    """

    def __init__(self):
        tk.Tk.__init__(self)
        self.minsize(800, 500)
        self.geometry('900x500+100+100')
        self.title('ElGamal Cryptosystem')
        container = ttk.Frame(self)
        container.pack(side='top', fill='both', expand=True)
        container.grid_rowconfigure(0, weight=1)
        container.grid_columnconfigure(0, weight=1)

        self.frames = dict()

        frame = MainPage(container, self)

        self.frames[MainPage] = frame

        frame.grid(row=0, column=0, sticky='nsew')

        self.show_frame(MainPage)

    def show_frame(self, controller):
        frame = self.frames[controller]
        frame.tkraise()


class MainPage(ttk.Frame):
    """
        Main page of cryptographer. Containing GUI (buttons, labels and inputs)
        for input file, input decryption key, handle file (encrypt or decrypt)
        and save it to another file.
    """

    def __init__(self, parent, controller):

        self.input_file_name = ''
        self.output_file_name = ''

        ttk.Frame.__init__(self, parent)
        style = ttk.Style()
        style.configure('TFrame', background=BACKGROUND_COLOR_GRAY)
        self.columnconfigure(0, weight=1)
        self.columnconfigure(1, weight=5)
        self.rowconfigure(0, weight=1)

        # Initializing styles
        style.configure('info.TLabel',
                        font=LABEL_FONT_INFO,
                        background=BACKGROUND_COLOR_GRAY,
                        foreground=BUTTON_COLOR_LIGHT)
        style.configure('warning.TLabel',
                        font=LABEL_FONT_SMALL,
                        background=BACKGROUND_COLOR_GRAY,
                        foreground=WARNING_COLOR)
        style.configure('info_value.TLabel',
                        font=LABEL_FONT,
                        background=BACKGROUND_COLOR_GRAY,
                        foreground=BUTTON_COLOR_LIGHT)
        style.configure('status.TLabel',
                        font=STATUS_FONT,
                        background=BACKGROUND_COLOR_GRAY,
                        foreground=SUCCESS_COLOR,
                        anchor=tk.CENTER)
        style.configure('dark.TButton',
                        font=BUTTON_FONT_LIGHT,
                        padding=8,
                        relief='flat',
                        foreground=BUTTON_COLOR_LIGHT)
        style.map('dark.TButton',
                  background=[('pressed', BUTTON_COLOR_GRAY_PRESSED),
                              ('active', BUTTON_COLOR_GRAY_ACTIVE),
                              ('!active', BUTTON_COLOR_GRAY)],
                  relief=[('pressed', 'flat'), ('!disabled', 'flat')])
        style.configure('Header.TLabel',
                        font=HEADER_FONT,
                        background=BACKGROUND_COLOR_GRAY_DARKER,
                        foreground=BUTTON_COLOR_LIGHT
                        )
        style.configure('navigate.TFrame',
                        background=BACKGROUND_COLOR_GRAY_DARKER)

        left_frame = ttk.Frame(self, style='navigate.TFrame')
        left_frame.rowconfigure(0, weight=1)
        left_frame.rowconfigure(1, weight=0)
        left_frame.rowconfigure(2, weight=0)
        left_frame.rowconfigure(3, weight=0)
        left_frame.rowconfigure(4, weight=0)
        left_frame.rowconfigure(5, weight=1)

        left_frame.columnconfigure(0, weight=1)
        right_frame = ttk.Frame(self)

        # Left part navigation settings
        label_header = ttk.Label(left_frame, style='Header.TLabel', text='ElGamal Cryptosystem').grid(column=0, row=0)
        button_open_file = ttk.Button(left_frame, style='dark.TButton', text='Open file')
        button_open_file.grid(column=0, row=1, sticky='e w', pady=1)
        button_set_keys = ttk.Button(left_frame, style='dark.TButton', text='Set keys')
        button_set_keys.grid(column=0, row=2, sticky='e w', pady=1)
        button_encrypt = ttk.Button(left_frame, style='dark.TButton', text='Encrypt')
        button_encrypt.grid(column=0, row=3, sticky='e w', pady=1)
        button_decrypt = ttk.Button(left_frame, style='dark.TButton', text='Decrypt')
        button_decrypt.grid(column=0, row=4, sticky='e w', pady=1)

        # Right part info
        right_frame.columnconfigure(0, weight=1)
        right_frame.columnconfigure(1, weight=5)
        right_frame.rowconfigure(0, weight=3)
        right_frame.rowconfigure(1, weight=1)
        right_frame.rowconfigure(2, weight=1)
        right_frame.rowconfigure(3, weight=1)
        right_frame.rowconfigure(4, weight=1)
        right_frame.rowconfigure(5, weight=0)
        right_frame.rowconfigure(6, weight=5)

        label_file_status = ttk.Label(right_frame, style='info.TLabel', text='File status:')
        label_file_status.grid(column=0, row=1, sticky='n e s w', padx=30)
        label_public_key = ttk.Label(right_frame, style='info.TLabel', text='Public key:')
        label_public_key.grid(column=0, row=2, sticky='n e w', padx=30)
        label_private_key = ttk.Label(right_frame, style='info.TLabel', text='Private key:')
        label_private_key.grid(column=0, row=3, sticky='n e s w', padx=30)
        label_session_key = ttk.Label(right_frame, style='info.TLabel', text='Session key:')
        label_session_key.grid(column=0, row=4, sticky='n e s w', padx=30)
        label_keys_status = ttk.Label(right_frame,
                                      style='warning.TLabel',
                                      text='Public/private keys are not set. Please configure keys!')
        label_keys_status.grid(column=0, columnspan=2, row=5, sticky='n e s w', padx=30)
        self.label_encrypt_status = ttk.Label(right_frame, style='status.TLabel')
        self.label_encrypt_status.grid(column=0, columnspan=2, row=6, sticky='n e s w')

        label_file_status_value = ttk.Label(right_frame, style='info_value.TLabel', text='')
        label_file_status_value.grid(column=1, row=1, sticky='n e s w')
        label_public_key_value = ttk.Frame(right_frame, style='info_value.TFrame')
        label_public_key_value.columnconfigure(0, weight=1)
        label_public_key_value.columnconfigure(1, weight=3)
        label_public_key_value.rowconfigure(0, weight=1)
        label_public_key_value.rowconfigure(1, weight=1)
        label_public_key_value.rowconfigure(2, weight=1)

        label_p_public = ttk.Label(label_public_key_value, style='info.TLabel', text='p:')
        label_p_public.grid(column=0, row=0, sticky='n e s w')
        label_g_public = ttk.Label(label_public_key_value, style='info.TLabel', text='g:')
        label_g_public.grid(column=0, row=1, sticky='n e s w')
        label_y_public = ttk.Label(label_public_key_value, style='info.TLabel', text='y:')
        label_y_public.grid(column=0, row=2, sticky='n e s w')
        self.label_p_public_value = ttk.Label(label_public_key_value, style='info_value.TLabel', text='')
        self.label_p_public_value.grid(column=1, row=0, sticky='n e s w')
        self.label_g_public_value = ttk.Label(label_public_key_value, style='info_value.TLabel')
        self.label_g_public_value.grid(column=2, row=0, sticky='n e s w')
        self.label_y_public_value = ttk.Label(label_public_key_value, style='info_value.TLabel')
        self.label_y_public_value.grid(column=3, row=0, sticky='n e s w')

        label_public_key_value.grid(column=1, row=2, sticky='n e s w')

        label_private_key_value = ttk.Label(right_frame, style='info_value.TLabel', text='not set')
        label_private_key_value.grid(column=1, row=3, sticky='n e s w')
        label_session_key_value = ttk.Label(right_frame, style='info_value.TLabel', text='')
        label_session_key_value.grid(column=1, row=4, sticky='n e s w')
        left_frame.grid(column=0, row=0, sticky='n e s w')
        right_frame.grid(column=1, row=0, sticky='n e s w')



app = CryptApp()
app.mainloop()
