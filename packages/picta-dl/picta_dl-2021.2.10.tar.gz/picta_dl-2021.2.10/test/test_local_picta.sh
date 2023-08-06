#!/usr/bin/env bash

# cd ..

# Let Errors
echo "No Exists, With Errors"
echo ""
python picta_dl/__main__.py -s https://www.picta.cu/medias/die-hart-1x01-2020-08-06-18-12-50-310131?playlist=96
echo ""
echo "Empty playlist"
python picta_dl/__main__.py -s -u "$USER" -p "$PASSWORD" https://www.picta.cu/medias/teaser-capitulo-1-2020-08-10-17-50-16-008651?playlist=130
echo ""

# Not Errors
set -e

echo "No Errors"
echo ""
echo "User PlayLists"
python picta_dl/__main__.py -s -u "$USER" -p "$PASSWORD" https://www.picta.cu/medias/fundamento-big-data-2020-08-09-19-47-15-230297?playlist=129
echo ""
echo "User PlayLists, No Playlist"
python picta_dl/__main__.py -s -u "$USER" -p "$PASSWORD" --no-playlist https://www.picta.cu/medias/fundamento-big-data-2020-08-09-19-47-15-230297?playlist=129
echo ""

echo "PlayList Embedded with videos"
python picta_dl/__main__.py -s https://www.picta.cu/medias/watchmen-s01e01-2019-10-29-12-40-23-392187
echo ""
echo "No PlayList options"
python picta_dl/__main__.py -s --no-playlist https://www.picta.cu/medias/watchmen-s01e01-2019-10-29-12-40-23-392187
echo ""

# Yes Errors
set +e

echo "Yes PlayList options, No Exists Playlist. With Error"
python picta_dl/__main__.py -s -u "$USER" -p "$PASSWORD" --playlist-start 5 https://www.picta.cu/medias/201-paradigma-devops-implementacion-tecnomatica-2020-07-05-22-44-41-299736?playlist=4441
echo ""

# Not Errors
set -e

echo "No PlayList options, Download Just the Video. No Error"
python picta_dl/__main__.py -s -u "$USER" -p "$PASSWORD" --no-playlist https://www.picta.cu/medias/201-paradigma-devops-implementacion-tecnomatica-2020-07-05-22-44-41-299736?playlist=4441
echo ""

echo "Movie URL path"
python picta_dl/__main__.py -s https://www.picta.cu/movie/phineas-ferb-pelicula-candace-universo-2020-08-28-21-00-32-857026
echo ""

echo "Run Test No Duplicates"
python -m unittest test.test_all_urls.TestAllURLsMatching.test_no_duplicates
echo ""

echo "Run Flake8 on Picta Extractor"
flake8 picta_dl/extractor/picta.py
echo "All done!"