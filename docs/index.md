## README

Here is the README:

<pre>
{{ d['/README'] }}
</pre>

## Command Line Interface

{{ d['command-line.sh|idio|shint|pyg']['help'] }}

## Documentation

Here is a doc string:

<pre>
'{{ d['modules.txt|pydoc']['oabiblio.journal.Journal.__doc__:value'] }}'
</pre>

Here is method source code for a method in JournalsWithCCLicence:

{{ d['modules.txt|pydoc']['oabiblio.journal_list.JournalsWithCCLicence.populate:html-source'] }}

## List of Keys

This is a list of keys available in `modules.txt|pydoc` you can include in documentation:

{% for k in sorted(d['modules.txt|pydoc'].kv_storage().keys()) -%}
* `{{ k }}`
{% endfor -%}
