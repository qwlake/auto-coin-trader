# auto-coin-trader

본 프로그램은 비트코인의 가격을 예측하여 자동으로 비트코인 거래소 Poloniex에서 자동 매매를 하는 프로그램이다.

## Features

* 전체적인 분석 진행은 유전 알고리즘을 사용하였다.
* 분석에 진행되는 입력은 [TA-lib](https://mrjbq7.github.io/ta-lib/)를 사용하여 나온 결과물을 사용했다.

## Getting Started

### Prerequisites

```
python3
```

### Installing

windows:
1. [본 사이트](https://www.lfd.uci.edu/~gohlke/pythonlibs/#ta-lib)에서 ```.whl``` 파일 다운로드
2. 다운로드 폴더로 이동 후 설치
```
cd "Your download folder"

# python3.6/64비트 사용시
pip install TA_Lib-0.4.10-cp36-cp36m-win_amd64.whl
pip install numpy matplotlib
```

Linux, mac:
```
pip install ta-lib
pip install numpy matplotlib
```
