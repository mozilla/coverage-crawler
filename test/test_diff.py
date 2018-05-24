# -*- coding: utf-8 -*-

import json

import diff


# diff.compare_objects(obj1, obj2) returns true if equall and false if different coverage
def test_compare_objects_same_coverage_same_functions():
    obj1 = json.loads('{"functions": [{"name": "func1", "start": 36, "exec": true}, {"name": "func2", "start": 64, "exec": false}], "branches": [], "name": "obj-firefox/dist/include/mozilla/dom/DOMRectListBinding.h", "coverage": [null, 2, null, null, 5], "source_digest": "another_generated_number_with_literals"}')
    obj2 = json.loads('{"functions": [{"name": "func1", "start": 36, "exec": true}, {"name": "func2", "start": 64, "exec": false}], "branches": [], "name": "obj-firefox/dist/include/mozilla/dom/DOMRectListBinding.h", "coverage": [null, 2, null, null, 5], "source_digest": "another_generated_number_with_literals2"}')
    assert diff.compare_source_files_objects(obj1, obj2) is None


def test_compare_objects_same_coverage_diff_functions():
    obj1 = json.loads('{"functions": [{"name": "func1", "start": 36, "exec": true}, {"name": "func2", "start": 64, "exec": true}], "branches": [], "name": "obj-firefox/dist/include/mozilla/dom/DOMRectListBinding.h", "coverage": [null, 2, null, null, 5], "source_digest": "another_generated_number_with_literals"}')
    obj2 = json.loads('{"functions": [{"name": "func1", "start": 36, "exec": true}, {"name": "func2", "start": 64, "exec": false}], "branches": [], "name": "obj-firefox/dist/include/mozilla/dom/DOMRectListBinding.h", "coverage": [null, 2, null, null, 5], "source_digest": "another_generated_number_with_literals2"}')
    assert diff.compare_source_files_objects(obj1, obj2) == {'branches': [], 'functions': [], 'coverage': [None, 0, None, None, 0], 'source_digest': 'another_generated_number_with_literals', 'name': 'obj-firefox/dist/include/mozilla/dom/DOMRectListBinding.h'}


def test_compare_objects_diff_coverage_same_func():
    obj1 = json.loads('{"functions": [{"name": "func1", "start": 36, "exec": true}, {"name": "func2", "start": 64, "exec": false}], "branches": [], "name": "obj-firefox/dist/include/mozilla/dom/DOMRectListBinding.h", "coverage": [null, 2, null, null, 5], "source_digest": "another_generated_number_with_literals"}')
    obj2 = json.loads('{"functions": [{"name": "func1", "start": 36, "exec": true}, {"name": "func2", "start": 64, "exec": false}], "branches": [], "name": "obj-firefox/dist/include/mozilla/dom/DOMRectListBinding.h", "coverage": [null, 2, null, null, 6], "source_digest": "another_generated_number_with_literals2"}')
    assert diff.compare_source_files_objects(obj1, obj2) == {'branches': [], 'name': 'obj-firefox/dist/include/mozilla/dom/DOMRectListBinding.h', 'coverage': [None, 0, None, None, 1], 'source_digest': 'another_generated_number_with_literals', 'functions': []}


def test_compare_objects_diff_coverage_same_func_2():
    obj1 = json.loads('{"functions": [{"name": "func1", "start": 36, "exec": true}, {"name": "func2", "start": 64, "exec": false}], "branches": [], "name": "obj-firefox/dist/include/mozilla/dom/DOMRectListBinding.h", "coverage": [null, 2, null, 1, 5], "source_digest": "another_generated_number_with_literals"}')
    obj2 = json.loads('{"functions": [{"name": "func1", "start": 36, "exec": true}, {"name": "func2", "start": 64, "exec": false}], "branches": [], "name": "obj-firefox/dist/include/mozilla/dom/DOMRectListBinding.h", "coverage": [null, 0, null, 0, 6], "source_digest": "another_generated_number_with_literals2"}')
    assert diff.compare_source_files_objects(obj1, obj2) == {'branches': [], 'name': 'obj-firefox/dist/include/mozilla/dom/DOMRectListBinding.h', 'coverage': [None, 0, None, 0, 1], 'source_digest': 'another_generated_number_with_literals', 'functions': []}


def test_compare_objects_diff_coverage_diff_functions():
    obj1 = json.loads('{"functions": [{"name": "func1", "start": 36, "exec": true}, {"name": "func2", "start": 64, "exec": false}], "branches": [], "name": "obj-firefox/dist/include/mozilla/dom/DOMRectListBinding.h", "coverage": [null, 2, 0, null, 5], "source_digest": "another_generated_number_with_literals"}')
    obj2 = json.loads('{"functions": [{"name": "func1", "start": 36, "exec": true}, {"name": "func2", "start": 64, "exec": true}], "branches": [], "name": "obj-firefox/dist/include/mozilla/dom/DOMRectListBinding.h", "coverage": [null, 2, 3, null, 5], "source_digest": "another_generated_number_with_literals2"}')
    assert diff.compare_source_files_objects(obj1, obj2) == {'name': 'obj-firefox/dist/include/mozilla/dom/DOMRectListBinding.h', 'functions': [{'start': 64, 'name': 'func2', 'exec': True}], 'source_digest': 'another_generated_number_with_literals', 'coverage': [None, 0, 3, None, 0], 'branches': []}


def test_compare_reports():
    baseline_report = json.loads('{"git":{"branch":"master","head":{"id":"UNUSED"}},"repo_token":"UNUSED","service_job_number":"","service_name":"","service_number":"","source_files":[{"functions": [{"name": "func1", "start": 36, "exec": true}, {"name": "func2", "start": 64, "exec": false}], "branches": [], "name": "obj-firefox/dist/include/mozilla/dom/DOMRectListBinding.h", "coverage": [null, 2, null, 1, 5], "source_digest": "another_generated_number_with_literals"}]}')
    report = json.loads('{"git":{"branch":"master","head":{"id":"UNUSED"}},"repo_token":"UNUSED","service_job_number":"","service_name":"","service_number":"","source_files":[{"functions": [{"name": "func1", "start": 36, "exec": true}, {"name": "func2", "start": 64, "exec": true}], "branches": [], "name": "obj-firefox/dist/include/mozilla/dom/DOMRectListBinding.h", "coverage": [null, 0, null, 0, 6], "source_digest": "another_generated_number_with_literals2"}]}')
    assert diff.compare_reports(baseline_report, report) == json.loads('{"git":{"branch":"master","head":{"id":"UNUSED"}},"repo_token":"UNUSED","service_job_number":"","service_name":"","service_number":"","source_files":[{"functions": [{"name": "func2", "start": 64, "exec": true}], "branches": [], "name": "obj-firefox/dist/include/mozilla/dom/DOMRectListBinding.h", "coverage": [null, 0, null, 0, 1], "source_digest": "another_generated_number_with_literals"}]}')


def test_compare_reports_2_files():
    baseline_report = json.loads('{"git":{"branch":"master","head":{"id":"UNUSED"}},"repo_token":"UNUSED","service_job_number":"","service_name":"","service_number":"","source_files":[{"functions": [{"name": "function1", "start": 36, "exec": true}, {"name": "function2", "start": 64, "exec": false}], "branches": [], "name": "name1", "coverage": [null, 2, null, 1, 5], "source_digest": "another_generated_number_with_literals"}, {"functions": [{"name": "func1", "start": 36, "exec": true}, {"name": "func2", "start": 64, "exec": false}], "branches": [], "name": "name2", "coverage": [null, 2, null, null, 5], "source_digest": "another_generated_number_with_literals"}]}')
    report = json.loads('{"git":{"branch":"master","head":{"id":"UNUSED"}},"repo_token":"UNUSED","service_job_number":"","service_name":"","service_number":"","source_files":[{"functions": [{"name": "function1", "start": 36, "exec": true}, {"name": "function2", "start": 64, "exec": true}], "branches": [], "name": "name1", "coverage": [null, 0, null, 0, 6], "source_digest": "another_generated_number_with_literals2"}, {"functions": [{"name": "func1", "start": 36, "exec": true}, {"name": "func2", "start": 64, "exec": false}], "branches": [], "name": "name2", "coverage": [null, 0, null, null, 6], "source_digest": "another_generated_number_with_literals2"}]}')
    assert diff.compare_reports(baseline_report, report) == json.loads('{"git":{"branch":"master","head":{"id":"UNUSED"}},"repo_token":"UNUSED","service_job_number":"","service_name":"","service_number":"","source_files":[{"functions": [{"name": "function2", "start": 64, "exec": true}], "branches": [], "name": "name1", "coverage": [null, 0, null, 0, 1], "source_digest": "another_generated_number_with_literals"}, {"name": "name2", "functions": [], "source_digest": "another_generated_number_with_literals", "coverage": [null, 0, null, null, 1], "branches": []}]}')
