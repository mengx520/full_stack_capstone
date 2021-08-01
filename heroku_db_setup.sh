#!/bin/bash
export FLASK_APP=casting_agency.app
flask db init
flask db migrate -m "Initial migration"
flask db upgrade