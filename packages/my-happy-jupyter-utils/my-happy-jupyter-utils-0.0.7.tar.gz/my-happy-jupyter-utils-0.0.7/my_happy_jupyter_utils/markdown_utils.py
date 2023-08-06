import requests
from pathlib import Path
from IPython.display import Markdown
from happy_path import shellUtils

from . import version

__version__ = version.current_version


def _get_rjust_number(opt={}):
    total_lines_number = opt.get('total_lines_number', 1)

    just_number = 2
    if total_lines_number > 0 and total_lines_number < 10:
        just_number = 1
    elif total_lines_number >= 10 and total_lines_number < 100:
        just_number = 2
    elif total_lines_number >= 100 and total_lines_number < 1000:
        just_number = 3
    else:
        just_number = 4

    return just_number


def get_content_with_line_number_by_url(opt={}, out_json={}):
    url = opt.get('url', '')
    file_path = opt.get('file_path', '')
    language = opt.get('language', 'c')
    title = opt.get('title', '')
    is_original = opt.get('is_original', False)
    show_line_number = opt.get('show_line_number', False)
    need_process_markdown = opt.get('need_process_markdown', True)


    content = ''

    if len(url) > 0:
        r = requests.get(url)
        r.encoding='utf-8'
        content = r.text

    if len(file_path) > 0:
        with open(Path(file_path)) as f:
            content = f.read()

    if len(content) == 0:
        msg = 'markdown content is blank'
        print(msg)
        return msg

    if len(title) > 0:
        title = '#### ' + title


    content_lines = content.splitlines()

    content_with_line_number = []

    total_lines_number = len(content_lines)

    rjust_number = _get_rjust_number({
        'total_lines_number': total_lines_number
    })


    for index in range(total_lines_number):
        line = '{line_number}:  {line_content}'.format(
                    line_number=str(index + 1).rjust(rjust_number),
                    line_content=content_lines[index])
        content_with_line_number.append(line)


    if show_line_number:
        content = '\n'.join(content_with_line_number)


    markdown_content = """
```{language}
{content}
```
""".format(language=language,
           content=content)

    if is_original:
        markdown_content = content


    markdown_string = """
{title}
{markdown_content}
""".format(title=title,
           url=url,
           markdown_content=markdown_content).strip()

    # print(markdown_string)

    out_json['markdown_string'] = markdown_string

    if need_process_markdown:
        return Markdown(markdown_string)

def get_content_with_line_number(opt={}, out_json={}):
    content = opt.get('content', '')
    language = opt.get('language', 'c')
    need_process_markdown = opt.get('need_process_markdown', True)

    content_lines = content.splitlines()

    content_with_line_number = []

    total_lines_number = len(content_lines)

    rjust_number = _get_rjust_number({
        'total_lines_number': total_lines_number
    })

    for index in range(len(content_lines)):
        line = '{line_number}:  {line_content}'.format(
                    line_number=str(index + 1).rjust(rjust_number),
                    line_content=content_lines[index])
        content_with_line_number.append(line)

    markdown_string = """
```{language}
{content}
```
""".format(
        language=language,
        content='\n'.join(content_with_line_number)
).strip()


    out_json['markdown_string'] = markdown_string

    if need_process_markdown:
        return Markdown(markdown_string)


def get_code_snippet(opt={}, out_json={}):
    url = opt.get('url', '')
    content = opt.get('content', '')
    file_path = opt.get('file_path', '')
    language = opt.get('language', 'python')
    show_line_number = opt.get('show_line_number', True)
    start_line_number = opt.get('start_line_number', 1)
    end_line_number = opt.get('end_line_number', 2)
    line_numbers = opt.get('line_numbers', '')
    title = opt.get('title', '')
    need_process_markdown = opt.get('need_process_markdown', True)


    markdown_content = ''

    if len(url) > 0:
        r = requests.get(url)
        r.encoding='utf-8'
        markdown_content = r.text

    if len(file_path) > 0:
        with open(Path(file_path)) as f:
            markdown_content = f.read()

    if len(content) > 0:
        markdown_content = content


    if len(markdown_content) == 0:
        msg = 'markdown content is blank'
        print(msg)
        return msg


    markdown_content_lines = markdown_content.splitlines()


    content_lines = \
        markdown_content_lines[start_line_number - 1:end_line_number]

    if len(line_numbers) > 0:
        line_numbers_array = line_numbers.split(',')
        content_lines = []
        for item in line_numbers_array:
            content_lines.append(markdown_content_lines[int(item) - 1])


    content_with_line_number = []

    total_lines_number = len(content_lines)

    rjust_number = _get_rjust_number({
        'total_lines_number': total_lines_number
    })

    if show_line_number:
        for index in range(total_lines_number):
            line = '{line_number}:  {line_content}'.format(
                        line_number=str(index + 1).rjust(rjust_number),
                        line_content=content_lines[index])

            content_with_line_number.append(line)
    else:
        content_with_line_number = content_lines

    if len(title) > 0:
        title = '#### ' + title

    markdown_string = """
{title}
```{language}
{content}
```
""".format(title=title,
           language=language,
           content='\n'.join(content_with_line_number)).strip()


    # print(markdown_string)

    out_json['markdown_string'] = markdown_string

    if need_process_markdown:
        return Markdown(markdown_string)


def get_source_code(opt={}, out_json={}):
    """
    get source with content
    """
    content = opt.get('content', '')
    language = opt.get('language', 'python')
    show_line_number = opt.get('show_line_number', False)
    line_numbers = opt.get('line_numbers', '')
    title = opt.get('title', '')

    return get_code_snippet({
            'content': content,
            'title': title,
            'show_line_number': show_line_number,
            'line_numbers': line_numbers,
            'start_line_number': 1,
            'end_line_number': len(content.splitlines()),
            'language': language
        })

def check_directory(opt={}):
    default_command = """
cd ./data/projects/
ls -la
""".strip()
    commands = opt.get('commands', default_command)
    title = opt.get('title', '')

    if len(title) > 0:
        title = '#### ' + title

    out, error = shellUtils.runCommands(commands)

    markdown_content = ''

    if len(error) > 0:
        markdown_content = error
    else:
        markdown_content = out

    markdown_string = """
{title}
```shell
{markdown_content}
```
""".format(
markdown_content=markdown_content,
title=title)

    return Markdown(markdown_string)
