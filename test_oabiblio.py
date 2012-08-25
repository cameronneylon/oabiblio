from oabiblio import *
import unittest
import random

class DOAJTest(unittest.TestCase):

    def setUp(self):
        self.pone = Journal("PLoS ONE")
        self.actamaz = Journal("Acta Amazonica")

    def test_doaj_plosone(self):
        self.pone.get_licence_from_doaj()
        self.assertEqual(self.pone.licence, "http://creativecommons.org/licenses/by/3.0/legalcode")
        self.assertTrue(self.pone.isCCBY())
        self.assertFalse(self.pone.isCCBYNC())

    def test_actam_plosone(self):
        self.actamaz.get_licence_from_doaj()
        self.assertEqual(self.actamaz.licence, "http://creativecommons.org/licenses/by-nc/3.0/legalcode")
        self.assertFalse(self.actamaz.isCCBY())
        self.assertTrue(self.actamaz.isCCBYNC())
 

class CrossRefTest(unittest.TestCase):

    def setUp(self):
        self.test_quarter = "Q311"
        self.crossreftest = CrossRefDepRecordParser(self.test_quarter, test = True)
        self.testpub = [{'ud': 28, 'cy': 25, 'by': 0, 'type': 'J',
                        'name': 'American Journal of Critical Care'},
                        {'ud': 15, 'cy': 15, 'by': 0, 'type': 'J',
                         'name': 'Critical Care Nurse'}]
        self.testparsedlist = [{'ud': 28, 'cy': 25, 'by': 0, 'type': 'J',
                                'name': 'American Journal of Critical Care'},
                               {'ud': 15, 'cy': 15, 'by': 0, 'type': 'J',
                                'name': 'Critical Care Nurse'},
                               {'ud': 0, 'cy': 7, 'type': 'J',
                                'name': 'AAPG Bulletin', 'by': 0},
                               {'ud': 0, 'cy': 12, 'by': 22, 'type': 'J',
                                'name': 'The International Journal of Forensic Computer Science'}]
        self.testfiletext = """name,type,cy,by,ud
American Journal of Critical Care,J,25,0,28
Critical Care Nurse,J,15,0,15
AAPG Bulletin,J,7,0,0
The International Journal of Forensic Computer Science,J,12,22,0
"""

    def tearDown(self):
        self.crossreftest = None

    def test_crossref_parse_functions(self):
        
        parsed_response = self.crossreftest.parse_response(self.crossreftest.get_record())
        publishers = self.crossreftest.get_publishers(parsed_response)
        self.assertEqual(len(publishers), 5)
        test_journals = self.crossreftest.parse_journals(publishers[1])
        self.assertEqual(test_journals, self.testpub)

    def test_crossref_get_and_parse_records(self):

        self.crossreftest.get_and_parse_dep_record()
        self.assertEqual(self.crossreftest.journal_list, self.testparsedlist)

    def test_write_csv(self):

        self.crossreftest.get_and_parse_dep_record()
        self.crossreftest.write_journal_list("crossreftest.csv")
        with open("crossreftest.csv", 'rU') as f:
            self.assertEqual(f.read(), self.testfiletext)

        
class TestPopulateJournalsWithCCLicence(unittest.TestCase):

    def setUp(self):
        self.testlicence = "http://creativecommons.org/licenses/by/3.0/legalcode"
        self.testcase = JournalsWithCCLicence()

    def test_populate_CCBY(self):
        self.testcase.populate()        

        # Test the correct licences for 5 random entries. This test currently
        # fails on journal names with non-english characters.
        i=0
        while i < 3:
            random.seed()
            index = random.randint(1, len(self.testcase.journal_list))
            test_journal = self.testcase.journal_list[index]
            print test_journal.name
            doaj_journal = Journal(test_journal.name)
            if doaj_journal.get_licence_from_doaj():
                self.assertEqual(test_journal.licence, doaj_journal.licence)
            i+=1
        
        
if __name__ == '__main__':
    unittest.main()
