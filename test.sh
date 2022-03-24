#!/bin/sh
# -*- coding: utf-8 -*-
# ./test.sh

install_dependencies() {
  ./pprint_center "Installing required packages"
  pip install pytest pytest-html pytest-cov flake8 "genbadge[all]"
}

run_pytest_coverage(){
  ./pprint_center "Running pytest and Generating XML, HTML, and Coverage Reports"
  pytest src --junitxml=reports/junit/junit.xml --html=reports/junit/report.html --cov-config=.coveragerc \
  --cov=src --cov-report xml:reports/coverage/coverage.xml --cov-report html:reports/coverage/htmlcov
}

run_flake8() {
  if [ -e reports/flake8/flake8stats.txt ]
  then
    ./pprint_center "Removing old flake8stats.txt"
    rm ./reports/flake8/flake8stats.txt
  fi
  ./pprint_center "Generating flake8 HTML"
  flake8 . --exit-zero --count --select=E9,F63,F7,F82 --output-file ./reports/flake8/flake8stats.txt --format=html \
  --htmldir ./reports/flake8
}

generate_badges(){
  ./pprint_center "Generating Tests Badge"
  genbadge tests
  ./pprint_center "Generating Coverage Badge"
  genbadge coverage
  ./pprint_center "Generating flake8 Badge"
  genbadge flake8
}


install_dependencies
run_pytest_coverage
run_flake8
generate_badges
