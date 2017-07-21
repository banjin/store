#!/bin/bash

cp tests/test_local_settings.py store/local_settings.py
# code coverage report
coverage run --omit=*/migrations/* manage.py test tests
test_result=$?
coverage report --omit=*/migrations/* --omit=tests/* --include=./*.py
coverage html --omit=*/migrations/* --omit=tests/* --include=./*.py --directory=coverage_report
mkdir -p $CIRCLE_ARTIFACTS/coverage_report/
mv coverage_report/* $CIRCLE_ARTIFACTS/coverage_report/

# code quality check
pylint -f parseable -d I0011,R0801 store > pylint.txt
mkdir -p $CIRCLE_ARTIFACTS/code_quality/
mv pylint.txt $CIRCLE_ARTIFACTS/code_quality/

if [ "X$test_result" = "X1" ];then
exit 1
fi