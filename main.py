import os
import filecmp
import tkinter as tk
from tkinter import filedialog, messagebox

def count_sloc(file_path):
    with open(file_path, 'r', encoding='utf-8') as file:
        lines = file.readlines()
        sloc = 0
        for line in lines:
            # Remove leading/trailing whitespace and newline characters
            line = line.strip()

            # Skip empty lines and comment lines
            if not line or line.startswith('#'):
                continue

            # If the line contains a multi-line string, skip it
            if '"""' in line or "'''" in line:
                continue

            sloc += 1

        return sloc

def calculate_sloc_for_file(file_path):
    if not os.path.isfile(file_path) or not file_path.endswith('.py'):
        print(f"Error: '{file_path}' is not a valid Python file.")
        return

    sloc_count = count_sloc(file_path)
    print(f"{file_path}: {sloc_count} SLOC")

def compare_files(file_path1, file_path2):
    with open(file_path1, 'r', encoding='utf-8') as file1, open(file_path2, 'r', encoding='utf-8') as file2:
        lines1 = file1.readlines()
        lines2 = file2.readlines()

    num_lines = max(len(lines1), len(lines2))
    comparison_results = ""
    total_changes = 0  # Initialize a counter for total changes

    for i in range(num_lines):
        line1 = lines1[i].strip() if i < len(lines1) else ""
        line2 = lines2[i].strip() if i < len(lines2) else ""

        if line1 != line2:
            total_changes += 1  # Increment the counter for each difference
            comparison_results += f"Line {i + 1}:\n"
            comparison_results += f"- {line1}\n"
            comparison_results += f"+ {line2}\n"

    if comparison_results:
        comparison_results = f"Comparison of {os.path.basename(file_path1)} and {os.path.basename(file_path2)}:\n\n{comparison_results}\n"
    else:
        comparison_results = f"No differences found between {os.path.basename(file_path1)} and {os.path.basename(file_path2)}\n"

    # Append the total changes information to the result
    comparison_results += f"Total changes: {total_changes}\n"

    return comparison_results  # Return the result as a string

def compare_files_individuals(file_path1, file_path2):
    comparison_results = compare_files(file_path1, file_path2)

    # Format the comparison results with color
    comparison_results = comparison_results.replace("+ ", "\n+ ", 1).replace("- ", "\n- ", 1)
    comparison_results = comparison_results.replace("+ ", "\n+ ", 1).replace("- ", "\n- ", 1)

    output_text.config(state=tk.NORMAL)
    output_text.insert(tk.END, comparison_results)
    output_text.tag_configure("added", foreground="green")
    output_text.tag_configure("deleted", foreground="red")
    output_text.tag_add("added", "2.0", tk.END)
    output_text.tag_add("deleted", "3.0", tk.END)
    output_text.config(state=tk.DISABLED)

def extract_total_changes(comparison_results):
    try:
        total_changes = int(comparison_results.split("Total changes: ")[1].split("\n")[0])
        return total_changes
    except IndexError:
        return 0

def compare_folders(folder_path1, folder_path2):
    if not os.path.exists(folder_path1) or not os.path.exists(folder_path2):
        print("Error: Both folders must exist.")
        return

    folder_cmp = filecmp.dircmp(folder_path1, folder_path2)
    total_changes = 0  # Initialize total changes counter

    print(f"Files added in {folder_path2} compared to {folder_path1}:")
    for file_added in folder_cmp.right_only:
        total_changes += 1  # Increment total changes for added files
        print(f"+ {os.path.join(folder_path2, file_added)}")

    print(f"\nFiles deleted in {folder_path2} compared to {folder_path1}:")
    for file_deleted in folder_cmp.left_only:
        total_changes += 1  # Increment total changes for deleted files
        print(f"- {os.path.join(folder_path1, file_deleted)}")

    print("\nCommon files with differences:")
    for file_diff in folder_cmp.diff_files:
        total_changes += 1  # Increment total changes for different files
        file_path1 = os.path.join(folder_path1, file_diff)
        file_path2 = os.path.join(folder_path2, file_diff)
        file_diff_results = compare_files(file_path1, file_path2)
        total_changes += extract_total_changes(file_diff_results) - 1  # Subtract 1 for the current comparison

        print(f"* {os.path.join(folder_path1, file_diff)}")
        print(file_diff_results)

    print("\nCommon subfolders with differences:")
    for subdir in folder_cmp.subdirs.values():
        subfolder_changes = compare_folders(subdir.left, subdir.right)  # Recursively count subfolder changes
        total_changes += extract_total_changes(subfolder_changes)

        print(f"--- In {subdir.left} ---")
        print(f"+++ In {subdir.right} +++")
        print(subfolder_changes)

    comparison_results = f"Total changes: {total_changes}\n\n"
    comparison_results += f"Files added in {folder_path2} compared to {folder_path1}:\n"
    for file_added in folder_cmp.right_only:
        comparison_results += f"+ {os.path.join(folder_path2, file_added)}\n"

    comparison_results += f"\nFiles deleted in {folder_path2} compared to {folder_path1}:\n"
    for file_deleted in folder_cmp.left_only:
        comparison_results += f"- {os.path.join(folder_path1, file_deleted)}\n"

    comparison_results += "\nCommon files with differences:\n"
    for file_diff in folder_cmp.diff_files:
        comparison_results += f"* {os.path.join(folder_path1, file_diff)}\n"
        file_path1 = os.path.join(folder_path1, file_diff)
        file_path2 = os.path.join(folder_path2, file_diff)
        file_diff_results = compare_files(file_path1, file_path2)
        comparison_results += file_diff_results

    comparison_results += "\nCommon subfolders with differences:\n"
    for subdir in folder_cmp.subdirs.values():
        comparison_results += f"--- In {subdir.left} ---\n"
        comparison_results += f"+++ In {subdir.right} +++\n"
        comparison_results += compare_folders(subdir.left, subdir.right)

    return comparison_results

def browse_file():
    file_path = filedialog.askopenfilename(filetypes=[("Python Files", "*.py")])
    if file_path:
        sloc_count = count_sloc(file_path)
        messagebox.showinfo("SLOC Count", f"{os.path.basename(file_path)}\nSLOC: {sloc_count}")

def browse_folders():
    folder_path1 = filedialog.askdirectory()
    folder_path2 = filedialog.askdirectory()
    if folder_path1 and folder_path2:
        comparison_results = compare_folders(folder_path1, folder_path2)
        output_text.config(state=tk.NORMAL)
        output_text.delete("1.0", tk.END)
        output_text.insert(tk.END, comparison_results)
        output_text.config(state=tk.DISABLED)

def compare_individual_files():
    file_path1 = filedialog.askopenfilename(filetypes=[("Python Files", "*.py")])
    file_path2 = filedialog.askopenfilename(filetypes=[("Python Files", "*.py")])
    if file_path1 and file_path2:
        compare_files_individuals(file_path1, file_path2)

if __name__ == '__main__':
    # Create the Tkinter window
    root = tk.Tk()
    root.title("Python Code Analyzer")
    root.geometry("600x400")

    # Set a background color for the window
    root.configure(bg="#f0f0f0")

    # Create a header label
    header_label = tk.Label(root, text="Python Code Analyzer", font=("Arial", 18), bg="#f0f0f0")
    header_label.pack(pady=10)

    file_button = tk.Button(root, text="Browse File", font=("Arial", 12), bg="#4caf50", fg="white", command=browse_file)
    file_button.pack(pady=5, padx=10, fill=tk.BOTH)

    folder_button = tk.Button(root, text="Compare Folders", font=("Arial", 12), bg="#2196f3", fg="white",
                              command=browse_folders)
    folder_button.pack(pady=5, padx=10, fill=tk.BOTH)

    compare_files_button = tk.Button(root, text="Compare Individual Files", font=("Arial", 12), bg="#ff9800",
                                     fg="white", command=compare_individual_files)
    compare_files_button.pack(pady=5, padx=10, fill=tk.BOTH)

    # Create a Text widget to display the comparison results
    output_text = tk.Text(root, wrap=tk.WORD, font=("Arial", 12), bg="white", state=tk.DISABLED)
    output_text.pack(pady=10, padx=20, fill=tk.BOTH, expand=True)

    # Run the Tkinter main loop
    root.mainloop()