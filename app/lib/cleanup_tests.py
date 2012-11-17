#!/usr/bin/env python
#-=- encoding: utf-8 -=-

import unittest
#import cleanup
from cleanup import *
from hashlib import md5
import os

class TasksTests(unittest.TestCase):

    def testAdd(self):
        """ Add a 'test' task"""
        _now = str(datetime.datetime.now())
        Tasks.create(
                name='test',
                md5hash=md5('test'+_now).hexdigest())
        _t = Tasks.get(name='test')
        self.failUnless(_t.name == 'test')
        self.failUnless(_t.md5hash == md5('test'+_now).hexdigest())
        self.failUnless(_t.project.name == DEFAULTPROJECT)
        self.failUnless(_t.status.name == DEFAULTSTATUS)


    def testRename(self):
        """ Rename 'test' to 'Test'"""
        _t1 = Tasks.get(name='test')
        _t1.rename('Test')
        _t2 = Tasks.get(name='Test')
        self.failUnless(_t2.name == 'Test')
        self.failUnless(_t2.md5hash == _t1.md5hash)
        self.failUnless(_t2.project.name == DEFAULTPROJECT)
        self.failUnless(_t2.status.name == DEFAULTSTATUS)

    def testChangePos(self):
        """ Move 'Test' to pos 1"""
        _t = Tasks.get(name='Test')
        _t.position = 1
        _t.save()
        self.failUnless( _t.position == 1)

    def testDelete(self):
        """ Delete 'Test' from the list"""
        _t = Tasks.get(name='Test')
        _count = _t.delete_instance()
        self.failUnless(_count == 1)

class RepoTest(unittest.TestCase):
    # FIXME: remove directories at the end
    """ Test repo can be hg or git """
    def testOpenRepo(self):
        """ Test opening a repo"""
        Repo('/tmp/hg_test', 'hg')
        self.failUnless( os.path.exists('/tmp/hg_test'))
        self.failUnless( os.path.exists('/tmp/hg_test/.hg'))
        Repo('/tmp/git_test', 'git')
        self.failUnless( os.path.exists('/tmp/git_test'))
        self.failUnless( os.path.exists('/tmp/git_test/.git'))

    def testAddFile(self):
        """ Test adding a file to the repo"""
        _r = Repo('/tmp/hg_test', 'hg')
        with open('/tmp/hg_test/TestFile', 'w') as f:
            f.write("UNITTEST")
        _r.add_file('/tmp/hg_test/TestFile')
        self.failUnless( os.path.exists('/tmp/hg_test/TestFile'))
        _r = Repo('/tmp/git_test', 'git')
        with open('/tmp/git_test/TestFile', 'w') as f:
            f.write("UNITTEST")
        _r.add_file('/tmp/git_test/TestFile')
        self.failUnless( os.path.exists('/tmp/git_test/TestFile'))

    def testrmFile(self):
        """ Test removing a file from the repo"""
        pass
    
class ProjectTest(unittest.TestCase):
    """ Test project with a wiki and task db and task files"""

    def testCreate(self):
        pass

    def testRename(self):
        pass

    def testListTasks(self):
        pass

    def testAddDocuments(self):
        pass

if __name__ == '__main__':
    unittest.main()
