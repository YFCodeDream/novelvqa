import os


# noinspection PyAttributeOutsideInit
class PATH:
    """
    关于项目中所有的文件路径管理类
    """
    def __init__(self):

        # vqav2 dataset root path
        # VQA v2数据集的路径
        self.DATASET_PATH = './datasets/vqa/'

        # bottom up features root path
        # 特征路径
        self.FEATURE_PATH = './datasets/coco_extract/'

        self.init_path()

    def init_path(self):
        # 图像特征路径
        self.IMG_FEAT_PATH = {
            'train': self.FEATURE_PATH + 'train2014/',
            'val': self.FEATURE_PATH + 'val2014/',
            'test': self.FEATURE_PATH + 'test2015/',
        }

        # 问题路径
        self.QUESTION_PATH = {
            'train': self.DATASET_PATH + 'v2_OpenEnded_mscoco_train2014_questions.json',
            'val': self.DATASET_PATH + 'v2_OpenEnded_mscoco_val2014_questions.json',
            'test': self.DATASET_PATH + 'v2_OpenEnded_mscoco_test2015_questions.json',
            'vg': self.DATASET_PATH + 'VG_questions.json',
        }

        # 答案路径
        self.ANSWER_PATH = {
            'train': self.DATASET_PATH + 'v2_mscoco_train2014_annotations.json',
            'val': self.DATASET_PATH + 'v2_mscoco_val2014_annotations.json',
            'vg': self.DATASET_PATH + 'VG_annotations.json',
        }

        # 结果路径
        self.RESULT_PATH = './results/result_test/'
        # 预测路径
        self.PRED_PATH = './results/pred/'
        # 缓存路径
        self.CACHE_PATH = './results/cache/'
        # 日志路径
        self.LOG_PATH = './results/log/'
        # 检查点路径
        self.CKPTS_PATH = './ckpts/'
        self.ATTN_PATH = './results/attn/'
        self.ANA_PATH = './results/analysis'

        if 'result_test' not in os.listdir('./results'):
            os.mkdir('./results/result_test')

        if 'pred' not in os.listdir('./results'):
            os.mkdir('./results/pred')

        if 'cache' not in os.listdir('./results'):
            os.mkdir('./results/cache')

        if 'log' not in os.listdir('./results'):
            os.mkdir('./results/log')

        if 'ckpts' not in os.listdir('./'):
            os.mkdir('./ckpts')

    def check_path(self):
        """
        检查图像特征，问题和答案路径里是否存在
        train, val, (test), (vg)
        """
        print('Checking dataset ...')

        for mode in self.IMG_FEAT_PATH:
            if not os.path.exists(self.IMG_FEAT_PATH[mode]):
                print(self.IMG_FEAT_PATH[mode] + ' DOES NOT EXIST')
                exit(-1)

        for mode in self.QUESTION_PATH:
            if not os.path.exists(self.QUESTION_PATH[mode]):
                print(self.QUESTION_PATH[mode] + ' DOES NOT EXIST')
                exit(-1)

        for mode in self.ANSWER_PATH:
            if not os.path.exists(self.ANSWER_PATH[mode]):
                print(self.ANSWER_PATH[mode] + ' DOES NOT EXIST')
                exit(-1)

        print('Finished')
        print('')
