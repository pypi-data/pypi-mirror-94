from IPython.display import HTML

from . import version

__version__ = version.current_version


def get_default_host():
    return "http://127.0.0.1:7160/";

def show_image_with_title_by_url(opt={}):

    url = opt.get('url', '')

    file_path = opt.get('file_path', '')

    if len(file_path) > 0:
        url = file_path

    use_default_host = opt.get('use_default_host',  False)

    if use_default_host:
        url = get_default_host() + url;

    title = opt.get('title', '')

    if len(title) > 0:
        title = '<a href="{url}" target="blank"><h4>{title}</h4></a>'.format(
            url=url,
            title=title
        )



    html_string = """
{title}
<img src="{url}" style="max-width: 100%" />
""".format(
      url=url,
      title=title
    ).strip()

    return HTML(html_string)
