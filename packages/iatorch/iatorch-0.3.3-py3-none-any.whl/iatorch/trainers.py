import sys, socket, getpass
import torch
from pytorch_lightning import Trainer
from pytorch_lightning.loggers import MLFlowLogger
from pytorch_lightning.callbacks import ProgressBar
from pytorch_lightning.callbacks.early_stopping import EarlyStopping


################################################################################################################################
# CALLBACKS
#
################################################################################################################################

################################################################
# Progress bar - default progress bar 사용 시 print line 밀리는 것 보완 (validation progress bar off)
################################################################
class SimpleProgressBar(ProgressBar):
    '''
    pytorch-lightning의 ProgressBar 사용 시 valiation epoch마다 line break 발생하여 print 지저분해짐
    SimpleProgressBar는 validation epoch의 progress bar를 off하여 line break 문제 회피
    '''
    def init_validation_tqdm(self):
        pass
    
    def on_validation_start(self, trainer, pl_module):
        pass

    def on_validation_batch_end(self, trainer, pl_module, outputs, batch, batch_idx, dataloader_idx):
        pass

    def on_validation_end(self, trainer, pl_module):
        pass
    
    
################################################################################################################################
# TRAINER MODULES
#
################################################################################################################################

################################################################
# BasicTrainer
################################################################
class BasicTrainer(Trainer):
    '''
    BasicTrainer, pytorch_lightning trainer에 logger, progress_bar callback만 정의해서 넘기는 형태
    Main code 간결하게 하기 위해서 따로 뽑음
    '''
    
    def __init__(
        self, 
        # logger
        tracking_uri='sqlite:///mlruns.db',
        experiment_name='Default',
        run_name='noname',
        user=None,
        data_dir=None,
        # batch and epochs
        batch_size=8,
        epochs=2,
        # early stopping
        monitor='var/loss',
        early_stop=0,
        patience=3,
        # device
        cpu=False,
        half_precision=False,
        # options
        silence=False,
    ):
        # set logger
        logger = MLFlowLogger(
            experiment_name=experiment_name,
            tracking_uri=tracking_uri,
            tags={
                'mlflow.runName': run_name, 
                'mlflow.user': getpass.getuser() if user is None else user, 
                'mlflow.source.name': sys.argv[0].rsplit('/', 1)[-1], 
                'data': f"{socket.getfqdn()}:{data_dir if data_dir is not None else '<unknown>'}",
            },
        )

        # set early-stopping callback
        early_stopping = EarlyStopping(monitor=monitor, min_delta=early_stop, patience=patience)
        
        # set progress bar callback
        bar = SimpleProgressBar()

        # SET TRAINER ARGUMENTS
        gpus = torch.cuda.device_count() if not cpu else 0
        accelerator = 'ddp' if gpus > 1 else None
        precision = 16 if half_precision and gpus != 0 else 32
        train_args = {
            'gpus': gpus,
            'accelerator': accelerator,
            'precision': precision,
            'max_epochs': epochs,
            'logger': logger,
            'callbacks': [early_stopping, bar],
            'log_every_n_steps': int(128/batch_size),            # data 128개 학습마다 log
            'flush_logs_every_n_steps': int(1024/batch_size),    # data 1,024개 학습마다 write log
            'progress_bar_refresh_rate': 1 if not silence else 0
        }
        
        # init 
        super().__init__(**train_args)
        
    def info(self):
        '''
        Traniner의 Summary 출력
        '''
        _early = None
        for cb in self.callbacks:
            if isinstance(cb, EarlyStopping):
                _early = cb
        
        _mlflow = None
        if isinstance(self.logger, list):
            for cb in self.logger:
                if isinstance(cv, MLFlowLogger):
                    _mlflow = cb
        else:
            if isinstance(self.logger, MLFlowLogger):
                _mlflow = self.logger
            
        print(f"Check Your Trainer:")
        print(f"  - Max epochs is {self.max_epochs}.")
        if _early is not None:
            print(f"  - Stop early when the decrease in '{_early.monitor}' is below {_early.min_delta} for {_early.patience} times.")
        if _mlflow is not None:
            print(f"  - MlFLow logger is ready - {_mlflow._tracking_uri}:{_mlflow._experiment_name}, all metrics will be saved.")
        print(f"  - Train on {self.gpus} gpu(s) w/ {self.precision}-bit precision")
