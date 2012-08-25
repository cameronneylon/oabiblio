This is a report

one plus one is {{ 1+1 }}.

<table>
<tr><th>Quarter</th><th>Total Deposits</th></tr>
{% for row in data -%}
<tr><td>{{ row.quarter }}</td><td>{{ row.total_deposits }}</tr></tr>
{% endfor -%}
</table>

Here is a chart:

<img src="chart.svg" />
