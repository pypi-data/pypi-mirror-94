=============================
scrapinghub-entrypoint-scrapy
=============================

Scrapy entrypoint for Scrapinghub job runner.

The package implements a base wrapper layer to extract job data from
environment, parse/prepare it properly and execute job using Scrapy
or custom executor.


Features
========

- parsing job data from environment
- processing job args and settings
- running a job with Scrapy
- collecting stats
- advanced logging & error handling
- full hubstorage support
- custom scripts support


Install
=======

::

    pip install scrapinghub-entrypoint-scrapy
