import os
import rawpy
import imageio
import multiprocessing
import tkinter as tk
from tkinter import filedialog, messagebox
import time
import sys
from multiprocessing import Manager

def get_new_filename(counter, output_directory):
    # Increment the counter using the Manager dictionary
    counter['value'] += 1
    current_number = counter['value']
    
    # Create the new filename
    return os.path.join(output_directory, f'jpeg{current_number}.jpg')

def process_raw(input_file, output_directory, counter):
    try:
        # Get new filename using the counter
        output_file = get_new_filename(counter, output_directory)
        
        print(f"Processing {input_file}")
        with rawpy.imread(input_file) as raw:
            rgb = raw.postprocess()
            imageio.imsave(output_file, rgb, format='jpeg')
        print(f"Completed {input_file} -> {os.path.basename(output_file)}")
        return True
        
    except Exception as e:
        print(f"Error processing {input_file}: {str(e)}")
        return False

def process_images(input_directory, output_directory):
    # Get list of RAW files
    raw_files = [
        os.path.join(input_directory, filename)
        for filename in os.listdir(input_directory)
        if filename.lower().endswith(('.nef', '.cr2', '.arw', '.raw'))  # Common RAW formats
    ]
    
    if not raw_files:
        raise Exception("No RAW files found")
    
    print(f"Found {len(raw_files)} RAW files to process")
    
    # Create a manager and shared counter dictionary
    with Manager() as manager:
        counter = manager.dict()
        counter['value'] = 0
        
        # Create a pool and process files
        num_processes = max(1, multiprocessing.cpu_count() - 1)  # Leave one core free
        completed = 0
        
        with multiprocessing.Pool(processes=num_processes) as pool:
            results = []
            last_activity = time.time()
            
            # Submit all tasks
            for file in raw_files:
                results.append(pool.apply_async(process_raw, (file, output_directory, counter)))
            
            # Monitor results
            while results:
                for i in range(len(results) - 1, -1, -1):
                    if results[i].ready():
                        if results[i].get():  # If processing was successful
                            completed += 1
                        results.pop(i)
                        last_activity = time.time()
                        print(f"Progress: {completed}/{len(raw_files)} files processed")
                
                # Check for timeout
                if time.time() - last_activity > 10:  # 10 second timeout
                    print("\nTimeout reached - no activity for 10 seconds")
                    pool.terminate()
                    return False
                
                time.sleep(0.5)  # Prevent CPU overuse
        
        return completed > 0

def main():
    # Initialize Tkinter
    root = tk.Tk()
    root.withdraw()

    try:
        # Select input directory
        messagebox.showinfo("Select Input Directory", "Please select the directory containing RAW images.")
        input_directory = filedialog.askdirectory(title="Select Input Directory")
        if not input_directory:
            messagebox.showerror("Error", "No input directory selected.")
            return

        # Select output directory
        messagebox.showinfo("Select Output Directory", "Please select the directory to save JPEG images.")
        output_directory = filedialog.askdirectory(title="Select Output Directory")
        if not output_directory:
            messagebox.showerror("Error", "No output directory selected.")
            return

        # Create output directory if it doesn't exist
        os.makedirs(output_directory, exist_ok=True)

        print("Starting conversion process...")
        success = process_images(input_directory, output_directory)
        
        if success:
            messagebox.showinfo("Success", f"Processing completed. Images saved in {output_directory}")
        else:
            messagebox.showwarning("Warning", "Processing completed but no images were converted successfully")

    except Exception as e:
        messagebox.showerror("Error", f"An error occurred: {str(e)}")
    finally:
        root.destroy()
        sys.exit(0)

if __name__ == '__main__':
    multiprocessing.freeze_support()
    main()
