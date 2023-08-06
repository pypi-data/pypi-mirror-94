====
Home
====

.. :Author: Yuanhua Huang
.. :Version: 0.2.0
.. :Last viewed: Jun 30, 2019

About Vireo
===========

This document gives an introduction and usage manual of Vireo (Variational 
inference for reconstructing ensemble origins), a Bayesian method to demultiplex
pooled scRNA-seq data without genotype reference.

Vireo is primarily designed demultiplexing cells into donors by modelling of
expressed alleles. It supports a variety of settings of donor genotype (from
entirely missing, to partially missing, to fully observed). See more details in
`manual`_ section.

As a general cell clustering methods by allelic ratio (equivalent to genotyping),
Vireo is applicable for more settings besides donor demultiplexing, including
reconstruction of somatic clones, see `vireoSNP_clones.ipynb`_ for example on 
mitochondral mutations.

.. _manual: https://vireosnp.readthedocs.io/en/latest/manual.html


Tutorials
=========
**donors**: `vireoSNP_donors.ipynb`_ gives example on donor deconvolution 
manually

**donors**: `donor_match.ipynb`_ gives example on aligning donors to other
omics data or other batches

**clones**: `vireoSNP_clones.ipynb`_ gives example on clone reconstruction on 
mitochondral mutations

.. _donor_match.ipynb: https://github.com/single-cell-genetics/vireo/blob/master/examples/donor_match.ipynb
.. _vireoSNP_donors.ipynb: https://github.com/single-cell-genetics/vireo/blob/master/examples/vireoSNP_donors.ipynb
.. _vireoSNP_clones.ipynb: https://github.com/single-cell-genetics/vireo/blob/master/examples/vireoSNP_clones.ipynb



Quick Resources
===============

**Latest version on GitHub**
https://github.com/single-cell-genetics/vireo

**Scripts for simulation**
https://github.com/single-cell-genetics/vireo/tree/master/simulate

**All releases**
https://pypi.org/project/vireoSNP/#history


Issue reports
=============
If you find any error or suspicious bug, we will appreciate your report.
Please write them in the github issues: 
https://github.com/single-cell-genetics/vireo/issues


References
==========

Yuanhua Huang, Davis J. McCarthy, and Oliver Stegle. `Vireo: Bayesian 
demultiplexing of pooled single-cell RNA-seq data without genotype reference 
<https://genomebiology.biomedcentral.com/articles/10.1186/s13059-019-1865-2>`_. 
\ **Genome Biology** \ 20, 273 (2019)

