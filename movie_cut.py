import csv
import os 
import sys
import tkinter
import tkinter.ttk as ttk
from pathlib import Path
import chardet
from chardet.universaldetector import UniversalDetector

from moviepy.editor import VideoFileClip
from moviepy.audio.fx.audio_fadein import audio_fadein
from moviepy.audio.fx.audio_fadeout import audio_fadeout
from moviepy.audio.fx.audio_left_right import audio_left_right
from moviepy.audio.fx.audio_loop import audio_loop
from moviepy.audio.fx.audio_normalize import audio_normalize
from moviepy.audio.fx.volumex import volumex

from moviepy.video.fx.accel_decel import accel_decel
from moviepy.video.fx.blackwhite import blackwhite
from moviepy.video.fx.blink import blink
from moviepy.video.fx.colorx import colorx
from moviepy.video.fx.crop import crop
from moviepy.video.fx.even_size import even_size
from moviepy.video.fx.fadein import fadein
from moviepy.video.fx.fadeout import fadeout
from moviepy.video.fx.freeze import freeze
from moviepy.video.fx.freeze_region import freeze_region
from moviepy.video.fx.gamma_corr import gamma_corr
from moviepy.video.fx.headblur import headblur
from moviepy.video.fx.invert_colors import invert_colors
from moviepy.video.fx.loop import loop
from moviepy.video.fx.lum_contrast import lum_contrast
from moviepy.video.fx.make_loopable import make_loopable
from moviepy.video.fx.margin import margin
from moviepy.video.fx.mask_and import mask_and
from moviepy.video.fx.mask_color import mask_color
from moviepy.video.fx.mask_or import mask_or
from moviepy.video.fx.mirror_x import mirror_x
from moviepy.video.fx.mirror_y import mirror_y
from moviepy.video.fx.painting import painting
from moviepy.video.fx.resize import resize
from moviepy.video.fx.rotate import rotate
from moviepy.video.fx.scroll import scroll
from moviepy.video.fx.speedx import speedx
from moviepy.video.fx.supersample import supersample
from moviepy.video.fx.time_mirror import time_mirror
from moviepy.video.fx.time_symmetrize import time_symmetrize
def get_source_path():
    if getattr(sys, 'frozen', False):
        # The application is frozen
        exe_path  = Path(sys.executable).resolve()
        main_path = exe_path.parent
        dist_path = main_path.parent
        src_path  = dist_path.parent
    else:
        # The application is not frozen
        # Change this bit to match where you store your data files:
        py_path  = Path(__file__).resolve()
        src_path = py_path.parent

    return src_path


def getFileEncoding(file_path):
    detector = UniversalDetector()
    with open(file_path, mode= "rb" ) as f:
        for binary in f:
            detector.feed( binary )
            if detector.done:
                break
    detector.close()
    return detector.result[ "encoding" ]

def movie_cut(movie_path, start, end, save_folder):
    '''

    '''

    movie_path = Path(movie_path)
    movie_name = movie_path.stem
    save_folder = Path(save_folder) 
    save_path =  save_folder /  f'{movie_name}_{start}_{end}.mp4'.replace(':', '_')
    #save_path = save_folder /'test.mp4'
    movie_path = str(movie_path)
    save_path = str(save_path)
    video = VideoFileClip(movie_path).subclip(start, end)
    video.write_videofile(save_path)

def read_csv():
    csv_path = csv_path_.get()
    encoding = getFileEncoding(csv_path)
    save_folder = save_folder_.get()

    with open(csv_path, encoding=encoding) as f:
        reader = csv.reader(f)
        for idx, row in enumerate(reader):
            if idx==0:
                continue
            movie_path = row[0].replace('"', '').replace('"', '')
            start = row[1]
            end = row[2]
            try:
                movie_cut(movie_path, start, end, save_folder)
            except:
                print(f'{movie_path} は変換できませんでした')
                pass

    print('finished')


if __name__ == '__main__':
    root = tkinter.Tk()
    root.title('movie_cutter')
    root.geometry("600x120")
    csv_path_ = tkinter.StringVar()
    csv_path_path = get_source_path() / 'csv_path.txt'
    save_folder_ = tkinter.StringVar()

    if csv_path_path.exists():
        with open(get_source_path() / 'csv_path.txt', mode='r', encoding='utf-8') as f:
            list_str = [s.strip() for s in f.readlines()]
            csv_path = list_str[0]
            save_folder = list_str[1]
            csv_path_.set(s_url)
            save_folder_.set(s_folder)

    else:
        #user_path = Path(os.path.expanduser('~'))
        movie_path = get_source_path() / 'movie'
        movie_path.mkdir(parents=True, exist_ok=True)
        save_folder_.set(movie_path)
        csv_path_.set(f"{get_source_path()}/example.csv")


    csv_path_entry  = ttk.Entry(root,
                            textvariable=csv_path_,
                            width=60)

    save_folder_entry = ttk.Entry(root,
                            textvariable=save_folder_,
                            width=60)
    csv_label = ttk.Label(root, text = 'CSVパス')
    save_label = ttk.Label(root, text = '保存先フォルダ')

    csv_label.grid(row = 0, column = 0)
    csv_path_entry.grid(row = 0, column = 1)

    save_label.grid(row = 1, column = 0)
    save_folder_entry.grid(row = 1, column = 1)
    button = tkinter.Button(root, text="movie_cut", command=read_csv)
    button.grid(row = 2, column = 1)
    
    root.mainloop()