import argparse
import yaml
from distutils import util as dutil

from cfgs.base_cfgs import Cfgs
from core.eval_novel import Execution as NovelEval
from core.exec2steps import Execution as Exec2Steps

import os

os.environ['CUDA_LAUNCH_BLOCKING'] = "1"


def str2bool(v):
    """
    字符串转换为布尔值
    """
    return bool(dutil.strtobool(v))


def parse_args():
    """
    命令行参数指定
    Parse input arguments
    """
    parser = argparse.ArgumentParser(description='Model training/evaluation args')

    # 运行模式
    parser.add_argument('--RUN', dest='RUN_MODE',
                        choices=['train', 'val', 'test', 'valNovel'],
                        help='{train, val, test, valNovel}',
                        type=str, required=True)

    # bert模型种类
    parser.add_argument('--MODEL', dest='MODEL',
                        choices=['small', 'large'],
                        help='{small, large}',
                        default='small', type=str)

    # 隐层数
    parser.add_argument('--num_hidden_layers', dest='num_hidden_layers',
                        default=6, type=int)

    # multi-head attention的head数
    parser.add_argument('--num_attention_heads', dest='num_attention_heads',
                        default=8, type=int)

    # dropout
    parser.add_argument('--ATTN_DROPOUT', dest='ATTN_DROPOUT',
                        type=str2bool, default=True)

    # 加强新概念
    parser.add_argument('--NOVEL_AUGMENT', dest='NOVEL_AUGMENT',
                        type=int, default=1)  # during pointing, can augment exposure to novel concepts

    parser.add_argument('--GROUND_LAYER', dest='GROUND_LAYER',
                        type=int, default=0)  # last layer id = 0, second-last layer id = 1, etc.

    # 结果评估的文件
    parser.add_argument('--RESULT_EVAL_FILE', dest='RESULT_EVAL_FILE',
                        type=str, default=None, help='JSON file containing generated answers for evaluation.')

    # 新概念 在训练中没有标注的数据
    parser.add_argument('--CONCEPT', dest='CONCEPT',
                        type=str, default=None,
                        help='Novel concepts with no labeled data in training (string with commas separating concepts)')

    # 新技能 结合CONCEPT参数，删除标注数据。对于技能概念组合
    parser.add_argument('--SKILL', dest='SKILL',
                        type=str, default=None,
                        help='Novel skill with no labeled data in training. ' +
                             'When combined with the CONCEPT arg, this will ' +
                             'remove labeled data for skill-concept compositions')

    parser.add_argument('--SPLIT', dest='TRAIN_SPLIT',
                        choices=['train', 'train+val', 'train+val+vg'],
                        help="set training split, "
                             "eg.'train', 'train+val+vg'"
                             "set 'train' can trigger the "
                             "eval after every epoch",
                        default='train',
                        type=str)

    # 学习率衰减
    parser.add_argument('--LR_DECAY_LIST', dest='LR_DECAY_LIST',
                        type=int, nargs='*', default=[10, 12])

    # 使用grounding的概念
    parser.add_argument('--USE_GROUNDING', dest='USE_GROUNDING',
                        type=str2bool, default=True)

    parser.add_argument('--TGT_MASKING', dest='TGT_MASKING',
                        type=str, default='target', choices=['target', 'bert', 'even', 'none'])

    parser.add_argument('--USE_POINT_PROJ', dest='USE_POINT_PROJ',
                        type=str2bool, default=True)

    parser.add_argument('--PT_TEMP', dest='PT_TEMP',
                        type=float, default=1.0)

    # p_esp：以p_esp的概率使用本文loss，否则使用VQA loss
    parser.add_argument('--GROUNDING_PROB', dest='GROUNDING_PROB',
                        type=float, default=0.1)

    # skill matching 里的 tao_s
    parser.add_argument('--SK_TEMP', dest='SK_TEMP',
                        type=float, default=0.5)

    parser.add_argument('--SKILL_CONT_LOSS', dest='SKILL_CONT_LOSS',
                        type=str2bool, default=True)

    # 技能的池化
    parser.add_argument('--SKILL_POOL', dest='SKILL_POOL',
                        type=str, default='mean', choices=['cls', 'mean', 'max'])

    # 在每一个epoch训练完评估验证集（仅在train时有效）
    parser.add_argument('--EVAL_EE', dest='EVAL_EVERY_EPOCH',
                        help='set True to evaluate the '
                             'val split when an epoch finished'
                             "(only work when train with "
                             "'train' split)",
                        type=bool)

    # 保存预测向量（仅在prediction时有效）
    parser.add_argument('--SAVE_PRED', dest='TEST_SAVE_PRED',
                        help='set True to save the '
                             'prediction vectors'
                             '(only work in testing)',
                        type=bool)

    parser.add_argument('--BS', dest='BATCH_SIZE',
                        help='batch size during training',
                        type=int)

    parser.add_argument('--MAX_EPOCH', dest='MAX_EPOCH',
                        help='max training epoch',
                        type=int)

    parser.add_argument('--GPU', dest='GPU',
                        help="gpu select, eg.'0, 1, 2'",
                        type=str)

    parser.add_argument('--SEED', dest='SEED',
                        help='fix random seed',
                        type=int)

    parser.add_argument('--VERSION', dest='VERSION',
                        help='version control',
                        type=str)

    parser.add_argument('--RESUME', dest='RESUME',
                        help='resume training',
                        type=str2bool)

    parser.add_argument('--CKPT_V', dest='CKPT_VERSION',
                        help='checkpoint version',
                        type=str)

    parser.add_argument('--CKPT_E', dest='CKPT_EPOCH',
                        help='checkpoint epoch',
                        type=int)

    parser.add_argument('--CKPT_PATH', dest='CKPT_PATH',
                        help='load checkpoint path, we '
                             'recommend that you use '
                             'CKPT_VERSION and CKPT_EPOCH '
                             'instead',
                        type=str)

    parser.add_argument('--ACCU', dest='GRAD_ACCU_STEPS',
                        help='reduce gpu memory usage',
                        type=int)

    parser.add_argument('--NW', dest='NUM_WORKERS',
                        help='multithreaded loading',
                        type=int)

    parser.add_argument('--PINM', dest='PIN_MEM',
                        help='use pin memory',
                        type=bool)

    parser.add_argument('--VERB', dest='VERBOSE',
                        help='verbose print',
                        type=bool)

    parser.add_argument('--DATA_PATH', dest='DATASET_PATH',
                        help='vqav2 dataset root path',
                        type=str)

    parser.add_argument('--FEAT_PATH', dest='FEATURE_PATH',
                        help='bottom up features root path',
                        type=str)

    # noinspection PyShadowingNames
    args = parser.parse_args()
    return args


if __name__ == '__main__':
    __C = Cfgs()

    # 获取命令行参数
    args = parse_args()
    # 将其转换为字典类型
    args_dict = __C.parse_to_dict(args)

    print(args)

    # 根据传入的MODEL命令行参数，选择large模型还是small模型
    # 加载对应的large_model.yml和small_model.yml
    cfg_file = "cfgs/{}_model.yml".format(args.MODEL)
    with open(cfg_file, 'r') as f:
        yaml_dict = yaml.safe_load(f)

    # 将命令行参数和yml中BERT模型参数合并为一个参数字典
    args_dict = {**yaml_dict, **args_dict}
    # 添加配置信息
    __C.add_args(args_dict)
    __C.fix_and_add_args(args_dict)
    # 设备，模型配置初始化
    __C.proc()

    print('Hyper Parameters:')
    print(__C)

    __C.check_path()

    if __C.RUN_MODE == 'valNovel':
        # 在新子集计算验证精度
        print('Compute validation accuracy on novel subsets')
        execution = NovelEval(__C)
    else:
        if __C.USE_GROUNDING:
            # 使用技能-概念组合
            print('Use 2-step Loss')
        else:
            # 仅使用VQA loss
            print('No grounding loss')
        execution = Exec2Steps(__C)

    execution.run(__C.RUN_MODE)
