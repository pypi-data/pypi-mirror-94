Change Log
----------

..
   All enhancements and patches to django_occupations will be documented
   in this file.  It adheres to the structure of https://keepachangelog.com/ ,
   but in reStructuredText instead of Markdown (for ease of incorporation into
   Sphinx documentation and the PyPI description).

   This project adheres to Semantic Versioning (https://semver.org/).

.. There should always be an "Unreleased" section for changes pending release.

Unreleased
~~~~~~~~~~

Refer to the "Roadmap" section of the README.

[0.2.2] 2021-02-10
~~~~~~~~~~~~~~~~~~

* Makes the ONetAlternateTitles-to-SOCOccupations relationship many-to-many. This better matches the ONET taxonomy.  
* You must migrate after upgrading.  


[0.2.1] 2020-06-19
~~~~~~~~~~~~~~~~~~

* Adds name field to SOCHighLevelAggregationGroup model.
* Removes directtitlematch model.  
* You must migrate after upgrading.  


[0.2.0] 2020-06-13
~~~~~~~~~~~~~~~~~~

* Adds ONet models for Occupations and Alternate Titles.  
* You must migrate after upgrading.  


[0.1.0] 2020-06-06
~~~~~~~~~~~~~~~~~~

* First release on PyPI.  
* Defines SOC models.  
