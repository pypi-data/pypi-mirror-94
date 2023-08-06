import os
import re
import pybars
import errno
import markdown
import json
import sys
import shutil

__version__ = "1.0.0"
resources_dir = './resources'
out_dir = './public'


def get_paths(from_path):
    paths = []
    items = os.listdir(from_path)

    for item in items:
        if item.endswith(".md"):
            complete_path = (from_path + "/" + item)
            path = complete_path.replace(resources_dir + '/content', '')
            paths.append(path)
        else:
            paths.extend(get_paths(from_path + '/' + item))

    return paths


def remove_all_occurrences_from_list(given_list, to_remove):
    result = []

    for item in given_list:
        if item != to_remove:
            result.append(item)

    return result


def remove_spaces_from_around_items_in_list(given_list):
    result = []

    for item in given_list:
        result.append(re.sub(r'^\s+|\s+$', '', item, flags=re.UNICODE))

    return result


def get_content_meta(content):
    meta_block = re.search('(?s)^---(.*?)---*', content)

    if meta_block:
        match = meta_block.group(0)
        meta_lines = match.splitlines()
        meta_lines = remove_spaces_from_around_items_in_list(meta_lines)
        meta_lines = remove_all_occurrences_from_list(meta_lines, '---')
        meta = {}

        for meta_line in meta_lines:
            if ':' in meta_line:
                key = meta_line.split(':')[0].strip().replace(' ', '_')
                key = re.sub('[^a-zA-Z_]', '', key)
                value = meta_line.split(':')[1].strip()
                meta[key] = value

        return meta
    else:
        return {}


def get_content_entry(content):
    entry = re.sub('(?s)^---(.*?)---*', '', content)
    return entry.strip()


def get_contents(paths):
    contents = []

    for path in paths:
        with open(resources_dir + "/content" + path, 'r') as reader:
            content = reader.read()
            contents.append({
                'path': path.replace('.md', ''),
                **get_content_meta(content),
                'entry': markdown.markdown(get_content_entry(content))
            })

    return contents


def generate_file(content, config, template):
    compiler = pybars.Compiler()
    compiled_template = compiler.compile(template)
    output = compiled_template({**config, **content})
    file_path = out_dir + content['path'] + '/index.html'

    if not os.path.exists(os.path.dirname(file_path)):
        try:
            os.makedirs(os.path.dirname(file_path))
        except OSError as exc:
            if exc.errno != errno.EEXIST:
                raise

    file = open(file_path, 'w')
    file.write(output)
    file.close()


def generate_files(contents):
    with open(resources_dir + '/template.hbs', 'r') as template_file, \
            open(resources_dir + '/config.json', 'r') as config_file:
        template = template_file.read()
        config = config_file.read()
        blog_paths = get_paths(resources_dir + '/content/blog')
        blog_contents = get_contents(blog_paths)
        site_config = json.loads(config)
        post_config = {'is_home': False, 'is_post': True}
        home_config = {
            'is_home': True,
            'is_post': False,
            'posts': blog_contents
        }

        # Generate all content
        for content in contents:
            generate_file(content, {**post_config, **site_config}, template)

        # Generate home page
        generate_file({
            'path': '/',
            'entry': ''
        }, {**home_config, **site_config}, template)


def generate():
    # Before we do anything let's make sure needed files exist
    if not os.path.exists(resources_dir + '/config.json'):
        sys.exit(resources_dir + '/config.json file does not exist.')

    if not os.path.exists(resources_dir + '/template.hbs'):
        sys.exit(resources_dir + '/template.hbs file does not exist.')

    # We are victorious!
    paths_to_files = get_paths(resources_dir + '/content')
    contents_of_files = get_contents(paths_to_files)

    if os.path.exists(out_dir):
        shutil.rmtree(out_dir)

    shutil.copytree(resources_dir + '/assets', out_dir + '/assets')
    generate_files(contents_of_files)


def run():
    argv = sys.argv[1:]

    if '--version' in argv:
        print(__version__)
    else:
        generate()
