#!/bin/bash
# export DATABASE_URL="postgresql://postgres@localhost:5432/postgres"
export DATABASE_URL="postgresql://postgres:tydelikeUdacity@localhost:5432/botwdb"
export TEST_DATABASE_URL="postgresql://postgres:tydelikeUdacity@localhost:5432/testbotwdb"
export EXCITED="true"

echo "setup.sh script executed successfully!"