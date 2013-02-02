#!/usr/bin/env python
import sys
sys.path.extend(['lib'])
from webui_cleanup import is_logged
from bottle import request
from bottle import view, redirect, url
from bottle import post, get
from cleanup import Projects, Statuses, Tasks
from orgapp_globals import o, auth, is_ajax


t = Tasks()


def make_tasks_menu():
    """menus for tasks"""
    menu = []
    if is_logged():
        menu.append(
            {'url': url("add_task"), 'title': "Add tasks"})
    return(menu)


@get('/tasks', name='tasks')
@get('/')
@view('tasks/list_tasks')
def list_tasks():
    menu = make_tasks_menu()
    statuses = Statuses.select()
    tasks_list = {}
    for s in statuses:
        tasks_list[s.name] = t.select().where(Tasks.status == s)
    return(
        dict(
        tasks_list=tasks_list,
        statuses=statuses,
        title="Task list",
        leftmenu=menu,
        project=None))


@get('/tasks/add', name='add_task')
@view('tasks/tasks_add')
def add_task():
    _redirect = '/tasks/add',
    auth.require(
        role='edit',
        fail_redirect='/login?redirect=' + _redirect[0])
    menu = make_tasks_menu()
    statuses = Statuses.select()
    print [x.name for x in statuses]
    projects = Projects.select()
    print [x.name for x in projects]
    return(dict(title="Add task",
        leftmenu=menu,
        project=None,
        projects=projects,
        statuses=statuses))


@post('/tasks/add')
def create_task():
    auth.require(role='edit', fail_redirect='/login')
    name = request.forms.name
    description = request.forms.description
    #position = request.forms.position
    status = request.forms.status
    project = request.forms.project
    # do something with tasklists
    #t.create(name, position, status)
    print "name: " + name
    print "projects :" + str(o[project])
    print "project path: " + o[project].r.path
    o.add_task(name, status, description, project)
    redirect('/tasks')


@post('/tasks/<tid>/update')
@get('/tasks/<tid>/update')
def update_task(tid):
    auth.require(role='edit', fail_redirect='/login')
    new_pos = request.query.new_pos
    new_status = request.query.new_status
    #new_description = request.query.description
    # change status before position, moving position is relative to statuses
    # FIXME: reduce number of commits/writes
    if new_status != 'null':
        _count = o.count_tasks_by_status(tid)
        o.set_position(tid, _count - 1)
        o.set_status(tid, new_status)
        _count = o.count_tasks_by_status(tid)
        o.force_position(tid, _count - 1)
    o.set_position(tid, new_pos)
    #t.description(tid, new_description)


@post('/tasks/<tid>/update/ajax')
@is_ajax
def update_task_ajax(tid):
    auth.require(role='edit', fail_redirect='/login')
    o.set_title(tid, request.query.title)
    o.set_description(tid, request.query.description)
    print request.query.title
    print request.query.description
    # TODO add possibility to change project too


@get('/sync/tasks')
def get_tasks_to_sync():
    """The server renders a json of tasks he has to give
    ie: {'status': [{'id': 0, ...},] }
    """
    return t.get_unsynced()


@get('/sync/tasks/<guid>')
def get_task_from_guid(guid):
    """API to get one task's datas"""
    return t.get_from_guid(guid)


@get('/sync/faketasks')
def get_faketasks_to_sync():
    return {"b675228bf0aceac1fc64efe0d7bb207f": "2012-08-21 10:36:48"}


@get('/sync/to_sync')
def show_to_sync():
    auth.require(role='edit', fail_redirect='/login')
    return {'local': t.sync_tasks()[0], 'remote': t.sync_tasks()[1]}


@get('/sync/conflicts')
def sync_conflicts():
    """The client presents a page to handle tasks conflicts
    after comparing results from http://remote/sync/tasks and
    http://localhost/sync/tasks"""
    pass


@post('/sync/tasks/<guid>')
def post_tasks_to_sync(guid):
    """The client forces the server to get new list of tasks
    ie: {'status': [{'id': 0, ...},] }
    """
    #datas = request.post.data
    #print datas
    print dir(request.json.keys())
    auth.require(role='edit', fail_redirect='/login')
    t.save_from_json(request.json)
