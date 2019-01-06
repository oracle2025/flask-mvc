import pytest
from todo import *
from app import app

@pytest.fixture
def DOM():
    from htmldom import htmldom
    dom = htmldom.HtmlDom()
    return dom.createDom("<div></div>")

@pytest.fixture
def myapp():
    return app.test_client()


def test_an_empty_todo_list():
    '''the todo list view :: an empty todo list :: returns an empty todo list'''
    view = TodoListView([])
    assert view.render() == '<ul class="todo-list"></ul>'

def test_a_list_of_one_element(DOM):
    '''the todo list view :: a list of one element :: renders as html'''
    # print TodoListView(['Pippo']).render()
    DOM.find('div').html(str(TodoListView(['Pippo']).render()))
    assert DOM.find('ul.todo-list li').text() == 'Pippo';

def test_index(myapp):
    '''the app :: the initial start page :: ensure it is empty'''
    response = myapp.get('/', content_type='html/text')
    assert response.status_code == 200
    assert response.data == ""
