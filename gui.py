import tkinter as tk
from random import randrange
from tkinter import ttk
from tkinter import filedialog
from time import time
import ElGamalCipher.encryption as encrypt
import ElGamalCipher.primes as primes

# Constant colors and fonts using in this GUI
HEADER_FONT = ('Open Sans', 17)
BUTTON_FONT_LIGHT = ('Open Sans light', 13)
LABEL_FONT = ('Open Sans', 13)
LABEL_FONT_INFO = ('Open Sans light', 13)
LABEL_FONT_SMALL = ('Open Sans', 11)
ENTRY_FONT = ('Open Sans', 10)
STATUS_FONT = ('Open Sans Bold', 20)
STATUS_FONT_LIGHT = ('Open Sans Light', 20)

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
KEY_SIZE = 1024

encryption = encrypt.ElGamal()


def popup_message(message, status=1, **kwargs):
    """
    Initializing error message with close button and other buttons as args
    :param message: Text of message
    :param status: 0 is Success, 1 is warning, 2 is error
    :param kwargs: dict with button_name: button_command
    :return:
    """
    window = tk.Tk()
    window.minsize(300, 200)
    window.geometry('300x200+350+150')
    window.resizable(False, False)

    # Generating header
    try:
        if status == 1:
            header_message = 'Warning: '
        elif status == 2:
            header_message = 'Error: '
        else:
            header_message = ''
        header_message += ' '.join(message.split(' ')[:2])
    except IndexError:
        header_message = message
    window.title(header_message)

    # Initializing styles
    style = ttk.Style(window)
    style.configure('TFrame',
                    background=BACKGROUND_COLOR_GRAY
                    )
    style.configure('TButton',
                    font=BUTTON_FONT_LIGHT,
                    padding=0,
                    relief='flat',
                    foreground=BUTTON_COLOR_LIGHT)
    style.map('TButton',
              background=[('pressed', BUTTON_COLOR_GRAY_PRESSED),
                          ('active', BUTTON_COLOR_GRAY_ACTIVE),
                          ('!active', BUTTON_COLOR_GRAY)],
              relief=[('pressed', 'flat'), ('!disabled', 'flat')])
    frame = ttk.Frame(window)
    frame.configure(style='TFrame')
    frame.pack(fill='both', expand=True)
    frame.grid_columnconfigure(0, weight=1)
    frame.grid_rowconfigure(0, weight=3)
    frame.grid_rowconfigure(1, weight=1)

    # Initializing main message
    message_content = tk.Message(frame,
                                 text=message,
                                 background=BACKGROUND_COLOR_GRAY,
                                 font=LABEL_FONT,
                                 justify=tk.LEFT,
                                 width=300)
    # Changing colors:
    #   0 (success) is green,
    #   1 (warning) is yellow,
    #   2 (error) is red
    if status == 0:
        message_content.configure(foreground=SUCCESS_COLOR)
    elif status == 1:
        message_content.configure(foreground=WARNING_COLOR)
    else:
        message_content.configure(foreground=ERROR_COLOR)

    message_content.grid(column=0, row=0, sticky='n e s w')

    button_frame = ttk.Frame(frame, style='TFrame')
    button_frame.rowconfigure(0, weight=1)
    button_frame.columnconfigure(0, weight=1)

    # Initializing close button
    cancel_button = ttk.Button(button_frame,
                               text='Close',
                               style='TButton',
                               command=window.destroy)
    cancel_button.grid(column=0, row=0, padx=3, sticky='n e s w')

    # Initializing other buttons if they are set
    if kwargs:
        button_count = 1
        for name, action in kwargs.items():
            button_frame.columnconfigure(button_count, weight=1)
            button = ttk.Button(button_frame,
                                text=name,
                                style='TButton',
                                command=action)
            button.grid(column=button_count, row=0, padx=3, sticky='n e s w')
            button_count += 1
    button_frame.grid(column=0, row=1, sticky='n e s w', padx=2, pady=5)


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
        for F in (MainPage, SelectKeys):
            frame = F(container, self)
            self.frames[F] = frame
            frame.grid(row=0, column=0, sticky='nsew')

        # After running program, MainPage window will be shown
        self.show_frame(MainPage)

    def show_frame(self, controller):
        """
        Loading initialized window
        :param controller: Parent object to control system
        :return: None
        """
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
        controller.geometry('900x500+100+100')
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
        style.configure('success.TLabel',
                        font=LABEL_FONT,
                        background=BACKGROUND_COLOR_GRAY,
                        foreground=SUCCESS_COLOR)
        style.configure('warning_message.TLabel',
                        font=LABEL_FONT,
                        background=BACKGROUND_COLOR_GRAY,
                        foreground=WARNING_COLOR)
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
        label_header = ttk.Label(left_frame, style='Header.TLabel', text='ElGamal Cryptosystem')
        label_header.grid(column=0, row=0)
        button_open_file = ttk.Button(left_frame, style='dark.TButton', text='Open file', command=self.open_file)
        button_open_file.grid(column=0, row=1, sticky='e w', pady=1)
        button_set_keys = ttk.Button(left_frame, style='dark.TButton', text='Set keys',
                                     command=lambda: controller.show_frame(SelectKeys))
        button_set_keys.grid(column=0, row=2, sticky='e w', pady=1)
        button_encrypt = ttk.Button(left_frame, style='dark.TButton', text='Encrypt',
                                    command=lambda: self.encrypt_file(controller, is_encrypt=True))
        button_encrypt.grid(column=0, row=3, sticky='e w', pady=1)
        button_decrypt = ttk.Button(left_frame, style='dark.TButton', text='Decrypt',
                                    command=lambda: self.encrypt_file(controller, is_encrypt=False))
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

        # Initializing right side info
        label_file_status = ttk.Label(right_frame, style='info.TLabel', text='File status:')
        label_file_status.grid(column=0, row=1, sticky='n e s w', padx=30)
        label_public_key = ttk.Label(right_frame, style='info.TLabel', text='Public key:')
        label_public_key.grid(column=0, row=2, sticky='n e w', padx=30)
        label_private_key = ttk.Label(right_frame, style='info.TLabel', text='Private key:')
        label_private_key.grid(column=0, row=3, sticky='n e s w', padx=30)
        label_session_key = ttk.Label(right_frame, style='info.TLabel', text='Session key:')
        label_session_key.grid(column=0, row=4, sticky='n e s w', padx=30)
        self.label_keys_status = ttk.Label(right_frame)
        self.label_keys_status.grid(column=0, columnspan=2, row=5, sticky='n e s w', padx=30)
        self.label_encrypt_status = ttk.Label(right_frame, style='status.TLabel')
        self.label_encrypt_status.grid(column=0, columnspan=2, row=6, sticky='n e s w')

        self.label_file_status_value = ttk.Label(right_frame, style='info_value.TLabel', text='')
        self.label_file_status_value.grid(column=1, row=1, sticky='n e s w')
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
        self.label_g_public_value.grid(column=1, row=1, sticky='n e s w')
        self.label_y_public_value = ttk.Label(label_public_key_value, style='info_value.TLabel')
        self.label_y_public_value.grid(column=1, row=2, sticky='n e s w')

        label_public_key_value.grid(column=1, row=2, sticky='n e s w')

        self.label_private_key_value = ttk.Label(right_frame, style='info_value.TLabel', text='not set')
        self.label_private_key_value.grid(column=1, row=3, sticky='n e s w')
        self.label_session_key_value = ttk.Label(right_frame, style='info_value.TLabel', text='')
        self.label_session_key_value.grid(column=1, row=4, sticky='n e s w')
        left_frame.grid(column=0, row=0, sticky='n e s w')
        right_frame.grid(column=1, row=0, sticky='n e s w')

        self.check_file_status()
        self.check_keys_status()

    def check_file_status(self):
        """
        Updating file opened status
        :return: None
        """
        if self.input_file_name:
            self.label_file_status_value.configure(text=f"File opened: {self.input_file_name.split('/')[-1]}",
                                                   style='success.TLabel')
        else:
            self.label_file_status_value.configure(text=f"File is not opened!",
                                                   style='warning_message.TLabel')

    def check_keys_status(self):
        """
        Updating keys info
        :return: None
        """
        if encryption.is_keys_configured:
            p_key = str(encryption.keys['public']['p'])[:30] + '...' \
                if len(str(encryption.keys['public']['p'])) > 30 else str(encryption.keys['public']['p'])
            self.label_p_public_value.configure(text=p_key)
            g_key = str(encryption.keys['public']['g'])[:30] + '...' \
                if len(str(encryption.keys['public']['g'])) > 30 else str(encryption.keys['public']['g'])
            self.label_g_public_value.configure(text=g_key)
            y_key = str(encryption.keys['public']['y'])[:30] + '...' \
                if len(str(encryption.keys['public']['y'])) > 30 else str(encryption.keys['public']['y'])
            self.label_y_public_value.configure(text=y_key)
            self.label_private_key_value.configure(text='set successful!', style='success.TLabel')
            session_key = str(encryption.keys['session'])[:30] + '...' \
                if len(str(encryption.keys['session'])) > 30 else str(encryption.keys['session'])
            self.label_session_key_value.configure(text=session_key)
            self.label_keys_status.config(style='success.TLabel',
                                          text='Public/private keys have been set successful!')
        else:
            self.label_p_public_value.configure(text='')
            self.label_g_public_value.configure(text='')
            self.label_y_public_value.configure(text='')
            self.label_private_key_value.configure(text='not set!', style='warning_message.TLabel')
            self.label_session_key_value.configure(text='')
            self.label_keys_status.config(style='warning.TLabel',
                                          text='Public/private keys are not set. Please configure keys!')

    def open_file(self):
        """
        Handling open file dialog
        :return: None
        """
        self.input_file_name = filedialog.askopenfilename(title="Select file",
                                                          filetypes=(("all files", "*.*"),))
        if self.input_file_name:
            short_file_name = self.input_file_name.split('/')[-1]
            self.check_file_status()
            encrypt.debug_message(f'File {short_file_name} opened successful!')

    def save_file(self):
        """
        Handling saving file dialog
        :return: None
        """
        self.output_file_name = filedialog.asksaveasfilename(title="Save file as...",
                                                             filetypes=(("all files", "*.*"),))
        if self.output_file_name:
            return True
        else:
            return False

    def encrypt_file(self, controller, is_encrypt=True):
        """
        Encrypting file if it's opened
        :return: none
        """
        if is_encrypt:
            make_encryption = encryption.encrypt_file
            MSG_ENCRYPT = 'Encryption'
        else:
            MSG_ENCRYPT = 'Decryption'
            make_encryption = encryption.decrypt_file

        if not self.input_file_name:
            popup_message(f'{MSG_ENCRYPT} failed! (File is not opened)', status=2)
            encrypt.debug_message('File is not opened!')
        elif not encryption.is_keys_configured:
            set_keys = {'Set keys': lambda: controller.show_frame(SelectKeys)}
            popup_message(f'Keys are not configured correctly. Please, fix it!', status=2, **set_keys)
        else:
            if self.save_file():
                operation_time = time()
                try:
                    if make_encryption(self.input_file_name, self.output_file_name):
                        operation_time = time() - operation_time
                        self.label_encrypt_status.configure(
                            text=f'{MSG_ENCRYPT} successful!', foreground=SUCCESS_COLOR)
                        self.label_keys_status.configure(
                            text=f'Total {MSG_ENCRYPT} time: {operation_time} c.',
                            foreground=SUCCESS_COLOR)
                        encrypt.debug_message(f'{MSG_ENCRYPT} successful! Total time: {operation_time}')

                    else:
                        self.label_encrypt_status.configure(text=f'{MSG_ENCRYPT} failed!',
                                                            foreground=ERROR_COLOR)
                    encrypt.debug_message('{} successful!'.format(MSG_ENCRYPT))
                    encrypt.debug_message('Saved as {}'.format(self.output_file_name.split('/')[-1]))
                except AssertionError:
                    encrypt.debug_message(AssertionError)
            else:
                self.label_keys_status.config(
                    text='{} failed! (File to save is not selected)'.format(MSG_ENCRYPT),
                    foreground=WARNING_COLOR)
                encrypt.debug_message('File to save is not selected!')


class SelectKeys(ttk.Frame):
    """
    Class for setting up public / private / session keys
    """
    def __init__(self, parent, controller):
        ttk.Frame.__init__(self, parent)
        controller.geometry('900x650+100+0')
        style = ttk.Style()
        style.configure('TFrame', background=BACKGROUND_COLOR_GRAY)

        # Main fields that includes public/ private keys
        self.public_p_key = tk.IntVar()
        self.public_g_key = tk.IntVar()
        self.public_y_key = tk.IntVar()
        self.private_x_key = tk.IntVar()
        self.session_k_key = tk.IntVar()

        self.columnconfigure(0, weight=1)
        self.columnconfigure(1, weight=1)
        self.columnconfigure(2, weight=1)

        # Header
        self.rowconfigure(0, weight=2)
        # Public key
        self.rowconfigure(1, weight=1)
        # p
        self.rowconfigure(2, weight=1)
        # g
        self.rowconfigure(3, weight=1)
        # y
        self.rowconfigure(4, weight=1)
        # Private key
        self.rowconfigure(5, weight=1)
        # X
        self.rowconfigure(6, weight=1)
        # Session key
        self.rowconfigure(7, weight=1)
        # K
        self.rowconfigure(8, weight=1)
        # Main info
        self.rowconfigure(9, weight=1)
        # handle buttons
        self.rowconfigure(10, weight=2)

        # Initializing styles
        style.configure('h1.TLabel',
                        font=STATUS_FONT_LIGHT,
                        background=BACKGROUND_COLOR_GRAY,
                        foreground=BUTTON_COLOR_LIGHT,
                        anchor=tk.CENTER)
        style.configure('warning.TLabel',
                        font=LABEL_FONT_INFO,
                        background=BACKGROUND_COLOR_GRAY,
                        foreground=WARNING_COLOR,
                        anchor=tk.CENTER)
        style.configure('key.TEntry',
                        font=ENTRY_FONT,
                        background=BUTTON_COLOR_LIGHT,
                        foreground=BACKGROUND_COLOR_GRAY_DARKER,
                        padding=[10, 3, 3, 3])
        style.configure('h2.TLabel',
                        font=HEADER_FONT,
                        background=BACKGROUND_COLOR_GRAY,
                        foreground=BUTTON_COLOR_LIGHT,
                        padding=[0, 15, 0, 2])
        style.configure('info.TLabel',
                        font=LABEL_FONT_INFO,
                        background=BACKGROUND_COLOR_GRAY,
                        foreground=BUTTON_COLOR_LIGHT)
        style.configure('prefix.TLabel',
                        font=LABEL_FONT,
                        background=BACKGROUND_COLOR_GRAY,
                        foreground=BUTTON_COLOR_LIGHT)
        style.configure('dark.TFrame',
                        background=BACKGROUND_COLOR_GRAY_DARKER)
        style.configure('TButton',
                        font=BUTTON_FONT_LIGHT,
                        padding=[10, 3, 10, 3],
                        relief='flat',
                        foreground=BUTTON_COLOR_LIGHT)
        style.map('TButton',
                  background=[('pressed', BUTTON_COLOR_GRAY_PRESSED),
                              ('active', BUTTON_COLOR_GRAY_ACTIVE),
                              ('!active', BUTTON_COLOR_GRAY)],
                  relief=[('pressed', 'flat'), ('!disabled', 'flat')])

        # Main interface configuring
        header_label = ttk.Label(self, style='h1.TLabel', text='Select keys')
        header_label.grid(column=0, columnspan=3, row=0, sticky='n e s w')

        public_key_label = ttk.Label(self, style='h2.TLabel', text='Public key:')
        public_key_label.grid(column=1, row=1, sticky='n s w')

        public_p_label = ttk.Label(self, style='prefix.TLabel', text='P: ')
        public_p_label.grid(column=0, row=2, sticky='n e s')
        self.public_p = ttk.Entry(self, style='key.TEntry', textvariable=self.public_p_key)
        self.public_p.grid(column=1, row=2, sticky='n e s w', pady=5)
        public_p_generate_button = ttk.Button(self, style='TButton', text='Generate', command=self.generate_p_key)
        public_p_generate_button.grid(column=2, row=2, sticky='n s w', padx=10)
        public_g_label = ttk.Label(self, style='prefix.TLabel', text='G: ')
        public_g_label.grid(column=0, row=3, sticky='n e s')
        self.public_g = ttk.Entry(self, style='key.TEntry', textvariable=self.public_g_key)
        self.public_g.grid(column=1, row=3, sticky='n e s w', pady=5)
        public_y_label = ttk.Label(self, style='prefix.TLabel', text='Y: ')
        public_y_label.grid(column=0, row=4, sticky='n e s')
        self.public_y = ttk.Entry(self, style='key.TEntry', textvariable=self.public_y_key)
        self.public_y.grid(column=1, row=4, sticky='n e s w', pady=5)

        private_key_label = ttk.Label(self, style='h2.TLabel', text='Private key:')
        private_key_label.grid(column=1, row=5, sticky='n s w')
        private_x_label = ttk.Label(self, style='prefix.TLabel', text='X: ')
        private_x_label.grid(column=0, row=6, sticky='n e s')
        self.private_x = ttk.Entry(self, style='key.TEntry', textvariable=self.private_x_key)
        self.private_x.grid(column=1, row=6, sticky='n e s w', pady=5)

        session_key_label = ttk.Label(self, style='h2.TLabel', text='Session key:')
        session_key_label.grid(column=1, row=7, sticky='n s w')
        session_k_label = ttk.Label(self, style='prefix.TLabel', text='K: ')
        session_k_label.grid(column=0, row=8, sticky='n e s')
        self.session_k = ttk.Entry(self, style='key.TEntry', textvariable=self.session_k_key)
        self.session_k.grid(column=1, row=8, sticky='n e s w', pady=5)
        session_k_generate_button = ttk.Button(self, style='TButton', text='Generate', command=self.generate_k_key)
        session_k_generate_button.grid(column=2, row=8, sticky='n s w', padx=10)

        info_label = ttk.Label(self,
                               style='warning.TLabel',
                               text="""You should set 'p', 'x', 'k' fields. Other fields will be filled automatically. 
Also you can keep all fields empty. They will be filled automatically.""")
        info_label.grid(column=0, columnspan=3, row=9, sticky='n e s w')
        footer_frame = ttk.Frame(self, style='dark.TFrame')
        footer_frame.columnconfigure(0, weight=5)
        footer_frame.columnconfigure(1, weight=1)
        footer_frame.columnconfigure(2, weight=1)
        footer_frame.columnconfigure(3, weight=1)
        footer_frame.rowconfigure(0, weight=1)

        cancel_button = ttk.Button(footer_frame, style='TButton', text='Close',
                                   command=lambda: self.update_main(controller))
        cancel_button.grid(column=0, row=0, sticky='s w', padx=10, pady=10)
        open_button = ttk.Button(footer_frame, style='TButton', text='Open...')
        open_button.grid(column=1, row=0, sticky='e s', padx=10, pady=10)
        fill_confirm_button = ttk.Button(footer_frame, style='TButton', text='Fill & Confirm',
                                         command=self.fill_confirm_keys)
        fill_confirm_button.grid(column=2, row=0, sticky='e s', padx=10, pady=10)
        save_button = ttk.Button(footer_frame, style='TButton', text='Save as...')
        save_button.grid(column=3, row=0, sticky='e s', padx=10, pady=10)

        footer_frame.grid(column=0, columnspan=3, row=10, sticky='e s w')

    @staticmethod
    def update_main(controller):
        """
        Switching window to main and updating key info in main
        :param controller: parent window to call MainPage
        :return: None
        """
        MainPage.check_keys_status(controller.frames[MainPage])
        controller.show_frame(MainPage)

    def generate_p_key(self):
        """
        Generating p key if it's not set
        :return: p key value
        """
        key = primes.generate_large_prime(key_size=KEY_SIZE)
        self.public_p_key.set(key)
        self.generate_g_key()
        return key

    def generate_g_key(self):
        """
        Generating g key if it's not set
        :return: g key value
        """
        key = primes.primitive_roots(self.public_p_key.get())
        self.public_g_key.set(key)
        return key

    def generate_k_key(self):
        """
        Generating session k key if it's not set and if p key is set
        :return: session k key value
        """
        p = self.public_p_key.get()
        if p:
            while True:
                key = randrange(1, p - 1)
                if primes.gcd(key, p) == 1:
                    self.session_k_key.set(key)
                    return key
        else:
            generate_button = {'Generate': self.generate_p_key}
            popup_message('P key must be set!', status=2, **generate_button)

    def generate_y_key(self):
        """
        Generating public y key if public p and private x keys are set
        :return: public y key
        """
        if self.public_p_key.get() and self.private_x_key.get() and self.public_p_key.get():
            key = pow(self.public_g_key.get(), self.private_x_key.get(), self.public_p_key.get())
            self.public_y_key.set(key)
            return key

    def generate_x_key(self):
        """
        Generating private x key if p key is set
        :return:
        """
        if self.public_p_key.get():
            key = randrange(2, self.public_p_key.get() - 1)
            self.private_x_key.set(key)
            return key

    def check_fields(self):
        """
        Checking all fields if they are correct
        :return: True if fields are correct, else False
        """
        error_fields = []
        try:
            self.public_p_key.get()
        except Exception:
            error_fields.append('P')
        try:
            self.public_g_key.get()
        except Exception:
            error_fields.append('G')
        try:
            self.public_y_key.get()
        except Exception:
            error_fields.append('Y')
        try:
            self.private_x_key.get()
        except Exception:
            error_fields.append('X')
        try:
            self.session_k_key.get()
        except Exception:
            error_fields.append('K')
        if error_fields:
            popup_message(', '.join(error_fields) + ' fields are incorrect. Please, fix them')
            return False
        return True

    def fill_confirm_keys(self):
        """
        If all fields are correct, key will be applied successfully
        :return: None
        """
        if self.check_fields():
            p = self.public_p_key.get()
            g = self.public_g_key.get()
            y = self.public_y_key.get()
            x = self.private_x_key.get()
            k = self.session_k_key.get()
            keys = {
                'public': {
                    'p': p if encryption.check_p_key(p) else self.generate_p_key(),
                    'g': g if encryption.check_g_key(g, p) else self.generate_g_key()
                },
                'private': x if encryption.check_x_key(x, p) else self.generate_x_key(),
                'session': k if encryption.check_k_key(k, p) else self.generate_k_key()
            }
            if y and encryption.check_y_key(y, p, g, x):
                keys['public']['y'] = y
            else:
                keys['public']['y'] = self.generate_y_key()
            popup_message('Filled and checked successfully!', status=0)
            encryption.set_keys(keys)
        else:
            encryption.is_keys_configured = False


app = CryptApp()
app.mainloop()
