def test_empty_object(worksheet):
    ws = worksheet
    sheet_items = ws.sheet_items
    assert sheet_items == []


def test_parse_xlsx_headers(worksheet):
    ws = worksheet
    path = "tests/inventory.csv"
    csv_file = open(path, "r", encoding="utf-8-sig")
    ws.csv_to_dict(csv_file=csv_file, delimiter=";")
    ws_headers = ws.headers()
    assert "Bratislava" in str(ws_headers)
    assert "SK" in str(ws_headers)
    assert ws_headers == {
        "state": "SK",
        "city": "Bratislava",
        "citizens": "400000",
        "": "11",
        "random_field": "cc",
    }


def test_parse_xlsx_all_items(worksheet):
    ws = worksheet
    path = "tests/inventory.csv"
    csv_file = open(path, "r", encoding="utf-8-sig")
    ws_items = ws.csv_to_dict(csv_file=csv_file, delimiter=";")
    assert "Bratislava" in str(ws_items)
    assert "Miami" in str(ws_items)


def test_parse_xlsx_sheet_items(worksheet):
    ws = worksheet
    path = "tests/inventory.csv"
    csv_file = open(path, "r", encoding="utf-8-sig")
    ws.csv_to_dict(csv_file=csv_file, delimiter=";")
    ws_items = ws.sheet_items
    assert "Bratislava" in str(ws_items)
    assert "Miami" in str(ws_items)
    assert len(ws_items) > 1
    assert len(ws_items) == 6
