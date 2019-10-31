"""
!/usr/bin/env python
-*- coding:utf-8 -*-
Author: eric.lai
Created on 2019/10/29 10:08
"""
import os
import numpy as np
import preprocess_data.audio_ops as ops

speech = 'F:/data_split/event/speech/'
mechanic_noise = 'F:/data_split/event/mechanic_noise/'
noise = 'F:/data_split/event/noise/'
DIR = [speech, mechanic_noise, noise]

train = 'F:/data_split/scene/train/'
metro_station = 'F:/data_split/scene/metro_station/'
coffee_shop = 'F:/data_split/scene/coffee_shop/'
road = 'F:/data_split/scene/road/'
mall = 'F:/data_split/scene/mall/'
office = 'F:/data_split/scene/office/'
DIR2 = [train, metro_station, coffee_shop, road, mall, office]

def search_file(root_dir, data_type, file_head):
    for root, dirs, files in os.walk(root_dir):
        for file in files:
            if os.path.splitext(file)[-1].lower() == data_type and file_head in file.split('_'):
                file_name = root_dir + file
    return file_name


def split_audio(in_audio, in_txt):
    in_audio_str = in_audio.split('\\')
    save_head = in_audio_str[-1]
    save_head = save_head.split(".")[0]
    nchannels, framerate, wave_data = ops.read_audio(in_audio)
    txt_data = read_txt(in_txt)
    # print(len(out_dir))
    print("start split")
    for i in range(txt_data.shape[0]):
        start = int(float(txt_data[i][0])*framerate)
        end = int(float(txt_data[i][2])*framerate+start)
        data_temp = wave_data[start:end]
        split_file = DIR[int(txt_data[i][1])-1]+save_head+"_"+str(i)
        ops.save_wave_file(data_temp, split_file)
        print("split file name :", split_file, len(data_temp))
        print("split file",i)
    print("split end")

def read_txt(txt_file):
    f = open(txt_file,'r')
    lines = f.readlines()
    txt_data = []
    for line in lines:
        line = line.strip('\n')
        line = line.split("\t")
        txt_data.append(line)
    txt_data = np.array(txt_data)
    # print(txt_data)
    return txt_data

def main_function(in_dir):
    for root, dirs, files in os.walk(in_dir):
        for file in files:
            video_path = os.path.join(root, file)
            if 'wav' in video_path.split('.'):
                try:
                    wav_file = video_path
                    file_head = wav_file.split('\\')[0] + '/' + wav_file.split('\\')[1] + '/'
                    txt_event_file = search_file(file_head, '.txt', 'event')
                    txt_scene_file = search_file(file_head, '.txt', 'scene')
                    split_audio(wav_file, txt_event_file)
                    # split_audio(wav_file, txt_scene_file)
                except:
                    pass

if __name__ == '__main__':
    in_dir = 'F:/已标注/'
    main_function(in_dir)