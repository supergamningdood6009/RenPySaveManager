import pytest
import RPSN
import os

orcpath = ["path/","../saves/"]

def TstProf(name,per):
    RPSN.makeprof(lambda: name,lambda:per)

    assert RPSN.data["profiles"][-1] ==name
    for elfpath in orcpath:
        assert os.path.exists(elfpath+name)
        if(per):
            assert os.path.exists(elfpath+"yay/persistent")
    yield True

    for elfpath in orcpath:
        if(per):
            os.remove(elfpath+"yay/persistent")
        os.rmdir(elfpath+name)

    RPSN.unmakeprof(lambda: name)
    assert RPSN.data["profiles"][-1] != name
    yield True
    
def test_makeunmake_prof():
    profiler = TstProf("yay",False)
    next(profiler)
    next(profiler)

def test_makeunmake_persistent():
    profiler = TstProf("yay",True)
    next(profiler)
    next(profiler)

# def test_changeprof():
#     profiler = TstProf("yay",False)
#     active