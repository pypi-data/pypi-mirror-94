# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['alacritty_colorscheme']

package_data = \
{'': ['*']}

install_requires = \
['pynvim>=0.4.2,<0.5.0',
 'ruamel.yaml>=0.16.10,<0.17.0',
 'typed-argument-parser>=1.6.1,<2.0.0']

entry_points = \
{'console_scripts': ['alacritty-colorscheme = alacritty_colorscheme.cli:main']}

setup_kwargs = {
    'name': 'alacritty-colorscheme',
    'version': '1.0.0',
    'description': 'Change colorscheme of alacritty with ease',
    'long_description': '# Alacritty Colorscheme\n\n![PyPI](https://img.shields.io/pypi/v/alacritty-colorscheme) ![PyPI - Downloads](https://img.shields.io/pypi/dm/alacritty-colorscheme)\n\nChange colorscheme of alacritty with ease.\n\n![Usage](https://user-images.githubusercontent.com/4928045/106160031-8267a880-61ad-11eb-9acf-b9d5cd5de3e4.gif)\n\n## Installation\n\nYou can install alacritty-colorscheme using pip:\n\n```bash\npip install --user alacritty-colorscheme\n```\n\n## Usage\n\n```\nusage: alacritty-colorscheme [-c configuration file] [-C colorscheme directory] [-V] [-h]\n                             {list,status,toggle,apply} ...\n```\n\n## Getting colorschemes\n\n- You can get colorschemes from [aaron-williamson/base16-alacritty](https://github.com/aaron-williamson/base16-alacritty)\n\n    ```bash\n    REPO="https://github.com/aaron-williamson/base16-alacritty.git"\n    DEST="$HOME/.aarors-williamson-colorschemes"\n\n    # Get colorschemes \n    git clone $REPO $DEST\n    # Create symlink at default colors location (optional)\n    ln -s "$DEST/colors" "$HOME/.config/alacritty/colors"\n    ```\n\n- You can also get colorschemes from from [eendroroy/alacritty-theme](https://github.com/eendroroy/alacritty-theme)\n\n    ```bash\n    REPO=https://github.com/eendroroy/alacritty-theme.git\n    DEST="$HOME/.eendroroy-colorschemes"\n    # Get colorschemes\n    git clone $REPO $DEST\n    # Create symlink at default colors location (optional)\n    ln -s "$DEST/themes" "$HOME/.config/alacritty/colors"\n    ```\n\n## Sync with vim/neo-vim\n\nIf you are using base16 colorschemes from\n[base16-vim](https://github.com/chriskempson/base16-vim) plugin, you can use\nthe `-V` argument to automatically generate `~/.vimrc_background` file when you\nchange alacritty colorscheme. You will need to source this file in your vimrc\nto load the same colorscheme in vim.\n\nAdd this in your `.vimrc` file:\n\n```vim\nif filereadable(expand("~/.vimrc_background"))\n  let base16colorspace=256          " Remove this line if not necessary\n  source ~/.vimrc_background\nendif\n```\n\nWhen you change your alacritty colorscheme, you simply need to source\n`~/.vimrc_background` or your `vimrc`.\nIf you are a neo-vim user, `~/.vimrc_background` will be automatically sourced.\n\n## Examples\n\n### bash/zsh aliases\n\nAdd this in your `.zshrc` or `.bashrc` file:\n\n```bash\nLIGHT_COLOR=\'base16-gruvbox-light-soft.yml\'\nDARK_COLOR=\'base16-gruvbox-dark-soft.yml\'\n\nalias day="alacritty-colorscheme -V apply $LIGHT_COLOR"\nalias night="alacritty-colorscheme -V apply $DARK_COLOR"\nalias toggle="alacritty-colorscheme -V toggle $LIGHT_COLOR $DARK_COLOR"\n```\n\n### i3wm/sway bindings\n\nAdd this in your i3 `config` file:\n\n```bash\nset $light_color base16-gruvbox-light-soft.yml\nset $dark_color base16-gruvbox-dark-soft.yml\n\n# Toggle between light and dark colorschemes\nbindsym $mod+Shift+n exec alacritty-colorscheme -V toggle $light_color $dark_color\n\n# Toggle between all available colorschemes\nbindsym $mod+Shift+m exec alacritty-colorscheme -V toggle\n\n# Get notification with current colorscheme\nbindsym $mod+Shift+b exec notify-send "Alacritty Colorscheme" `alacritty-colorscheme status`\n```\n\n## Development\n\n### Running locally\n\n```bash\npip install --user poetry\n\ngit clone https://github.com/toggle-corp/alacritty-colorscheme.git\ncd alacritty-colorscheme\n\npoetry install\npoetry run python -m alacritty_colorscheme.cli\n```\n\n### Installing locally\n\n```bash\npip install --user .\n```\n\n## License\n\nContent of this repository is released under the [Apache License, Version 2.0].\n\n[Apache License, Version 2.0](./LICENSE-APACHE)\n',
    'author': 'Safar Ligal',
    'author_email': 'weathermist@gmail.com',
    'maintainer': None,
    'maintainer_email': None,
    'url': 'https://github.com/toggle-corp/alacritty-colorscheme/',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'entry_points': entry_points,
    'python_requires': '>=3.6,<4.0',
}


setup(**setup_kwargs)
