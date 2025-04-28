#Project Support
Core principles:

* Please work only on what interests you and what you plan to use yourself.
* Please test your code on real systems to ensure it works.
* If possible, use your code in practice — this will improve its quality.

## Plugins

If you’re creating a plugin, please:

* Create a separate GitHub (or other platform) repository for it.
* The project can consist of just a single plugin_*.py file. Do not copy the entire core repository — avoid unnecessary duplication.
* Once created, share the link in here in github or here https://github.com/janvarev/Irene-Voice-Assistant/issues/1.
* Maintain your plugin independently if possible.



## Core Code
If your contribution requires changes to the core code and you want to submit a **Pull Request**:

For non-universal changes (i.e., improvements in some cases but drawbacks in others):

1. Modify the core.py plugin.
2. Add a toggle option to enable/disable your feature.
3. Set it to DISABLED by default.
4. Add any additional options for your feature to core.py (e.g., neural network recognition thresholds).
5. Document these options in Readme.md.

Additional guidelines:
1. Move anything that can be a standalone plugin into a plugin
2. Import heavy libraries only when they are actively used


## Code Style
The project has no strict code style guidelines, as the author is not fully committed to following standards at this time. Keep PEP8 in head but pull requests like "PEP8 compliance" are not the best right now.

Please avoid code style reformatting in your contributions.
