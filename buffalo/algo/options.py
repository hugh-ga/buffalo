# -*- coding: utf-8 -*-
from buffalo.misc.aux import InputOptions, Option


class AlgoOption(InputOptions):
    def __init__(self, *args, **kwargs):
        super(AlgoOption, self).__init__(*args, **kwargs)

    def get_default_option(self):
        opt = {
            'compute_loss_on_training': True,
            'save_best': False,
            'evaluation_period': 1,
            'save_period': 10,

            'random_seed': 0,
        }
        return opt

    def get_default_optimize_option(self):
        opt = {
            'loss': 'train_loss',
        }
        return opt

    def get_default_tensorboard_option(self):
        opt = {
            'name': 'default',
            'root': './tb',
            'name_template': '{name}.{dtm}'
        }
        return opt

    def is_valid_option(self, opt):
        b = super().is_valid_option(opt)
        for f in ['num_workers']:
            if not f in opt:
                raise RuntimeError(f'{f} not defined')
        return b


class AlsOption(AlgoOption):
    def __init__(self, *args, **kwargs):
        super(AlsOption, self).__init__(*args, **kwargs)

    def get_default_option(self):
        opt = super().get_default_option()
        opt.update({
            'adaptive_reg': False,
            'save_factors': False,

            'd': 20,
            'num_iters': 10,
            'num_workers': 1,
            'early_stopping_rounds': 5,
            'reg_u': 0.1,
            'reg_i': 0.1,
            'alpha': 8,
            'use_conjugate_gradient': True,
            'num_iteration_for_conjugate_gradient': 3,

            'model_path': '',
            'data_opt': {}
        })
        return Option(opt)

    def get_default_optimize_option(self):
        """Optimization Options for ALS
        options:
            loss(str): Target loss to optimize.
            max_trials(int, option): Maximum experiments for optimization. If not given, run forever.
            min_trials(int, option): Minimum experiments before deploying model. (Since the best parameter may not be found after `min_trials`, the first best parameter is always deployed)
            deployment(bool): Set True to train model with the best parameter. During the optimization, it try to dump the model which beated the previous best loss.
            start_with_default_parameters(bool): If set to True, the loss value of the default parameter is used as the starting loss to beat.
            space(dict): Parameter space definition. For more information, pleases reference hyperopt's express. Note) Due to hyperopt's `randint` does not provide lower value, we had to implement it a bait tricky. Pleases see optimize.py to check how we deal with `randint`.k
        """
        opt = super().get_default_optimize_option()
        opt.update({
            'loss': 'train_loss',
            'max_trials': 100,
            'min_trials': 0,
            'deployment': True,
            'start_with_default_parameters': True,
            'space': {
                'adaptive_reg': ['choice', ['adaptive_reg', [0, 1]]],
                'd': ['randint', ['d', 10, 30]],
                'reg_u': ['uniform', ['reg_u', 0.1, 1]],
                'reg_i': ['uniform', ['reg_i', 0.1, 1]],
                'alpha': ['randint', ['alpha', 1, 32]]
            }
        })
        return Option(opt)


class BprmfOption(AlgoOption):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

    def get_default_option(self):
        opt = super().get_default_option()
        opt.update({
            'use_bias': True,
            'evaluation_period': 100,

            'num_workers': 1,
            'num_iters': 100,
            'd': 20,
            'update_i': True,
            'update_j': True,
            'reg_u': 0.025,
            'reg_i': 0.025,
            'reg_j': 0.025,
            'reg_b': 0.025,

            'optimizer': 'sgd',
            'lr': 0.002,
            'lr_decay': 0.0,
            'min_lr': 0.0001,
            'beta1': 0.9,
            'beta2': 0.999,
            'batch_size': -1,
            'early_stopping_rounds': 5,

            'per_coordinate_normalize': False,
            'num_negative_samples': 1,
            'sampling_power': 0.0,

            'model_path': '',
            'data_opt': {}
        })
        return Option(opt)

    def get_default_optimize_option(self):
        """Optimization Options for BPRMF
        """
        opt = super().get_default_optimize_option()
        opt.update({
            'loss': 'train_loss',
            'max_trials': 100,
            'min_trials': 0,
            'deployment': True,
            'start_with_default_parameters': True,
            'space': {
                'd': ['randint', ['d', 10, 30]],
                'reg_u': ['uniform', ['reg_u', 0.1, 1]],
                'reg_i': ['uniform', ['reg_i', 0.1, 1]]
            }
        })
        return Option(opt)


class W2vOption(AlgoOption):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

    def get_default_option(self):
        opt = super().get_default_option()
        opt.update({
            'evaluation_on_learning': False,

            'num_workers': 1,
            'num_iters': 3,
            'd': 20,
            'window': 5,
            'min_count': 5,
            'sample': 0.001,

            'lr': 0.025,
            'min_lr': 0.0001,
            'batch_size': -1,
            'early_stopping_rounds': 5,

            'num_negative_samples': 5,

            'model_path': '',
            'data_opt': {}
        })
        return Option(opt)

    def get_default_optimize_option(self):
        """Optimization Options for W2V
        """
        #
        opt = super().get_default_optimize_option()
        opt.update({
            'loss': 'train_loss',
            'max_trials': 100,
            'min_trials': 0,
            'deployment': True,
            'start_with_default_parameters': True,
            'space': {
                'd': ['randint', ['d', 10, 30]],
                'window': ['randint', ['window', 2, 8]],
                'num_negative_samples': ['randint', ['alpha', 1, 12]]
            }
        })
        return Option(opt)
