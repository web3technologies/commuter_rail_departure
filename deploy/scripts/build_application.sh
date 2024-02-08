#!/bin/bash

echo "Creating the commuter_rail_departure Application"

rm -rf /applications/commuter_rail_departure/
mkdir /applications/commuter_rail_departure/

echo "BUILDING"

workspace_name="commuter_rail_departure"
jenkins_proj_path="/var/lib/jenkins/workspace/$workspace_name"
JENKINS_VENV_DIR=$jenkins_proj_path/venv 

python -m venv $JENKINS_VENV_DIR
echo "VENV created"
. "${JENKINS_VENV_DIR}/bin/activate"
pip install --upgrade pip
pip install $jenkins_proj_path .
pip install wheel
python setup.py bdist_wheel 
deactivate
echo "*** Commuter Rail Departure Created***"

echo "Building the application"
application_build_path=/applications/commuter_rail_departure.tar
python -m venv /applications/commuter_rail_departure/venv
. "/applications/commuter_rail_departure/venv/bin/activate"
pip install --upgrade pip
pip install wheel
pip install $jenkins_proj_path/dist/commuter_rail_departure-0.1.4-py3-none-any.whl
cp $jenkins_proj_path/src/manage.py /applications/commuter_rail_departure/
cp $jenkins_proj_path/src/commuter_rail_departure/wsgi.py /applications/commuter_rail_departure/
cp "/var/lib/jenkins/envs/commuter_rail_departure/.env" /applications/commuter_rail_departure/
echo "Application packages installed into Venv"

echo "Gzipping Application"
tar -czf /tmp/commuter_rail_departure.tar /applications/commuter_rail_departure/
