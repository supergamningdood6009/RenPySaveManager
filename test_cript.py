import pytest
import RPSN
import os
from pathlib import Path
orcpath = [Path("path/").resolve(),Path("../saves/").resolve()]

def TstProf(name,per):
    RPSN.makeprof(lambda: name,lambda:per)

    assert RPSN.data["profiles"][-1] ==name
    for elfpath in orcpath:
        assert (elfpath/name).exists()
        if(per):
            assert (elfpath/name/"persistent").exists()
    yield True

    for elfpath in orcpath:
        if(per):
            (elfpath/name/"persistent").unlink()
        (elfpath/name).rmdir()

    RPSN.unmakeprof(lambda: name)
    assert RPSN.data["profiles"][-1] != name
    yield True
    
def TstChange(name):
    active = RPSN.data["active"]
    flights = {}
    for elfpath in orcpath:
        flights[elfpath] = (elfpath).iterdir()
    
    RPSN.putFilesAway()
    flys = {}
    for elfpath in orcpath:

        flies = (elfpath).iterdir()
        flys[elfpath] = flies
        fleas = (elfpath/active).iterdir()
        
        # for flight in flights[elfpath]:
        #     if flight not in flies:
        #         if flight.suffix!=".Σ":
        #             assert flight.suffix==".save"
        #             # assert flight in fleas
    yield True
    flees = {}
    for elfpath in orcpath:
        flees[elfpath] = (elfpath/name).iterdir()
    RPSN.takeFilesOut(name)
    RPSN.data["active"]=name
    for elfpath in orcpath:
        
        flies = (elfpath).iterdir()
        # for fly in flies:
        #     if fly not in flys[elfpath]:
        #         if fly.suffix!=".Σ":
        #             assert fly.suffix==".save"
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
        pers = open(elfpath/"yay"/"πενισ.save","w")
        pers.write("yayayyippee")
        pers.close()

    next(changer)
    for elfpath in orcpath:
        assert (elfpath/"πενισ.save").exists()
        erms = open(elfpath/"πενισ.save","r")
        assert erms.read()=="yayayyippee"
        erms.close()

    rechanger = TstChange(active)
    next(rechanger)
    next(rechanger)
    
    for elfpath in orcpath:
        assert (elfpath/"yay"/"πενισ.save").exists()
        erms = open(elfpath/"yay"/"πενισ.save","r")
        assert erms.read()=="yayayyippee"
        erms.close()
        (elfpath/"yay"/"πενισ.save").unlink()

    next(profiler)

