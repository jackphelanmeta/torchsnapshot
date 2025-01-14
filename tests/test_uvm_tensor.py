#!/usr/bin/env python3
# Copyright (c) Meta Platforms, Inc. and affiliates.
# All rights reserved.
#
# This source code is licensed under the BSD-style license found in the
# LICENSE file in the root directory of this source tree.

# pyre-ignore-all-errors[56]

import pytest
import torch
from torchsnapshot.uvm_tensor import (
    _UVM_TENSOR_AVAILABLE,
    is_uvm_tensor,
    new_managed_tensor,
    uvm_to_cpu,
)


@pytest.mark.cpu_and_gpu
def test_uvm_tensor() -> None:
    if torch.cuda.is_available() and _UVM_TENSOR_AVAILABLE:
        uvm_tensor = torch.rand(
            (64, 64),
            out=new_managed_tensor(
                torch.empty(0, dtype=torch.float32, device="cuda:0"),
                [64, 64],
            ),
        )
        assert is_uvm_tensor(uvm_tensor)
        cpu_tensor = uvm_to_cpu(uvm_tensor)
        assert not is_uvm_tensor(cpu_tensor)
    else:
        tensor = torch.rand(64, 64)
        assert not is_uvm_tensor(tensor)
