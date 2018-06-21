# -*- coding: utf-8 -*-


def ignore_third_party_filter(report):
    with open('mozilla-central/tools/rewriting/ThirdPartyPaths.txt') as f:
        third_party_paths = [path.strip('\n') for path in f]
    report['source_files'] = [sf for sf in report['source_files'] if not any(sf['name'].startswith(path) for path in third_party_paths)]
