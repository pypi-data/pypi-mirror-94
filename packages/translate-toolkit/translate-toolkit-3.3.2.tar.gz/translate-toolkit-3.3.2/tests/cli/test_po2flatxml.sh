#!/bin/bash

source $(dirname $0)/test.inc.sh

python $PYTHON_ARGS $(which po2flatxml) --progress=none $one $out
check_results
