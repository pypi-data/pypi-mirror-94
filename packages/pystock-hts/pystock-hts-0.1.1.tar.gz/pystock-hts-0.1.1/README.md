# pystock
- running stock in Python3
- HTS API to Python

## HTS service

- 환경: Windows10
- 언어: Python3 

```
pip3 install pystock-hts
```
or
```
pip install pystock-hts
```

- 항목 별 사용법
    - 대신증권 : Cybos Plus 가 활성화 되어 있어야함. [다운로드](https://money2.daishin.com/E5/WTS/Customer/GuideTrading/DW_CybosPlus_Page.aspx?p=8812&v=8632&m=9508)
    ```python
    from pystock_hts import Daishin

    ```
    - 키움증권 : *미구현*
    ```python
    from pystock_hts import Kiwoom
    ```
    - 유틸리티 : hts 이 외에 도움이 될만한 또는 개인적으로 만들어 놓고 싶은 것들 구현되어 있음.
    ```python
    from pystock_hts import Util
    ```

### StockApiService

- [Daishin API](Documents/daishin.md)

- [Kiwoom API](Documents/Kiwoom.md)

- [Util API](Documents/util.md)