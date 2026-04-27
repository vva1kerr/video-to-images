""" NOTES
01. Install python from https://www.python.org/
02. Run this command only once in CMD/Terminal "pip install opencv-python" (https://pypi.org/project/opencv-python/) 
03. Run the script. It will ask you for full video path and second to take screenshot repeatedly.
04. You will find a folder on desktop containing all the screenshots.


double click on video
hold option to find copy pathname
then copy & paste path name in terminal
"""


# Importing all necessary libraries
import argparse
import cv2
import os
from tqdm import tqdm

parser = argparse.ArgumentParser(
    description='Extract frames from a video at a set interval and save them as JPGs on the Desktop.',
    epilog=(
        'Examples:\n'
        '  python video_to_images.py\n'
        '  python video_to_images.py --file ~/Desktop/video.mp4 --seconds 5 --show DBZ --ep 1'
    ),
    formatter_class=argparse.RawDescriptionHelpFormatter,
)
parser.add_argument('--file',    metavar='PATH',   help='path to the video file')
parser.add_argument('--seconds', metavar='N', type=int, help='interval between screenshots in seconds')
parser.add_argument('--show',    metavar='NAME',   help='show name (used in output folder and filenames)')
parser.add_argument('--ep',      metavar='N',      help='episode number (used in output folder and filenames)')
args = parser.parse_args()

filename = args.file    or input('--> input file path: ')
sec      = args.seconds or int(input('--> input seconds: '))
show     = args.show    or input('--> input show name: ')
ep       = args.ep      or input('--> input episode number: ')

# Read the video from specified path
filename = os.path.expanduser(filename)
vid = cv2.VideoCapture(filename)
if not vid.isOpened():
    print(f'Error: could not open video file: {filename}')
    exit(1)
# Getting fps
fps = vid.get(cv2.CAP_PROP_FPS)
# Skip frames number (integer so modulo works reliably)
skip_frames = round(sec * fps)

# creating a folder on the Desktop
save_path = os.path.join(os.path.dirname(os.path.abspath(__file__)), f'Images from {show}-ep{ep}')
if not os.path.exists(save_path):
    os.makedirs(save_path)

# total frame in file
cap = cv2.VideoCapture(filename)
total_frame_length = int(cap.get(cv2.CAP_PROP_FRAME_COUNT))

past_second = -1
for current_frame in tqdm(range(total_frame_length)):

    # reading from frame
    ret, frame = vid.read()

    # if video is still left continue creating images
    if ret:
        # Skipping by second
        if current_frame % skip_frames == 0:

            total_seconds = int(current_frame / fps)
            minute = str(total_seconds // 60)
            second = str(total_seconds % 60)

            if past_second == second:
                second = second + "b"
            past_second = second

            timestr = "min" + minute + "-" + "sec" + str(second)
            name = f'{save_path}/{show}-ep{ep}-{timestr}.jpg'
            print('Creating...' + name)

            # writing the extracted images
            cv2.imwrite(name, frame)
    else:
        break

# Release all space and windows once done
vid.release()
# cv2.destroyAllWindows()
