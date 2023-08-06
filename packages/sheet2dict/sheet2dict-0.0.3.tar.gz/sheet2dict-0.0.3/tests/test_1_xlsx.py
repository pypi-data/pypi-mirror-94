def test_empty_object(worksheet):
    ws = worksheet
    sheet_items = ws.sheet_items
    assert sheet_items == []


def test_parse_xlsx_headers(worksheet):
    ws = worksheet
    ws.xlsx_to_dict(path="tests/inventory.xlsx")
    ws_headers = ws.headers()
    assert ws_headers == {
        "state": "SK",
        "city": "Bratislava",
        "citizens": "400000",
        None: "11",
        "random_field": "cc",
    }


def test_parse_xlsx_all_items(worksheet):
    ws = worksheet
    ws_items = ws.xlsx_to_dict(path="tests/inventory.xlsx")
    assert "Bratislava" in str(ws_items)
    assert "Miami" in str(ws_items)


def test_parse_xlsx_sheet_items(worksheet):
    ws = worksheet
    ws.xlsx_to_dict(path="tests/inventory.xlsx")
    ws_items = ws.sheet_items
    assert "Bratislava" in str(ws_items)
    assert "Miami" in str(ws_items)
    assert len(ws_items) > 1
    assert len(ws_items) == 6


from io import BytesIO

path = "tests/inventory.xlsx"
xlsx_file = open(path, "rb")
xlsx_file = BytesIO(xlsx_file.read())


def test_parse_xlsx_all_items_as_object(worksheet):
    ws = worksheet
    ws_items = ws.xlsx_to_dict(path=xlsx_file)
    assert "Bratislava" in str(ws_items)
    assert "Miami" in str(ws_items)


def test_parse_xlsx_sheet_items_as_object(worksheet):
    ws = worksheet
    ws.xlsx_to_dict(path=xlsx_file)
    ws_items = ws.sheet_items
    assert "Bratislava" in str(ws_items)
    assert "Miami" in str(ws_items)
    assert len(ws_items) > 1
    assert len(ws_items) == 6
