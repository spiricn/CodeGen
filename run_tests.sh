#!/bin/bash

export PYTHONPATH=`pwd`:$PYTHONPATH

pushd ./test

python Basic.py

python Advanced.py

python Nesting.py

popd

