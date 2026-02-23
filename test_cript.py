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
    
def TstChange(name):
    active = RPSN.data["active"]
    flights = {}
    for elfpath in orcpath:
        flights[elfpath] = os.listdir(elfpath)
    
    RPSN.putFilesAway()
    flys = {}
    for elfpath in orcpath:

        flies = os.listdir(elfpath)
        flys[elfpath] = flies
        fleas = os.listdir(elfpath+active)
        
        for flight in flights[elfpath]:
            if flight not in flies:
                if flight[-2:]!=".Σ":
                    assert flight[-5:]==".save"
                    assert flight in fleas
    yield True
    flees = {}
    for elfpath in orcpath:
        flees[elfpath] = os.listdir(elfpath+name)
    RPSN.takeFilesOut(name)
    RPSN.data["active"]=name
    for elfpath in orcpath:
        
        flies = os.listdir(elfpath)
        for fly in flies:
            if fly not in flys[elfpath]:
                if fly[-2:]!=".Σ":
                    assert fly[-5:]==".save"
    yield True


def test_makeunmake_prof():
    profiler = TstProf("yay",False)
    next(profiler)
    next(profiler)

def test_makeunmake_persistent():
    profiler = TstProf("yay",True)
    next(profiler)
    next(profiler)


def test_changeprof():
    active = RPSN.data["active"]
    profiler = TstProf("yay",False)
    next(profiler)
    changer = TstChange("yay") 
    next(changer)

    for elfpath in orcpath:    
        pers = open(elfpath+"yay/πενισ.save","w")
        pers.write("yayayyippee")
        pers.close()

    next(changer)
    for elfpath in orcpath:
        assert os.path.exists(elfpath+"πενισ.save")
        erms = open(elfpath+"πενισ.save","r")
        assert erms.read()=="yayayyippee"
        erms.close()

    rechanger = TstChange(active)
    next(rechanger)
    next(rechanger)
    
    for elfpath in orcpath:
        assert os.path.exists(elfpath+"yay/πενισ.save")
        erms = open(elfpath+"yay/πενισ.save","r")
        assert erms.read()=="yayayyippee"
        erms.close()
        os.remove(elfpath+"yay/πενισ.save")

    next(profiler)

