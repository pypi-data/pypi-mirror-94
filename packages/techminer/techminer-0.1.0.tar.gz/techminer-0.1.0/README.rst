Analysis of bibliographic datasets using Python
============================================================================================

*TechMiner* is a package for mining relevant information about topics related to Research and 
Development (R&D) literature extracted from bibliographical databases as Scopus. *TechMiner*
facilitates studies of systematic mapping of literature and Tech mining studies. The package can 
be used by users with basic knowledge of Python programming. However, users with advanced 
knowledge in programming and text mining can easily incorporate their codes to maximize the power 
of the library and develop advanced analysis. The package can be used to:

* Realize analyzes based on document-by-term pattern, for example, number of documents by author, by source or by keyword. 

* Calculate and plot the number of documents or citations by year.

* Realize analyzes based on term-by-term pattern, for example, number of documents by keywords and by author, by keyword and by year and so on.

* Compute and plot co-ocurrence, correlation and autocorrelation matrices.

* Realize Principal Component Analysis to detect and analyze clusters of data.

* Plot heatmaps, networks and many other types of plots for analyzing data.

*TechMiner* is an open source (distributed under the MIT license) and friendly-user
package developed and tested in Python version 3.6. 

*TechMiner* runs on top of Jupyter Lab and Google Colaboratory with its own
graphical user interfase. This feature allows to new user to run *TechMiner* 
easily. This is particulary benefical because of the large number of analysis
functions that the tool has. Due to the design of the package, it is easy 
to use techMiner with the tools available in the ecosystem
of open source tools.



Getting Started
---------------------------------------------------------

The current stable version can be installed from the command line using:

.. code:: bash

    $ pip install techminer


The current development version can be installed by clonning the GitHub repo 
`<https://github.com/jdvelasq/techminer>`_ and executing 

.. code:: bash

    $ python3 setup.py install develop

at the command prompt.

To run the *TechMiner* GUI, the user must execute

.. code:: python

    from techminer.app import App

    App().run()


in a cell of Jupiter Lab or Google Colaboratory.



Release Information
---------------------------------------------------

* **Author**:

    | Prof. Juan David Velásquez-Henao, MSc, PhD
    | Universidad Nacional de Colombia, Sede Medellín.
    | jdvelasq@unal.edu.co


* **Date**: 

    February 01, 2021  **Version**: 0.0.0

* **Binary Installers:** 
   
    `<https://pypi.org/project/techminer>`_

* **Source Repository**: 

    `<https://github.com/jdvelasq/techminer>`_

* **Documentation**: 

    `<https://jdvelasq.github.io/techminer/>`_


Table of Contents
------------------------------------------------------------------------------------------

.. toctree::
   :maxdepth: 2

   tutorial/index

.. toctree::
   :maxdepth: 2

   modules

* :ref:`genindex`
* :ref:`modindex`
* :ref:`search`

MIT license
-------------------------------------------------------------------------------

Copyright (c) 2021 Juan David Velásquez-Henao

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
