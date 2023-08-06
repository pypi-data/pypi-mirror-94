"""
Copyright (c) 2019-2020 Patrice Ferlet

Permission is hereby granted, free of charge, to any person obtaining a copy
of this software and associated documentation files (the "Software"), to deal
in the Software without restriction, including without limitation the rights
to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
copies of the Software, and to permit persons to whom the Software is
furnished to do so, subject to the following conditions:

The above copyright notice and this permission notice shall be included in all
copies or substantial portions of the Software.

THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
SOFTWARE.


Video Generator package
=======================

Provides generators for video sequence that can be injected in Time Distributed layer.

It is made to provide several types of sequences:

- Frames from video
- Sliding samples of frame from video
- Optical Flow variation

So the package provides 3 classes. The mother class is VideoFrameGenerator,
and the other ones inherits from it.

Each generator can use ImageDataGenerator from keras to make data augmentation,
and takes common params as `nb_frames`, `batch_size`, and so on.

The goal is to provide ``(BS, N, W, H, C)`` shape of data where:

- ``BS`` is the batch size
- ``N`` is the number of frames
- ``W`` and ``H`` are width and height
- ``C`` is the number of channels (1 for gray scale, 3 for RGB)

For example ``(16, 5, 224, 224, 3)`` is a batch of 16 sequences where
sequence has got 5 frames sized to ``(224, 224)`` in RGB.

"""

__version__ = "1.0.0"

from . import generator

FrameGenerator = generator.FrameGenerator
