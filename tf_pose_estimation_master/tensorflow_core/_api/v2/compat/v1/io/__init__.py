# This file is MACHINE GENERATED! Do not edit.
# Generated by: tensorflow/python/tools/api/generator/create_python_api.py script.
"""Public API for tf.io namespace.
"""

from __future__ import print_function as _print_function

import sys as _sys

from . import gfile
from tensorflow.python.framework.graph_io import write_graph
from tensorflow.python.lib.io.tf_record import TFRecordCompressionType
from tensorflow.python.lib.io.tf_record import TFRecordOptions
from tensorflow.python.lib.io.tf_record import TFRecordWriter
from tensorflow.python.lib.io.tf_record import tf_record_iterator
from tensorflow.python.ops.data_flow_ops import PaddingFIFOQueue
from tensorflow.python.ops.data_flow_ops import PriorityQueue
from tensorflow.python.ops.data_flow_ops import QueueBase
from tensorflow.python.ops.data_flow_ops import RandomShuffleQueue
from tensorflow.python.ops.gen_decode_proto_ops import decode_proto_v2 as decode_proto
from tensorflow.python.ops.gen_encode_proto_ops import encode_proto
from tensorflow.python.ops.gen_image_ops import decode_and_crop_jpeg
from tensorflow.python.ops.gen_image_ops import decode_bmp
from tensorflow.python.ops.gen_image_ops import decode_gif
from tensorflow.python.ops.gen_image_ops import decode_jpeg
from tensorflow.python.ops.gen_image_ops import decode_png
from tensorflow.python.ops.gen_image_ops import encode_jpeg
from tensorflow.python.ops.gen_image_ops import extract_jpeg_shape
from tensorflow.python.ops.gen_io_ops import matching_files
from tensorflow.python.ops.gen_io_ops import read_file
from tensorflow.python.ops.gen_io_ops import write_file
from tensorflow.python.ops.gen_parsing_ops import decode_compressed
from tensorflow.python.ops.gen_parsing_ops import decode_json_example
from tensorflow.python.ops.gen_parsing_ops import parse_tensor
from tensorflow.python.ops.gen_parsing_ops import serialize_tensor
from tensorflow.python.ops.gen_string_ops import decode_base64
from tensorflow.python.ops.gen_string_ops import encode_base64
from tensorflow.python.ops.image_ops_impl import decode_image
from tensorflow.python.ops.image_ops_impl import is_jpeg
from tensorflow.python.ops.parsing_ops import FixedLenFeature
from tensorflow.python.ops.parsing_ops import FixedLenSequenceFeature
from tensorflow.python.ops.parsing_ops import SparseFeature
from tensorflow.python.ops.parsing_ops import VarLenFeature
from tensorflow.python.ops.parsing_ops import decode_csv
from tensorflow.python.ops.parsing_ops import decode_raw_v1 as decode_raw
from tensorflow.python.ops.parsing_ops import parse_example
from tensorflow.python.ops.parsing_ops import parse_sequence_example
from tensorflow.python.ops.parsing_ops import parse_single_example
from tensorflow.python.ops.parsing_ops import parse_single_sequence_example
from tensorflow.python.ops.sparse_ops import deserialize_many_sparse
from tensorflow.python.ops.sparse_ops import serialize_many_sparse
from tensorflow.python.ops.sparse_ops import serialize_sparse
from tensorflow.python.training.input import match_filenames_once

del _print_function
