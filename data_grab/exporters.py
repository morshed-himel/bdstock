from scrapy.exporters import CsvItemExporter


class MyCsvItemExporter(CsvItemExporter):
    header_map = {
        'category': "Category",
        'company_name': "Name of the Company",
        'code': 'Trading Code',
        'op': 'Opening Price',
        'cp': 'Closing Price',
        'dif_op_cp': 'Difference (Open-Closing)',
        'ltp': 'Last Traded Price',
        'high': 'Highest Price',
        'low': 'Lowest Price',
        'dif_high_low': 'Difference (High-Low)',
        'days_vol': 'Days Volume (mn)',
        'no_shares_traded': 'No. of shares traded',
        'no_trades': 'No. of  Trades',
        'market_cap': 'Market Capitalization (mn)',
        '52_high': '52 Weeks Moving Range High',
        '52_low': '52 Weeks Moving Range Low',
        'total_shares': 'Total No. of shares',
        'total_shares_10': '10% of Total shares',
        'time': 'Update Time',
    }

    def __init__(self, *args, **kwargs):
        kwargs["delimiter"] = "\t"
        super(MyCsvItemExporter, self).__init__(*args, **kwargs)

    def _write_headers_and_set_fields_to_export(self, item):
        if not self.include_headers_line:
            return
        # this is the parent logic taken from parent class
        if not self.fields_to_export:
            if isinstance(item, dict):
                # for dicts try using fields of the first item
                self.fields_to_export = list(item.keys())
            else:
                # use fields declared in Item
                self.fields_to_export = list(item.fields.keys())
        headers = list(self._build_row(self.fields_to_export))

        # here we add our own extra mapping
        # map headers to our value
        headers = [self.header_map.get(header, header) for header in headers]
        self.csv_writer.writerow(headers)


class cseItemExporter(CsvItemExporter):
    header_map = {
        'company_name': "Company",
        'code': 'Trading Code',
        'op': 'Opening Price',
        'cp': 'Closing Price',
        'ltp': 'Last Traded Price',
        'high': 'Highest Price',
        'low': 'Lowest Price',
        'days_vol': 'Days Volume (mn)',
        'no_trades': 'No. of  Trades',
        'market_cap': 'Market Capitalization (mn)',
        'auth_cap': 'Authorized Capital in BDT* (mn)',
        'paid_cap': 'Paid-up Capital in BDT* (mn)',
        'face_val': 'Face Value',
        'paid_shr': 'Paid up Share',
        'time': 'Update Time',
    }

    def __init__(self, *args, **kwargs):
        kwargs["delimiter"] = "\t"
        super(cseItemExporter, self).__init__(*args, **kwargs)

    def _write_headers_and_set_fields_to_export(self, item):
        if not self.include_headers_line:
            return
        # this is the parent logic taken from parent class
        if not self.fields_to_export:
            if isinstance(item, dict):
                # for dicts try using fields of the first item
                self.fields_to_export = list(item.keys())
            else:
                # use fields declared in Item
                self.fields_to_export = list(item.fields.keys())
        headers = list(self._build_row(self.fields_to_export))

        # here we add our own extra mapping
        # map headers to our value
        headers = [self.header_map.get(header, header) for header in headers]
        self.csv_writer.writerow(headers)
