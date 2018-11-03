#!/bin/bash

EXAMPLES="\
minimal \
styled \
cover \
fonts \
toc \
header-footer \
figures \
revisions \
numbering \
"

set -e
cd "$(dirname "$(readlink -f "${0}")")"/../examples/pdf

for EXAMPLE in $EXAMPLES
do
  cd $EXAMPLE
  ../../../doker/main.py --pdf $EXAMPLE
  cd ..
done
