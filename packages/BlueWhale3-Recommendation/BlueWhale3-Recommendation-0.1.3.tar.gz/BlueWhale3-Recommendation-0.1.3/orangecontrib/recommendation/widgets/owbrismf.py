from AnyQt.QtCore import Qt

from Orange.data import Table
from Orange.widgets import settings, gui
from Orange.widgets.utils.owlearnerwidget import OWBaseLearner
from Orange.widgets.utils.widgetpreview import WidgetPreview

from orangecontrib.recommendation import BRISMFLearner
from orangecontrib.recommendation.utils import format_data
import orangecontrib.recommendation.optimizers as opt
from orangecontrib.recommendation.i18n_config import *


def __(key):
    return i18n.t('recommendation.owbrismf.' + key)


class OWBRISMF(OWBaseLearner):
    # Widget needs a name, or it is considered an abstract widget
    # and not shown in the menu.
    name = __("name")
    description = __("desc")
    icon = "icons/brismf.svg"
    priority = 80

    LEARNER = BRISMFLearner

    outputs = [("P", Table),
               ("Q", Table)]

    # Parameters (general)
    num_factors = settings.Setting(10)
    num_iter = settings.Setting(15)
    learning_rate = settings.Setting(0.01)
    bias_learning_rate = settings.Setting(0.01)
    lmbda = settings.Setting(0.1)
    bias_lmbda = settings.Setting(0.1)

    # Seed (Random state)
    RND_SEED, FIXED_SEED = range(2)
    seed_type = settings.Setting(RND_SEED)
    random_seed = settings.Setting(42)

    # SGD optimizers
    class _Optimizer:
        SGD, MOMENTUM, NAG, ADAGRAD, RMSPROP, ADADELTA, ADAM, ADAMAX = range(8)
        names = [__("gbox.vanilla_sgd"), __("gbox.momentum"), __("gbox.nesterov_momentum"),
                 __("gbox.adagrad"), __("gbox.rmsprop"), __("gbox.adadelta"), __("gbox.adam"), __("gbox.adamax")]

    opt_type = settings.Setting(_Optimizer.SGD)
    momentum = settings.Setting(0.9)
    rho = settings.Setting(0.9)
    beta1 = settings.Setting(0.9)
    beta2 = settings.Setting(0.999)

    def add_main_layout(self):
        # hbox = gui.hBox(self.controlArea, "Settings")

        # Frist groupbox (Common parameters)
        box = gui.widgetBox(self.controlArea, __("box_parameter"))

        gui.spin(box, self, "num_factors", 1, 10000,
                 label=__("row.latent_factor_num"),
                 alignment=Qt.AlignRight, callback=self.settings_changed)

        gui.spin(box, self, "num_iter", 1, 10000,
                 label=__("row.iteration_num"),
                 alignment=Qt.AlignRight, callback=self.settings_changed)

        gui.doubleSpin(box, self, "learning_rate", minv=1e-5, maxv=1e+5,
                       step=1e-5, label=__("row.learn_rate"), decimals=5,
                       alignment=Qt.AlignRight, controlWidth=90,
                       callback=self.settings_changed)

        gui.doubleSpin(box, self, "bias_learning_rate", minv=1e-5, maxv=1e+5,
                       step=1e-5, label=__("row.bias_learn_rate"), decimals=5,
                       alignment=Qt.AlignRight, controlWidth=90,
                       callback=self.settings_changed)

        gui.doubleSpin(box, self, "lmbda", minv=1e-4, maxv=1e+4, step=1e-4,
                       label=__("row.regularization"), decimals=4,
                       alignment=Qt.AlignRight, controlWidth=90,
                       callback=self.settings_changed)

        gui.doubleSpin(box, self, "bias_lmbda", minv=1e-4, maxv=1e+4, step=1e-4,
                       label=__("row.bias_regularization"), decimals=4,
                       alignment=Qt.AlignRight, controlWidth=90,
                       callback=self.settings_changed)

        # Second groupbox (SGD optimizers)
        box = gui.widgetBox(self.controlArea, __("box_sgd_optimizer"))

        gui.comboBox(box, self, "opt_type", label=__("row.sgd_optimizer"),
                     items=self._Optimizer.names, orientation=Qt.Horizontal,
                     addSpace=4, callback=self._opt_changed)

        _m_comp = gui.doubleSpin(box, self, "momentum", minv=1e-4, maxv=1e+4,
                                 step=1e-4, label=__("row.momentum"), decimals=4,
                                 alignment=Qt.AlignRight, controlWidth=90,
                                 callback=self.settings_changed)

        _r_comp = gui.doubleSpin(box, self, "rho", minv=1e-4, maxv=1e+4,
                                 step=1e-4, label=__("row.rho"), decimals=4,
                                 alignment=Qt.AlignRight, controlWidth=90,
                                 callback=self.settings_changed)

        _b1_comp = gui.doubleSpin(box, self, "beta1", minv=1e-5, maxv=1e+5,
                                  step=1e-4, label=__("row.beta1"), decimals=5,
                                  alignment=Qt.AlignRight, controlWidth=90,
                                  callback=self.settings_changed)

        _b2_comp = gui.doubleSpin(box, self, "beta2", minv=1e-5, maxv=1e+5,
                                  step=1e-4, label=__("row.beta2"), decimals=5,
                                  alignment=Qt.AlignRight, controlWidth=90,
                                  callback=self.settings_changed)
        gui.rubber(box)
        self._opt_params = [_m_comp, _r_comp, _b1_comp, _b2_comp]
        self._show_right_optimizer()

        # Third groupbox (Random state)
        box = gui.widgetBox(self.controlArea, __("box_random_state"))
        rndstate = gui.radioButtons(box, self, "seed_type",
                                    callback=self.settings_changed)
        gui.appendRadioButton(rndstate, __("btn_random_seed"))
        gui.appendRadioButton(rndstate, __("btn_fixed_seed"))
        ibox = gui.indentedBox(rndstate)
        self.spin_rnd_seed = gui.spin(ibox, self, "random_seed", -1e5, 1e5,
                                      label=__("row.seed"), alignment=Qt.AlignRight,
                                      callback=self.settings_changed)
        self.settings_changed()  # Update (extra) settings

    def settings_changed(self):
        # Enable/Disable Fixed seed control
        self.spin_rnd_seed.setEnabled(self.seed_type == self.FIXED_SEED)
        super().settings_changed()

    def _show_right_optimizer(self):
        enabled = [[False, False, False, False],  # SGD
                   [True, False, False, False],  # Momentum
                   [True, False, False, False],  # NAG
                   [False, False, False, False],  # AdaGrad
                   [False, True, False, False],  # RMSprop
                   [False, True, False, False],  # AdaDelta
                   [False, False, True, True],  # Adam
                   [False, False, True, True],  # Adamax
                   ]

        mask = enabled[self.opt_type]
        for spin, enabled in zip(self._opt_params, mask):
            [spin.box.hide, spin.box.show][enabled]()

    def _opt_changed(self):
        self._show_right_optimizer()
        self.settings_changed()

    def select_optimizer(self):
        if self.opt_type == self._Optimizer.MOMENTUM:
            return opt.Momentum(momentum=self.momentum)

        elif self.opt_type == self._Optimizer.NAG:
            return opt.NesterovMomentum(momentum=self.momentum)

        elif self.opt_type == self._Optimizer.ADAGRAD:
            return opt.AdaGrad()

        elif self.opt_type == self._Optimizer.RMSPROP:
            return opt.RMSProp(rho=self.rho)

        elif self.opt_type == self._Optimizer.ADADELTA:
            return opt.AdaDelta(rho=self.rho)

        elif self.opt_type == self._Optimizer.ADAM:
            return opt.Adam(beta1=self.beta1, beta2=self.beta2)

        elif self.opt_type == self._Optimizer.ADAMAX:
            return opt.Adamax(beta1=self.beta1, beta2=self.beta2)

        else:
            return opt.SGD()

    def create_learner(self):
        # Set random state
        if self.seed_type == self.FIXED_SEED:
            seed = self.random_seed
        else:
            seed = None

        return self.LEARNER(
            num_factors=self.num_factors,
            num_iter=self.num_iter,
            learning_rate=self.learning_rate,
            bias_learning_rate=self.bias_learning_rate,
            lmbda=self.lmbda,
            bias_lmbda=self.bias_lmbda,
            optimizer=self.select_optimizer(),
            random_state=seed,
            callback=self.progress_callback
        )

    def get_learner_parameters(self):
        return ((__("back_row.latent_factor_num"), self.num_factors),
                (__("back_row.iteration_num"), self.num_iter),
                (__("back_row.learn_rate"), self.learning_rate),
                (__("back_row.bias_learn_rate"), self.bias_learning_rate),
                (__("back_row.regularization"), self.lmbda),
                (__("back_row.bias_regularization"), self.bias_lmbda),
                (__("back_row.sgd_optimizer"), self._Optimizer.names[self.opt_type]))

    def _check_data(self):
        self.valid_data = False

        if self.data is not None:
            try:  # Check ratings data
                valid_ratings = format_data.check_data(self.data)
            except Exception as e:
                valid_ratings = False
                print(__("error_check_rate_data") + str(e))

            if not valid_ratings:  # Check if it's valid
                self.Error.data_error(
                    __("error_data_invalid_for_rate_model"))
            else:
                self.valid_data = True

        return self.valid_data

    def update_learner(self):
        self._check_data()

        # If our method returns 'False', it could be because there is no data.
        # But when cross-validating, a learner is required, as the data is in
        # the widget Test&Score
        if self.valid_data or self.data is None:
            super().update_learner()

    def update_model(self):
        self._check_data()
        super().update_model()

        P = None
        Q = None
        if self.valid_data:
            P = self.model.getPTable()
            Q = self.model.getQTable()

        self.send("P", P)
        self.send("Q", Q)

    def progress_callback(self, *args, **kwargs):
        iter = args[0]

        # Start/Finish progress bar
        if iter == 1:  # Start it
            self.progressBarInit()

        if iter == self.num_iter:  # Finish
            self.progressBarFinished()
            return

        if self.num_iter > 0:
            self.progressBarSet(int(iter / self.num_iter * 100))


if __name__ == '__main__':
    WidgetPreview(OWBRISMF).run()
