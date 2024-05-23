import unittest
from unittest.mock import patch, MagicMock
import pandas as pd
from pj_div import Dividend

class TestDividend(unittest.TestCase):
    def setUp(self):
        # 각 테스트 전에 실행되어 Dividend 객체를 생성합니다.
        self.dividend = Dividend()

    @patch('pj_div.fdr.StockListing')
    def test_GetStockList(self, mock_StockListing):
        # fdr.StockListing를 모킹하여 상장회사 목록을 반환합니다.
        mock_StockListing.return_value = pd.DataFrame({
            'Code': ['0001', '0002', '0003'],
            'Name': ['Company A', 'Company B', 'Company C'],
            'Market': ['KOSPI', 'KOSDAQ', 'KONEX']
        })

        # GetStockList 메서드를 호출하고 결과를 검증합니다.
        result = self.dividend.GetStockList()

        # KRX 거래소에서 KONEX를 제외하는지 확인합니다.
        self.assertEqual(len(result), 2)  # KOSPI와 KOSDAQ만 포함
        self.assertNotIn('0003', result['Code'].values)  # KONEX는 제외

    @patch('pj_div.OpenDartReader')
    def test_DispalyTable(self, mock_OpenDartReader):
        # OpenDartReader 객체와 그 report 메서드를 모킹합니다.
        mock_dart = MagicMock()
        mock_dart.report.return_value = pd.DataFrame({
            'se': ['현금배당수익률(%)', '주당 현금배당금(원)'],
            'thstrm': ['5.0', '1000']
        })
        mock_OpenDartReader.return_value = mock_dart

        # DispalyTable 메서드를 호출하고 결과를 검증합니다.
        result = self.dividend.DispalyTable('fake_api_code', '0001', 2023)
        self.assertEqual(result.loc[0, 'thstrm'], '5.0')
        self.assertEqual(result.loc[1, 'thstrm'], '1000')

    @patch('pj_div.OpenDartReader')
    def test_GetDividendRate(self, mock_OpenDartReader):
        # OpenDartReader 객체와 그 report 메서드를 모킹합니다.
        mock_dart = MagicMock()
        mock_dart.report.return_value = pd.DataFrame({
            'se': ['현금배당수익률(%)'],
            'thstrm': ['5.0']
        })
        mock_OpenDartReader.return_value = mock_dart

        # GetStockList 메서드를 모킹하여 상장회사 목록을 반환합니다.
        with patch.object(self.dividend, 'GetStockList') as mock_GetStockList:
            mock_GetStockList.return_value = pd.DataFrame({
                'Code': ['0001'],
                'Name': ['Company A'],
                'Market': ['KOSPI']
            })

            # GetDividendRate 메서드를 호출하고 결과를 검증합니다.
            result = self.dividend.GetDividendRate('fake_api_code', 2023, print_option=False)
            self.assertEqual(result, [5.0])

    @patch('pj_div.OpenDartReader')
    def test_GetDividendPerShare(self, mock_OpenDartReader):
        # OpenDartReader 객체와 그 report 메서드를 모킹합니다.
        mock_dart = MagicMock()
        mock_dart.report.return_value = pd.DataFrame({
            'se': ['주당 현금배당금(원)'],
            'thstrm': ['1000']
        })
        mock_OpenDartReader.return_value = mock_dart

        # GetStockList 메서드를 모킹하여 상장회사 목록을 반환합니다.
        with patch.object(self.dividend, 'GetStockList') as mock_GetStockList:
            mock_GetStockList.return_value = pd.DataFrame({
                'Code': ['0001'],
                'Name': ['Company A'],
                'Market': ['KOSPI']
            })

            # GetDividendPerShare 메서드를 호출하고 결과를 검증합니다.
            result = self.dividend.GetDividendPerShare('fake_api_code', 2023, print_option=False)
            self.assertEqual(result, [1000.0])

if __name__ == '__main__':
    unittest.main()