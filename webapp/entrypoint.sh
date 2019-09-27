#!/bin/sh

cd webapp
yarn install

exec "$@"
