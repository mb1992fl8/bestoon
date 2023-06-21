#! /bin/bash

# Please set these variables

BASE_URL=http://bestoon.ir
TOKEN=12345678

curl --data "token=$TOKEN&amount=$1&text=$2" $BASE_URL/submit/expense/
