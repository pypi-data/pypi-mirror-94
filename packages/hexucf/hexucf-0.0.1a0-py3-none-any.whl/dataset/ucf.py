import urllib.request
import os
import sys
import patoolib
import ssl
import pandas as pd
import numpy as np
import cv2
import math
import shutil
from PIL import Image

ssl._create_default_https_context = ssl._create_unverified_context


def __reporthook(block_num, block_size, total_size):
    read_so_far = block_num * block_size
    if total_size > 0:
        percent = read_so_far * 1e2 / total_size
        s = "\r%5.1f%% %*d / %d" % (
            percent, len(str(total_size)), read_so_far, total_size)
        sys.stderr.write(s)
        if read_so_far >= total_size:  # near the end
            sys.stderr.write("\n")
    else:  # total size is unknown
        sys.stderr.write("read %d\n" % (read_so_far,))


def __download_ucf101(data_dir_path):
    ucf_rar = data_dir_path + '/UCF101.rar'

    URL_LINK = 'https://crcv.ucf.edu/data/UCF101/UCF101.rar'

    if not os.path.exists(data_dir_path):
        os.makedirs(data_dir_path)

    if not os.path.exists(ucf_rar):
        print('ucf file does not exist, downloading from Internet')
        urllib.request.urlretrieve(url=URL_LINK, filename=ucf_rar,
                                   reporthook=__reporthook)

    print('unzipping ucf file')
    patoolib.extract_archive(ucf_rar, outdir=data_dir_path)


def __scan_ucf101(data_dir_path, limit):
    input_data_dir_path = data_dir_path + '/UCF-101'

    result = dict()

    dir_count = 0
    for f in os.listdir(input_data_dir_path):
        __help_scan_ucf101(input_data_dir_path, f, dir_count, result)
        if dir_count == limit:
            break
    return result


def __help_scan_ucf101(input_data_dir_path, f, dir_count, result):
    file_path = input_data_dir_path + os.path.sep + f
    if not os.path.isfile(file_path):
        dir_count += 1
        for ff in os.listdir(file_path):
            video_file_path = file_path + os.path.sep + ff
            result[video_file_path] = f


def __scan_ucf101_with_labels(data_dir_path, labels):
    input_data_dir_path = data_dir_path + '/UCF-101'

    result = dict()

    dir_count = 0
    for label in labels:
        __help_scan_ucf101(input_data_dir_path, label, dir_count, result)
    return result


def __download_ucf50(data_dir_path):
    ucf_rar = data_dir_path + '/UCF50.rar'

    URL_LINK = 'https://www.crcv.ucf.edu/data/UCF50.rar'

    if not os.path.exists(data_dir_path):
        os.makedirs(data_dir_path)

    if not os.path.exists(ucf_rar):
        print('ucf file does not exist, downloading from Internet')
        urllib.request.urlretrieve(url=URL_LINK, filename=ucf_rar,
                                   reporthook=__reporthook)

    print('unzipping ucf file')
    patoolib.extract_archive(ucf_rar, outdir=data_dir_path)


def __scan_ucf50(data_dir_path, limit):
    input_data_dir_path = data_dir_path + '/UCF-50'

    result = dict()

    dir_count = 0
    for f in os.listdir(input_data_dir_path):
        __help_scan_ucf50(input_data_dir_path, f, dir_count, result)
        if dir_count == limit:
            break
    return result


def __help_scan_ucf50(input_data_dir_path, f, dir_count, result):
    file_path = input_data_dir_path + os.path.sep + f
    if not os.path.isfile(file_path):
        dir_count += 1
        for ff in os.listdir(file_path):
            video_file_path = file_path + os.path.sep + ff
            result[video_file_path] = f


def __scan_ucf50_with_labels(data_dir_path, labels):
    input_data_dir_path = data_dir_path + '/UCF-50'

    result = dict()

    dir_count = 0
    for label in labels:
        __help_scan_ucf50(input_data_dir_path, label, dir_count, result)
    return result


def __video_capturing_function(video_directory, dataset, folder_name):
    for i in np.arange(len(dataset)):
        video_name = dataset.video_name[i]
        video_read_path = os.path.join(video_name)
        cap = cv2.VideoCapture(video_read_path)
        train_write_file = None
        try:
            train_write_file = video_directory + os.path.sep + folder_name + os.path.sep + \
                               os.path.basename(video_name.split(".")[0])
            os.mkdir(train_write_file)

            cap.set(cv2.CAP_PROP_FPS, 20)
            frameRate = cap.get(5)
            x = 1
            count = 0
            while cap.isOpened():
                frameId = cap.get(1)  # current frame number
                ret, frame = cap.read()
                if not ret:
                    break
                if frameId % math.floor(frameRate) == 0:
                    filename = "frame%d.jpg" % count
                    count += 1
                    frame_grey = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
                    cv2.imwrite(os.path.join(train_write_file, filename), frame_grey)
            cap.release()

        except:
            print("File Already Created")

    return print("All frames written in the: " + folder_name + " Folder")


def __frame_generating_function(dataset, dir_path):
    for i in np.arange(len(dataset.video_name)):
        vid_name = dataset.video_name[i]
        vid_path = os.path.join(dir_path, os.path.basename(vid_name.split(".")[0]))
        len_frame = len(os.listdir(vid_path))
        j = 10 - len(os.listdir(vid_path))
        if j > 0:
            c = 0
            for k in np.arange(j):
                list_frames = os.listdir(vid_path)
                frame = os.path.join(vid_path, list_frames[c])
                count = k + len_frame
                new_frame = "frame%d.jpg" % count
                shutil.copy2(frame, os.path.join(vid_path, new_frame))
                c += 1
        else:
            pass
    return print("Frame Generation Done!")


def __data_load_function_10frames(dataset, directory):
    frames = []
    for i in np.arange(len(dataset)):
        vid_name = dataset.video_name[i]
        vid_dir_path = os.path.join(directory, os.path.basename(vid_name.split(".")[0]))
        frames_to_select = []
        for l in np.arange(0, 10):
            frames_to_select.append('frame%d.jpg' % l)
        vid_data = []
        for frame in frames_to_select:
            img = Image.open(os.path.join(vid_dir_path, frame))
            img = img.resize((50, 50), Image.ANTIALIAS)
            data = np.asarray(img)
            norma_data = data / 255
            vid_data.append(norma_data)
        vid_data = np.array(vid_data)
        frames.append(vid_data)
    return np.array(frames)


def load_ucf101(data_dir_path):
    UFC101_data_dir_path = data_dir_path + "/UCF-101"
    if not os.path.exists(UFC101_data_dir_path):
        __download_ucf101(data_dir_path)

    videos = []
    labels = []
    name_class_labels = dict()

    dir_count = 0
    for f in os.listdir(UFC101_data_dir_path):
        file_path = UFC101_data_dir_path + os.path.sep + f
        print(file_path)
        if not os.path.isfile(file_path):
            dir_count += 1
            for video in os.listdir(file_path):
                videos.append(file_path + os.path.sep + video)
                labels.append(dir_count - 1)
                name_class_labels[dir_count - 1] = f

    videos = pd.DataFrame(videos, labels).reset_index()
    videos.columns = ["labels", "video_name"]
    videos.groupby('labels').count()

    train_set = pd.DataFrame()
    test_set = pd.DataFrame()
    for i in set(labels):
        vs = videos.loc[videos["labels"] == i]
        vs_range = np.arange(len(vs))
        np.random.seed(12345)
        np.random.shuffle(vs_range)

        vs = vs.iloc[vs_range]
        last_train = len(vs) - len(vs) // 3
        train_vs = vs.iloc[:last_train]
        train_set = train_set.append(train_vs)
        test_vs = vs.iloc[last_train:]
        test_set = test_set.append(test_vs)

    train_set = train_set.reset_index().drop("index", axis=1)
    test_set = test_set.reset_index().drop("index", axis=1)

    train_videos_dir = os.path.join(UFC101_data_dir_path, "Train_Videos")
    test_videos_dir = os.path.join(UFC101_data_dir_path, "Test_Videos")
    try:
        os.mkdir(train_videos_dir)
    except FileExistsError as ae:
        print("Folder Already Created")
    try:
        os.mkdir(test_videos_dir)
    except FileExistsError as ae:
        print("Folder Already Created")

    __video_capturing_function(UFC101_data_dir_path, train_set, "Train_Videos")
    __video_capturing_function(UFC101_data_dir_path, test_set, "Test_Videos")

    train_dir_path = UFC101_data_dir_path + os.path.sep + 'Train_Videos'
    test_dir_path = UFC101_data_dir_path + os.path.sep + 'Test_Videos'

    train_frames = []
    for i in np.arange(len(train_set.video_name)):
        vid_file_name = os.path.basename(train_set.video_name[i]).split(".")[0]
        train_frames.append(len(os.listdir(os.path.join(train_dir_path, vid_file_name))))

    test_frames = []
    for i in np.arange(len(test_set.video_name)):
        vid_file_name = os.path.basename(test_set.video_name[i]).split('.')[0]
        test_frames.append(len(os.listdir(os.path.join(test_dir_path, vid_file_name))))

    __frame_generating_function(train_set, train_dir_path)
    __frame_generating_function(test_set, test_dir_path)

    train_vid_dat = pd.DataFrame()
    validation_vid_dat = pd.DataFrame()
    for label in set(labels):
        label_dat = train_set.loc[train_set["labels"] == label]
        train_len_label = math.floor(len(label_dat) * 0.80)

        train_dat_label = label_dat.iloc[:train_len_label]
        validation_dat_label = label_dat.iloc[train_len_label:]

        train_vid_dat = train_vid_dat.append(train_dat_label, ignore_index=True)
        validation_vid_dat = validation_vid_dat.append(validation_dat_label, ignore_index=True)

    train_dataset = __data_load_function_10frames(train_vid_dat, train_dir_path)
    test_dataset = __data_load_function_10frames(test_set, test_dir_path)
    validation_dataset = __data_load_function_10frames(validation_vid_dat, train_dir_path)

    train_labels = np.array(train_vid_dat.labels)
    test_labels = np.array(test_set.labels)
    validation_labels = np.array(validation_vid_dat.labels)

    return (train_dataset, train_labels), (test_dataset, test_labels), (validation_dataset, validation_labels)


def load_ucf50(data_dir_path):
    UFC50_data_dir_path = data_dir_path + "/UCF-50"
    if not os.path.exists(UFC50_data_dir_path):
        __download_ucf50(data_dir_path)

    videos = []
    labels = []
    name_class_labels = dict()

    dir_count = 0
    for f in os.listdir(UFC50_data_dir_path):
        file_path = UFC50_data_dir_path + os.path.sep + f
        print(file_path)
        if not os.path.isfile(file_path):
            dir_count += 1
            for video in os.listdir(file_path):
                videos.append(file_path + os.path.sep + video)
                labels.append(dir_count - 1)
                name_class_labels[dir_count - 1] = f

    videos = pd.DataFrame(videos, labels).reset_index()
    videos.columns = ["labels", "video_name"]
    videos.groupby('labels').count()

    train_set = pd.DataFrame()
    test_set = pd.DataFrame()
    for i in set(labels):
        vs = videos.loc[videos["labels"] == i]
        vs_range = np.arange(len(vs))
        np.random.seed(12345)
        np.random.shuffle(vs_range)

        vs = vs.iloc[vs_range]
        last_train = len(vs) - len(vs) // 3
        train_vs = vs.iloc[:last_train]
        train_set = train_set.append(train_vs)
        test_vs = vs.iloc[last_train:]
        test_set = test_set.append(test_vs)

    train_set = train_set.reset_index().drop("index", axis=1)
    test_set = test_set.reset_index().drop("index", axis=1)

    train_videos_dir = os.path.join(UFC50_data_dir_path, "Train_Videos")
    test_videos_dir = os.path.join(UFC50_data_dir_path, "Test_Videos")
    try:
        os.mkdir(train_videos_dir)
    except FileExistsError as ae:
        print("Folder Already Created")
    try:
        os.mkdir(test_videos_dir)
    except FileExistsError as ae:
        print("Folder Already Created")

    __video_capturing_function(UFC50_data_dir_path, train_set, "Train_Videos")
    __video_capturing_function(UFC50_data_dir_path, test_set, "Test_Videos")

    train_dir_path = UFC50_data_dir_path + os.path.sep + 'Train_Videos'
    test_dir_path = UFC50_data_dir_path + os.path.sep + 'Test_Videos'

    train_frames = []
    for i in np.arange(len(train_set.video_name)):
        vid_file_name = os.path.basename(train_set.video_name[i]).split(".")[0]
        train_frames.append(len(os.listdir(os.path.join(train_dir_path, vid_file_name))))

    test_frames = []
    for i in np.arange(len(test_set.video_name)):
        vid_file_name = os.path.basename(test_set.video_name[i]).split('.')[0]
        test_frames.append(len(os.listdir(os.path.join(test_dir_path, vid_file_name))))

    __frame_generating_function(train_set, train_dir_path)
    __frame_generating_function(test_set, test_dir_path)

    train_vid_dat = pd.DataFrame()
    validation_vid_dat = pd.DataFrame()
    for label in set(labels):
        label_dat = train_set.loc[train_set["labels"] == label]
        train_len_label = math.floor(len(label_dat) * 0.80)

        train_dat_label = label_dat.iloc[:train_len_label]
        validation_dat_label = label_dat.iloc[train_len_label:]

        train_vid_dat = train_vid_dat.append(train_dat_label, ignore_index=True)
        validation_vid_dat = validation_vid_dat.append(validation_dat_label, ignore_index=True)

    train_dataset = __data_load_function_10frames(train_vid_dat, train_dir_path)
    test_dataset = __data_load_function_10frames(test_set, test_dir_path)
    validation_dataset = __data_load_function_10frames(validation_vid_dat, train_dir_path)

    train_labels = np.array(train_vid_dat.labels)
    test_labels = np.array(test_set.labels)
    validation_labels = np.array(validation_vid_dat.labels)

    return (train_dataset, train_labels), (test_dataset, test_labels), (validation_dataset, validation_labels)

