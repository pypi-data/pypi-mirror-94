# MkDocs i18n plugin

A plugin to internationalize MkDocs. It adds links to translated pages for each page. It also hides other languages page links of navigation menu if there is a translation for current page language.

Example of mkdocs-18n usage: <https://mkdocs-i18n.gitlab.io/mkdocs-i18n>

Feel free to write your comments or request adaptations to your requirements at <https://gitlab.com/mkdocs-i18n/mkdocs-i18n/-/issues>.

## Case Studies

<http://isardvdi.com> (<https://isard.gitlab.com/isardvdi-docs>) is a multilingual community, most members know 2 languages but not the same ones, some understand 3... Each one has its favorite language and has different levels of knowledge about other languages. In addition, community documentation doesn't have a source language and not all documents need to be translated into all languages. Therefore, this plugin shows all available translations for the page shown at the top of the document and also for pages not translated into the language selected in the navigation menu.

## Setup

Install the plugin using pip:

`pip install mkdocs-i18n`

Configure the plugin via [mkdocs.yml](https://gitlab.com/mkdocs-i18n/mkdocs-i18n/-/blob/main/mkdocs.yml)

If you have no `plugins` entry in your configuration file you have `search` plugin enabled. If you create `plugins` entry to enable `i18n` plugin you also need to add `search` plugin if you want to have `search` plugin enabled.

## Donations:

- [Liberapay](https://liberapay.com/mkdocs-i18n/donate)
- [Bitcoin](bitcoin:15QqofyoWxDSZU9VbXwVZKFxAVdmpkE5uH?message=mkdocs-i18n)

## Other interesting works:

- [MkDocs Theme i18n](https://github.com/mkdocs/mkdocs/pull/1778): Work in progress.
- [Markdown i18n plugin](https://github.com/gisce/markdown-i18n): Provide translation of documents via po files but images cannot be localized.
- [MkDocs Multilang](https://pypi.org/project/mkdocs-multilang/): Only released for MkDocs < 1.0
- [Site language selector of Material for MkDocs](https://squidfunk.github.io/mkdocs-material/setup/changing-the-language/#site-language-selector): Do you know what it does?
