import subprocess
import os
from datetime import datetime
import tkinter as tk
from tkinter import scrolledtext, messagebox, filedialog

class iOSDeviceScanner:
    def __init__(self):
        # Ruta relativa a los binarios
        self.bin_path = os.path.join(os.path.dirname(__file__), "libimobiledevice-bin")
        
    def get_device_info(self):
        exe = os.path.join(self.bin_path, "ideviceinfo.exe")
        try:
            output = subprocess.check_output([exe], encoding="utf-8", errors="ignore")
            info = {}
            for line in output.splitlines():
                if ":" in line:
                    key, value = line.split(":", 1)
                    info[key.strip()] = value.strip()
            return info
        except Exception as e:
            return {"Error": f"Error ejecutando ideviceinfo: {e}"}

scanner = iOSDeviceScanner()

def show_info():
    info = scanner.get_device_info()
    text_area.config(state=tk.NORMAL)
    text_area.delete(1.0, tk.END)
    if info:
        header = f"iCosm8 Detector - {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}\n"
        text_area.insert(tk.END, header)
        text_area.insert(tk.END, "="*60 + "\n")
        for key, value in info.items():
            text_area.insert(tk.END, f"{key.replace('_', ' ').title():<30}: {value}\n")
        text_area.insert(tk.END, "="*60 + "\n")
    else:
        messagebox.showerror("Error", "No se pudo obtener información del dispositivo")
    text_area.config(state=tk.DISABLED)

def save_info():
    content = text_area.get(1.0, tk.END).strip()
    if not content:
        messagebox.showwarning("Advertencia", "No hay información para guardar.")
        return
    file_path = filedialog.asksaveasfilename(
        defaultextension=".txt",
        filetypes=[("Archivo de texto", "*.txt")],
        title="Guardar información"
    )
    if file_path:
        try:
            with open(file_path, "w", encoding="utf-8") as f:
                f.write(content)
            messagebox.showinfo("Guardado", f"Información guardada en:\n{file_path}")
        except Exception as e:
            messagebox.showerror("Error", f"No se pudo guardar el archivo:\n{e}")

def detect_dfu_mode():
    irecovery_exe = os.path.join(scanner.bin_path, "irecovery.exe")
    if not os.path.exists(irecovery_exe):
        return "No se encontró irecovery.exe para detectar DFU/Recovery."
    try:
        output = subprocess.check_output([irecovery_exe, "-q"], encoding="utf-8", errors="ignore")
        if "DFU" in output or "Recovery" in output:
            return "¡Dispositivo detectado en modo DFU/Recovery!\n\n" + output
        else:
            return "No hay dispositivos en modo DFU/Recovery conectados."
    except subprocess.CalledProcessError:
        return "No hay dispositivos en modo DFU/Recovery conectados."
    except Exception as e:
        return f"Error al detectar DFU/Recovery: {e}"

def show_dfu_info():
    text_area.config(state=tk.NORMAL)
    text_area.delete(1.0, tk.END)
    dfu_info = detect_dfu_mode()
    text_area.insert(tk.END, f"iCosm8 Detector - Detección DFU\n")
    text_area.insert(tk.END, "="*60 + "\n")
    text_area.insert(tk.END, dfu_info)
    text_area.insert(tk.END, "\n" + "="*60 + "\n")
    text_area.config(state=tk.DISABLED)

# Interfaz gráfica mejorada
root = tk.Tk()
root.title("iCosm8 Detector")
root.geometry("700x550")
root.configure(bg="#f0f4f8")

frame = tk.Frame(root, bg="#e3eaf2", bd=2, relief=tk.RIDGE)
frame.pack(padx=20, pady=20, fill=tk.BOTH, expand=True)

title_label = tk.Label(
    frame, text="iCosm8 Detector", font=("Segoe UI", 20, "bold"),
    bg="#e3eaf2", fg="#2d415a"
)
title_label.pack(pady=(10, 5))

desc_label = tk.Label(
    frame, text="Escanea y guarda información de dispositivos iOS conectados.",
    font=("Segoe UI", 12), bg="#e3eaf2", fg="#4a5a6a"
)
desc_label.pack(pady=(0, 15))

btn_frame = tk.Frame(frame, bg="#e3eaf2")
btn_frame.pack(pady=5)

scan_btn = tk.Button(
    btn_frame, text="Obtener información", command=show_info,
    font=("Segoe UI", 11), bg="#4a90e2", fg="white", width=18, relief=tk.FLAT
)
scan_btn.pack(side=tk.LEFT, padx=5)

save_btn = tk.Button(
    btn_frame, text="Guardar lectura", command=save_info,
    font=("Segoe UI", 11), bg="#7ed957", fg="white", width=15, relief=tk.FLAT
)
save_btn.pack(side=tk.LEFT, padx=5)

dfu_btn = tk.Button(
    btn_frame, text="Detectar DFU", command=show_dfu_info,
    font=("Segoe UI", 11), bg="#f5a623", fg="white", width=15, relief=tk.FLAT
)
dfu_btn.pack(side=tk.LEFT, padx=5)

text_area = scrolledtext.ScrolledText(
    frame, width=80, height=22, font=("Consolas", 10), bg="#f8fafc", fg="#222",
    borderwidth=2, relief=tk.GROOVE, state=tk.DISABLED
)
text_area.pack(padx=10, pady=15, fill=tk.BOTH, expand=True)

# Iniciar el bucle de la interfaz gráfica
root.mainloop()