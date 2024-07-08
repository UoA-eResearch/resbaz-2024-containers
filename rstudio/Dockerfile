FROM rocker/verse:4.4

RUN install2.r --error --skipinstalled --repos https://cran.stat.auckland.ac.nz \
    janitor \
  && rm -rf /tmp/downloaded_packages
