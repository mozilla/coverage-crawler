# -*- coding: utf-8 -*-


def ignore_third_party_filter(report):

    with open('mozilla-central/tools/rewriting/ThirdPartyPaths.txt') as f:
        third_party_paths = [path.strip('\n') for path in f]

    files = report['source_files']

    filtered_report = {}
    filtered_files = []
    for i in files:
        if any(i['name'].startswith(path) for path in third_party_paths):
                continue
        filtered_files.append(i)
    filtered_report['source_files'] = filtered_files
    for name in ['git', 'repo_token', 'service_job_number', 'service_name', 'service_number']:
        filtered_report[name] = report[name]

    return filtered_report
