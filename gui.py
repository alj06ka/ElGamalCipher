import tkinter as tk
from tkinter import ttk
from tkinter import filedialog
from time import time

# Constant colors and fonts using in this GUI
HEADER_FONT = ('Open Sans', 15)
BUTTON_FONT = ('Open Sans', 12)
LABEL_FONT = ('Open Sans light', 10)
LABEL_SUCCESS_FONT = ('Open Sans', 10)
ENTRY_FONT = ('Open Sans', 10)
STATUS_FONT = ('Open Sans Bold', 12)
DARK_VIOLET_COLOR = '#342E37'
GREEN_COLOR = '#9FD356'
WHITE_COLOR = '#FAFFFD'
ORANGE_COLOR = '#FA824C'
BLUE_COLOR = '#3C91E6'

# Other settings
DEBUG = True
SIZE_OF_BITS = 1024
INPUT_FILE_BITS = False


class CryptApp(tk.Tk):
    """
        Main class for initializing multiple windows and handle it.
    """
    def __init__(self):
        tk.Tk.__init__(self)
        self.minsize(640, 480)
        self.geometry('640x480+300+250')
        self.title('ElGamal Encipher')
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
        style.configure('TFrame', background=DARK_VIOLET_COLOR)
        self.columnconfigure(0, weight=1)
        self.columnconfigure(1, weight=3)
        self.columnconfigure(2, weight=1)
        self.columnconfigure(3, weight=3)
        self.rowconfigure(7, weight=2)

        # Initializing styles
        style.configure('TButton',
                        font=BUTTON_FONT,
                        padding=10,
                        relief='flat',
                        foreground=DARK_VIOLET_COLOR)

        style.configure('open.TButton',
                        background=GREEN_COLOR)

        style.configure('encrypt.TButton',
                        background=GREEN_COLOR)

        style.configure('key.TEntry',
                        font=ENTRY_FONT,
                        background=GREEN_COLOR,
                        foreground=DARK_VIOLET_COLOR,
                        padding='10 2 2 2')

        style.configure('TLabel',
                        font=LABEL_FONT,
                        background=DARK_VIOLET_COLOR,
                        foreground=WHITE_COLOR)

        style.configure('success.TLabel',
                        font=LABEL_SUCCESS_FONT,
                        background=DARK_VIOLET_COLOR,
                        foreground=BLUE_COLOR)

        style.configure("Vertical.TScrollbar",
                        gripcount=0,
                        background=GREEN_COLOR,
                        darkcolor=DARK_VIOLET_COLOR,
                        lightcolor=ORANGE_COLOR,
                        troughcolor=WHITE_COLOR,
                        bordercolor=ORANGE_COLOR,
                        arrowcolor=DARK_VIOLET_COLOR,
                        relief='flat')

        header_label = tk.Label(self, text="ElGamal Encryption",
                                font=HEADER_FONT,
                                background=DARK_VIOLET_COLOR,
                                foreground=BLUE_COLOR,
                                justify='center')
        header_label.grid(padx=10, pady=10, column=0, row=0, columnspan=4, sticky='n e s w')

        # File open button
        open_file_button = ttk.Button(self, text='Open file...', style='open.TButton', command=self.open_file)
        open_file_button.grid(padx=10, pady=0, column=0, row=2, sticky='n w e s ')

        self.open_file_status_label = ttk.Label(self, text='File is not opened!')
        self.open_file_status_label.grid(padx=10, column=0, row=3, sticky='n w')

        # Encryption key input
        self.encrypt_decrypt_key_label = ttk.Label(self, text='Encryption/ Decryption key:')
        self.encrypt_decrypt_key_label.grid(padx=10, column=2, row=1, sticky='n w')

        vcmd = (self.register(self._change_key_len),
                '%P', '%V')
        self.encryption_key = tk.StringVar()
        self.encrypt_decrypt_key_entry = ttk.Entry(self,
                                                   style='key.TEntry',
                                                   validate='all',
                                                   validatecommand=vcmd,
                                                   textvariable=self.encryption_key)
        self.encrypt_decrypt_key_entry.grid(padx=10, column=2, row=2, sticky='n w e s')

        self.encrypt_decrypt_key_label_len = tk.Label(self,
                                                      text='0/23',
                                                      background=DARK_VIOLET_COLOR,
                                                      foreground=WHITE_COLOR)
        self.encrypt_decrypt_key_label_len.grid(padx=10, column=2, row=3, sticky='n w')

        # Encrypt button
        encrypt_button = ttk.Button(self,
                                    text='Encrypt',
                                    style='encrypt.TButton',
                                    command=lambda: self.encrypt_file(True))
        encrypt_button.grid(padx=10, pady=25, column=0, columnspan=2, row=4, sticky='n w e s')

        # Decrypt button
        decrypt_button = ttk.Button(self,
                                    text='Decrypt',
                                    style='encrypt.TButton',
                                    command=lambda: self.encrypt_file(False))
        decrypt_button.grid(padx=10, pady=25, column=2, columnspan=2, row=4, sticky='n w e s')

        self.encrypt_decrypt_status_label = tk.Label(self,
                                                     text='',
                                                     background=DARK_VIOLET_COLOR,
                                                     foreground=WHITE_COLOR,
                                                     font=STATUS_FONT)
        self.encrypt_decrypt_status_label.grid(padx=10, column=0, columnspan=4, row=5, sticky='n w e')

        if not INPUT_FILE_BITS:
            # Input & Output file bytes fields
            encrypt_file_bytes_label = ttk.Label(self, text='Encryption key bytes:')
            encrypt_file_bytes_label.grid(padx=10, pady=5, column=0, row=6, sticky='n w')

            output_file_bytes_label = ttk.Label(self, text='Output file bytes:')
            output_file_bytes_label.grid(padx=10, pady=5, column=2, row=6, sticky='n w')

            key_file_frame = tk.Frame(self)

            key_scroll = ttk.Scrollbar(key_file_frame, orient='vertical')
            key_scroll.pack(side='right', fill='y')
            self.key_file_bytes = tk.Text(key_file_frame,
                                          font=ENTRY_FONT,
                                          background=WHITE_COLOR,
                                          foreground=DARK_VIOLET_COLOR,
                                          relief='flat')
            self.key_file_bytes.pack(fill='both')

            key_scroll.config(command=self.key_file_bytes.yview)
            self.key_file_bytes.config(yscrollcommand=key_scroll.set, state=tk.DISABLED)
            key_file_frame.grid(padx=10, pady=10, column=0, columnspan=2, row=7, sticky='n w e s')

            output_file_frame = tk.Frame(self)
            output_scroll = ttk.Scrollbar(output_file_frame, orient='vertical')
            output_scroll.pack(side='right', fill='y')
            self.output_file_bytes = tk.Text(output_file_frame,
                                             font=ENTRY_FONT,
                                             background=WHITE_COLOR,
                                             foreground=DARK_VIOLET_COLOR,
                                             relief='flat')
            self.output_file_bytes.pack(fill='both')
            output_file_frame.grid(padx=10, pady=10, column=2, columnspan=2, row=7, sticky='n w e s')
        else:
            input_output_key_frame = tk.Frame(self, background=DARK_VIOLET_COLOR)
            input_output_key_frame.columnconfigure(0, weight=1)
            input_output_key_frame.columnconfigure(1, weight=1)
            input_output_key_frame.columnconfigure(2, weight=1)

            # Input & Output file bytes fields
            input_file_bytes_label = ttk.Label(input_output_key_frame, text='Input file bytes:')
            input_file_bytes_label.grid(padx=10, pady=5, column=0, row=0, sticky='n w')
            key_file_bytes_label = ttk.Label(input_output_key_frame, text='Encryption key bytes:')
            key_file_bytes_label.grid(padx=10, pady=5, column=1, row=0, sticky='n w')
            output_file_bytes_label = ttk.Label(input_output_key_frame, text='Output file bytes:')
            output_file_bytes_label.grid(padx=10, pady=5, column=2, row=0, sticky='n w')

            input_file_frame = tk.Frame(input_output_key_frame)
            input_scroll = ttk.Scrollbar(input_file_frame, orient='vertical')
            input_scroll.pack(side='right', fill='y')
            self.input_file_bytes = tk.Text(input_file_frame,
                                            font=ENTRY_FONT,
                                            background=WHITE_COLOR,
                                            foreground=DARK_VIOLET_COLOR,
                                            relief='flat')
            self.input_file_bytes.pack(fill='both')
            input_file_frame.grid(padx=10, pady=10, column=0, row=1, sticky='n w e s')

            key_file_frame = tk.Frame(input_output_key_frame)
            key_scroll = ttk.Scrollbar(key_file_frame, orient='vertical')
            key_scroll.pack(side='right', fill='y')
            self.key_file_bytes = tk.Text(key_file_frame,
                                          font=ENTRY_FONT,
                                          background=WHITE_COLOR,
                                          foreground=DARK_VIOLET_COLOR,
                                          relief='flat')
            self.key_file_bytes.pack(fill='both')
            key_file_frame.grid(padx=10, pady=10, column=1, row=1, sticky='n w e s')

            output_file_frame = tk.Frame(input_output_key_frame)
            output_scroll = ttk.Scrollbar(output_file_frame, orient='vertical')
            output_scroll.pack(side='right', fill='y')
            self.output_file_bytes = tk.Text(output_file_frame,
                                             font=ENTRY_FONT,
                                             background=WHITE_COLOR,
                                             foreground=DARK_VIOLET_COLOR,
                                             relief='flat')
            self.output_file_bytes.pack(fill='both')
            output_file_frame.grid(padx=10, pady=10, column=2, row=1, sticky='n w e s')

            input_output_key_frame.grid(padx=10, pady=10, column=0, columnspan=4, row=6, rowspan=2, sticky='n w e s')

    def _change_key_len(self, text, callback):
        """
        Checking input Encryption key
        :param text: encryption key
        :return: True if key is valid, else False
        """
        if callback == 'focusout':
            self.encryption_key.set(text)
        if len(text) < 23:
            self.encrypt_decrypt_key_label_len.configure(text='{}/23'.format(len(text)), foreground=WHITE_COLOR)
        elif len(text) == 23:
            self.encrypt_decrypt_key_label_len.configure(text='23/23', foreground=BLUE_COLOR)
        else:
            self.encrypt_decrypt_key_label_len.configure(text='Value is invalid, please, fix it!',
                                                         foreground=ORANGE_COLOR)
        return True

    def open_file(self):
        """
        Handling open file dialog
        :return: None
        """
        self.input_file_name = filedialog.askopenfilename(title="Select file",
                                                          filetypes=(("all files", "*.*"),))
        if self.input_file_name:
            short_file_name = self.input_file_name.split('/')[-1]
            self.open_file_status_label.configure(text='File opened: {}'.format(short_file_name),
                                                  style='success.TLabel')
            self.encrypt_decrypt_status_label.config(text='')
            debug_message('File {} opened successful!'.format(short_file_name))

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

    def encrypt_file(self, is_encrypt):
        """
        Encrypting file if it's opened
        :argument is_encrypt: True if Encrypt, else False
        :return: none
        """
        if is_encrypt:
            MSG_ENCRYPT = 'Encryption'
        else:
            MSG_ENCRYPT = 'Decryption'
        if not self.input_file_name:
            self.encrypt_decrypt_status_label.configure(text='{} failed! (File is not opened)'.format(MSG_ENCRYPT),
                                                        foreground=ORANGE_COLOR)
            debug_message('File is not opened!')
        elif not len(handle_entry_bin(self.encryption_key.get())) == 23:
            self.encrypt_decrypt_status_label.configure(text='Encryption key is incorrect!',
                                                        foreground=ORANGE_COLOR)
        else:
            if self.save_file():
                key = convert_str_to_int(self.encryption_key.get())
                operation_time = time()
                if binaryEncipher.encryptFile(self.input_file_name, self.output_file_name, key):
                    operation_time = time() - operation_time
                    self.encrypt_decrypt_status_label.configure(
                        text='%s successful! Total time: %.2f sec.' % (MSG_ENCRYPT, operation_time),
                        foreground=BLUE_COLOR)
                    self.key_file_bytes.delete(1.0, tk.END)
                    self.output_file_bytes.delete(1.0, tk.END)
                    self.key_file_bytes.insert(tk.END, get_file_bits('tmp.bin', SIZE_OF_BITS))
                    self.output_file_bytes.insert(tk.END, get_file_bits(self.output_file_name, SIZE_OF_BITS))
                    if INPUT_FILE_BITS:
                        self.input_file_bytes.delete(1.0, tk.END)
                        self.input_file_bytes.insert(tk.END, get_file_bits(self.input_file_name, SIZE_OF_BITS))
                else:
                    self.encrypt_decrypt_status_label.configure(text='{} failed!'.format(MSG_ENCRYPT),
                                                                foreground=ORANGE_COLOR)
                debug_message('{} successful!'.format(MSG_ENCRYPT))
                debug_message('Saved as {}'.format(self.output_file_name.split('/')[-1]))
            else:
                self.encrypt_decrypt_status_label.config(
                    text='{} failed! (File to save is not selected)'.format(MSG_ENCRYPT),
                    foreground=ORANGE_COLOR)
                debug_message('File to save is not selected!')


def debug_message(message):
    """
    Sending debug message if DEBUG is enabled
    :param message: message to send
    :return:
    """
    if DEBUG:
        print('[DEBUG]: {}'.format(message))
    return 0


app = CryptApp()
app.mainloop()
