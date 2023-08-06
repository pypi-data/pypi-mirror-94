from copy import deepcopy

import pytest
from torch import nn

from pytorch_widedeep.models import Wide, TabMlp, DeepText, WideDeep, DeepImage

embed_input = [(u, i, j) for u, i, j in zip(["a", "b", "c"][:4], [4] * 3, [8] * 3)]
column_idx = {k: v for v, k in enumerate(["a", "b", "c"])}
wide = Wide(10, 1)
deepdense = TabMlp(
    mlp_hidden_dims=[16, 8], column_idx=column_idx, embed_input=embed_input
)
deeptext = DeepText(vocab_size=100, embed_dim=8)
deepimage = DeepImage(pretrained=False)

###############################################################################
#  test raising 'output dim errors'
###############################################################################


@pytest.mark.parametrize(
    "deepcomponent, component_name",
    [
        (None, "dense"),
        (deeptext, "text"),
        (deepimage, "image"),
    ],
)
def test_history_callback(deepcomponent, component_name):
    if deepcomponent is None:
        deepcomponent = deepcopy(deepdense)
    deepcomponent.__dict__.pop("output_dim")
    with pytest.raises(AttributeError):
        if component_name == "dense":
            model = WideDeep(wide, deeptabular=deepcomponent)
        elif component_name == "text":
            model = WideDeep(wide, deeptabular=deepdense, deeptext=deepcomponent)
        elif component_name == "image":
            model = WideDeep(  # noqa: F841
                wide, deeptabular=deepdense, deepimage=deepcomponent
            )


###############################################################################
#  test warning on head_layers_dim and deephead
###############################################################################


def test_deephead_and_head_layers_dim():
    deephead = nn.Sequential(nn.Linear(32, 16), nn.Linear(16, 8))
    with pytest.raises(ValueError):
        model = WideDeep(  # noqa: F841
            wide=wide,
            deeptabular=deepdense,
            head_hidden_dims=[16, 8],
            deephead=deephead,
        )


###############################################################################
#  test deephead is None and head_layers_dim is not None
###############################################################################


def test_no_deephead_and_head_layers_dim():
    out = []
    model = WideDeep(
        wide=wide, deeptabular=deepdense, head_hidden_dims=[8, 4]
    )  # noqa: F841
    for n, p in model.named_parameters():
        if n == "deephead.head_layer_0.0.weight":
            out.append(p.size(0) == 8 and p.size(1) == 8)
        if n == "deephead.head_layer_1.0.weight":
            out.append(p.size(0) == 4 and p.size(1) == 8)
    assert all(out)
