"""Compact 3D U-Net (nnU-Net-style conventions, CPU-sized).

Conv(3³) → InstanceNorm → LeakyReLU, two per stage; strided-conv downsampling; transposed-conv
upsampling; deep supervision optional. Default: 4 resolution levels, base 12 channels
(~0.6 M parameters) so that training on 4 CPU cores is feasible. Architecture hyper-
parameters are stored in every checkpoint so models are reconstructable from the artifact.
"""
from __future__ import annotations

import torch
import torch.nn as nn
import torch.nn.functional as F


class ConvBlock(nn.Module):
    def __init__(self, cin, cout, stride=1, p_drop=0.0):
        super().__init__()
        self.net = nn.Sequential(
            nn.Conv3d(cin, cout, 3, stride=stride, padding=1, bias=False),
            nn.InstanceNorm3d(cout, affine=True), nn.LeakyReLU(0.01, inplace=True),
            nn.Dropout3d(p_drop) if p_drop > 0 else nn.Identity(),
            nn.Conv3d(cout, cout, 3, padding=1, bias=False),
            nn.InstanceNorm3d(cout, affine=True), nn.LeakyReLU(0.01, inplace=True),
        )

    def forward(self, x):
        return self.net(x)


class UNet3D(nn.Module):
    def __init__(self, in_ch=1, n_classes=4, base=12, levels=4, p_drop=0.0, max_ch=96):
        super().__init__()
        self.hparams = dict(in_ch=in_ch, n_classes=n_classes, base=base, levels=levels, p_drop=p_drop,
                            max_ch=max_ch)
        chs = [min(base * 2 ** i, max_ch) for i in range(levels)]
        self.enc = nn.ModuleList()
        c = in_ch
        for i, ch in enumerate(chs):
            self.enc.append(ConvBlock(c, ch, stride=1 if i == 0 else 2, p_drop=p_drop if i > 0 else 0))
            c = ch
        self.up = nn.ModuleList()
        self.dec = nn.ModuleList()
        for i in range(levels - 1, 0, -1):
            self.up.append(nn.ConvTranspose3d(chs[i], chs[i - 1], 2, stride=2))
            self.dec.append(ConvBlock(chs[i - 1] * 2, chs[i - 1], p_drop=p_drop))
        self.head = nn.Conv3d(chs[0], n_classes, 1)

    def forward(self, x):
        skips = []
        for e in self.enc:
            x = e(x)
            skips.append(x)
        x = skips.pop()
        for up, dec in zip(self.up, self.dec):
            x = up(x)
            s = skips.pop()
            if x.shape[2:] != s.shape[2:]:
                x = F.interpolate(x, size=s.shape[2:], mode="trilinear", align_corners=False)
            x = dec(torch.cat([x, s], 1))
        return self.head(x)


def n_params(m):
    return sum(p.numel() for p in m.parameters())


# ----------------------------------------------------------------------------- losses
def soft_dice_loss(logits, target, n_classes, ignore_index=255, eps=1e-5, include_bg=False):
    p = torch.softmax(logits, 1)
    valid = (target != ignore_index).unsqueeze(1).float()
    t = target.clone()
    t[t == ignore_index] = 0
    oh = F.one_hot(t.long(), n_classes).permute(0, 4, 1, 2, 3).float()
    p, oh = p * valid, oh * valid
    dims = (0, 2, 3, 4)
    inter = (p * oh).sum(dims)
    den = p.sum(dims) + oh.sum(dims)
    dice = (2 * inter + eps) / (den + eps)
    if not include_bg:
        dice = dice[1:]
    return 1 - dice.mean()


def focal_ce(logits, target, gamma=2.0, weight=None, ignore_index=255):
    ce = F.cross_entropy(logits, target.long(), weight=weight, ignore_index=ignore_index, reduction="none")
    if gamma == 0:
        return ce[target != ignore_index].mean()
    pt = torch.exp(-ce)
    return (((1 - pt) ** gamma) * ce)[target != ignore_index].mean()


def boundary_weight_map(target, n_classes, w=2.0, ignore_aware: bool = False):
    """Voxels whose 3×3×3 neighbourhood contains another class get weight (1+w).

    ``ignore_aware`` (review ML-09): the ignore label 255 is not a class, so a voxel next to ignored voxels is not
    a boundary. Default False keeps the behaviour that trained the Gen-0 models (needed for consistent seeds)."""
    t = target.float().unsqueeze(1)
    if ignore_aware:
        ign = t == 255
        mx = F.max_pool3d(torch.where(ign, torch.full_like(t, -1.0), t), 3, 1, 1)
        mn = -F.max_pool3d(-torch.where(ign, torch.full_like(t, 1e4), t), 3, 1, 1)
        b = (mx != mn) & (mx >= 0) & (mn < 1e4)
        return 1.0 + w * b.float().squeeze(1)
    mx = F.max_pool3d(t, 3, 1, 1)
    mn = -F.max_pool3d(-t, 3, 1, 1)
    return 1.0 + w * (mx != mn).float().squeeze(1)


def combined_loss(logits, target, n_classes, cfg):
    loss = 0.0
    if cfg.get("dice", 1.0):
        loss = loss + cfg.get("dice", 1.0) * soft_dice_loss(logits, target, n_classes)
    gamma = cfg.get("focal_gamma", 0.0)
    if cfg.get("boundary_w", 0.0) > 0:
        ce = F.cross_entropy(logits, target.long(), ignore_index=255, reduction="none")
        bw = boundary_weight_map(target, n_classes, cfg["boundary_w"], cfg.get("boundary_ignore_aware", False))
        m = target != 255
        loss = loss + cfg.get("ce", 1.0) * (ce * bw)[m].mean()
    else:
        loss = loss + cfg.get("ce", 1.0) * focal_ce(logits, target, gamma)
    return loss
