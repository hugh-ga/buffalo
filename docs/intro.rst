Introduction
============

Buffalo is a fast and scalable production-ready open source project for recommendation systems. Buffalo effectively utilizes system resources, enabling high performance even on low-spec machines. The implementation is optimized for CPU and SSD. Even so, it shows good performance with GPU accelerator, too. Buffalo, developed by Kakao, has been reliably used in production for various Kakao services.

Buffalo provides the following algorithms:

  - Alternating Least Squares (ALS)
  - Bayesian Personalized Ranking Matrix Factorization (BPR)
  - Word2Vec (W2V)
  - CoFactors (CFR)
  - Weighted Approximate Rank Pairwise (WARP), along with L2 distance variant (CML)
  - Probabilistic latent semantic indexing (pLSI)

ALS is one of the most famous matrix factorization models which decompose the observed user-item interaction matrix into user and item latent factors. One disitnguishing feature of the implementation of Buffalo ALS is that we offer both GPU based optimization and recently proposed [Block Coordinate Least Squares](https://arxiv.org/abs/2110.14044) which enable blazingly fast model training. More ranking optimized models are BPR and WARP. W2V and CFR mainly focus on the item co-occurrence data. Unlike other models, pLSI (a.k.a probabilistic latent semantic analysis) is a soft clustering module that performs a low-rank approximation of user-item matrix on the basis of their frequencies.

All algorithms are optimized for multi-threading and some support GPU accelerators.

One of the best things about this library is a very low memory usage compared to other competing libraries. With chunked data management and batch learning with HDF5, handling a large-scale data, even bigger than memory size on laptop machine, is made possible. Check out the benchmarks page for more details on Buffalo performance.

Plus, Buffalo provides a variety of convenient features for research and production purposes, such as tensorboard integration, hyper-parameter optimization and so on.


Installation
------------

Type `pip install buffalo`.


Requirements
^^^^^^^^^^^^
  - numpy
  - cython
  - n2
  - cmake


From source code
^^^^^^^^^^^^^^^^

.. code-block:: bash

    $> git clone -b master https://github.com/kakao/buffalo
    $> cd buffalo
    $> git submodule update --init
    $> pip install -r requirements.txt
    $> python setup.py install


Basic Usage
-----------
We highly recommend starting with the unit-test codes. Checkout ./tests directory, `./tests/algo/test_algo.py` will be a good starting point.

.. code-block:: bash

    $ buffalo.git/tests> nosetests ./algo/test_als.py -v


or

.. code-block:: bash

    $ buffalo.git/tests> pytest ./algo/test_als.py -v


Database
--------
We call term `database` as a data file format used by the buffalo internally. Buffalo take data that the Matrix Market or Stream format as input and converts it into a database class which store rawdata using h5py(http://www.h5py.org). The main reason to make custom database is to use the least amount of memory without compromising capacity of data volume and learning speed.

The Stream data format consists of two files:

  - main

    - Assumed that the data is reading history of users from some blog service, then each line is a reading history corresponding to each row of UID files. (i.e. users lists)
    - The reading history is separated by spaces, and the past is the left and the right is the most recent history.
    - e.g. `A B C D D E` means that a user read the contents in the order A B C D D E.

  - uid

    - Each line is repersentational value of a user corresponding to each row in the MAIN file (e.g. user name)
    - Do not allow spaces in each line

For Matrix Market format, please refer to https://math.nist.gov/MatrixMarket/formats.html.

  - main

    - Matrix Market data file.

  - uid

    - Each line is the actual userkey corresponding to the row id in the MM file.

  - iid

    - Each line is the actual itemkey corresponding to the column id in the MM file.

uid and iid are the data needed to provide human readable results only, not required.


Logging
-------
It is recommend to use the log library of buffalo for consistent log format.

.. code-block:: python

    >>> from buffalo.misc import log
    >>> print(log.NOTSET, log.WARN, log.INFO, log.DEBUG, log.TRACE)
    (0, 1, 2, 3, 4, 5)
    >>> log.set_log_level(log.WARN)  # this set log-level on Python, C++ both sides.
    >>> log.get_log_level()
    1
    >>>

    >>> from buffalo.misc import log
    >>> logger = log.get_logger()
    >>> with log.pbar(logger.debug, desc='Test', mininterval=1):
        for(i in range(100)):
            time.sleep(0.1)
