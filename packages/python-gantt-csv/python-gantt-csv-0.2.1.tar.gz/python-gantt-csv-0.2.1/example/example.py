#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import datetime
from pathlib import Path

import gantt

from gantt_csv import create_project_from_csv, RESOURCES


YMD_VACATIONS = [
    (2014, 12, 30),
    (2014, 12, 31),
    (2015, 1, 1),
    (2015, 1, 2),
]


# Change font default
gantt.define_font_attributes(fill='black',
                             stroke='black',
                             stroke_width=0,
                             font_family="Verdana")

# Add vacations for everyone
for year, month, date in YMD_VACATIONS:
    gantt.add_vacations(datetime.date(year, month, date))

# Create project from csv files
projects = []
for csv_path in Path('.').glob('*.csv'):
    p1 = create_project_from_csv(csv_path)
    projects.append(p1)

# Create parent project
parent_project = gantt.Project(name='Parent Project')
# which contains the other projects
for project in projects:
    parent_project.add_task(project)

# MAKE DRAW
parent_project.make_svg_for_tasks(filename='test_full.svg',
                                  today=datetime.date.today(),
                                  start=datetime.date(2014, 12, 20),
                                  end=datetime.date(2015, 2, 20))
parent_project.make_svg_for_resources(filename='test_resources.svg',
                                      today=datetime.date.today(),
                                      resources=tuple(RESOURCES.values()))
parent_project.make_svg_for_tasks(filename='test_weekly.svg',
                                  today=datetime.date.today(),
                                  scale=gantt.DRAW_WITH_WEEKLY_SCALE)
