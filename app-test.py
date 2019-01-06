from app import app
from todo import *

import unittest


class BasicTestCase(unittest.TestCase):

# describe('an empty todo list', function() {
  # it('returns an empty html list', function() {
    # expect(new TodoListView([]).render()).to.equal('<ul class="todo-list"></ul>');
  # });
# });
    def test_an_empty_todo_list(self):
        view = TodoListView([])
        self.assertEqual(view.render(), '<ul class="todo-list"></ul>')

    def test_index(self):
        tester = app.test_client(self)
        response = tester.get('/', content_type='html/text')
        self.assertEqual(response.status_code, 200)


if __name__ == '__main__':
    unittest.main()
