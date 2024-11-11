import tkinter as tk
from tkinter import ttk, scrolledtext, filedialog, messagebox
from gtts import gTTS
import os
from datetime import datetime
from tkinter.font import Font

class FuturisticApp(tk.Tk):
    def __init__(self):
        super().__init__()

        self.title("Neural Voice Synthesizer")
        self.geometry("800x600")
        self.configure(bg='#0F1626')  # Dark blue background

        # Custom styles
        self.style = ttk.Style()
        self.style.theme_use('default')
        
        # Configure custom styles
        self.style.configure(
            'Futuristic.TFrame',
            background='#0F1626'
        )
        
        self.style.configure(
            'Futuristic.TLabel',
            background='#0F1626',
            foreground='#4CC9F0',
            font=('Helvetica', 10)
        )
        
        self.style.configure(
            'Title.TLabel',
            background='#0F1626',
            foreground='#4CC9F0',
            font=('Helvetica', 24, 'bold')
        )
        
        self.style.configure(
            'Futuristic.TButton',
            background='#4361EE',
            foreground='white',
            padding=10,
            font=('Helvetica', 10, 'bold')
        )
        
        # Define language mappings
        self.languages = {
            'English': 'en',
            'Hindi': 'hi',
            'Spanish': 'es',
            'French': 'fr',
            'German': 'de',
            'Italian': 'it',
            'Japanese': 'ja'
        }

        self.create_widgets()

    def create_widgets(self):
        # Main container
        main_frame = ttk.Frame(self, style='Futuristic.TFrame', padding="20")
        main_frame.grid(row=0, column=0, sticky="nsew")
        self.grid_rowconfigure(0, weight=1)
        self.grid_columnconfigure(0, weight=1)

        # Title with glow effect
        title_frame = ttk.Frame(main_frame, style='Futuristic.TFrame')
        title_frame.grid(row=0, column=0, columnspan=2, pady=(0, 20))
        
        title = ttk.Label(
            title_frame,
            text="NEURAL VOICE SYNTHESIZER",
            style='Title.TLabel'
        )
        title.grid(row=0, column=0, pady=10)

        # Custom text area with futuristic styling
        text_frame = ttk.Frame(main_frame, style='Futuristic.TFrame')
        text_frame.grid(row=1, column=0, columnspan=2, sticky="nsew", pady=(0, 20))
        
        self.text_area = scrolledtext.ScrolledText(
            text_frame,
            width=70,
            height=15,
            font=('Consolas', 11),
            bg='#1B2439',  # Darker blue background
            fg='#7DF9FF',  # Cyan text
            insertbackground='#4CC9F0',  # Cursor color
            relief='flat',
            borderwidth=0
        )
        self.text_area.pack(expand=True, fill='both')
        
        # Add placeholder text
        placeholder = "Enter your text here for neural synthesis..."
        self.text_area.insert('1.0', placeholder)
        self.text_area.bind('<FocusIn>', lambda e: self.on_focus_in(e, placeholder))
        self.text_area.bind('<FocusOut>', lambda e: self.on_focus_out(e, placeholder))

        # Language selection with custom styling
        lang_frame = ttk.Frame(main_frame, style='Futuristic.TFrame')
        lang_frame.grid(row=2, column=0, columnspan=2, pady=(0, 20))
        
        lang_label = ttk.Label(
            lang_frame,
            text="SELECT NEURAL MODEL:",
            style='Futuristic.TLabel'
        )
        lang_label.grid(row=0, column=0, padx=(0, 10))
        
        self.selected_language = tk.StringVar(value='English')
        self.lang_combo = ttk.Combobox(
            lang_frame,
            textvariable=self.selected_language,
            values=list(self.languages.keys()),
            state='readonly',
            width=20
        )
        self.lang_combo.set('English')
        self.lang_combo.grid(row=0, column=1)

        # Custom styled button
        self.convert_btn = tk.Button(
            main_frame,
            text="SYNTHESIZE VOICE",
            command=self.convert_text,
            bg='#4361EE',
            fg='white',
            font=('Helvetica', 12, 'bold'),
            relief='flat',
            borderwidth=0,
            padx=20,
            pady=10,
            cursor='hand2'
        )
        self.convert_btn.grid(row=3, column=0, columnspan=2, pady=20)
        
        # Bind hover effects
        self.convert_btn.bind('<Enter>', lambda e: self.convert_btn.config(bg='#3051DE'))
        self.convert_btn.bind('<Leave>', lambda e: self.convert_btn.config(bg='#4361EE'))

        # Status display with sci-fi styling
        self.status_frame = ttk.Frame(main_frame, style='Futuristic.TFrame')
        self.status_frame.grid(row=4, column=0, columnspan=2, sticky="ew", pady=(0, 10))
        
        self.status_label = ttk.Label(
            self.status_frame,
            text="SYSTEM READY",
            style='Futuristic.TLabel'
        )
        self.status_label.pack()

        # Custom progress bar
        self.progress = ttk.Progressbar(
            main_frame,
            mode='indeterminate',
            style='Futuristic.Horizontal.TProgressbar'
        )
        self.progress.grid(row=5, column=0, columnspan=2, sticky="ew", pady=(0, 10))

        # Configure progress bar style
        self.style.configure(
            'Futuristic.Horizontal.TProgressbar',
            troughcolor='#1B2439',
            background='#4CC9F0',
            darkcolor='#4CC9F0',
            lightcolor='#4CC9F0',
            bordercolor='#1B2439'
        )

    def on_focus_in(self, event, placeholder):
        if self.text_area.get('1.0', 'end-1c') == placeholder:
            self.text_area.delete('1.0', tk.END)

    def on_focus_out(self, event, placeholder):
        if not self.text_area.get('1.0', 'end-1c'):
            self.text_area.insert('1.0', placeholder)

    def convert_text(self):
        text = self.text_area.get("1.0", tk.END).strip()
        if not text:
            messagebox.showerror("Error", "Please enter text for synthesis!")
            return
        
        try:
            self.progress.start()
            self.status_label.config(text="SYNTHESIZING...")
            self.convert_btn.config(state='disabled')
            self.update()
            
            selected_lang = self.selected_language.get()
            lang_code = self.languages[selected_lang]
            
            tts = gTTS(text=text, lang=lang_code, slow=False)
            
            timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
            default_filename = f"neural_voice_{timestamp}.mp3"
            file_path = filedialog.asksaveasfilename(
                defaultextension=".mp3",
                filetypes=[("MP3 files", "*.mp3")],
                initialfile=default_filename
            )
            
            if file_path:
                tts.save(file_path)
                self.status_label.config(text="SYNTHESIS COMPLETE")
                messagebox.showinfo("Success", "Neural voice synthesis completed successfully!")
            else:
                self.status_label.config(text="SYNTHESIS CANCELLED")
                
        except Exception as e:
            self.status_label.config(text="SYNTHESIS ERROR")
            messagebox.showerror("Error", f"Synthesis error occurred: {str(e)}")
        
        finally:
            self.progress.stop()
            self.convert_btn.config(state='normal')
            self.update()

if __name__ == "__main__":
    app = FuturisticApp()
    app.mainloop()
