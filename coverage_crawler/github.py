# -*- coding: utf-8 -*-

import os
import shutil
import subprocess


def upload_to_github(reports_list, git_user_name, git_password):
    # Clone the repository if doesn't exist
    if not os.path.isdir('coverage-crawler-reports'):
        subprocess.run(['git', 'clone', 'https://github.com/rhcu/coverage-crawler-reports'])
    os.chdir('coverage-crawler-reports')

    # Remove the content of repository except of README
    prev_files = os.listdir(os.getcwd())
    for f in prev_files:
        if os.path.isdir(f):
            shutil.rmtree(f)
        elif f.startswith('.') is False:
            os.remove(f)
    subprocess.run(['git', 'pull', 'https://github.com/rhcu/coverage-crawler-reports', 'master'])

    with open('index.html', 'w') as f:
        f.write("""
            <html>
            <head>
            <title>Reports</title>
            </head>
            <body>
            <h1>The list of available reports for websites:</h1>
            <br>
        """)
        for website, report in reports_list.items():
            # Push the new content
            shutil.move(report, os.getcwd())
            name_of_folder = report.rsplit('/', 1)[-1]
            f.write('<a href="{}">{}</a>'.format(os.path.join(name_of_folder, 'report/index.html'), website))
            f.write('<br>')
        f.write("""
            </body>
            </html>
        """)

    # Commit the content
    subprocess.run(['git', 'init'])
    subprocess.run(['git', 'add', '*'])
    subprocess.run(['git', 'commit', '-m', 'Coverage crawler reports upload'])
    subprocess.run(['git', 'push', 'https://{}:{}@github.com/rhcu/coverage-crawler-reports'.format(git_user_name, git_password), 'master', '--force'])
