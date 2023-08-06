# -*- coding: utf-8 -*-
from setuptools import setup

package_dir = \
{'': 'src'}

packages = \
['marklink']

package_data = \
{'': ['*']}

install_requires = \
['beautifulsoup4', 'configargparse', 'lxml', 'requests']

entry_points = \
{'console_scripts': ['marklink = marklink:main']}

setup_kwargs = {
    'name': 'marklink',
    'version': '1.0.0',
    'description': 'Create markdown links from text containing URLs',
    'long_description': '# marklink\n\n`marklink` replaces URLs found in text with a markup hyperlink with the contents\nof the `<title>` tag in the HTML of the URL. It works like a typical [Unix\nfilter](https://en.wikipedia.org/wiki/Filter_(software)):\n\n```sh\necho "I like https://github.com?something=what" | marklink --format md --remove-query\n\nI like [GitHub: Where the world builds software · GitHub](https://github.com)\n```\n\nIts goal is to increase the ergonomics of writing, thus leading you to write more. You get to experience the joy of having robots helping you while writing.\n\nInspired by [Titler by Brett Terpstra](http://brettterpstra.com/2015/02/18/titler-system-service/) for Mac OS and [org-cliplink](https://github.com/rexim/org-cliplink) for Emacs.\n\nThe ultimate goal of this project is to be cross platform and support many formats, workflows and editors.\n\n![Using marklink](marklink.gif)\n\n# Installation\n\nWith `pip`:\n\n```sh\npip install --user git+https://github.com/staticaland/marklink.git#egg=marklink\n```\n\nWith `pipx`:\n\n```sh\npipx install \'git+https://github.com/staticaland/marklink.git#egg=marklink\'\n```\n\n# Editor integration\n\n## Vim\n\n```\nnnoremap <leader>l :%!marklink<CR>\nvnoremap <leader>l :!marklink<CR>\n```\n\nThis is reminiscent of the [Vim Kōan *Master Wq and the Markdown\nacolyte*](https://blog.sanctum.geek.nz/vim-koans/).\n\n## Emacs\n\nI use `reformatter.el` (see [my reformatter.el config here](https://github.com/staticaland/doom-emacs-config/blob/master/modules/editor/reformatter/config.el)).\n\nYou can also use some variant of `shell-command-on-region`:\n\n```elisp\n(defun marklink-org ()\n  (interactive *)\n  (save-excursion\n    (shell-command-on-region (mark) (point) "marklink --format org" (buffer-name) t)))\n```\n\nYou may have to set the following if you like an exotic `$SHELL`:\n\n```elisp\n(setq explicit-shell-file-name "/bin/bash")\n(setq shell-file-name explicit-shell-file-name)\n```\n\n## Atom, Sublime Text, VS Code et al.\n\nPull requests most welcome.\n\nYou may want to consider [Paste URL at the Visual Studio\nMarketplace](https://marketplace.visualstudio.com/items?itemName=kukushi.pasteurl).\n\n# Usage\n\n```sh\nusage: marklink [-h] [-f {md,org,html}] [-q] [files]\n\nArgs that start with \'--\' (eg. -f) can also be set in a config file\n(~/.marklink). Config file syntax allows: key=value, flag=true, stuff=[a,b,c]\n(for details, see syntax at https://goo.gl/R74nmi). If an arg is specified in\nmore than one place, then commandline values override config file values which\noverride defaults.\n\npositional arguments:\n  files\n\noptional arguments:\n  -h, --help            show this help message and exit\n  -f {md,org,html}, --format {md,org,html}\n                        which format\n  -q, --remove-query    remove query parameters\n```\n\n# Other alternatives\n\nUse a bookmarklet ([source](https://old.reddit.com/r/emacs/comments/682wsu/bookmarklet_to_copy_link_to_clipboard_formatted/)):\n\n```js\njavascript:(\n    function(){\n        prompt(\n            \'\',\n            \'[[\'\n                +location.href\n                +\'][\'\n                +document.title.replace(/ [-,|].*$/,\'\')\n                +\']]\'\n        )\n    }\n)()\n```\n\nSome useful links:\n\n[Using external filter commands to reformat HTML](http://vimcasts.org/episodes/using-external-filter-commands-to-reformat-html/)\n\n[Formatting text with par](http://vimcasts.org/episodes/formatting-text-with-par/)\n\n[GitHub - ferrine/md-img-paste.vim: paste image to markdown](https://github.com/ferrine/md-img-paste.vim)\n\n[Vim Tip: Paste Markdown Link with Automatic Title Fetching | Ben Congdon](https://benjamincongdon.me/blog/2020/06/27/Vim-Tip-Paste-Markdown-Link-with-Automatic-Title-Fetching/)\n\n[GitHub - alphapapa/org-web-tools: View, capture, and archive Web pages in Org-mode](https://github.com/alphapapa/org-web-tools)\n\n# Plans\n\nAdd to Python Package Index.\n\nMake it faster. Do concurrent HTTP requests somehow.\n\nIgnore files such as images.\n\nRewrite to golang to avoid dependencies for end users.\n\nSet another user agent.\n\nChange the name.\n\norg-mode gif.\n',
    'author': 'Anders K. Pettersen',
    'author_email': 'andstatical@gmail.com',
    'maintainer': None,
    'maintainer_email': None,
    'url': None,
    'package_dir': package_dir,
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'entry_points': entry_points,
    'python_requires': '>=3.8.0',
}


setup(**setup_kwargs)
