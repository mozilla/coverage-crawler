# -*- coding: utf-8 -*-


from coverage_crawler import diff


# diff.compare_objects(obj1, obj2) returns true if equal and false if different coverage
def test_compare_objects_same_coverage_same_functions():
    obj1 = {
        'functions': [
            {
                'name': 'func1',
                'start': 36,
                'exec': True
            },
            {
                'name': 'func2',
                'start': 64,
                'exec': False
            }
        ],
        'branches': [],
        'name': 'obj-firefox/dist/include/mozilla/dom/DOMRectListBinding.h',
        'coverage': [
                None,
                2,
                None,
                None,
                5
        ],
        'source_digest': 'another_generated_number_with_literals'
    }
    obj2 = {
        'functions': [
            {
                'name': 'func1',
                'start': 36,
                'exec': True
            },
            {
                'name': 'func2',
                'start': 64,
                'exec': False
            }
        ],
        'branches': [],
        'name': 'obj-firefox/dist/include/mozilla/dom/DOMRectListBinding.h',
        'coverage': [
                None,
                2,
                None,
                None,
                5
        ],
        'source_digest': 'another_generated_number_with_literals'
    }
    assert diff.compare_source_files_objects(obj1, obj2, False) is None


def test_compare_objects_same_coverage_diff_functions():
    obj1 = {
        'functions': [
            {
                'name': 'func1',
                'start': 36,
                'exec': True
            },
            {
                'name': 'func2',
                'start': 64,
                'exec': True
            }
        ],
        'branches': [],
        'name': 'obj-firefox/dist/include/mozilla/dom/DOMRectListBinding.h',
        'coverage': [
            None,
            2,
            None,
            None,
            5
        ],
        'source_digest': 'another_generated_number_with_literals'
    }
    obj2 = {
        'functions': [
            {
                'name': 'func1',
                'start': 36,
                'exec': True
            },
            {
                'name': 'func2',
                'start': 64,
                'exec': False
            }
        ],
        'branches': [],
        'name': 'obj-firefox/dist/include/mozilla/dom/DOMRectListBinding.h',
        'coverage': [
            None,
            2,
            None,
            None,
            5
        ],
        'source_digest': 'another_generated_number_with_literals2'
    }

    assert diff.compare_source_files_objects(obj1, obj2, False) is None


def test_compare_objects_diff_coverage_same_func():
    obj1 = {
        'functions': [
            {
                'name': 'func1',
                'start': 36,
                'exec': True
            },
            {
                'name': 'func2',
                'start': 64,
                'exec': False
            }
        ],
        'branches': [],
        'name': 'obj-firefox/dist/include/mozilla/dom/DOMRectListBinding.h',
        'coverage': [
            None,
            2,
            None,
            None,
            5
        ],
        'source_digest': 'another_generated_number_with_literals'
    }
    obj2 = {
        'functions': [
            {
                'name': 'func1',
                'start': 36,
                'exec': True
            },
            {
                'name': 'func2',
                'start': 64,
                'exec': False
            }
        ],
        'branches': [],
        'name': 'obj-firefox/dist/include/mozilla/dom/DOMRectListBinding.h',
        'coverage': [
            None,
            2,
            None,
            None,
            6
        ],
        'source_digest': 'another_generated_number_with_literals2'
    }

    assert diff.compare_source_files_objects(obj1, obj2, False) == {
        'functions': [],
        'branches': [],
        'name': 'obj-firefox/dist/include/mozilla/dom/DOMRectListBinding.h',
        'coverage': [
            None,
            0,
            None,
            None,
            1
        ],
        'source_digest': 'another_generated_number_with_literals'
    }


def test_compare_objects_diff_coverage_same_func_2():
    obj1 = {
        'functions': [
            {
                'name': 'func1',
                'start': 36,
                'exec': True
            },
            {
                'name': 'func2',
                'start': 64,
                'exec': False
            }
        ],
        'branches': [],
        'name': 'obj-firefox/dist/include/mozilla/dom/DOMRectListBinding.h',
        'coverage': [
            None,
            2,
            None,
            1,
            5
        ],
        'source_digest': 'another_generated_number_with_literals'
    }

    obj2 = {
        'functions': [
            {
                'name': 'func1',
                'start': 36,
                'exec': True
            },
            {
                'name': 'func2',
                'start': 64,
                'exec': False
            }
        ],
        'branches': [],
        'name': 'obj-firefox/dist/include/mozilla/dom/DOMRectListBinding.h',
        'coverage': [
            None,
            0,
            None,
            0,
            6
        ],
        'source_digest': 'another_generated_number_with_literals2'
    }

    assert diff.compare_source_files_objects(obj1, obj2, False) == {
        'functions': [],
        'branches': [],
        'name': 'obj-firefox/dist/include/mozilla/dom/DOMRectListBinding.h',
        'coverage': [
            None,
            0,
            None,
            0,
            1
        ],
        'source_digest': 'another_generated_number_with_literals'
    }


def test_compare_objects_diff_coverage_diff_functions():
    obj1 = {
        'functions': [
            {
                'name': 'func1',
                'start': 36,
                'exec': True
            },
            {
                'name': 'func2',
                'start': 64,
                'exec': False
            }
        ],
        'branches': [],
        'name': 'obj-firefox/dist/include/mozilla/dom/DOMRectListBinding.h',
        'coverage': [
            None,
            2,
            0,
            None,
            5
        ],
        'source_digest': 'another_generated_number_with_literals'
    }
    obj2 = {
        'functions': [
            {
                'name': 'func1',
                'start': 36,
                'exec': True
            },
            {
                'name': 'func2',
                'start': 64,
                'exec': True
            }
        ],
        'branches': [],
        'name': 'obj-firefox/dist/include/mozilla/dom/DOMRectListBinding.h',
        'coverage': [
            None,
            2,
            3,
            None,
            5
        ],
        'source_digest': 'another_generated_number_with_literals2'
    }

    assert diff.compare_source_files_objects(obj1, obj2, False) == {
        'functions': [
            {
                'name': 'func2',
                'start': 64,
                'exec': True
            }
        ],
        'branches': [],
        'name': 'obj-firefox/dist/include/mozilla/dom/DOMRectListBinding.h',
        'coverage': [
            None,
            0,
            3,
            None,
            0
        ],
        'source_digest': 'another_generated_number_with_literals'
    }


def test_compare_reports():
    baseline_report = {
        'git': {
            'branch': 'master',
            'head': {
                'id': 'UNUSED'
            }
        },
        'repo_token': 'UNUSED',
        'service_job_number': '',
        'service_name': '',
        'service_number': '',
        'source_files': [
            {
                'functions': [
                    {
                        'name': 'func1',
                        'start': 36,
                        'exec': True
                    },
                    {
                        'name': 'func2',
                        'start': 64,
                        'exec': False
                    }
                ],
                'branches': [],
                'name': 'obj-firefox/dist/include/mozilla/dom/DOMRectListBinding.h',
                'coverage': [
                    None,
                    2,
                    None,
                    1,
                    5
                ],
                'source_digest': 'another_generated_number_with_literals'
            }
        ]
    }
    report = {
        'git': {
            'branch': 'master',
            'head': {
                'id': 'UNUSED'
            }
        },
        'repo_token': 'UNUSED',
        'service_job_number': '',
        'service_name': '',
        'service_number': '',
        'source_files': [
            {
                'functions': [
                    {
                        'name': 'func1',
                        'start': 36,
                        'exec': True
                    },
                    {
                        'name': 'func2',
                        'start': 64,
                        'exec': True
                    }
                ],
                'branches': [],
                'name': 'obj-firefox/dist/include/mozilla/dom/DOMRectListBinding.h',
                'coverage': [
                    None,
                    0,
                    None,
                    0,
                    6
                ],
                'source_digest': 'another_generated_number_with_literals2'
            }
        ]
    }
    assert diff.compare_reports(baseline_report, report, False) == {
        'git': {
            'branch': 'master',
            'head': {
                'id': 'UNUSED'
            }
        },
        'repo_token': 'UNUSED',
        'service_job_number': '',
        'service_name': '',
        'service_number': '',
        'source_files': [
            {
                'functions': [
                    {
                        'name': 'func2',
                        'start': 64,
                        'exec': True
                    }
                ],
                'branches': [],
                'name': 'obj-firefox/dist/include/mozilla/dom/DOMRectListBinding.h',
                'coverage': [
                    None,
                    0,
                    None,
                    0,
                    1
                ],
                'source_digest': 'another_generated_number_with_literals'
            }
        ]
    }


def test_compare_reports_coverage_no_problems():
    baseline_report = {
        'git': {
            'branch': 'master',
            'head': {
                'id': 'UNUSED'
            }
        },
        'repo_token': 'UNUSED',
        'service_job_number': '',
        'service_name': '',
        'service_number': '',
        'source_files': [
            {
                'functions': [
                    {
                        'name': 'func1',
                        'start': 36,
                        'exec': True
                    }
                ],
                'branches': [],
                'name': 'obj-firefox/dist/include/mozilla/dom/DOMRectListBinding.h',
                'coverage': [
                    None,
                    2,
                    None,
                    1,
                    5
                ],
                'source_digest': 'another_generated_number_with_literals'
            }
        ]
    }
    report = {
        'git': {
            'branch': 'master',
            'head': {
                'id': 'UNUSED'
            }
        },
        'repo_token': 'UNUSED',
        'service_job_number': '',
        'service_name': '',
        'service_number': '',
        'source_files': [
            {
                'functions': [
                    {
                        'name': 'func1',
                        'start': 36,
                        'exec': True
                    }
                ],
                'branches': [],
                'name': 'obj-firefox/dist/include/mozilla/dom/DOMRectListBinding.h',
                'coverage': [
                    None,
                    0,
                    None,
                    0,
                    5
                ],
                'source_digest': 'another_generated_number_with_literals2'
            }
        ]
    }
    assert diff.compare_reports(baseline_report, report, False) == {
        'git': {
            'branch': 'master',
            'head': {
                'id': 'UNUSED'
            }
        },
        'repo_token': 'UNUSED',
        'service_job_number': '',
        'service_name': '',
        'service_number': '',
        'source_files': []
    }


def test_compare_reports_2_files():
    baseline_report = {
        'git': {
            'branch': 'master',
            'head': {
                'id': 'UNUSED'
            }
        },
        'repo_token': 'UNUSED',
        'service_job_number': '',
        'service_name': '',
        'service_number': '',
        'source_files': [
            {
                'functions': [
                    {
                        'name': 'function1',
                        'start': 36,
                        'exec': True
                    },
                    {
                        'name': 'function2',
                        'start': 64,
                        'exec': False
                    }
                ],
                'branches': [],
                'name': 'name1',
                'coverage': [
                    None,
                    2,
                    None,
                    1,
                    5
                ],
                'source_digest': 'another_generated_number_with_literals'
            },
            {
                'functions': [
                    {
                        'name': 'func1',
                        'start': 36,
                        'exec': True
                    },
                    {
                        'name': 'func2',
                        'start': 64,
                        'exec': False
                    }
                ],
                'branches': [],
                'name': 'name2',
                'coverage': [
                    None,
                    2,
                    None,
                    None,
                    5
                ],
                'source_digest': 'another_generated_number_with_literals'
            }
        ]
    }
    report = {
        'git': {
            'branch': 'master',
            'head': {
                'id': 'UNUSED'
            }
        },
        'repo_token': 'UNUSED',
        'service_job_number': '',
        'service_name': '',
        'service_number': '',
        'source_files': [
            {
                'functions': [
                    {
                        'name': 'function1',
                        'start': 36,
                        'exec': True
                    },
                    {
                        'name': 'function2',
                        'start': 64,
                        'exec': True
                    }
                ],
                'branches': [],
                'name': 'name1',
                'coverage': [
                    None,
                    0,
                    None,
                    0,
                    6
                ],
                'source_digest': 'another_generated_number_with_literals2'
            },
            {
                'functions': [
                    {
                        'name': 'func1',
                        'start': 36,
                        'exec': True
                    },
                    {
                        'name': 'func2',
                        'start': 64,
                        'exec': False
                    }
                ],
                'branches': [],
                'name': 'name2',
                'coverage': [
                    None,
                    0,
                    None,
                    None,
                    6
                ],
                'source_digest': 'another_generated_number_with_literals2'
            }
        ]
    }

    assert diff.compare_reports(baseline_report, report, False) == {
        'git': {
            'branch': 'master',
            'head': {
                'id': 'UNUSED'
            }
        },
        'repo_token': 'UNUSED',
        'service_job_number': '',
        'service_name': '',
        'service_number': '',
        'source_files': [
            {
                'functions': [
                    {
                        'name': 'function2',
                        'start': 64,
                        'exec': True
                    }
                ],
                'branches': [],
                'name': 'name1',
                'coverage': [
                    None,
                    0,
                    None,
                    0,
                    1
                ],
                'source_digest': 'another_generated_number_with_literals'
            },
            {
                'functions': [],
                'branches': [],
                'name': 'name2',
                'coverage': [
                    None,
                    0,
                    None,
                    None,
                    1
                ],
                'source_digest': 'another_generated_number_with_literals'
            }
        ]
    }


def test_compare_reports_no_diff():
    baseline_report = {
        'git': {
            'branch': 'master',
            'head': {
                'id': 'UNUSED'
            }
        },
        'repo_token': 'UNUSED',
        'service_job_number': '',
        'service_name': '',
        'service_number': '',
        'source_files': [
            {
                'functions': [
                    {
                        'name': 'func1',
                        'start': 36,
                        'exec': True
                    },
                    {
                        'name': 'func2',
                        'start': 64,
                        'exec': False
                    }
                ],
                'branches': [],
                'name': 'obj-firefox/dist/include/mozilla/dom/DOMRectListBinding.h',
                'coverage': [
                    None,
                    2,
                    None,
                    None,
                    5
                ],
                'source_digest': 'another_generated_number_with_literals'
            }
        ]
    }
    report = {
        'git': {
            'branch': 'master',
            'head': {
                'id': 'UNUSED'
            }
        },
        'repo_token': 'UNUSED',
        'service_job_number': '',
        'service_name': '',
        'service_number': '',
        'source_files': [
            {
                'functions': [
                    {
                        'name': 'func1',
                        'start': 36,
                        'exec': True
                    },
                    {
                        'name': 'func2',
                        'start': 64,
                        'exec': False
                    }
                ],
                'branches': [],
                'name': 'obj-firefox/dist/include/mozilla/dom/DOMRectListBinding.h',
                'coverage': [
                    None,
                    2,
                    None,
                    None,
                    5
                ],
                'source_digest': 'another_generated_number_with_literals2'
            }
        ]
    }

    assert diff.compare_reports(baseline_report, report, False) == {
        'git': {
            'branch': 'master',
            'head': {
                'id': 'UNUSED'
            }
        },
        'repo_token': 'UNUSED',
        'service_job_number': '',
        'service_name': '',
        'service_number': '',
        'source_files': []
    }


def test_compare_reports_ignore_hits():
    baseline_report = {
        'git': {
            'branch': 'master',
            'head': {
                'id': 'UNUSED'
            }
        },
        'repo_token': 'UNUSED',
        'service_job_number': '',
        'service_name': '',
        'service_number': '',
        'source_files': [
            {
                'functions': [
                    {
                        'name': 'func1',
                        'start': 36,
                        'exec': True
                    },
                    {
                        'name': 'func2',
                        'start': 64,
                        'exec': False
                    }
                ],
                'branches': [],
                'name': 'obj-firefox/dist/include/mozilla/dom/DOMRectListBinding.h',
                'coverage': [
                    None,
                    2,
                    None,
                    1,
                    5
                ],
                'source_digest': 'another_generated_number_with_literals'
            }
        ]
    }
    report = {
        'git': {
            'branch': 'master',
            'head': {
                'id': 'UNUSED'
            }
        },
        'repo_token': 'UNUSED',
        'service_job_number': '',
        'service_name': '',
        'service_number': '',
        'source_files': [
            {
                'functions': [
                    {
                        'name': 'func1',
                        'start': 36,
                        'exec': True
                    },
                    {
                        'name': 'func2',
                        'start': 64,
                        'exec': True
                    }
                ],
                'branches': [],
                'name': 'obj-firefox/dist/include/mozilla/dom/DOMRectListBinding.h',
                'coverage': [
                    None,
                    2,
                    None,
                    5,
                    6
                ],
                'source_digest': 'another_generated_number_with_literals2'
            }
        ]
    }
    assert diff.compare_reports(baseline_report, report, True) == {
        'git': {
            'branch': 'master',
            'head': {
                'id': 'UNUSED'
            }
        },
        'repo_token': 'UNUSED',
        'service_job_number': '',
        'service_name': '',
        'service_number': '',
        'source_files': [
            {
                'functions': [
                    {
                        'name': 'func2',
                        'start': 64,
                        'exec': True
                    }
                ],
                'branches': [],
                'name': 'obj-firefox/dist/include/mozilla/dom/DOMRectListBinding.h',
                'coverage': [
                    None,
                    0,
                    None,
                    0,
                    0
                ],
                'source_digest': 'another_generated_number_with_literals'
            }
        ]
    }


def test_compare_reports_ignore_hits_2():
    baseline_report = {
        'git': {
            'branch': 'master',
            'head': {
                'id': 'UNUSED'
            }
        },
        'repo_token': 'UNUSED',
        'service_job_number': '',
        'service_name': '',
        'service_number': '',
        'source_files': [
            {
                'functions': [
                    {
                        'name': 'func1',
                        'start': 36,
                        'exec': True
                    },
                    {
                        'name': 'func2',
                        'start': 64,
                        'exec': False
                    }
                ],
                'branches': [],
                'name': 'obj-firefox/dist/include/mozilla/dom/DOMRectListBinding.h',
                'coverage': [
                    None,
                    2,
                    None,
                    1,
                    0
                ],
                'source_digest': 'another_generated_number_with_literals'
            }
        ]
    }
    report = {
        'git': {
            'branch': 'master',
            'head': {
                'id': 'UNUSED'
            }
        },
        'repo_token': 'UNUSED',
        'service_job_number': '',
        'service_name': '',
        'service_number': '',
        'source_files': [
            {
                'functions': [
                    {
                        'name': 'func1',
                        'start': 36,
                        'exec': True
                    },
                    {
                        'name': 'func2',
                        'start': 64,
                        'exec': True
                    }
                ],
                'branches': [],
                'name': 'obj-firefox/dist/include/mozilla/dom/DOMRectListBinding.h',
                'coverage': [
                    None,
                    2,
                    None,
                    5,
                    6
                ],
                'source_digest': 'another_generated_number_with_literals2'
            }
        ]
    }
    assert diff.compare_reports(baseline_report, report, True) == {
        'git': {
            'branch': 'master',
            'head': {
                'id': 'UNUSED'
            }
        },
        'repo_token': 'UNUSED',
        'service_job_number': '',
        'service_name': '',
        'service_number': '',
        'source_files': [
            {
                'functions': [
                    {
                        'name': 'func2',
                        'start': 64,
                        'exec': True
                    }
                ],
                'branches': [],
                'name': 'obj-firefox/dist/include/mozilla/dom/DOMRectListBinding.h',
                'coverage': [
                    None,
                    0,
                    None,
                    0,
                    1
                ],
                'source_digest': 'another_generated_number_with_literals'
            }
        ]
    }
