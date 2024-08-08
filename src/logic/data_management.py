def get_table_data(table):
    data = []
    for row in range(table.rowCount()):
        row_data = []
        for col in range(table.columnCount()):
            item = table.item(row, col)
            if item is not None:
                value = item.text()
                if col == 5:  # Amount column
                    try:
                        # Remove the pound sign and any commas, then convert to float
                        amount_str = value.replace('£', '').replace(',', '')
                        value = float(amount_str)
                    except ValueError:
                        print(f"Warning: Could not convert amount to float: {value}")
                        continue
                row_data.append(value)
        if len(row_data) == table.columnCount():  # Only append if all columns have data
            data.append(row_data)
    return data