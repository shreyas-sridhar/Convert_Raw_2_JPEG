import os
import rawpy
import imageio
import multiprocessing
#Set the input and output directories
input_directory = 'E:\\Shaurya Graduation\\Raw pics'
output_directory = 'E:\\Shaurya Graduation\\new_jpg'
#Make sure the output directory exists
if not os.path.exists(output_directory):
    os.makedirs(output_directory)
#function to process a single raw image
def process_raw(input_file):
    output_file = os.path.join(output_directory, os.path.splitext(os.path.basename(input_file))[0] + '.jpg')
    with rawpy.imread(input_file) as raw:
        rgb = raw.postprocess()
        imageio.imsave(output_file, rgb, format='jpeg')
if __name__ == '__main__':
    #Get a list of raw files in the input directory
    raw_files = [os.path.join(input_directory, filename) for filename in os.listdir(input_directory) if filename.lower().startswith('dsc')]
    #Gets the logical cores of the cpu
    num_processes = multiprocessing.cpu_count()
    #Creates a pool and distribute the work to the processes
    with multiprocessing.Pool(processes=num_processes) as pool:
        pool.map(process_raw, raw_files)
    print(f'Processing completed. Compressed images saved in {output_directory}')