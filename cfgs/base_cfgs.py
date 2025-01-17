from types import MethodType

import numpy as np
import random
import torch

from cfgs.path_cfgs import PATH


# noinspection PyMethodMayBeStatic,PyAttributeOutsideInit
class Cfgs(PATH):
    """
    配置类，在这个类里封装各种配置信息
    继承了封装路径信息的类
    """
    def __init__(self):
        super(Cfgs, self).__init__()

        # 设备配置

        # Set Devices
        # If use multi-gpu training, set e.g.'0, 1, 2' instead
        self.GPU = 'cuda:0'

        # Set RNG For CPU And GPUs
        self.SEED = random.randint(0, 99999999)

        # -------------------------
        # ---- Version Control ----
        # -------------------------

        # Define a specific name to start new training 为新训练定义一个新的名称
        # self.VERSION = 'Anonymous_' + str(self.SEED)
        self.VERSION = str(self.SEED)

        # Resume training 重新开始训练
        self.RESUME = False

        # Used in Resume training and testing 在重新训练和测试中使用
        self.CKPT_VERSION = self.VERSION
        self.CKPT_EPOCH = 0

        # Absolutely checkpoint path, 'CKPT_VERSION' and 'CKPT_EPOCH' will be overridden
        # 检查点的路径，CKPT_VERSION CKPT_EPOCH被重写
        self.CKPT_PATH = None

        # Print loss every step
        # 在每一步打印输出
        self.VERBOSE = True

        # ------------------------------
        # ---- Data Provider Params ----
        # ------------------------------

        # {'train', 'val', 'test'}
        # 三种模式，train, val, test
        self.RUN_MODE = 'train'

        # Set True to evaluate offline
        # 离线评估时设置为True
        self.EVAL_EVERY_EPOCH = True

        # Set True to save the prediction vector (Ensemble)
        # 保存预测向量设为true
        self.TEST_SAVE_PRED = False

        # Define the 'train' 'val' 'test' data split
        # 定义train, val, test的数据划分
        # (EVAL_EVERY_EPOCH triggered when set {'train': 'train'})
        # 设置{'train': 'train'}时，EVAL_EVERY_EPOCH被触发
        self.SPLIT = {
            'train': '',
            'val': 'val',
            'test': 'test',
            'valNovel': 'val'
        }

        # A external method to set train split
        # 设置训练划分的外部方法
        # 在proc里将SPLIT['train']设置为此值 在load_data.py的Dataset类里用到 line 23
        self.TRAIN_SPLIT = 'train+val+vg'

        # Set True to use pretrained word embedding
        # 使用预训练的词嵌入时设置为True
        # (GloVe: spaCy https://spacy.io/)
        self.USE_GLOVE = True

        # Word embedding matrix size
        # 词嵌入的输出维度
        # (token size x WORD_EMBED_SIZE)
        self.WORD_EMBED_SIZE = 300

        # Max length of question sentences
        # 问题句子的最大长度
        self.MAX_TOKEN = 14

        # Filter the answer by occurrence
        # self.ANS_FREQ = 8

        # Max length of extracted faster-rcnn 2048D features
        # faster-rcnn提取特征（2048维）的最大长度
        # (bottom-up and Top-down: https://github.com/peteanderson80/bottom-up-attention)
        self.IMG_FEAT_PAD_SIZE = 100

        # Faster-rcnn 2048D features
        # faster-rcnn提取的特征维数
        self.IMG_FEAT_SIZE = 2048

        self.IMG_SPATIAL_FEAT_SIZE = 7

        # Default training batch size: 64
        self.BATCH_SIZE = 32

        # Multi-thread I/O
        # self.NUM_WORKERS = 8
        self.NUM_WORKERS = 0

        # Use pin memory
        # (Warning: pin memory can accelerate GPU loading but may
        # increase the CPU memory usage when NUM_WORKS is large)
        self.PIN_MEM = True

        # Large model can not training with batch size 64
        # Gradient accumulate can split batch to reduce gpu memory usage
        # large模型不能以batch size为64训练，梯度累积可以划分batch，减少GPU消耗
        # (Warning: BATCH_SIZE should be divided by GRAD_ACCU_STEPS)
        self.GRAD_ACCU_STEPS = 1

        # Set 'external': use external shuffle method to implement training shuffle
        # Set 'internal': use pytorch dataloader default shuffle method
        self.SHUFFLE_MODE = 'external'

        # ------------------------
        # ---- Network Params ----
        # ------------------------
        # 网络参数

        # Model deeps
        # (Encoder and Decoder will be same deeps)
        # 模型深度，编码器和解码器有同样的深度
        self.LAYER = 6

        # Model hidden size
        # 隐层的size
        # (512 as default, bigger will be a sharp increase of gpu memory usage)
        self.HIDDEN_SIZE = 512

        # Multi-head number in MCA layers
        # Modular Co-Attention 模块化共同注意中multi-head的数量
        # (Warning: HIDDEN_SIZE should be divided by MULTI_HEAD) HIDDEN_SIZE应该被MULTI_HEAD整除
        self.MULTI_HEAD = 8

        # Dropout rate for all dropout layers
        # 所有的dropout率
        # (dropout can prevent overfitting： [Dropout: a simple way to prevent neural networks from overfitting])
        self.DROPOUT_R = 0.1

        # MLP size in flatten layers
        # 展平的线性层的size
        self.FLAT_MLP_SIZE = 512

        # Flatten the last hidden to vector with {n} attention glimpses
        self.FLAT_GLIMPSES = 1
        self.FLAT_OUT_SIZE = 1024

        self.SK_TEMP = 1.0

        # --------------------------
        # ---- Optimizer Params ----
        # --------------------------

        # The base learning rate
        # 基础学习率
        self.LR_BASE = 0.0001

        # Learning rate decay ratio
        # 学习率衰减比例
        self.LR_DECAY_R = 0.2

        # Learning rate decay at {x, y, z...} epoch
        # 在10，12个epoch执行衰减
        self.LR_DECAY_LIST = [10, 12]

        # Max training epoch
        # 最大训练轮数
        self.MAX_EPOCH = 13

        # Gradient clip
        # (default: -1 means not using)
        self.GRAD_NORM_CLIP = -1

        # Adam optimizer betas and eps
        self.OPT_BETAS = (0.9, 0.98)
        self.OPT_EPS = 1e-9

    def parse_to_dict(self, args):
        """
        将定义的属性转换成字典
        """
        args_dict = {}
        for arg in dir(args):
            if not arg.startswith('_') and not isinstance(getattr(args, arg), MethodType):
                if getattr(args, arg) is not None:
                    args_dict[arg] = getattr(args, arg)

        return args_dict

    def add_args(self, args_dict):
        """
        添加属性
        """
        for arg in args_dict:
            setattr(self, arg, args_dict[arg])

    def fix_and_add_args(self, args_dict):
        # 设置问题和答案的路径
        print('Manually fix question paths for reference sets ...')

        self.QUESTION_PATH['train'] = './datasets/vqa/train2014_scr_questions.json'
        self.ANSWER_PATH['train'] = './datasets/vqa/train2014_scr_annotations.json'

        self.QUESTION_PATH['val'] = './datasets/vqa/val2014_sc_questions.json'
        self.ANSWER_PATH['val'] = './datasets/vqa/val2014_sc_annotations.json'

        if args_dict.get('SKILL', None) is None:
            args_dict['SKILL'] = None

        if args_dict.get('CONCEPT', None) is None:
            args_dict['CONCEPT'] = None

        for arg in args_dict:
            setattr(self, arg, args_dict[arg])

    def proc(self):
        # 确保RUN_MODE为train/val/test/valNovel
        assert self.RUN_MODE in ['train', 'val', 'test', 'valNovel']

        # ------------ Devices setup 设置设备信息
        # os.environ['CUDA_VISIBLE_DEVICES'] = self.GPU
        # GPU数
        self.N_GPU = len(self.GPU.split(','))
        # 设备列表
        self.DEVICES = [_ for _ in range(self.N_GPU)]
        # 线程数为2
        torch.set_num_threads(2)

        # ------------ Seed setup
        # 设置随机种子
        # fix pytorch seed
        torch.manual_seed(self.SEED)
        if self.N_GPU < 2:
            torch.cuda.manual_seed(self.SEED)
        else:
            torch.cuda.manual_seed_all(self.SEED)
        torch.backends.cudnn.deterministic = True

        # fix numpy seed
        np.random.seed(self.SEED)

        # fix random seed
        random.seed(self.SEED)

        # 如果设置了检查点路径，则生成CKPT_VERSION
        if self.CKPT_PATH is not None:
            print('Warning: you are now using CKPT_PATH args, '
                  'CKPT_VERSION and CKPT_EPOCH will not work')
            self.CKPT_VERSION = self.CKPT_PATH.split('/')[-2] + '_' + str(random.randint(0, 99999999))

        # ------------ Split setup
        self.SPLIT['train'] = self.TRAIN_SPLIT
        # 当前模式处于验证集/没有设置train，不在每一轮后进行评估
        if 'val' in self.SPLIT['train'].split('+') or self.RUN_MODE not in ['train']:
            self.EVAL_EVERY_EPOCH = False

        # 没有设置test，不保存预测向量
        if self.RUN_MODE not in ['test']:
            self.TEST_SAVE_PRED = False

        # ------------ Gradient accumulate setup
        # 保证batch size能被梯度累积的步数整除，每一个分批次大小就是batch size除以梯度累积的步数
        assert self.BATCH_SIZE % self.GRAD_ACCU_STEPS == 0
        self.SUB_BATCH_SIZE = int(self.BATCH_SIZE / self.GRAD_ACCU_STEPS)

        # Use a small eval batch will reduce gpu memory usage
        # 使用小的评估batch
        self.EVAL_BATCH_SIZE = int(self.SUB_BATCH_SIZE / 2)

        # ------------ Networks setup
        # FeedForwardNet size in every MCA layer
        # 在每一个MCA层的前馈网络的size
        self.FF_SIZE = int(self.HIDDEN_SIZE * 4)

        # A pipe line hidden size in attention compute
        assert self.HIDDEN_SIZE % self.MULTI_HEAD == 0
        # multi-head attention中每一个head对应的维度
        self.HIDDEN_SIZE_HEAD = int(self.HIDDEN_SIZE / self.MULTI_HEAD)

    def __str__(self):
        for attr in dir(self):
            if not attr.startswith('__') and not isinstance(getattr(self, attr), MethodType):
                print('{ %-17s }->' % attr, getattr(self, attr))

        return ''
