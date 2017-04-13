#!/bin/bash

echo [+]  Automated Harvester [+]
echo  Please enter target domain as so: example.com
read domain
echo  Please enter the source to extract data. It must be one 
echo of the following:
echo ------------------------------------------------------------------
echo google, googleCSE, bing, bingapi, pgp, linkedin,
echo google-profiles, people123, jigsaw, twitter, googleplus, all
echo ------------------------------------------------------------------ 
read source
echo Running....

python theHarvester.py -d $domain -b $source
