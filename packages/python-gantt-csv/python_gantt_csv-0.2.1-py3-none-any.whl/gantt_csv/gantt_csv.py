#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""python-gantt-csv manages the arguments of gantt.Task in csv format and
resolves dependencies between tasks. You will be able to edit tasks
without worrying about the order in which you define them.


Author : Shota Horie - horie.shouta at gmail.com


Licence : GPL v3 or any later version


This program is free software: you can redistribute it and/or modify
it under the terms of the GNU General Public License as published by
the Free Software Foundation, either version 3 of the License, or
any later version.

This program is distributed in the hope that it will be useful,
but WITHOUT ANY WARRANTY; without even the implied warranty of
MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
GNU General Public License for more details.

You should have received a copy of the GNU General Public License
along with this program.  If not, see <http://www.gnu.org/licenses/>.

"""


import csv
import datetime
import re
from collections import OrderedDict
from pathlib import Path
from typing import Dict, List, NamedTuple, Optional

import gantt    # type: ignore


__author__ = 'Shota Horie (horie.shouta at gmail.com)'
__version__ = '0.2.1'


RESOURCES: dict = {}


class TaskArgs(NamedTuple):
    """Arguments for gantt.Task"""
    name: str
    start: str
    depends_of: str
    duration: int
    percent_done: int
    resources: str
    color: str
    id: str


TaskArgsList = List[TaskArgs]
Gantt_Resources = List[gantt.Resource]


def decode_start(start: str) -> datetime.date:
    """Decode start date string from iso format..

    Args:
        start (str): ISO format date string.
            Exceptionally, 'today' is accepted and returns today's date.

    Returns:
        datetime.date: The date the project starts

    Raises:
        ValueError: Raises when string format is invalid.
    """
    if start == "today":
        return datetime.date.today()

    match_isodate = re.compile(r"[\d]+-[\d]+-[\d]+")
    m = match_isodate.search(start)
    if m:
        yeay, month, day = [int(s) for s in start.split('-')]
        return datetime.date(yeay, month, day)
    raise ValueError(f'{start} must be hyphen separated string or "today".')


def decode_depends_of(depends_of: str) -> List[str]:
    """Decode depends_of split by separator character."""
    SEPARATOR_CHARACTER = ':'
    if depends_of == "None":
        return []
    if not depends_of.count(SEPARATOR_CHARACTER):
        return [depends_of]
    return depends_of.split(SEPARATOR_CHARACTER)


def decode_percent_done(percent_done: str) -> int:
    """Decode percent_done."""
    return int(percent_done)


def decode_duration(duration: str) -> int:
    """Decode duration."""
    return int(duration)


def decode_resources(resources: str) -> Gantt_Resources:
    """Decode resource names split by separator character
    and create Resource object.
    """
    SEPARATOR_CHARACTER = ':'
    if resources == 'None':
        return []
    if not resources.count(SEPARATOR_CHARACTER):
        return [get_resource(resources)]
    return [get_resource(key) for key in resources.split(SEPARATOR_CHARACTER)]


def decode(row: dict) -> dict:
    """Decode gantt_Task arguments form csv format."""
    new_row = row.copy()
    for key in row:
        if key == 'name':
            pass
        if key == 'start':
            new_row[key] = decode_start(row[key])
        if key == 'depends_of':
            new_row[key] = decode_depends_of(row[key])
        if key == 'duration':
            new_row[key] = decode_duration(row[key])
        if key == 'percent_done':
            new_row[key] = decode_percent_done(row[key])
        if key == 'resources':
            new_row[key] = decode_resources(row[key])
        if key == 'color':
            pass
        if key == 'id':
            pass
    return new_row


def append_order(task_args: TaskArgs, order: int) -> dict:
    """Append order number."""
    new_task_args = task_args._asdict()
    new_task_args["order"] = order
    return new_task_args


def remove_order(task_args: dict) -> dict:
    """Inplace operation"""
    task_args.pop("order")
    return task_args


def get_task_by_id(id_: str, task_args_list: List[dict]) -> Optional[dict]:
    """Get task by id."""
    for task_args in task_args_list:
        if task_args["id"] == id_:
            return task_args
    return None


def get_dependent_tasks(task_args: dict,
                        task_args_list: List[dict]) -> List[dict]:
    """Get dependent tasks."""
    dependent_tasks = []
    for id_ in task_args["depends_of"]:
        task = get_task_by_id(id_, task_args_list)
        if task:
            dependent_tasks.append(task)
    return dependent_tasks


def get_highest_dependent_order(dependent_tasks: List[dict]) -> int:
    """Get highest order number."""
    dependent_orders = [task["order"] for task in dependent_tasks]
    if not dependent_orders:
        return 0
    return sorted(dependent_orders)[-1]


def set_task_order(task_args_list: List[dict]) -> List[dict]:
    """Set number to order objects.

    Args:
        task_args_list (List[dict]): A list of gantt.Task arguments

    Returns:
        List[dict]: A list of gantt.Task arguments with order
    """
    new_task_args_list = task_args_list.copy()
    for task_args in new_task_args_list:
        dependent_tasks = get_dependent_tasks(task_args, new_task_args_list)
        highest_order = get_highest_dependent_order(dependent_tasks)
        if highest_order != 0:
            task_args["order"] = highest_order + 1
    return new_task_args_list


def sort_tasks(task_args_list: TaskArgsList) -> TaskArgsList:
    """Order objects referenced by other objects so that they come first.

    Args:
        task_args_list (TaskArgsList): A list of gantt.Task arguments

    Returns:
        TaskArgsList: A sorted list of gantt.Task arguments
    """
    new_task_args_list = [append_order(task_args, i)
                          for i, task_args in enumerate(task_args_list)]
    set_task_order(new_task_args_list)
    new_task_args_list.sort(key=lambda x: x["order"])
    new_task_args_list = [remove_order(task_args)
                          for task_args in new_task_args_list]
    return [TaskArgs(**task_args) for task_args in new_task_args_list]


def create_task(task_args: TaskArgs,
                task_id_map: Dict[str, gantt.Task]) -> gantt.Task:
    """Create gantt.Task object and add to task_id_map in place.
    task_id_map is used to retrieve dependent tasks.
    """
    new_task_args = task_args._asdict()
    keys = ['name', 'start', 'depends_of', 'duration',
            'percent_done', 'resources', 'color']
    kw = {key: new_task_args[key] for key in keys}

    if not kw["resources"]:
        kw["resources"] = None

    if not kw["depends_of"]:
        kw["depends_of"] = None
    else:
        # Convert from id string to gantt.Task object
        kw["depends_of"] = [task_id_map[id_] for id_ in kw["depends_of"]]
    return gantt.Task(**kw)


def create_tasks(task_args_list: TaskArgsList) -> List[gantt.Task]:
    """Create objects that are referenced by other objects first.

    Args:
        task_args_list (TaskArgsList): A list of gantt.Task arguments

    Returns:
        List[gantt.Task]: A list of gantt.Task
    """
    task_id_map: Dict[str, gantt.Task] = OrderedDict()
    for task_args in task_args_list:
        task_id_map[task_args.id] = create_task(task_args, task_id_map)
    return list(task_id_map.values())


def parse_csv_task(filename: Path) -> TaskArgsList:
    """Read the arguments from the csv file.

    Args:
        filename (Path): csv file path

    Returns:
        TaskArgsList: A list of gantt.Task arguments
    """
    data = []
    with open(filename, 'r', encoding='utf-8') as f:
        reader = csv.reader(f)
        header = reader.__next__()
        for row in reader:
            row_dict: Dict[str, str] = OrderedDict()
            row_dict.update(zip(header, row))
            data.append(TaskArgs(**decode(row_dict)))
    return data


def create_project_from_csv(filename: Path) -> gantt.Project:
    """Create tasks from the arguments read from the csv file and
    organize them into a project.

    Args:
        filename (Path): csv file path

    Returns:
        gantt.Project: gantt.Project
    """
    # Create a project
    p1 = gantt.Project(name=filename.stem)

    # Load csv
    tasks = parse_csv_task(filename)

    # Create Tasks
    Tasks = create_tasks(sort_tasks(tasks))
    for Task in Tasks:
        p1.add_task(Task)
    return p1


def get_resource(name: str) -> gantt.Resource:
    """The same name returns the same object

    Args:
        name (str): resource name

    Returns:
        gantt.Resource: Resources identified by name
    """
    if RESOURCES.get(name):
        return RESOURCES.get(name)

    RESOURCES[name] = gantt.Resource(name)
    return RESOURCES[name]
