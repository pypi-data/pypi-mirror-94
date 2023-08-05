import os
import cv2    # to fix num. of threads
import numpy as np
import pytorch_lightning as pl
import torch
from torch.utils.data import Dataset, DataLoader
from .utils import parser
from .utils.utils import make_dataset_df, encode_labels, split_dataset


################################################################################################################################
# DATASET
################################################################################################################################

################################################################
# BasicDataset - Use dataframe w/ filepath, label
################################################################
class BasicDataset(Dataset):
    '''
    Parmeters
    ---------
    df : DataFrame
        List of Files ~ filepath, label column을 포함하고 있는 데이터프레임.
    filepath_co : string
        column name of filepath in df
    label_cols : string (or list)
        column name of labels in df. it will be a list if the problem type is one vs. all.
    y_dtype : dtype
        dtype of label. 특별한 상황이 아니면 default (None) 사용.
    loader : function
        file load function. (예: x = cv2.imread(filepath)) 이미 load된 데이터를 사용할 경우 None.
    transform : function
        transfrom function. resize, augment 등의 transform function.
    force_binary : boolean
        multi-class 문제 (개 or 고양이)를 one vs. all 문제(개가 있음/없음, 고양이가 있음/없음)로 강제하여 풀고 싶을 때 True.
    class_nothing : string
        multi-class를 one vs. all로 강제하여 풀 때, 아무것도 아닌 class의 이름. 예를 들어, OK, NG1, NG2에서 OK는 class_nothing일 수 있음.
        
    Returns
    -------
    Dataset
        (NOTE!) DL 라이브러리의 일반적인 Dataset과 달리 x, y가 아닌 x, y, fp를 반환. (fp: filepath ~ logging할 때 유용하게 사용됨.)
    '''
    
    def __init__(self, df, filepath_col='filepath', label_cols=['label'], y_dtype=None, loader=None, transform=None, force_binary=False, class_nothing='ok'):
        
        if not isinstance(label_cols, list):
            label_cols = [label_cols]
            
        if len(label_cols) > 1:
            self.force_binary = True
        else:
            self.force_binary = True if force_binary else False
        self.class_nothing = class_nothing
        
        #### filepath ####
        self.filepaths = np.array(df[filepath_col].tolist())
        
        #### label ####
        self.y, self.is_binary, self.classes, self.decoder = encode_labels(df[label_cols], force_binary=self.force_binary, class_nothing=self.class_nothing)
        
        # sometimes y_dtype is not int
        if y_dtype is not None:
            self.y_dtype = y_dtype 
        elif self.is_binary:
            self.y_dtype = torch.float32
        else:
            self.y_dtype = torch.int64
        self.y = torch.tensor(data=self.y, dtype=self.y_dtype)
        
        #### loader and transform ####
        self.loader = loader
        self.transform = transform
    
    def __len__(self):
        return len(self.filepaths)
    
    def __getitem__(self, idx):
        
        # index to list
        idx = idx.tolist() if torch.is_tensor(idx) else idx
        
        # get input x
        fp = self.filepaths[idx]
        x = fp
        if self.loader is not None:
            x = self.loader(x)
        if self.transform is not None:
            x = self.transform(x)
        
        # get label y
        y = self.y[idx]
        
        return x, y, fp


################################################################
# MediaFolder
################################################################
class MediaFolderDataset(BasicDataset):
    def __init__(self, data_dir, extensions='all', hrchy='label', label_cols=['label'], y_dtype=None, loader=None, transform=None, force_binary=None, class_nothing='ok'):
        
        # create dataset df
        df = make_dataset_df(data_dir, hrchy=hrchy, extensions=extensions)
        
        # init super
        super().__init__(df, label_cols=label_cols, y_dtype=y_dtype, loader=loader, transform=transform, force_binary=force_binary, class_nothing=class_nothing)


################################################################################################################################
# DATA MODULES
################################################################################################################################

################################################################
# BasicDataModule
################################################################
class BasicDataLoader(pl.LightningDataModule):
    '''
    가장 기본적인 기능만을 포함한 DataModule
    
    Parameters
    ----------
    trainset : DataSet
        train dataset, trainset은 학습 시 train, validation set으로 자동 split됨
    testset : Dataset
        testset, 학습이 완전히 종료되었을 때 1회만 실행되는 evaluation set
    val_ratio : float
        trainset을 train, validation set으로 자동 split할 때 validation set의 비율
    batch_size : int
        batch size
        
    Returns
    -------
    (void)        
    '''
    
    def __init__(self, trainset, testset, val_ratio=0.2, batch_size=8, shuffle=False, num_workers=0, pin_memory=False):
        super().__init__()
        
        self.trainset = trainset
        self.testset = testset
        self.val_ratio = val_ratio
        self.batch_size = batch_size
        self.shuffle = shuffle
        self.num_workers = num_workers
        self.pin_memory = pin_memory
        
    def setup(self, stage=None):
        self.train_trainset, self.train_valset = split_dataset(self.trainset, self.val_ratio)
        
        # fix cv2's no. of threads
        cv2.setNumThreads(0)
            
    def train_dataloader(self):
        return DataLoader(self.train_trainset, batch_size=self.batch_size, shuffle=self.shuffle, num_workers=self.num_workers, pin_memory=self.pin_memory)
    
    def val_dataloader(self):
        return DataLoader(self.train_valset, batch_size=self.batch_size, shuffle=False, num_workers=self.num_workers, pin_memory=self.pin_memory)
    
    def test_dataloader(self):
        return DataLoader(self.testset, batch_size=self.batch_size, shuffle=False, num_workers=self.num_workers, pin_memory=self.pin_memory)
    
    
################################################################
# ImageFolderDataLoader
################################################################    
class MediaFolderDataLoader(pl.LightningDataModule):
    '''
    (All-in-One) Media (Image, Audio) Folder로부터 DataLoader 생성, 인스턴스는 train_dataloader, val_dataloader, test_dataloader를 포함
    
    Parameters
    ----------
    data_dir : dataset directory
    extensions : string or list
        dataset directory를 scan할 때 포함할 확장자 - 'all'은 Image, Audio 확장자 전부, 'Image'는 Image, 'Audio'는 Audio, 혹은 확장자의 리스트 입력 가능.
    loader : function
        filepath로부터 data를 읽어오는 함수. cv2.imread() 등.
    transform : function or dict of functions
        data를 model input으로 변환하는 함수. {'train': train_transform, 'test': test_transform}으로 입력하면 train, test 서로 다른 transform 사용 가능.
    criterion : string
        dataloader가 criterion을 받는 이유는 multi-class (1 column)와 one vs. all(n columns)의 label 차원이 다르기 때문.
    val_ratio : float
        trainset을 train, validation set으로 자동 split할 때 validation set의 비율.
    batch_size : int
        batch size
        
    Returns
    -------
    (void)        
    '''
    
    def __init__(self, data_dir, extensions='all', loader=None, transform=None, criterion=None, val_ratio=0.2, batch_size=8, shuffle=False, num_workers=0, pin_memory=False):
        super().__init__()
        
        # data directory
        self.data_dir = data_dir
        self.train_dir = os.path.join(data_dir, 'train')
        self.test_dir = os.path.join(data_dir, 'test')
        if not os.path.exists(self.train_dir) and not os.path.exists(self.test_dir):
            if 'train' in self.train_dir.rsplit('/', 1)[-1]:
                raise ValueError(f"Enter dataset root directory not '<root>/train'. May be '{self.data_dir.rsplit('/', 1)[0]}'?")
            elif 'test' in self.train_dir.rsplit('/', 1)[-1]:
                raise ValueError(f"Enter dataset root directory not '<root>/test'. May be '{self.data_dir.rsplit('/', 1)[0]}'?")
            else:
                print("Directory '{data_dir}' does not have subdirs name 'train' and 'test'. Assume train dataset only, test dataset will be empty.")
                self.train_dir, self.test_dir = self.data_dir, None
        
        # set attributes
        self.extensions = extensions
        self.loader = loader
        if isinstance(transform, dict):
            self.train_transform = transform['train']
            # if transform for validation is defined
            val_key = [k for k in transform.keys() if k.lower() in ['val', 'validation']]
            self.val_transform = None if len(val_key) == 0 else transform[val_key[0]]                
            self.test_transform = transform['test']
        else:
            self.train_transform = self.val_transform = self.test_transform = transform
        self.val_ratio = val_ratio
        self.batch_size = batch_size
        self.shuffle = shuffle
        self.num_workers = num_workers
        self.pin_memory = pin_memory
        
        # create train, test dataset 
        self.trainset = MediaFolderDataset(self.train_dir, loader=self.loader, transform=self.train_transform, force_binary=False)
        if self.test_dir is not None:
            self.testset = MediaFolderDataset(self.test_dir, loader=self.loader, transform=self.test_transform, force_binary=False)
        else:
            self.testset = None
            
        # criterion이 binary type이면 force_binary=True로 하여 multi-class를 multi-label로 강제 - (주의!) multi-label to multi-class (역방향)은 불가능!
        self.is_binary = self.trainset.is_binary
        if not self.is_binary and parser.is_binary(criterion):
            self.trainset = MediaFolderDataset(self.train_dir, loader=self.loader, transform=self.train_transform, force_binary=True)
            if self.test_dir is not None:
                self.testset = MediaFolderDataset(self.test_dir, loader=self.loader, transform=self.test_transform, force_binary=True)
            self.is_binary = self.trainset.is_binary
        elif parser.is_binary(criterion) != self.is_binary:
            raise ValueError(f"Your criterion does not fit the data. Try 'BCEWithLogitsLoss' or something.")
        
        # (IMPORTANT) We must pass the no. of classes to the model
        self.num_classes = len(self.trainset.classes)
        
    def setup(self, stage=None):
        # split train and validation from trainset
        self.trainset, self.valset = split_dataset(self.trainset, self.val_ratio)
        if self.val_transform is not None:
            self.valset.transform = self.val_transform
        self.testset = self.testset
        
        # fix cv2's no. of threads
        cv2.setNumThreads(0)
            
    def train_dataloader(self):
        return DataLoader(self.trainset, batch_size=self.batch_size, shuffle=self.shuffle, num_workers=self.num_workers, pin_memory=self.pin_memory)
    
    def val_dataloader(self):
        return DataLoader(self.valset, batch_size=self.batch_size, shuffle=False, num_workers=self.num_workers, pin_memory=self.pin_memory)
    
    def test_dataloader(self):
        if self.testset is None:
            return None
        return DataLoader(self.testset, batch_size=self.batch_size, shuffle=False, num_workers=self.num_workers, pin_memory=self.pin_memory)
    
    def info(self):
        if self.num_classes == 1:
            msg = f"Binary Problem w/ class"
        elif not self.is_binary:
            msg = f"Multi-class Problem w/ {self.num_classes} classes"
        else:
            msg = f"Multi-label Problem w/ {self.num_classes} classes"
        n_train = len(self.trainset) if not hasattr(self, 'valset') else len(self.trainset) + len(self.valset)
        n_test = 0 if not hasattr(self, 'testset') else len(self.testset)
        
        print(f"Check Your Data:")
        print(f"  - {msg} {', '.join(self.trainset.classes)} - coded {self.trainset.decoder}.")
        print(f"  - Trainset: {n_train} files in '{self.train_dir}'.")
        print(f"  - Testset: {n_test} files in '{self.test_dir}'.")
