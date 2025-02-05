import os, sys
import unittest

from numpy import unique, all
from pandas.core import frame
from pandas import DataFrame, Index
from ecodynelec.preprocessing import load_impacts
from ecodynelec.preprocessing.auxiliary import get_default_file


def get_rootpath(level=0):
    rp = os.path.dirname( os.path.abspath(__file__) )
    for _ in range(level):
        rp = os.path.dirname(rp)
    return (rp + "/").replace("\\","/").replace("//","/")


class TestLoadImpacts(unittest.TestCase):
    
    def __init__(self, *args, **kargs):
        super().__init__(*args, **kargs)
        parent_dir = os.path.dirname( os.path.dirname( os.path.abspath(__file__) ) ) # Parent of file dir

        self.template = get_default_file('mapping_template.xlsx')
        self.mapping = os.path.join(parent_dir, "examples/test_data/other/mapping_test.xlsx")
        self.noRes_mapping = os.path.join(parent_dir, "examples/test_data/other/mapping_testNoResidual.xlsx")
        
        
    ###########################
    #### EXTRACT UI
    def test_extractUI_isFrame(self):
        self.assertIsInstance( load_impacts.extract_UI(path_ui=None, ctry=['AT','CH','CZ','DE','FR','IT'],
                                                       target='CH', residual=False),
                              frame.DataFrame)
        
    def test_extractUI_isFrameResidual(self):
        self.assertIsInstance( load_impacts.extract_UI(path_ui=None, ctry=['AT','CH','CZ','DE','FR','IT'],
                                                       target='CH', residual=True),
                              frame.DataFrame)
        
    ###########################
    #### COUNTRY FROM EXCEL
    def test_ctryFromExcel_MissingCtry(self):
        with self.assertRaises(ValueError):
            load_impacts.country_from_excel(self.template, place="KZ")
            
    def test_ctryFromExcel_TemplateCtry(self):
        ctry = ['AT','BA','BE','BG','CH','CY','CZ','DE','DK','EE','ES','FI','FR',
                'GE','GR','HR','HU','IE','IT','LT','LU','LV','MD','ME','MK','NL',
                'NO','PL','PT','RO','RS','SE','SI','SK','UA','UK','XK']
        self.assertTrue( all(isinstance(load_impacts.country_from_excel(self.template, place=c),
                                        frame.DataFrame, msg=c)
                             for c in ctry)  )
    
    ###########################
    #### RESIDUAL FROM EXCEL
    def test_residualFromExcel_NoCHError(self):
        with self.assertRaises(ValueError):
            load_impacts.residual_from_excel(self.noRes_mapping, place='CH')
            
    ###########################
    #### OTHER FROM EXCEL
    def test_otherFromExcel_fromTemplate(self):
        self.assertIsInstance( load_impacts.other_from_excel(self.template),
                               frame.DataFrame, msg="other from Template")
            
    ###########################
    #### EXTRACT MAPPING
    def test_extractMapping_PathError(self):
        with self.assertRaises(TypeError):
            load_impacts.extract_mapping(ctry=None)
            
    def test_extractMapping_NoCHError(self):
        with self.assertRaises(ValueError):
            load_impacts.extract_mapping(ctry='AT',mapping_path=self.mapping,residual=True,target='AT')
            
    def test_extractMapping_rightValues(self):
        self.assertTrue( all( load_impacts.extract_mapping(ctry='CH',mapping_path=self.mapping,residual=False,target='CH').values==-1 ) )
        
        
#############
if __name__=='__main__':
    res = unittest.main(verbosity=2)
