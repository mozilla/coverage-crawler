# -*- coding: utf-8 -*-


def diff_line(i, j):
    if j is None:
        return None
    elif i is None:
        return j
    elif j > 0 and j >= i:
        return j - i
    else:
        return 0


def compare_source_files_objects(obj1, obj2):
    diff_funcs = []
    if obj1['name'] == obj2['name']:
        are_funcs_equal = False
        is_cov_equal = False

        if obj1['coverage'] == obj2['coverage']:
            is_cov_equal = True
        if obj1['functions'] == obj2['functions']:
            are_funcs_equal = True

        # both are different
        if are_funcs_equal is False and is_cov_equal is False:
            obj1['coverage'] = [diff_line(k, m) for k, m in zip(obj1['coverage'], obj2['coverage'])]
            for func1 in obj1['functions']:
                for func2 in obj2['functions']:
                    if func1['name'] == func2['name']:
                        if func1['exec'] is False and func2['exec'] is True:
                            diff_funcs.append(func2)
            obj1['functions'] = diff_funcs
        elif are_funcs_equal is True and is_cov_equal is False:
            obj1['coverage'] = [diff_line(k, m) for k, m in zip(obj1['coverage'], obj2['coverage'])]
            obj1['functions'] = []
        elif are_funcs_equal is False and is_cov_equal is True:
            for func1 in obj1['functions']:
                for func2 in obj2['functions']:
                    if func1['name'] == func2['name']:
                        if func1['exec'] is False and func2['exec'] is True:
                            diff_funcs.append(func2)
            obj1['functions'] = diff_funcs
            obj1['coverage'] = []
        # both are same
        else:
            return None
        return obj1

    return None


def compare_reports(baseline_report, report):
    baseline_coverage = baseline_report['source_files']
    coverage = report['source_files']
    source_files = []
    diff_report = {}
    for i in baseline_coverage:
        for j in coverage:
            comp_result = compare_source_files_objects(i, j)
            if comp_result is not None:
                source_files.append(comp_result)
    diff_report['source_files'] = source_files
    for name in ['git', 'repo_token', 'service_job_number', 'service_name', 'service_number']:
        diff_report[name] = baseline_report[name]

    return diff_report
