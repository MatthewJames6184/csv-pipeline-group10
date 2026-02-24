from functions.scan_input_folder import scan_input_folder_for_new_csv

def test_scan_returns_list():
    result = scan_input_folder_for_new_csv()
    assert isinstance(result, list)
