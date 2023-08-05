# htmcatalog
Tool to query existing catalogs stored in Hierarchical Triangular Mesh format (htm)


# Installation


using pip

`pip install htmcatalog`
using git
```
git clone https://github.com/MickaelRigault/htmcatalog.git
cd htmcatalog
python setup.py install
```

dependencies: `HMpTy` (pip install it)[https://pypi.org/project/HMpTy/]



# Usage

if you know the depth of your HTM (say 7) and the location of the
directory containing the catalog split by htm tiles (say
~/data/catalog/)

then:

```python
from htmcatalog import htmquery
hq = htmquery.HTMQuery(7, "~/data/catalog/")
catdata = hq.fetch_cat(RA_deg,Dec_deg, radius_deg)
```

catdata is a multi-index DataFrame (level 0=htm tile, level 1 =
indiviual tile_catalog index)

