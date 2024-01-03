#!/bin/bash
dropdb blogly
createdb blogly
psql blogly < blogly.sql
