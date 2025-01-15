import subprocess
import tkinter as tk
from tkinter import filedialog, messagebox
from tkinter import scrolledtext
from tkinter import ttk

# Function to run the identification process
def run_identification():
    jar_path = jar_entry.get()
    swath_file = swath_entry.get()
    library_file = library_entry.get()
    output_file = output_ident_entry.get()
    parent_mass_tol = parent_tol_entry.get()
    fragment_mass_tol = fragment_tol_entry.get()
    num_scans = num_scans_entry.get()

    if not all([jar_path, swath_file, library_file, output_file, parent_mass_tol, fragment_mass_tol, num_scans]):
        messagebox.showwarning("Missing Information", "Please fill all fields for Identification.")
        return

    command = (
        f'java -Xmx2500M -cp "{jar_path}" org.Spectrums.SWATHMSPLITSearch '
        f'{parent_mass_tol} {fragment_mass_tol} {num_scans} "{swath_file}" "{library_file}" "{output_file}"'
    )

    try:
        result = subprocess.run(command, shell=True, capture_output=True, text=True)
        output_text.insert(tk.END, result.stdout)
        output_text.insert(tk.END, result.stderr)
        messagebox.showinfo("Command Output", result.stdout if result.stdout else "No output")
    except Exception as e:
        messagebox.showerror("Error", str(e))

# Function to run the filtering process
def run_filtering():
    jar_path = jar_entry.get()
    filtered_input = filtered_input_entry.get()
    filtered_output = filtered_output_entry.get()
    fdr_value = fdr_entry.get()

    if not all([jar_path, filtered_input, filtered_output, fdr_value]):
        messagebox.showwarning("Missing Information", "Please fill all fields for Filtering.")
        return

    # Validate FDR value
    try:
        float(fdr_value)
    except ValueError:
        messagebox.showerror("Invalid FDR Value", "Please enter a valid number for FDR Threshold.")
        return

    command = (
        f'java -cp "{jar_path}" UI.SWATHFilter -r "{filtered_input}" '
        f'-o "{filtered_output}" -fdr {fdr_value}'
    )

    try:
        result = subprocess.run(command, shell=True, capture_output=True, text=True)
        output_text.insert(tk.END, result.stdout)
        output_text.insert(tk.END, result.stderr)
        messagebox.showinfo("Command Output", result.stdout if result.stdout else "No output")
    except Exception as e:
        messagebox.showerror("Error", str(e))

# Function to run the quantification process
def run_quantification():
    jar_path = jar_entry.get()
    quant_mode = quant_mode_var.get()  # e.g., PeakViewInput, OpenSwath, Skyline
    quant_library = quant_library_entry.get()
    quant_search_result = quant_search_entry.get()
    quant_fasta = quant_fasta_entry.get()
    quant_output = quant_output_entry.get()

    if not all([jar_path, quant_mode, quant_library, quant_search_result, quant_fasta, quant_output]):
        messagebox.showwarning("Missing Information", "Please fill all fields for Quantification.")
        return

    # Map quantification modes to their respective arguments
    quant_mode_flags = {
        "OpenSwath": "-OpenswathInput 1",
        "PeakViewInput": "-PeakviewInput 1",
        "Skyline": "-SkylineInput 1",
    }

    quant_mode_flag = quant_mode_flags.get(quant_mode, "")

    # Build the command
    command = (
        f'java -Xmx2000M -cp "{jar_path}" UI.SWATHQuant '
        f'-l "{quant_library}" -r "{quant_search_result}" -d "{quant_fasta}" '
        f'-o "{quant_output}" {quant_mode_flag}'
    )

    try:
        result = subprocess.run(command, shell=True, capture_output=True, text=True)
        output_text.insert(tk.END, result.stdout)
        output_text.insert(tk.END, result.stderr)
        messagebox.showinfo("Command Output", result.stdout if result.stdout else "No output")
    except Exception as e:
        messagebox.showerror("Error", str(e))

def run_spectral_counting():
    jar_path = jar_entry.get()
    spectral_search_result = spectral_search_entry.get()
    spectral_fasta = spectral_fasta_entry.get()
    experiment_name = experiment_entry.get()
    bait_name = bait_entry.get()
    spectral_output = spectral_output_entry.get()

    if not all([jar_path, spectral_search_result, spectral_fasta, experiment_name, bait_name, spectral_output]):
        messagebox.showwarning("Missing Information", "Please fill all fields for Spectral Counting.")
        return

    # Build the command for spectral counting
    command = (
        f'java -Xmx1000M -cp "{jar_path}" UI.SWATHQuant SAINTInput '
        f'"{spectral_search_result}" "{spectral_fasta}" "{experiment_name}" "{bait_name}" "{spectral_output}"'
    )

    try:
        result = subprocess.run(command, shell=True, capture_output=True, text=True)
        output_text.insert(tk.END, result.stdout)
        output_text.insert(tk.END, result.stderr)
        messagebox.showinfo("Command Output", result.stdout if result.stdout else "No output")
    except Exception as e:
        messagebox.showerror("Error", str(e))




# Helper functions for browsing and saving files
def browse_jar():
    jar_file = filedialog.askopenfilename(filetypes=[("Java JAR Files", "*.jar")])
    jar_entry.delete(0, tk.END)
    jar_entry.insert(0, jar_file)

def browse_file(entry):
    selected_file = filedialog.askopenfilename(filetypes=[("All Files", "*.*")])
    entry.delete(0, tk.END)
    entry.insert(0, selected_file)

def save_file(entry):
    save_location = filedialog.asksaveasfilename(defaultextension=".txt", 
                                                 filetypes=[("Text Files", "*.txt"), ("All Files", "*.*")])
    entry.delete(0, tk.END)
    entry.insert(0, save_location)

# GUI setup
root = tk.Tk()
root.title("MSPLIT-DIA Command Line GUI")

mainframe = ttk.Frame(root, padding="10")
mainframe.grid(row=0, column=0, sticky=(tk.N, tk.W, tk.E, tk.S))
root.columnconfigure(0, weight=1)
root.rowconfigure(0, weight=1)

# JAR file selection
jar_frame = ttk.Frame(mainframe, padding="5")
jar_frame.grid(row=0, column=0, columnspan=3, sticky=(tk.W, tk.E))
jar_frame.columnconfigure(0, weight=1)

ttk.Label(jar_frame, text="Select MSPLIT-DIA JAR File:").grid(row=0, column=0, sticky=tk.W)
jar_entry = ttk.Entry(jar_frame, width=60)
jar_entry.grid(row=1, column=0, sticky=(tk.W, tk.E), pady=5)
ttk.Button(jar_frame, text="Browse", command=browse_jar).grid(row=1, column=1, padx=5)

# Identification frame
ident_frame = ttk.LabelFrame(mainframe, text="Identification", padding="10")
ident_frame.grid(row=1, column=0, sticky=(tk.N, tk.W, tk.E, tk.S), padx=5, pady=5)
ident_frame.columnconfigure(0, weight=1)

ttk.Label(ident_frame, text="Select SWATH File:").grid(row=0, column=0, sticky=tk.W)
swath_entry = ttk.Entry(ident_frame)
swath_entry.grid(row=1, column=0, sticky=(tk.W, tk.E), pady=5)
ttk.Button(ident_frame, text="Browse", command=lambda: browse_file(swath_entry)).grid(row=1, column=1, padx=5)

ttk.Label(ident_frame, text="Select Library File (MGF):").grid(row=2, column=0, sticky=tk.W)
library_entry = ttk.Entry(ident_frame)
library_entry.grid(row=3, column=0, sticky=(tk.W, tk.E), pady=5)
ttk.Button(ident_frame, text="Browse", command=lambda: browse_file(library_entry)).grid(row=3, column=1, padx=5)

ttk.Label(ident_frame, text="Specify Output File for Identification:").grid(row=4, column=0, sticky=tk.W)
output_ident_entry = ttk.Entry(ident_frame)
output_ident_entry.grid(row=5, column=0, sticky=(tk.W, tk.E), pady=5)
ttk.Button(ident_frame, text="Save", command=lambda: save_file(output_ident_entry)).grid(row=5, column=1, padx=5)

ttk.Label(ident_frame, text="Parent Mass Tolerance (Da):").grid(row=6, column=0, sticky=tk.W)
parent_tol_entry = ttk.Entry(ident_frame)
parent_tol_entry.grid(row=7, column=0, sticky=(tk.W, tk.E), pady=5)

ttk.Label(ident_frame, text="Fragment Mass Tolerance (ppm):").grid(row=8, column=0, sticky=tk.W)
fragment_tol_entry = ttk.Entry(ident_frame)
fragment_tol_entry.grid(row=9, column=0, sticky=(tk.W, tk.E), pady=5)

ttk.Label(ident_frame, text="Number of Scans per Cycle:").grid(row=10, column=0, sticky=tk.W)
num_scans_entry = ttk.Entry(ident_frame)
num_scans_entry.grid(row=11, column=0, sticky=(tk.W, tk.E), pady=5)

ttk.Button(ident_frame, text="Run Identification", command=run_identification).grid(row=12, column=0, columnspan=2, pady=10)

# Filtering frame
filter_frame = ttk.LabelFrame(mainframe, text="Filtering", padding="10")
filter_frame.grid(row=1, column=1, sticky=(tk.N, tk.W, tk.E, tk.S), padx=5, pady=5)
filter_frame.columnconfigure(0, weight=1)

ttk.Label(filter_frame, text="Select Input File for Filtering:").grid(row=0, column=0, sticky=tk.W)
filtered_input_entry = ttk.Entry(filter_frame)
filtered_input_entry.grid(row=1, column=0, sticky=(tk.W, tk.E), pady=5)
ttk.Button(filter_frame, text="Browse", command=lambda: browse_file(filtered_input_entry)).grid(row=1, column=1, padx=5)

ttk.Label(filter_frame, text="Specify Output File for Filtering:").grid(row=2, column=0, sticky=tk.W)
filtered_output_entry = ttk.Entry(filter_frame)
filtered_output_entry.grid(row=3, column=0, sticky=(tk.W, tk.E), pady=5)
ttk.Button(filter_frame, text="Save", command=lambda: save_file(filtered_output_entry)).grid(row=3, column=1, padx=5)

ttk.Label(filter_frame, text="FDR Threshold:").grid(row=4, column=0, sticky=tk.W)
fdr_entry = ttk.Entry(filter_frame)
fdr_entry.grid(row=5, column=0, sticky=(tk.W, tk.E), pady=5)

ttk.Button(filter_frame, text="Run Filtering", command=run_filtering).grid(row=6, column=0, columnspan=2, pady=10)

# Quantification frame
quant_frame = ttk.LabelFrame(mainframe, text="Quantification", padding="10")
quant_frame.grid(row=1, column=2, sticky=(tk.N, tk.W, tk.E, tk.S), padx=5, pady=5)
quant_frame.columnconfigure(0, weight=1)

ttk.Label(quant_frame, text="Select Quantification Mode:").grid(row=0, column=0, sticky=tk.W)
quant_mode_var = tk.StringVar()
quant_mode_combo = ttk.Combobox(quant_frame, textvariable=quant_mode_var, values=["PeakViewInput", "OpenSwath", "Skyline"], state="readonly")
quant_mode_combo.grid(row=1, column=0, sticky=(tk.W, tk.E), pady=5)
quant_mode_combo.current(0)

ttk.Label(quant_frame, text="Select Library File:").grid(row=2, column=0, sticky=tk.W)
quant_library_entry = ttk.Entry(quant_frame)
quant_library_entry.grid(row=3, column=0, sticky=(tk.W, tk.E), pady=5)
ttk.Button(quant_frame, text="Browse", command=lambda: browse_file(quant_library_entry)).grid(row=3, column=1, padx=5)

ttk.Label(quant_frame, text="Select MSPLIT Search Result File:").grid(row=4, column=0, sticky=tk.W)
quant_search_entry = ttk.Entry(quant_frame)
quant_search_entry.grid(row=5, column=0, sticky=(tk.W, tk.E), pady=5)
ttk.Button(quant_frame, text="Browse", command=lambda: browse_file(quant_search_entry)).grid(row=5, column=1, padx=5)

ttk.Label(quant_frame, text="Select FASTA File:").grid(row=6, column=0, sticky=tk.W)
quant_fasta_entry = ttk.Entry(quant_frame)
quant_fasta_entry.grid(row=7, column=0, sticky=(tk.W, tk.E), pady=5)
ttk.Button(quant_frame, text="Browse", command=lambda: browse_file(quant_fasta_entry)).grid(row=7, column=1, padx=5)

ttk.Label(quant_frame, text="Specify Output File for Quantification:").grid(row=8, column=0, sticky=tk.W)
quant_output_entry = ttk.Entry(quant_frame)
quant_output_entry.grid(row=9, column=0, sticky=(tk.W, tk.E), pady=5)
ttk.Button(quant_frame, text="Save", command=lambda: save_file(quant_output_entry)).grid(row=9, column=1, padx=5)

ttk.Button(quant_frame, text="Run Quantification", command=run_quantification).grid(row=10, column=0, columnspan=2, pady=10)

# Spectral Counting frame
spectral_frame = ttk.LabelFrame(mainframe, text="Spectral Counting", padding="10")
spectral_frame.grid(row=1, column=3, sticky=(tk.N, tk.W, tk.E, tk.S), padx=5, pady=5)
spectral_frame.columnconfigure(0, weight=1)

# Search Result File
ttk.Label(spectral_frame, text="Select MSPLIT Search Result File:").grid(row=0, column=0, sticky=tk.W)
spectral_search_entry = ttk.Entry(spectral_frame)
spectral_search_entry.grid(row=1, column=0, sticky=(tk.W, tk.E), pady=5)
ttk.Button(spectral_frame, text="Browse", command=lambda: browse_file(spectral_search_entry)).grid(row=1, column=1, padx=5)

# FASTA File
ttk.Label(spectral_frame, text="Select FASTA File:").grid(row=2, column=0, sticky=tk.W)
spectral_fasta_entry = ttk.Entry(spectral_frame)
spectral_fasta_entry.grid(row=3, column=0, sticky=(tk.W, tk.E), pady=5)
ttk.Button(spectral_frame, text="Browse", command=lambda: browse_file(spectral_fasta_entry)).grid(row=3, column=1, padx=5)

# Experiment Name
ttk.Label(spectral_frame, text="Experiment Name:").grid(row=4, column=0, sticky=tk.W)
experiment_entry = ttk.Entry(spectral_frame)
experiment_entry.grid(row=5, column=0, sticky=(tk.W, tk.E), pady=5)

# Bait Name
ttk.Label(spectral_frame, text="Bait Name:").grid(row=6, column=0, sticky=tk.W)
bait_entry = ttk.Entry(spectral_frame)
bait_entry.grid(row=7, column=0, sticky=(tk.W, tk.E), pady=5)

# Output File for Spectral Counting
ttk.Label(spectral_frame, text="Specify Output File:").grid(row=8, column=0, sticky=tk.W)
spectral_output_entry = ttk.Entry(spectral_frame)
spectral_output_entry.grid(row=9, column=0, sticky=(tk.W, tk.E), pady=5)
ttk.Button(spectral_frame, text="Save", command=lambda: save_file(spectral_output_entry)).grid(row=9, column=1, padx=5)

# Run Spectral Counting Button
ttk.Button(spectral_frame, text="Run Spectral Counting", command=run_spectral_counting).grid(row=10, column=0, columnspan=2, pady=10)


# Output display frame
output_frame = ttk.Frame(mainframe, padding="5")
output_frame.grid(row=2, column=0, columnspan=3, sticky=(tk.W, tk.E, tk.N, tk.S))
output_frame.columnconfigure(0, weight=1)
output_frame.rowconfigure(0, weight=1)

output_text = scrolledtext.ScrolledText(output_frame, wrap=tk.WORD, height=10)
output_text.grid(row=0, column=0, sticky=(tk.W, tk.E, tk.N, tk.S))

mainframe.columnconfigure(0, weight=1)
mainframe.columnconfigure(1, weight=1)
mainframe.columnconfigure(2, weight=1)
mainframe.rowconfigure(2, weight=1)

root.mainloop()
