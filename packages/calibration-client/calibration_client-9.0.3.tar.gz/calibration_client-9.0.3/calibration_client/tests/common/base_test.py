"""Tests for Base class"""

from ...common.base import Base


def test_load_json_from_str():
    json_01 = Base.load_json_from_str('')
    assert json_01 == {}

    json_02 = Base.load_json_from_str('{"hello": "world"}')
    assert json_02 == {'hello': 'world'}


def test_response_success():
    # CREATE
    res = Base.response_success('MOD_01', 'CREATE', '{content hash}')
    expected_res = {'success': True, 'info': 'MOD_01 created successfully',
                    'app_info': {}, 'data': '{content hash}'}
    assert res == expected_res

    # UPDATE
    res = Base.response_success('MOD_02', 'UPDATE', '{content hash}')
    expected_res = {'success': True, 'info': 'MOD_02 updated successfully',
                    'app_info': {}, 'data': '{content hash}'}
    assert res == expected_res

    # GET
    res = Base.response_success('MOD_03', 'GET', '{content hash}')
    expected_res = {'success': True, 'info': 'Got MOD_03 successfully',
                    'app_info': {}, 'data': '{content hash}'}
    assert res == expected_res

    # DELETE
    res = Base.response_success('MOD_04', 'DELETE', '{content hash}')
    expected_res = {'success': True, 'info': 'MOD_04 deleted successfully',
                    'app_info': {}, 'data': '{content hash}'}
    assert res == expected_res

    # SET
    res = Base.response_success('MOD_05', 'SET', '{content hash}')
    expected_res = {'success': True, 'info': 'MOD_05 set successfully',
                    'app_info': {}, 'data': '{content hash}'}
    assert res == expected_res

    # OTHER_ACTION
    res = Base.response_success('MOD_06', 'OTHER_ACTION', '{content hash}')
    expected_res = {'success': False, 'info': 'ACTION is not correct!',
                    'app_info': '{content hash}', 'data': {}}
    assert res == expected_res


def test_response_error():
    # CREATE
    res = Base.response_error('MOD_01', 'CREATE', 'Error 01')
    expected_res = {'success': False, 'info': 'Error creating MOD_01',
                    'app_info': 'Error 01', 'data': {}}
    assert res == expected_res

    # UPDATE
    res = Base.response_error('MOD_02', 'UPDATE', 'Error 02')
    expected_res = {'success': False, 'info': 'Error updating MOD_02',
                    'app_info': 'Error 02', 'data': {}}
    assert res == expected_res

    # GET
    res = Base.response_error('MOD_03', 'GET', 'Error 03')
    expected_res = {'success': False, 'info': 'MOD_03 not found!',
                    'app_info': 'Error 03', 'data': {}}
    assert res == expected_res

    # DELETE
    res = Base.response_error('MOD_04', 'DELETE', 'Error 04')
    expected_res = {'success': False, 'info': 'Error deleting MOD_04',
                    'app_info': 'Error 04', 'data': {}}
    assert res == expected_res

    # SET
    res = Base.response_error('MOD_05', 'SET', 'Error 05')
    expected_res = {'success': False, 'info': 'Error setting MOD_05',
                    'app_info': 'Error 05', 'data': {}}
    assert res == expected_res

    # OTHER_ACTION
    res = Base.response_error('MOD_06', 'OTHER_ACTION', 'Error 06')
    expected_res = {'success': False, 'info': 'ACTION is not correct!',
                    'app_info': 'Error 06', 'data': {}}
    assert res == expected_res
