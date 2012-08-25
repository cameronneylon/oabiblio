from oabiblio import *

for year in ['12']:
    for quarter in ['Q1', 'Q2']:
        crossrefrecord = CrossRefDepRecordParser(quarter+year)
        crossrefrecord.get_and_parse_dep_record()
        crossrefrecord.write_journal_list(quarter+year+'.csv')
        
