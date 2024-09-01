# -*- coding: utf-8 -*-

import sys
import os
import json
from PyQt5.QtWidgets import QApplication, QWidget, QLabel, QLineEdit, QPushButton, QVBoxLayout, QHBoxLayout, QTableWidget, QTableWidgetItem, QMessageBox, QHeaderView, QDesktopWidget
from PyQt5.QtCore import Qt
import yfinance as yf

class StockApp(QWidget):
    def __init__(self):
        super().__init__()

        # 창의 제목과 크기 설정
        self.setWindowTitle('미국 주식 현재가 현황')
        self.setGeometry(100, 100, 900, 620)
        self.center()  # 창을 중앙에 위치시킴

        # 타이틀 라벨
        title_label = QLabel('미국 주식 현재가 현황', self)
        title_label.setAlignment(Qt.AlignCenter)
        title_label.setStyleSheet("font-size: 20pt;")

        # 입력 필드와 버튼 구성
        self.ticker_input = QLineEdit(self)
        self.ticker_input.setPlaceholderText('틱커명 입력')
        self.ticker_input.setStyleSheet("""
            font-size: 11pt;
            text-transform: uppercase;
            border-radius: 30px;
            padding: 10px;
        """)
        self.ticker_input.returnPressed.connect(self.search_stock)  # 엔터키로 검색 후 입력 필드 초기화

        search_button = QPushButton('검색', self)
        search_button.setStyleSheet("""
            QPushButton {
                font-size: 10pt;
                background-color: #5c92f7;
                color: white;
                border-radius: 30px;
                padding: 10px;
            }
            QPushButton:pressed {
                background-color: #3a6fb0;
            }
        """)
        search_button.clicked.connect(self.search_stock)

        delete_button = QPushButton('삭제', self)
        delete_button.setStyleSheet("""
            QPushButton {
                font-size: 10pt;
                background-color: #5c92f7;
                color: white;
                border-radius: 30px;
                padding: 10px;
            }
            QPushButton:pressed {
                background-color: #3a6fb0;
            }
        """)
        delete_button.clicked.connect(self.delete_stock)

        reset_button = QPushButton('리셋', self)
        reset_button.setStyleSheet("""
            QPushButton {
                font-size: 10pt;
                background-color: #5c92f7;
                color: white;
                border-radius: 30px;
                padding: 10px;
            }
            QPushButton:pressed {
                background-color: #3a6fb0;
            }
        """)
        reset_button.clicked.connect(self.reset_table)

        # 버튼 레이아웃
        button_layout = QHBoxLayout()
        button_layout.addWidget(search_button)
        button_layout.addWidget(delete_button)
        button_layout.addWidget(reset_button)

        # 리스트 테이블 타이틀 라벨
        table_title_label = QLabel('검색결과현황', self)
        table_title_label.setAlignment(Qt.AlignCenter)
        table_title_label.setStyleSheet("font-size: 15pt;")

        # 테이블 구성
        self.stock_table = QTableWidget(self)
        self.stock_table.setColumnCount(7)
        self.stock_table.setHorizontalHeaderLabels(['틱커명', '종목명', '1년전주가', '6개월전주가', '현재주가', '등락폭', '등락률'])
        self.stock_table.setStyleSheet("font-size: 10pt;")
        self.stock_table.horizontalHeader().setStyleSheet("QHeaderView::section {background-color: #898b8c; color: white;}")  # 헤더 바탕색 및 글자색 설정
        self.stock_table.horizontalHeader().setSectionResizeMode(QHeaderView.Stretch)  # 헤더 크기 자동 조정
        self.stock_table.setAlternatingRowColors(True)  # 셀의 배경색을 기본값으로

        # 테이블 클릭 이벤트 연결
        self.stock_table.cellClicked.connect(self.load_stock_to_input)

        # 하단 인용구 라벨
        footer_label = QLabel('made by 나종춘(2024)', self)
        footer_label.setAlignment(Qt.AlignRight)
        footer_label.setStyleSheet("font-size: 10pt;")

        # 레이아웃 구성
        layout = QVBoxLayout()
        layout.setSpacing(20)  # 위젯 간의 간격을 20px로 설정
        layout.setContentsMargins(10, 10, 10, 10)  # 레이아웃의 여백을 상하좌우 10px로 설정
        layout.addWidget(title_label)
        layout.addWidget(self.ticker_input)
        layout.addLayout(button_layout)
        layout.addWidget(table_title_label)
        layout.addWidget(self.stock_table)
        layout.addWidget(footer_label)

        self.setLayout(layout)

        # JSON 파일에서 데이터 로드
        self.load_data_from_json()

    def center(self):
        # 창을 모니터 중앙에 위치시키는 메서드
        qr = self.frameGeometry()
        cp = QDesktopWidget().availableGeometry().center()
        qr.moveCenter(cp)
        self.move(qr.topLeft())

    def load_data_from_json(self):
        # JSON 파일에서 데이터를 로드하거나 샘플 데이터를 생성
        file_path = "stock_price.json"

        if os.path.exists(file_path):
            with open(file_path, 'r') as file:
                data = json.load(file)
                for entry in data:
                    self.add_stock_to_table(entry['ticker'], entry)
        else:
            # 파일이 없을 경우 샘플 데이터 생성
            sample_data = [
                {
                    'ticker': 'AAPL',
                    'name': 'Apple Inc.',
                    'one_year_ago_price': 145.09,
                    'six_months_ago_price': 150.25,
                    'current_price': 175.64,
                    'change': 175.64 - 145.09,
                    'change_percent': ((175.64 - 145.09) / 145.09) * 100
                },
                {
                    'ticker': 'MSFT',
                    'name': 'Microsoft Corporation',
                    'one_year_ago_price': 230.35,
                    'six_months_ago_price': 240.15,
                    'current_price': 260.45,
                    'change': 260.45 - 230.35,
                    'change_percent': ((260.45 - 230.35) / 230.35) * 100
                }
            ]
            with open(file_path, 'w') as file:
                json.dump(sample_data, file, indent=4)
            for entry in sample_data:
                self.add_stock_to_table(entry['ticker'], entry)

    def search_stock(self):
        # 검색 버튼 클릭 시 실행되는 메서드
        ticker = self.ticker_input.text().upper()
        if ticker:
            stock_info = self.fetch_stock_info(ticker)
            if stock_info:
                self.add_stock_to_table(ticker, stock_info)
                self.save_data_to_json()  # 테이블에 추가 후 JSON 파일에 저장
            else:
                QMessageBox.warning(self, "오류", "유효하지 않은 틱커명입니다. 틱커명을 다시 확인해주세요.")
        else:
            QMessageBox.warning(self, "오류", "틱커명을 입력하세요.")
        self.clear_input()  # 검색 후 입력 필드 초기화

    def fetch_stock_info(self, ticker):
	    # yfinance를 사용하여 주식 및 ETF 정보 가져오기
	    try:
        	stock = yf.Ticker(ticker)
	        hist = stock.history(period="1y")
	        if hist.empty:
        	    raise ValueError("주식 데이터가 없습니다.")
	        current_price = stock.history(period="1d")['Close'].iloc[-1]
	        one_year_ago_price = hist.iloc[0]['Close']
	        six_months_ago_price = hist.iloc[len(hist)//2]['Close']
	        change = current_price - one_year_ago_price
        	change_percent = (change / one_year_ago_price) * 100
	        return {
	            'ticker': ticker,
	            'name': stock.info.get('longName', ticker),
	            'one_year_ago_price': one_year_ago_price,
	            'six_months_ago_price': six_months_ago_price,
	            'current_price': current_price,
	            'change': change,
	            'change_percent': change_percent
	        }
	    except requests.exceptions.ConnectionError:
	        QMessageBox.critical(self, "네트워크 오류", "인터넷 연결을 확인하세요.")
	        return None
	    except Exception as e:
	        QMessageBox.critical(self, "오류 발생", f"주식 정보를 가져오는 중 오류가 발생했습니다: {e}")
	        return None

    def add_stock_to_table(self, ticker, stock_info):
        # 테이블에 주식 정보 추가
        row_position = self.stock_table.rowCount()
        self.stock_table.insertRow(row_position)
        self.update_table_row(row_position, ticker, stock_info)

    def update_table_row(self, row_position, ticker, stock_info):
        # 테이블 행 업데이트
        self.stock_table.setItem(row_position, 0, QTableWidgetItem(ticker))
        self.stock_table.setItem(row_position, 1, QTableWidgetItem(stock_info['name']))
        self.set_currency_item(row_position, 2, stock_info['one_year_ago_price'])
        self.set_currency_item(row_position, 3, stock_info['six_months_ago_price'])
        self.set_currency_item(row_position, 4, stock_info['current_price'])
        change_item = self.set_currency_item(row_position, 5, stock_info['change'])
        change_percent_item = self.set_percent_item(row_position, 6, stock_info['change_percent'])

        # 등락폭 색상 적용
        if stock_info['change'] < 0:
            change_item.setForeground(Qt.red)
            change_percent_item.setForeground(Qt.red)
        else:
            change_item.setForeground(Qt.blue)
            change_percent_item.setForeground(Qt.blue)

    def load_stock_to_input(self, row, column):
        # 테이블의 행을 클릭하면 해당 행의 데이터를 입력 필드로 로드하는 메서드
        ticker = self.stock_table.item(row, 0).text()
        self.ticker_input.setText(ticker)

    def set_currency_item(self, row, column, value):
        # 숫자를 달러 통화 형식으로 설정하고 오른쪽 정렬
        item = QTableWidgetItem(f"${value:.2f}")
        item.setTextAlignment(Qt.AlignRight | Qt.AlignVCenter)
        self.stock_table.setItem(row, column, item)
        return item

    def set_percent_item(self, row, column, value):
        # 백분율 형식으로 설정하고 오른쪽 정렬
        item = QTableWidgetItem(f"{value:.2f}%")
        item.setTextAlignment(Qt.AlignRight | Qt.AlignVCenter)
        self.stock_table.setItem(row, column, item)
        return item

    def delete_stock(self):
        # 삭제 버튼 클릭 시 실행되는 메서드
        ticker = self.ticker_input.text().upper()
        for i in range(self.stock_table.rowCount()):
            if self.stock_table.item(i, 0).text() == ticker:
                self.stock_table.removeRow(i)
                break
        self.save_data_to_json()  # 삭제 후 JSON 파일에 저장
        self.clear_input()  # 삭제 후 입력 필드 초기화

    def reset_table(self):
        # 테이블에 있는 모든 주식의 현재가를 업데이트하는 메서드
        for i in range(self.stock_table.rowCount()):
            ticker = self.stock_table.item(i, 0).text()
            stock_info = self.fetch_stock_info(ticker)
            if stock_info:
                self.update_table_row(i, ticker, stock_info)
        self.save_data_to_json()  # 리셋 후 JSON 파일에 저장
        QMessageBox.information(self, "리셋 완료", "리셋 완료했습니다.")
        self.clear_input()  # 리셋 후 입력 필드 초기화

    def save_data_to_json(self):
        # 테이블의 데이터를 JSON 파일로 저장
        file_path = "stock_price.json"
        data = []
        for row in range(self.stock_table.rowCount()):
            data.append({
                'ticker': self.stock_table.item(row, 0).text(),
                'name': self.stock_table.item(row, 1).text(),
                'one_year_ago_price': float(self.stock_table.item(row, 2).text().replace('$', '')),
                'six_months_ago_price': float(self.stock_table.item(row, 3).text().replace('$', '')),
                'current_price': float(self.stock_table.item(row, 4).text().replace('$', '')),
                'change': float(self.stock_table.item(row, 5).text().replace('$', '')),
                'change_percent': float(self.stock_table.item(row, 6).text().replace('%', ''))
            })
        with open(file_path, 'w') as file:
            json.dump(data, file, indent=4)

    def clear_input(self):
        # 입력 필드 초기화 메서드
        self.ticker_input.clear()

if __name__ == '__main__':
    app = QApplication(sys.argv)
    window = StockApp()
    window.show()
    sys.exit(app.exec_())
