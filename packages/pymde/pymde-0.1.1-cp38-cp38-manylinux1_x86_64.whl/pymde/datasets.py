"""Datasets

Module for downloading datasets.

The functions in this module return a Dataset instance. Each function
takes at least two arguments:

    root:
        path to directory in which data should be downloaded (default './')
    download:
        bool indicating whether to download data if not present
        (default True)
"""

import os

import numpy as np
from pymde.preprocess.graph import Graph
from pymde.problem import LOGGER
import scipy.sparse as sp
import torch
import torchvision


def _is_cached(root, files):
    return all(os.path.exists(os.path.join(root, fname)) for fname in files)


def _install_headers():
    # install simple header to bypass mod_security
    import urllib

    opener = urllib.request.build_opener()
    opener.addheaders = [("User-agent", "Mozilla/5.0")]
    urllib.request.install_opener(opener)


class Dataset(object):
    """Represents a dataset.

    Each instance has two main attrs:

        data:
            either a data matrix, or an instance of pymde.Graph; the
            data to be embedded.

        attributes:
            a dictionary whose values give attributes associated
            with the items in the data, such as the digit labels in MNIST.

    Other data that the dataset might carry is in the (dict) attribute
    `other_data`. Metadata about where the data came from is stored in
    `metadata`.
    """

    def __init__(self, data, attributes, other_data=None, metadata=None):
        self.data = data
        self.attributes = attributes
        self.other_data = other_data if other_data is not None else {}
        self.metadata = metadata if metadata is not None else {}

    @property
    def attribute(self):
        if len(self.attributes) == 1:
            return list(self.attributes.values())[0]


def MNIST(root="./", download=True) -> Dataset:
    """MNIST dataset (LeCun, et al.).

    The MNIST dataset contains 70,000, 28x28 images of handwritten digits.

    - ``data``: ``torch.Tensor`` with 70,000 rows, each of
      length 784 (representing the pixels in the image).
    - ``attributes`` dict: the key ``digits`` holds an array
      in which each entry gives the digit depicted in the corresponding row of
      ``data``.
    """
    mnist_train = torchvision.datasets.MNIST(
        root=root, train=True, download=download
    )
    mnist_test = torchvision.datasets.MNIST(
        root=root, train=False, download=download
    )

    images = torch.cat([mnist_train.data, mnist_test.data])
    digits = torch.cat([mnist_train.targets, mnist_test.targets])
    attributes = {"digits": digits}
    return Dataset(
        data=images.reshape(-1, 784),
        attributes=attributes,
        metadata={
            "authors": "LeCunn, et al.",
            "url": "http://yann.lecun.com/exdb/mnist/",
        },
    )


def google_scholar(root="./", download=True, full=False) -> Dataset:
    """Google Scholar dataset (Agrawal, et al.).

    The Google Scholar dataset contains an academic coauthorship graph: the
    nodes are authors, and two authors are connected by an edge if either
    author listed the other as a coauthor on Google Scholar. (Note that if
    two authors collaborated on a paper, but neither has listed the other
    as a coauthor on their Scholar profiles, then they will not be connected
    by an edge).

    If ``full`` is False, obtains a small version of the dataset, on roughly
    40,000 authors, each with h-index at least 50. If ``full`` is True,
    obtains the whole dataset, on roughly 600,000 authors. The full dataset
    is roughly 1GB in size.

    - ``data``: a ``pymde.Graph``, with nodes representing authors
    - ``attributes``: the ``coauthors`` key has an array holding the number
      of coauthors of each other, normalized to be a percentile.
    - ``other_data``: holds a dataframe describing the dataset, keyed by
      ``dataframe``.
    """

    try:
        import pandas as pd
    except ImportError:
        raise ImportError("Please install pandas.")

    root = os.path.expanduser(root)

    if not full:
        url = "https://akshayagrawal.com/scholar/google_scholar.tar.gz"
    else:
        url = "https://akshayagrawal.com/scholar/google_scholar_full.tar.gz"

    extract_root = os.path.join(root, "scholar/")
    data_file = os.path.join(extract_root, "scholar_graph.npz")
    dataframe_file = os.path.join(extract_root, "scholar_df.pkl")
    if not full:
        disciplines_dataframe_file = os.path.join(
            extract_root, "scholar_disciplines_df.pkl"
        )

    def load_dataset():
        data = Graph(sp.load_npz(os.path.join(root, data_file)))
        df = pd.read_pickle(os.path.join(root, dataframe_file))
        attributes = {"coauthors": df["coauthors_pct"]}
        if not full:
            disciplines_df = pd.read_pickle(
                os.path.join(root, disciplines_dataframe_file)
            )
            other_data = {"dataframe": df, "disciplines": disciplines_df}
        else:
            other_data = None
        metadata = {"authors": "Agrawal"}
        return Dataset(data, attributes, other_data, metadata)

    if not full:
        files = [
            data_file,
            dataframe_file,
            disciplines_dataframe_file,
        ]
    else:
        files = [
            data_file,
            dataframe_file,
        ]

    if _is_cached(root, files):
        LOGGER.info("Load cached dataset.")
        return load_dataset()

    if not download:
        raise RuntimeError("`download` is False, but data is not cached.")

    _install_headers()

    filename = url.rpartition("/")[2]
    torchvision.datasets.utils.download_and_extract_archive(
        url, download_root=root, extract_root=extract_root, filename=filename
    )
    os.remove(os.path.join(root, filename))
    LOGGER.info("Dataset is now available.")
    return load_dataset()


def covid19_scrna_wilk(root="./", download=True) -> Dataset:
    """COVID-19 scRNA data (Wilk, et al.).

    The COVID-19 dataset includes a PCA embedding of single-cell
    mRNA transcriptomes of roughly 40,000 cells, taken from some patients
    with COVID-19 infections and from healthy controls.

    Instructions on how to obtain the full dataset are available in the
    Wilk et al. paper: https://www.nature.com/articles/s41591-020-0944-y,

    - ``data``: the PCA embedding
    - ``attributes``: two keys, ``cell_type`` and ``health_status``.
    """
    root = os.path.expanduser(root)

    url = "https://akshayagrawal.com/scrna/scrna_covid19_wilk.tar.gz"

    extract_root = os.path.join(root, "scrna_covid19_wilk/")
    data_file = os.path.join(extract_root, "scrna_data_matrix.npy")
    cell_type_attr_file = os.path.join(extract_root, "scrna_cell_type_attr.npy")
    health_status_attr_file = os.path.join(
        extract_root, "scrna_health_status_attr.npy"
    )

    def load_dataset():
        data = np.load(os.path.join(root, data_file))
        attributes = {
            "cell_type": np.load(
                os.path.join(root, cell_type_attr_file), allow_pickle=True
            ),
            "health_status": np.load(
                os.path.join(root, health_status_attr_file), allow_pickle=True
            ),
        }
        metadata = {
            "authors": "Wilk, et al.",
            "url": "https://www.nature.com/articles/s41591-020-0944-y",
        }
        return Dataset(data, attributes, metadata=metadata)

    files = [
        data_file,
        cell_type_attr_file,
        health_status_attr_file,
    ]

    if _is_cached(root, files):
        LOGGER.info("Load cached dataset.")
        return load_dataset()

    if not download:
        raise RuntimeError("`download` is False, but data is not cached.")

    _install_headers()

    filename = url.rpartition("/")[2]
    torchvision.datasets.utils.download_and_extract_archive(
        url, download_root=root, extract_root=extract_root, filename=filename
    )
    os.remove(os.path.join(root, filename))
    LOGGER.info("Dataset is now available.")
    return load_dataset()
