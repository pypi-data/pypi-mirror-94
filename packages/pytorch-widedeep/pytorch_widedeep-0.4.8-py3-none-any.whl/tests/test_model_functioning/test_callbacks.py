import os
import shutil
import string
from itertools import chain

import numpy as np
import torch
import pytest
from torch.optim.lr_scheduler import StepLR, CyclicLR

from pytorch_widedeep.optim import RAdam
from pytorch_widedeep.models import Wide, TabMlp, WideDeep, TabTransformer
from pytorch_widedeep.training import Trainer
from pytorch_widedeep.callbacks import (
    LRHistory,
    EarlyStopping,
    ModelCheckpoint,
)

# Wide array
X_wide = np.random.choice(50, (32, 10))

# Deep Array
colnames = list(string.ascii_lowercase)[:10]
embed_cols = [np.random.choice(np.arange(5), 32) for _ in range(5)]
embed_input = [(u, i, j) for u, i, j in zip(colnames[:5], [5] * 5, [16] * 5)]
cont_cols = [np.random.rand(32) for _ in range(5)]
column_idx = {k: v for v, k in enumerate(colnames)}
X_tab = np.vstack(embed_cols + cont_cols).transpose()

# target
target = np.random.choice(2, 32)


###############################################################################
# Test that history saves the information adequately
###############################################################################
wide = Wide(np.unique(X_wide).shape[0], 1)
deeptabular = TabMlp(
    mlp_hidden_dims=[32, 16],
    mlp_dropout=[0.5, 0.5],
    column_idx=column_idx,
    embed_input=embed_input,
    continuous_cols=colnames[-5:],
)
model = WideDeep(wide=wide, deeptabular=deeptabular)

# 1. Single optimizers_1, single scheduler, not cyclic and both passed directly
optimizers_1 = RAdam(model.parameters())
lr_schedulers_1 = StepLR(optimizers_1, step_size=4)

# 2. Multiple optimizers, single scheduler, cyclic and pass via a 1 item
# dictionary
wide_opt_2 = torch.optim.Adam(model.wide.parameters())
deep_opt_2 = RAdam(model.deeptabular.parameters())
deep_sch_2 = CyclicLR(
    deep_opt_2, base_lr=0.001, max_lr=0.01, step_size_up=5, cycle_momentum=False
)
optimizers_2 = {"wide": wide_opt_2, "deeptabular": deep_opt_2}
lr_schedulers_2 = {"deeptabular": deep_sch_2}

# 3. Multiple schedulers no cyclic
wide_opt_3 = torch.optim.Adam(model.wide.parameters())
deep_opt_3 = RAdam(model.deeptabular.parameters())
wide_sch_3 = StepLR(wide_opt_3, step_size=4)
deep_sch_3 = StepLR(deep_opt_3, step_size=4)
optimizers_3 = {"wide": wide_opt_3, "deeptabular": deep_opt_3}
lr_schedulers_3 = {"wide": wide_sch_3, "deeptabular": deep_sch_3}

# 4. Multiple schedulers with cyclic
wide_opt_4 = torch.optim.Adam(model.wide.parameters())
deep_opt_4 = torch.optim.Adam(model.deeptabular.parameters())
wide_sch_4 = StepLR(wide_opt_4, step_size=4)
deep_sch_4 = CyclicLR(
    deep_opt_4, base_lr=0.001, max_lr=0.01, step_size_up=5, cycle_momentum=False
)
optimizers_4 = {"wide": wide_opt_4, "deeptabular": deep_opt_4}
lr_schedulers_4 = {"wide": wide_sch_4, "deeptabular": deep_sch_4}

# 5. Single optimizers_5, single scheduler, cyclic and both passed directly
optimizers_5 = RAdam(model.parameters())
lr_schedulers_5 = CyclicLR(
    optimizers_5, base_lr=0.001, max_lr=0.01, step_size_up=5, cycle_momentum=False
)


@pytest.mark.parametrize(
    "optimizers, schedulers, len_loss_output, len_lr_output, init_lr, schedulers_type",
    [
        (optimizers_1, lr_schedulers_1, 5, 5, 0.001, "step"),
        (optimizers_2, lr_schedulers_2, 5, 11, 0.001, "cyclic"),
        (optimizers_3, lr_schedulers_3, 5, 5, None, None),
        (optimizers_4, lr_schedulers_4, 5, 11, None, None),
        (optimizers_5, lr_schedulers_5, 5, 11, 0.001, "cyclic"),
    ],
)
def test_history_callback(
    optimizers, schedulers, len_loss_output, len_lr_output, init_lr, schedulers_type
):

    trainer = Trainer(
        model=model,
        objective="binary",
        optimizers=optimizers,
        lr_schedulers=schedulers,
        callbacks=[LRHistory(n_epochs=5)],
        verbose=0,
    )
    trainer.fit(
        X_wide=X_wide,
        X_tab=X_tab,
        target=target,
        n_epochs=5,
        batch_size=16,
    )
    out = []
    out.append(len(trainer.history["train_loss"]) == len_loss_output)

    try:
        lr_list = list(chain.from_iterable(trainer.lr_history["lr_deeptabular_0"]))
    except Exception:
        try:
            lr_list = trainer.lr_history["lr_deeptabular_0"]
        except Exception:
            lr_list = trainer.lr_history["lr_0"]

    out.append(len(lr_list) == len_lr_output)
    if init_lr is not None and schedulers_type == "step":
        out.append(lr_list[-1] == init_lr / 10)
    elif init_lr is not None and schedulers_type == "cyclic":
        out.append(lr_list[-1] == init_lr)
    assert all(out)


###############################################################################
# Test that EarlyStopping stops as expected
###############################################################################
def test_early_stop():
    wide = Wide(np.unique(X_wide).shape[0], 1)
    deeptabular = TabMlp(
        mlp_hidden_dims=[32, 16],
        mlp_dropout=[0.5, 0.5],
        column_idx=column_idx,
        embed_input=embed_input,
        continuous_cols=colnames[-5:],
    )
    model = WideDeep(wide=wide, deeptabular=deeptabular)
    trainer = Trainer(
        model=model,
        objective="binary",
        callbacks=[
            EarlyStopping(
                min_delta=5.0, patience=3, restore_best_weights=True, verbose=1
            )
        ],
        verbose=1,
    )
    trainer.fit(X_wide=X_wide, X_tab=X_tab, target=target, val_split=0.2, n_epochs=5)
    # length of history = patience+1
    assert len(trainer.history["train_loss"]) == 3 + 1


###############################################################################
# Test that ModelCheckpoint behaves as expected
###############################################################################
@pytest.mark.parametrize(
    "save_best_only, max_save, n_files", [(True, 2, 2), (False, 2, 2), (False, 0, 5)]
)
def test_model_checkpoint(save_best_only, max_save, n_files):
    wide = Wide(np.unique(X_wide).shape[0], 1)
    deeptabular = TabMlp(
        mlp_hidden_dims=[32, 16],
        mlp_dropout=[0.5, 0.5],
        column_idx=column_idx,
        embed_input=embed_input,
        continuous_cols=colnames[-5:],
    )
    model = WideDeep(wide=wide, deeptabular=deeptabular)
    trainer = Trainer(
        model=model,
        objective="binary",
        callbacks=[
            ModelCheckpoint(
                "tests/test_model_functioning/weights/test_weights",
                save_best_only=save_best_only,
                max_save=max_save,
            )
        ],
        verbose=0,
    )
    trainer.fit(X_wide=X_wide, X_tab=X_tab, target=target, n_epochs=5, val_split=0.2)
    n_saved = len(os.listdir("tests/test_model_functioning/weights/"))

    shutil.rmtree("tests/test_model_functioning/weights/")

    assert n_saved <= n_files


def test_filepath_error():
    wide = Wide(np.unique(X_wide).shape[0], 1)
    deeptabular = TabMlp(
        mlp_hidden_dims=[16, 4],
        column_idx=column_idx,
        embed_input=embed_input,
        continuous_cols=colnames[-5:],
    )
    model = WideDeep(wide=wide, deeptabular=deeptabular)
    with pytest.raises(ValueError):
        trainer = Trainer(  # noqa: F841
            model=model,
            objective="binary",
            callbacks=[ModelCheckpoint(filepath="wrong_file_path")],
            verbose=0,
        )


###############################################################################
# Repeat 1st set of tests for TabTransormer
###############################################################################

# Wide array
X_wide = np.random.choice(50, (32, 10))

# Tab Array
colnames = list(string.ascii_lowercase)[:10]
embed_cols = [np.random.choice(np.arange(5), 32) for _ in range(5)]
embeds_input = [(i, j) for i, j in zip(colnames[:5], [5] * 5)]  # type: ignore[misc]
cont_cols = [np.random.rand(32) for _ in range(5)]
column_idx = {k: v for v, k in enumerate(colnames)}
X_tab = np.vstack(embed_cols + cont_cols).transpose()

# target
target = np.random.choice(2, 32)

wide = Wide(np.unique(X_wide).shape[0], 1)
tab_transformer = TabTransformer(
    column_idx={k: v for v, k in enumerate(colnames)},
    embed_input=embeds_input,
    continuous_cols=colnames[5:],
)
model_tt = WideDeep(wide=wide, deeptabular=tab_transformer)

# 1. Single optimizers_1, single scheduler, not cyclic and both passed directly
optimizers_1 = RAdam(model_tt.parameters())
lr_schedulers_1 = StepLR(optimizers_1, step_size=4)

# 2. Multiple optimizers, single scheduler, cyclic and pass via a 1 item
# dictionary
wide_opt_2 = torch.optim.Adam(model_tt.wide.parameters())
deep_opt_2 = RAdam(model_tt.deeptabular.parameters())
deep_sch_2 = CyclicLR(
    deep_opt_2, base_lr=0.001, max_lr=0.01, step_size_up=5, cycle_momentum=False
)
optimizers_2 = {"wide": wide_opt_2, "deeptabular": deep_opt_2}
lr_schedulers_2 = {"deeptabular": deep_sch_2}

# 3. Multiple schedulers no cyclic
wide_opt_3 = torch.optim.Adam(model_tt.wide.parameters())
deep_opt_3 = RAdam(model_tt.deeptabular.parameters())
wide_sch_3 = StepLR(wide_opt_3, step_size=4)
deep_sch_3 = StepLR(deep_opt_3, step_size=4)
optimizers_3 = {"wide": wide_opt_3, "deeptabular": deep_opt_3}
lr_schedulers_3 = {"wide": wide_sch_3, "deeptabular": deep_sch_3}

# 4. Multiple schedulers with cyclic
wide_opt_4 = torch.optim.Adam(model_tt.wide.parameters())
deep_opt_4 = torch.optim.Adam(model_tt.deeptabular.parameters())
wide_sch_4 = StepLR(wide_opt_4, step_size=4)
deep_sch_4 = CyclicLR(
    deep_opt_4, base_lr=0.001, max_lr=0.01, step_size_up=5, cycle_momentum=False
)
optimizers_4 = {"wide": wide_opt_4, "deeptabular": deep_opt_4}
lr_schedulers_4 = {"wide": wide_sch_4, "deeptabular": deep_sch_4}


@pytest.mark.parametrize(
    "optimizers, schedulers, len_loss_output, len_lr_output, init_lr, schedulers_type",
    [
        (optimizers_1, lr_schedulers_1, 5, 5, 0.001, "step"),
        (optimizers_2, lr_schedulers_2, 5, 11, 0.001, "cyclic"),
        (optimizers_3, lr_schedulers_3, 5, 5, None, None),
        (optimizers_4, lr_schedulers_4, 5, 11, None, None),
    ],
)
def test_history_callback_w_tabtransformer(
    optimizers, schedulers, len_loss_output, len_lr_output, init_lr, schedulers_type
):
    trainer_tt = Trainer(
        model_tt,
        objective="binary",
        optimizers=optimizers,
        lr_schedulers=schedulers,
        callbacks=[LRHistory(n_epochs=5)],
        verbose=0,
    )
    trainer_tt.fit(
        X_wide=X_wide,
        X_tab=X_tab,
        target=target,
        n_epochs=5,
        batch_size=16,
    )
    out = []
    out.append(len(trainer_tt.history["train_loss"]) == len_loss_output)
    try:
        lr_list = list(chain.from_iterable(trainer_tt.lr_history["lr_deeptabular_0"]))
    except TypeError:
        lr_list = trainer_tt.lr_history["lr_deeptabular_0"]
    except Exception:
        lr_list = trainer_tt.lr_history["lr_0"]
    out.append(len(lr_list) == len_lr_output)
    if init_lr is not None and schedulers_type == "step":
        out.append(lr_list[-1] == init_lr / 10)
    elif init_lr is not None and schedulers_type == "cyclic":
        out.append(lr_list[-1] == init_lr)
    assert all(out)
