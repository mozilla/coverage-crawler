# -*- coding: utf-8 -*-

import json
import os

import codecoverage


def generate_html(data_folder):
    with open('{}/diff.json'.format(data_folder), 'r') as report:
        parsed_json = json.load(report)

    file_obj = open('{}/output.info'.format(data_folder), 'w')

    source_files = parsed_json['source_files']
    file_obj.write('TN\n')

    for source_file in source_files:
        file_obj.write('SF:{}\n'.format(source_file['name']))
        executed = 0

        # Functions
        if len(source_file['functions']) != 0:
            for function in source_file['functions']:
                file_obj.write('FN:{},{}\n'.format(function['start'], function['name']))
            for function in source_file['functions']:
                if function['exec'] is True:
                    file_obj.write('FNDA:{},{}\n'.format(1, function['name']))
                    executed += 1
                else:
                    file_obj.write('FNDA:{},{}\n'.format(0, function['name']))
        file_obj.write('FNF:{}\n'.format(len(source_file['functions'])))
        file_obj.write('FNH:{}\n'.format(executed))

        # Branches
        branch_hits = 0
        if len(source_file['branches']) != 0:
            for branch in source_file['branches']:
                if branch['taken'] is True:
                    file_obj.write('BRDA:{},0,{},{}\n'.format(branch['line'], branch['number'], 1))
                    branch_hits += 1
                else:
                    file_obj.write('BRDA:{},0,{},{}\n'.format(branch['line'], branch['number'], '-'))
        file_obj.write('BRF:{}\n'.format(len(source_file['branches'])))
        file_obj.write('BRH:{}\n'.format(branch_hits))

        # Lines
        line_number = 0
        cov_line_count = 0
        if len(source_file['coverage']) != 0:
            for line_number, line in enumerate(source_file['coverage'], 1):
                if line is not None:
                    file_obj.write('DA:{},{}\n'.format(line_number, line))
                    if line > 0:
                        cov_line_count += 1
        file_obj.write('LF:{}\n'.format(len(source_file['coverage'])))
        file_obj.write('LH:{}\n'.format(cov_line_count))
        file_obj.write('end_of_record\n')
    file_obj.close()

    codecoverage.download_genhtml()
    codecoverage.generate_html_report('mozilla-central', os.path.join(os.getcwd(), '{}/output.info'.format(data_folder)), os.path.join(os.getcwd(), '{}/report'.format(data_folder)))
