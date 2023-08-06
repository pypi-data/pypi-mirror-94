Python-Gantt-Csv
====================

| python-gantt-csv manages the arguments of gantt.Task in csv format and resolves dependencies between tasks.
| You will be able to edit tasks without worrying about the order in which you define them.

Requirements
~~~~~~~~~~~~

This projects needs the following libraries:

-  python-gantt see http://xael.org/pages/python-gantt-en.html

Additionnal requirements
~~~~~~~~~~~~~~~~~~~~~~~~

Installation
~~~~~~~~~~~~

::

    pip install python-gantt-csv

Definition of Task Arguments in CSV Format
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

===============   ==============================================================
column name        valid value
===============   ==============================================================
name                str
start               'today' or iso format date (Ex: '2014-12-26')
duration           int
percent_done      int
resources          'None' or str or colon separated str (Ex: 'ANO:JLS')
depends_of         'None' or unique str or colon separated unique str (Ex: '1:2')
color               Hex color (Ex: #FF8080)
id                   unique str
===============   ==============================================================

Usage
-------

Directory structure

::

    .
    ├── example1.csv
    ├── example2.csv
    └── example.py

Run example

::

    python example.py


example1.csv
::

    name,start,depends_of,duration,percent_done,resources,color,id
    tache1,2014-12-25,None,4,44,ANO,#FF8080,1
    tache2,2014-12-28,None,6,0,JLS,#c70039,2
    tache3,2014-12-25,1:2:6,5,50,ANO:JLS,#f37121,3
    tache4,2015-01-01,1,4,40,JLS,#c0e218,4
    tache6,2014-12-25,6,4,0,ANO:JLS,#f37121,5
    tache7,2014-12-28,None,6,0,JLS,#c0e218,6
    tache8,today,6,4,0,ANO:JLS,#111d5e,7


example2.csv
::

    name,start,depends_of,duration,percent_done,resources,color,id
    tache5,2014-12-23,None,3,0,ANO:JLS,#f37121,1


example.py

::

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


Licence
-------

GPL v3 or any later version

Author
------

Shota Horie (horie.shouta at gmail.com)
