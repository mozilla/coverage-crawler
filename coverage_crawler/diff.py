# -*- coding: utf-8 -*-


def diff_line(i, j, ignore_hits):
    if j is None:
        return None
    elif i is None:
        return j
    elif j > 0 and j > i:
        if ignore_hits and i == 0:
            return 1
        elif ignore_hits is False:
            return j - i
        else:
            return 0
    else:
        return 0


def compare_source_files_objects(obj1, obj2, ignore_hits):
    diff_funcs = []
    diff_cov = []
    if obj1['name'] == obj2['name']:

        if obj1['coverage'] != obj2['coverage']:
            diff_cov = [diff_line(k, m, ignore_hits) for k, m in zip(obj1['coverage'], obj2['coverage'])]

        if obj1['functions'] != obj2['functions']:
            for func1 in obj1['functions']:
                for func2 in obj2['functions']:
                    if func1['name'] == func2['name']:
                        if func1['exec'] is False and func2['exec'] is True:
                            diff_funcs.append(func2)

    if len(diff_funcs) == 0 and all(cov == 0 or cov is None for cov in diff_cov):
        return None
    else:
        obj1['coverage'] = diff_cov
        obj1['functions'] = diff_funcs
        return obj1


def compare_reports(baseline_report, report, ignore_hits):
    baseline_coverage = baseline_report['source_files']
    coverage = report['source_files']
    source_files = []
    diff_report = {}
    for i in baseline_coverage:
        for j in coverage:
            comp_result = compare_source_files_objects(i, j, ignore_hits)
            if comp_result is not None:
                source_files.append(comp_result)
    diff_report['source_files'] = source_files
    for name in ['git', 'repo_token', 'service_job_number', 'service_name', 'service_number']:
        diff_report[name] = baseline_report[name]

    return diff_report
