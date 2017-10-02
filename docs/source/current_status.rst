Current State
=============


Database model:
---------------


For detailed documentation of the database tables and fields click here.

What is still missing?
----------------------

Not all of the information found in HMDB is yet integrated into PyHMDB.

PyHMDB does not yet inlcude:
- Taxonomy information
- Spectra information
- Experimental properties (datamodel is implemented but tables will not get populated)
- Predicted properties (datamodel is implemented but tables will not get populated)
- Normal concentration
- Abnormal concentration

PyHMDB does yet lack funtions to:
- convert metabolite namespaces from and to HMDB identifiers
- convert disease namespaces from and to HMDB disease names
- query functions (only querying with metabolite identifiers for diseases and proteins and vice versa is supported right now)
