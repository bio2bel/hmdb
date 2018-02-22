Current Status
==============
What is still missing?
----------------------
Not all of the information found in HMDB is yet integrated.

Bio2BEL HMDB does not yet include:
- Taxonomy information
- Spectra information
- Experimental properties (datamodel is implemented but tables will not get populated)
- Predicted properties (datamodel is implemented but tables will not get populated)
- Normal concentration
- Abnormal concentration

Bio2BEL HMDB still lacks functions to:
- convert metabolite namespaces from and to HMDB identifiers
- query functions (only querying with metabolite identifiers for diseases and proteins and vice versa is supported right now)

Roadmap
-------
The next steps in the development of Bio2BEL HMDB are:

1. add namespace mappings from metabolite HMDB identifiers to different databases/namespaces
2. add query functions for several tables and entries
#. change BEL enrichment functions to automatically work even when pathology nodes are not in HMDB disease namespace
#. include missing HMDB tables and relations listed above
#. maybe add parallelization to the database population to improve run time


