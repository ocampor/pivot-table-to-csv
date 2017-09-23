from models import PivotCacheDefinition


class test_PivotCacheDefinition():
    print(PivotCacheDefinition("/home/ocampor/AMIS/SESAS_2016/TD MT Robo Total 2016.xlsx").parse())
    assert False