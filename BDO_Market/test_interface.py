import pytest
import pytest_mock
import bdorequester as rq
import stonky_nerd_stuff as sn
import failstackcalculator as fs
import failstack_comparing as fc
import matplotlib.pyplot as plt
import interface as itf
import pprint



def test_help(capsys,monkeypatch):
    name = 'help'
    monkeypatch.setattr('builtins.input', lambda _: name)
    itf.Commander()
    captured = capsys.readouterr()
    assert captured.out[:11] == '\nEnchanting'
    
def test_prex1(capsys,monkeypatch):
    name = 'prex1'
    stats = 'disto, 4, 250'
    answers = iter([name, stats])
    monkeypatch.setattr('builtins.input', lambda _: next(answers))
    itf.Commander()
    captured = capsys.readouterr()
    assert captured.out == '-47.6 b\n'
    
def test_med1(capsys,monkeypatch):
    name = 'prmed1'
    stats = 'disto, 4, 250'
    answers = iter([name, stats])
    monkeypatch.setattr('builtins.input', lambda _: next(answers))
    itf.Commander()
    captured = capsys.readouterr()
    assert captured.out == '27.5 b\n'
    
def test_gamb1(capsys,monkeypatch):
    name = 'gamb1'
    stats = 'disto, 4, 250, 0'
    answers = iter([name, stats])
    monkeypatch.setattr('builtins.input', lambda _: next(answers))
    itf.Commander()
    captured = capsys.readouterr()
    assert captured.out == 'Tries to first success: 6\n'
    
def test_profx(capsys,monkeypatch):
    name = 'profx'
    stats = 'disto, 100, 0, 60'
    answers = iter([name, stats])
    monkeypatch.setattr('builtins.input', lambda _: next(answers))
    itf.Commander()
    captured = capsys.readouterr()
    assert captured.out == '22.5 b\n'
    
def test_gambx(capsys,monkeypatch):
    name = 'gambx'
    stats = 'disto, 100, 0, 60, 0'
    answers = iter([name, stats])
    monkeypatch.setattr('builtins.input', lambda _: next(answers))
    itf.Commander()
    captured = capsys.readouterr()
    assert captured.out == 'Successes: 90\n'
    
def test_progexp(capsys,monkeypatch):
    name='progexp'
    stats= 'disto, 100, 0, [40,60,70,110,250]'
    answers = iter([name, stats])
    monkeypatch.setattr('builtins.input', lambda _: next(answers))
    itf.Commander()
    captured = capsys.readouterr()
    assert captured.out[-8:] == '-14.8 b\n'
