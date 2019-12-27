import Assay
import Sample
import Microscope
```
"""This is an experimental user-interface for a largely motorized Olympus IX83
microscope using the Micro-manager Python API. 

The goal is to abstract out microscope functions, so that the microscope is
more aware of the experiment it is involved in, and so, can modify itself
during acquisition.

This is developed for fluorescence live cell microscopy.
"""

# Model API

# Scanning, recording data

# Biology and topology of the sample
# Images

# Sample analysis
# Adjustments to Microscope


scope = Microscope("config/Bright_Star.cfg")
scope.load()

# Useful to load default edges in positions and other parameters
# Max Z and XY allowed for objective to avoid damages

sample = Sample("35mm_IX3-HOW")

# Be more stringent with photon budget

sample.alive(True)

# Profiles of plasmids can be created that will determine channels
# to image on their own, and also allows for context dependent
# assays, such as cell cycle assay, because of PCNA-cb.

sample.add_plasmid("H2B-EGFP")
sample.add_plasmid("PCNA-cb")

# Assay has control over the scope, has access to images from sample
# - shading
# - dark
# - focus map
# - drifts - stage, focus
# - photobleaching correction
# - cell health and confluency mapping
# - colocalization between fields
# - cell cycle features - mitotic, sphase

assay = Assay(scope, sample)
assay.load(["all"])


# a fuzzy lapse can be introduced, that does time-conscious timelapse,
# with invidual position running its own time settings, with assay giving the
# que to exit timelapse.
# assay here has a measuring role, where it records the data for estimation

scope.explore(name="testrun",
              sample=sample,
              pos=sample.pos.default,
              assay=assay)

# with the images stored by scope, run assay.
assay.run("testrun")

# assay is useful here for its calculated values, like tilt, but also to feed
# back onto the scope settings, such as exposure time, if bleaching correction
# is included.


scope.scan(name="sphase", pos=assay.pos.sphase, assay=assay)
scope.scan(name="not_sphase", pos=assay.pos.not_sphase, assay=assay)
scope.timelapse(name="long_timelapse", groups=[
                "sphase", "not_sphase"], time=30, cycle=100)
scope.start(["long_timelapse"])
```
